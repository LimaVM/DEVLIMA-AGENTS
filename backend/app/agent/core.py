import hashlib
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.agent.action_engine import ActionEngine
from app.agent.action_parser import parse_response
from app.agent.context_builder import ContextBuilder
from app.agent.errors import AgentError
from app.agent.memory_manager import MemoryManager, content_hash
from app.agent.summarizer import Summarizer
from app.config import Settings
from app.llm.base import LLMError
from app.llm.service import build_router
from app.models import AuditLog, Conversation, Message, User
from app.schemas.chat import ChatReply, ChatSend


class AgentCore:
    def __init__(self, session: Session, settings: Settings, router_factory=build_router):
        self.session = session
        self.settings = settings
        self.router_factory = router_factory

    def _replay(self, assistant: Message) -> ChatReply:
        return ChatReply(
            conversation_id=assistant.conversation_id,
            user_message_id=assistant.in_reply_to,
            assistant_message_id=assistant.id,
            reply=assistant.content,
            replayed=True,
            **assistant.info,
        )

    def _claim(self, user_id: UUID, data: ChatSend, lease: UUID):
        digest = hashlib.sha256(f"{user_id}:{data.client_message_id}".encode()).digest()
        key = int.from_bytes(digest[:8], "big", signed=True)
        self.session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": key})
        source = self.session.scalar(
            select(Message).where(
                Message.user_id == user_id, Message.client_message_id == data.client_message_id
            )
        )
        if source:
            if source.content != data.content or (
                data.conversation_id and source.conversation_id != data.conversation_id
            ):
                raise AgentError("idempotency_key_conflict")
            assistant = self.session.scalar(select(Message).where(Message.in_reply_to == source.id))
            if assistant:
                response = self._replay(assistant)
                self.session.commit()
                return response
        conversation_id = source.conversation_id if source else data.conversation_id
        if conversation_id:
            conversation = self.session.scalar(
                select(Conversation)
                .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
            if conversation is None:
                raise AgentError("not_found", 404)
        else:
            conversation = Conversation(user_id=user_id, title=data.content[:100])
            self.session.add(conversation)
            self.session.flush()
        now = datetime.now(UTC)
        if conversation.archived:
            raise AgentError("conversation_archived")
        if conversation.lease_owner and conversation.lease_until > now:
            raise AgentError("conversation_busy")
        if conversation.pending_message_id and (
            not source or conversation.pending_message_id != source.id
        ):
            stale = self.session.get(Message, conversation.pending_message_id)
            if stale:
                stale.status, stale.error_code = "FAILED", "processing_lease_expired"
        if source:
            if source.sequence != conversation.last_sequence:
                raise AgentError("failed_turn_not_latest")
            source.status, source.error_code = "PENDING", None
        else:
            conversation.last_sequence += 1
            source = Message(
                user_id=user_id,
                conversation_id=conversation.id,
                client_message_id=data.client_message_id,
                sequence=conversation.last_sequence,
                role="user",
                content=data.content,
                status="PENDING",
                info={},
            )
            self.session.add(source)
            self.session.flush()
            self.session.add(
                AuditLog(
                    user_id=user_id,
                    event="chat.message_saved",
                    details={"message_id": str(source.id), "conversation_id": str(conversation.id)},
                )
            )
        conversation.lease_owner = lease
        conversation.lease_until = now + timedelta(
            seconds=max(
                300, 4 * (self.settings.local_llm_timeout + self.settings.groq_timeout) + 60
            )
        )
        conversation.pending_message_id = source.id
        conversation.updated_at = now
        self.session.commit()
        return conversation, source

    def _fail(self, conversation_id: UUID, source_id: UUID, lease: UUID, code: str):
        self.session.rollback()
        conversation = self.session.scalar(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if conversation.lease_owner == lease:
            source = self.session.get(Message, source_id)
            source.status, source.error_code = "FAILED", code
            conversation.lease_owner = conversation.lease_until = (
                conversation.pending_message_id
            ) = None
            self.session.add(
                AuditLog(
                    user_id=conversation.user_id,
                    event="chat.failed",
                    details={"message_id": str(source_id), "error_code": code},
                )
            )
        self.session.commit()

    def send(self, user_id: UUID, data: ChatSend) -> ChatReply:
        user = self.session.get(User, user_id)
        if user is None:
            raise AgentError("not_found", 404)
        lease = uuid4()
        claimed = self._claim(user_id, data, lease)
        if isinstance(claimed, ChatReply):
            return claimed
        conversation, source = claimed
        conversation_id, source_id = conversation.id, source.id
        try:
            with self.router_factory(self.settings, self.session) as router:
                Summarizer(self.session, self.settings).maybe_summarize(conversation, router)
                context = ContextBuilder(self.session, self.settings).build(
                    user, conversation, source
                )
                self.session.commit()
                result = router.chat(
                    context.messages, json_mode=True, max_tokens=1024, user_id=user_id
                )
                envelope = parse_response(result.completion.content)
            conversation = self.session.scalar(
                select(Conversation)
                .where(Conversation.id == conversation_id)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
            if conversation.lease_owner != lease:
                raise AgentError("processing_lease_lost")
            actions = ActionEngine(self.session).process(envelope.actions, source)
            manager = MemoryManager(self.session, user_id)
            candidates, seen = [], set()
            for proposal in envelope.memory_candidates:
                digest = content_hash(proposal.content)
                if digest in seen:
                    continue
                seen.add(digest)
                candidate = manager.consider(proposal, source)
                candidates.append({"id": str(candidate.id), "status": candidate.status})
            reply = envelope.reply
            if actions:
                reply = (
                    "Nesta fase ainda não consigo executar tarefas, lembretes, chamadas "
                    "ou operações de VMs. Seu pedido ficou salvo no histórico."
                )
            if any(item["status"] == "PENDING" for item in candidates):
                reply += " Há uma proposta de memória aguardando sua confirmação."
            if any(item["status"] == "ACCEPTED" for item in candidates):
                reply += " Memória salva conforme seu pedido explícito."
            if any(item["status"] == "REJECTED" for item in candidates):
                reply += " Uma proposta de memória foi recusada por conter dados sensíveis."
            info = {
                "request_id": str(result.request_id),
                "provider": result.completion.provider,
                "fallback_used": result.fallback_used,
                "latency_ms": result.latency_ms,
                "memory_candidates": candidates,
                "actions": actions,
                "context_stats": context.stats,
            }
            conversation.last_sequence += 1
            assistant = Message(
                user_id=user_id,
                conversation_id=conversation_id,
                in_reply_to=source_id,
                sequence=conversation.last_sequence,
                role="assistant",
                content=reply,
                status="COMPLETED",
                info=info,
            )
            self.session.add(assistant)
            source.status, source.error_code = "COMPLETED", None
            conversation.lease_owner = conversation.lease_until = (
                conversation.pending_message_id
            ) = None
            conversation.updated_at = datetime.now(UTC)
            self.session.flush()
            self.session.add(
                AuditLog(
                    user_id=user_id,
                    event="chat.completed",
                    request_id=str(result.request_id),
                    details={
                        "message_id": str(source_id),
                        "assistant_message_id": str(assistant.id),
                    },
                )
            )
            self.session.commit()
            return self._replay(assistant).model_copy(update={"replayed": False})
        except (AgentError, LLMError) as error:
            self._fail(conversation_id, source_id, lease, error.code)
            raise
