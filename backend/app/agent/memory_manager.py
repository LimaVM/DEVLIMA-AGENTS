import hashlib
import re
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.agent.action_parser import MemoryProposal
from app.agent.errors import AgentError
from app.models import AuditLog, Memory, MemoryCandidate, Message

SECRET_PATTERN = re.compile(
    r"gsk_[A-Za-z0-9_]{10,}|sk-[A-Za-z0-9_-]{12,}|BEGIN.{0,30}PRIVATE KEY|"
    r"\b(?:senha|password|api[ _-]?key|token)\s*[:=]\s*\S{6,}",
    re.IGNORECASE,
)


def normalize(value: str) -> str:
    return " ".join(value.casefold().split()).rstrip(".!?")


def content_hash(value: str) -> str:
    return hashlib.sha256(normalize(value).encode()).hexdigest()


def safe_memory_content(value: str) -> bool:
    return bool(value.strip()) and SECRET_PATTERN.search(value) is None


class MemoryManager:
    def __init__(self, session: Session, user_id: UUID):
        self.session = session
        self.user_id = user_id

    def create(self, content: str, category: str, source_message_id: UUID | None = None) -> Memory:
        if not safe_memory_content(content):
            raise AgentError("sensitive_memory_rejected", 422)
        digest = content_hash(content)
        if source_message_id:
            source = self.session.scalar(
                select(Message).where(
                    Message.id == source_message_id, Message.user_id == self.user_id
                )
            )
            if source is None:
                raise AgentError("not_found", 404)
        identifier = self.session.execute(
            insert(Memory)
            .values(
                id=uuid4(),
                user_id=self.user_id,
                source_message_id=source_message_id,
                content=content.strip(),
                content_hash=digest,
                category=category,
                is_active=True,
            )
            .on_conflict_do_nothing(index_elements=[Memory.user_id, Memory.content_hash])
            .returning(Memory.id)
        ).scalar()
        memory = (
            self.session.get(Memory, identifier)
            if identifier
            else self.session.scalar(
                select(Memory).where(Memory.user_id == self.user_id, Memory.content_hash == digest)
            )
        )
        memory.is_active = True
        memory.updated_at = datetime.now(UTC)
        self.session.add(
            AuditLog(
                user_id=self.user_id, event="memory.saved", details={"memory_id": str(memory.id)}
            )
        )
        return memory

    def consider(self, proposal: MemoryProposal, source: Message) -> MemoryCandidate:
        if source.user_id != self.user_id or source.role != "user":
            raise AgentError("not_found", 404)
        safe = safe_memory_content(proposal.content)
        candidate = MemoryCandidate(
            user_id=self.user_id,
            source_message_id=source.id,
            content=proposal.content.strip() if safe else "[conteúdo sensível recusado]",
            content_hash=content_hash(proposal.content),
            category=proposal.category,
            confidence=proposal.confidence,
            status="PENDING" if safe else "REJECTED",
            rejection_reason=None if safe else "sensitive_content",
        )
        self.session.add(candidate)
        self.session.flush()
        explicit = re.match(
            r"^(?:lembre que|lembra que|guarde que|memorize que|prefiro\b)",
            normalize(source.content),
        )
        grounded = normalize(proposal.content) in normalize(source.content)
        if safe and explicit and grounded and proposal.confidence >= 0.9:
            memory = self.create(proposal.content, proposal.category, source.id)
            candidate.accepted_memory_id = memory.id
            candidate.status = "ACCEPTED"
        self.session.add(
            AuditLog(
                user_id=self.user_id,
                event="memory.candidate",
                details={"candidate_id": str(candidate.id), "status": candidate.status},
            )
        )
        return candidate

    def accept(self, identifier: UUID) -> Memory:
        candidate = self.session.scalar(
            select(MemoryCandidate)
            .where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == self.user_id)
            .with_for_update()
        )
        if candidate is None:
            raise AgentError("not_found", 404)
        if candidate.status == "REJECTED":
            raise AgentError("candidate_rejected")
        if candidate.status == "ACCEPTED":
            memory = self.session.scalar(
                select(Memory).where(
                    Memory.id == candidate.accepted_memory_id, Memory.user_id == self.user_id
                )
            )
            if memory is None or not memory.is_active:
                raise AgentError("memory_no_longer_active")
            return memory
        memory = self.create(candidate.content, candidate.category, candidate.source_message_id)
        candidate.status = "ACCEPTED"
        candidate.accepted_memory_id = memory.id
        return memory

    def relevant(self, query: str, limit: int = 5) -> list[Memory]:
        terms = set(re.findall(r"\w{3,}", query.casefold()))
        rows = list(
            self.session.scalars(
                select(Memory)
                .where(Memory.user_id == self.user_id, Memory.is_active.is_(True))
                .order_by(Memory.updated_at.desc(), Memory.id)
                .limit(100)
            )
        )

        def score(memory):
            overlap = len(terms & set(re.findall(r"\w{3,}", memory.content.casefold())))
            return overlap + (2 if memory.category == "preference" else 0)

        return sorted((row for row in rows if score(row) > 0), key=score, reverse=True)[:limit]
