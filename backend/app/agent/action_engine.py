from sqlalchemy.orm import Session

from app.agent.action_parser import ActionProposal
from app.models import AgentAction, AuditLog, Message


class ActionEngine:
    def __init__(self, session: Session):
        self.session = session

    def process(self, actions: list[ActionProposal], source: Message) -> list[dict]:
        results = []
        for action in actions:
            record = AgentAction(
                user_id=source.user_id,
                source_message_id=source.id,
                type=action.type,
                arguments=action.arguments,
                status="UNSUPPORTED",
                result={"code": "feature_not_available"},
            )
            self.session.add(record)
            self.session.flush()
            results.append(
                {
                    "id": str(record.id),
                    "type": action.type,
                    "status": record.status,
                    "code": "feature_not_available",
                }
            )
            self.session.add(
                AuditLog(
                    user_id=source.user_id,
                    event="agent.action_unavailable",
                    details={"action_id": str(record.id), "type": action.type},
                )
            )
        return results
