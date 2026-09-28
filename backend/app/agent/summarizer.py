import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.action_parser import SummaryEnvelope, parse_response
from app.agent.errors import InvalidAgentResponse
from app.agent.prompts import SUMMARY_PROMPT
from app.config import Settings
from app.llm.base import LLMError, LLMMessage
from app.models import AuditLog, Conversation, ConversationSummary, Message


# Documentação: Define o tipo Summarizer e reúne o estado/contrato descrito para este módulo.
class Summarizer:
    # Documentação: Inicializa Summarizer com as dependências e estado declarados.
    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.settings = settings

    # Documentação: Cria resumo somente quando o limiar é atingido e preserva a faixa de mensagens
    # já coberta.
    def maybe_summarize(self, conversation: Conversation, router) -> ConversationSummary | None:
        previous = self.session.scalar(
            select(ConversationSummary)
            .where(
                ConversationSummary.user_id == conversation.user_id,
                ConversationSummary.conversation_id == conversation.id,
            )
            .order_by(ConversationSummary.through_sequence.desc())
            .limit(1)
        )
        covered = previous.through_sequence if previous else 0
        candidates = self.session.scalars(
            select(Message)
            .where(
                Message.conversation_id == conversation.id,
                Message.user_id == conversation.user_id,
                Message.sequence > covered,
                Message.status == "COMPLETED",
            )
            .order_by(Message.sequence)
            .limit(self.settings.summary_trigger_messages)
        ).all()
        if len(candidates) < self.settings.summary_trigger_messages:
            self.session.commit()
            return previous
        payload = {"previous_summary": previous.content if previous else None, "messages": []}
        through = covered
        recent = self.session.scalars(
            select(Message.sequence)
            .where(
                Message.conversation_id == conversation.id,
                Message.user_id == conversation.user_id,
                Message.status == "COMPLETED",
            )
            .order_by(Message.sequence.desc())
            .limit(self.settings.context_recent_messages)
        ).all()
        cutoff = min(recent) - 1 if recent else 0
        for message in candidates:
            if message.sequence > cutoff:
                break
            item = {"sequence": message.sequence, "role": message.role, "content": message.content}
            proposed = payload | {"messages": [*payload["messages"], item]}
            if (
                len(json.dumps(proposed, ensure_ascii=False)) + len(SUMMARY_PROMPT)
                > self.settings.context_max_chars
            ):
                break
            payload["messages"].append(item)
            through = message.sequence
        if not payload["messages"]:
            self.session.commit()
            return previous
        messages = [LLMMessage(role="system", content=SUMMARY_PROMPT)]
        # Split quoted source data to honor the provider's per-message bound.
        raw = json.dumps(payload, ensure_ascii=False)
        for start in range(0, len(raw), 7000):
            messages.append(LLMMessage(role="user", content=raw[start : start + 7000]))
        user_id, conversation_id = conversation.user_id, conversation.id
        self.session.commit()
        try:
            result = router.chat(messages, json_mode=True, max_tokens=768, user_id=user_id)
            parsed = parse_response(result.completion.content, SummaryEnvelope)
        except (LLMError, InvalidAgentResponse) as error:
            self.session.add(
                AuditLog(
                    user_id=user_id,
                    event="summary.failed",
                    details={"conversation_id": str(conversation_id), "error_code": error.code},
                )
            )
            self.session.commit()
            return previous
        summary = ConversationSummary(
            user_id=user_id,
            conversation_id=conversation_id,
            through_sequence=through,
            content=parsed.model_dump(),
        )
        self.session.add(summary)
        self.session.add(
            AuditLog(
                user_id=user_id,
                event="summary.created",
                request_id=str(result.request_id),
                details={"conversation_id": str(conversation_id), "through_sequence": through},
            )
        )
        self.session.commit()
        return summary
