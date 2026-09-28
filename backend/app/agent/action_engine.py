import json
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.agent.action_parser import ActionProposal
from app.agent.errors import AgentError
from app.models import AgentAction, AuditLog, Message
from app.planning.service import PlanningService, schedule_data, task_data
from app.workers.service import WorkerService, command_data, worker_data


class ActionEngine:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, action: ActionProposal, source: Message) -> tuple[dict, str]:
        service = PlanningService(self.session, source.user_id)
        args = dict(action.arguments)
        name = action.type
        workers = WorkerService(self.session, source.user_id)
        if name == "list_workers":
            rows = workers.workers()
            return {"items": [worker_data(row) for row in rows]}, "\n".join(
                f"• {row.name}: {row.status}" for row in rows
            ) or "Nenhum worker encontrado."
        if name == "get_worker_status":
            row = workers.worker(args["worker_id"])
            return worker_data(row), f"Worker {row.name}: {row.status}."
        worker_operations = {
            "create_linux_worker": "CREATE",
            "destroy_worker": "DESTROY",
            "reset_worker": "RESET",
            "snapshot_worker": "SNAPSHOT",
            "restore_worker": "RESTORE",
            "start_worker": "START",
            "stop_worker": "STOP",
            "run_worker_job": "EXECUTE",
        }
        if name in worker_operations:
            identifier = args.pop("worker_id", None)
            command = workers.queue(worker_operations[name], args, worker_id=identifier)
            return command_data(
                command
            ), f"Operação {command.kind} solicitada para o worker; status {command.status}."
        if name == "create_task":
            row = service.create_task(args)
            return task_data(row), f"Tarefa criada: {row.title}."
        if name in {"update_task", "complete_task"}:
            identifier = args.pop("id")
            row = (
                service.update_task(identifier, args)
                if name == "update_task"
                else service.complete_task(identifier)
            )
            verb = "atualizada" if name == "update_task" else "concluída"
            return task_data(row), f"Tarefa {verb}: {row.title}."
        if name == "list_tasks":
            rows = service.list_tasks(args.get("date"), limit=20)
            data = [task_data(row) for row in rows]
            text = (
                "\n".join(f"• {row.title} ({row.status})" for row in rows)
                or "Nenhuma tarefa encontrada."
            )
            return {"items": data}, text
        if name in {"create_reminder", "schedule_call"}:
            kind = "REMINDER" if name == "create_reminder" else "CALL"
            row = service.create_schedule(kind, args)
            local = row.next_run_at.astimezone(ZoneInfo(row.timezone)).strftime("%d/%m/%Y às %H:%M")
            label = "Lembrete" if kind == "REMINDER" else "Chamada"
            return schedule_data(
                row
            ), f"{label} agendado para {local} ({row.timezone}): {row.text}."
        if name == "update_reminder":
            identifier = args.pop("id")
            row = service.update_schedule(identifier, args)
            return schedule_data(row), f"Lembrete atualizado: {row.text}."
        if name in {"cancel_reminder", "cancel_call"}:
            kind = "REMINDER" if name == "cancel_reminder" else "CALL"
            row = service.cancel_schedule(args["id"], kind)
            label = "Lembrete cancelado" if kind == "REMINDER" else "Chamada cancelada"
            return schedule_data(row), f"{label}: {row.text}."
        if name in {"list_reminders", "list_scheduled_calls"}:
            kind = "REMINDER" if name == "list_reminders" else "CALL"
            rows = service.list_schedules(kind, args.get("date"), limit=20)
            data = [schedule_data(row) for row in rows]
            text = (
                "\n".join(f"• {row.text} ({row.status})" for row in rows)
                or "Nenhum agendamento encontrado."
            )
            return {"items": data}, text
        raise AgentError("feature_not_available", 409)

    def process(self, actions: list[ActionProposal], source: Message) -> list[dict]:
        results, seen = [], set()
        for action in actions:
            digest = json.dumps(action.model_dump(), sort_keys=True)
            if digest in seen:
                continue
            seen.add(digest)
            record = AgentAction(
                user_id=source.user_id,
                source_message_id=source.id,
                type=action.type,
                arguments=action.arguments,
                status="PENDING",
                result={},
            )
            self.session.add(record)
            self.session.flush()
            try:
                with self.session.begin_nested():
                    data, message = self.execute(action, source)
                record.status = "SUCCEEDED"
                record.result = {"data": data, "message": message}
            except AgentError as error:
                record.status = "UNSUPPORTED" if error.code == "feature_not_available" else "FAILED"
                messages = {
                    "feature_not_available": "Operações de VMs ainda não estão disponíveis.",
                    "not_found": "Não encontrei esse item entre seus registros.",
                    "schedule_date_out_of_range": (
                        "O agendamento precisa estar no futuro, dentro de um ano."
                    ),
                    "invalid_recurrence": "A regra de recorrência não é válida para esta versão.",
                }
                record.result = {
                    "code": error.code,
                    "message": messages.get(
                        error.code, "Não consegui executar essa ação; confira os dados do pedido."
                    ),
                }
            self.session.add(
                AuditLog(
                    user_id=source.user_id,
                    event="agent.action_result",
                    details={
                        "action_id": str(record.id),
                        "type": action.type,
                        "status": record.status,
                    },
                )
            )
            results.append(
                {
                    "id": str(record.id),
                    "type": action.type,
                    "status": record.status,
                    **record.result,
                }
            )
        return results
