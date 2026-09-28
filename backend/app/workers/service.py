import hashlib
import json
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select, text

from app.agent.errors import AgentError
from app.models import AuditLog
from app.models.workers import Worker, WorkerCommand, WorkerSnapshot


# Documentação: Implementa worker_data como parte do fluxo descrito para este arquivo.
def worker_data(row):
    return {
        key: str(getattr(row, key))
        if key in {"id", "user_id"}
        else getattr(row, key).isoformat()
        if isinstance(getattr(row, key), datetime)
        else getattr(row, key)
        for key in (
            "id",
            "user_id",
            "name",
            "provider",
            "vcpu",
            "ram_mb",
            "disk_gb",
            "status",
            "ip",
            "error_code",
            "created_at",
            "updated_at",
        )
    }


# Documentação: Implementa command_data como parte do fluxo descrito para este arquivo.
def command_data(row):
    return {
        key: str(getattr(row, key))
        if key in {"id", "worker_id"}
        else getattr(row, key).isoformat()
        if isinstance(getattr(row, key), datetime)
        else getattr(row, key)
        for key in (
            "id",
            "worker_id",
            "kind",
            "status",
            "attempts",
            "result",
            "error_code",
            "created_at",
            "updated_at",
        )
    }


# Documentação: Implementa snapshot_data como parte do fluxo descrito para este arquivo.
def snapshot_data(row):
    return {
        key: str(getattr(row, key))
        if key in {"id", "worker_id"}
        else getattr(row, key).isoformat()
        if isinstance(getattr(row, key), datetime)
        else getattr(row, key)
        for key in ("id", "worker_id", "status", "sha256", "created_at")
    }


# Documentação: Define o tipo WorkerService e reúne o estado/contrato descrito para este módulo.
class WorkerService:
    # Documentação: Inicializa WorkerService com as dependências e estado declarados.
    def __init__(self, session, owner):
        self.session, self.owner = session, UUID(str(owner))

    # Documentação: Implementa WorkerService.worker como parte do fluxo descrito para este
    # arquivo.
    def worker(self, identifier, lock=False):
        query = select(Worker).where(Worker.id == identifier, Worker.user_id == self.owner)
        if lock:
            query = query.with_for_update()
        row = self.session.scalar(query)
        if row is None:
            raise AgentError("not_found", 404)
        return row

    # Documentação: Implementa WorkerService.workers como parte do fluxo descrito para este
    # arquivo.
    def workers(self, limit=20):
        return self.session.scalars(
            select(Worker)
            .where(Worker.user_id == self.owner)
            .order_by(Worker.created_at.desc())
            .limit(limit)
        ).all()

    # Documentação: Implementa WorkerService.commands como parte do fluxo descrito para este
    # arquivo.
    def commands(self, identifier, limit=20):
        self.worker(identifier)
        return self.session.scalars(
            select(WorkerCommand)
            .where(WorkerCommand.worker_id == identifier, WorkerCommand.user_id == self.owner)
            .order_by(WorkerCommand.created_at.desc())
            .limit(limit)
        ).all()

    # Documentação: Implementa WorkerService.snapshots como parte do fluxo descrito para este
    # arquivo.
    def snapshots(self, identifier):
        self.worker(identifier)
        return self.session.scalars(
            select(WorkerSnapshot)
            .where(WorkerSnapshot.worker_id == identifier, WorkerSnapshot.user_id == self.owner)
            .order_by(WorkerSnapshot.created_at.desc())
            .limit(20)
        ).all()

    # Documentação: Valida operação e ownership e grava comando para execução posterior pelo
    # runner.
    def queue(self, kind, args, request_id=None, worker_id=None):
        identifier = UUID(str(request_id)) if request_id else uuid4()
        # Serialize request IDs across concurrent requests before checking replay.
        self.session.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
            {"key": f"worker-command:{identifier}"},
        )
        payload = dict(args)
        signature = hashlib.sha256(
            json.dumps(
                {"kind": kind, "worker_id": str(worker_id) if worker_id else None, "args": payload},
                sort_keys=True,
                default=str,
            ).encode()
        ).hexdigest()
        existing = self.session.get(WorkerCommand, identifier)
        if existing is not None:
            if existing.user_id != self.owner:
                raise AgentError("not_found", 404)
            if existing.signature != signature:
                raise AgentError("idempotency_conflict", 409)
            return existing
        if kind == "CREATE":
            row = Worker(
                user_id=self.owner,
                name=payload.get("name") or "linux-worker",
                vcpu=payload.get("vcpu", 2),
                ram_mb=payload.get("ram_mb", 2048),
                disk_gb=payload.get("disk_gb", 20),
            )
            self.session.add(row)
            self.session.flush()
            payload = {
                "name": row.name,
                "vcpu": row.vcpu,
                "ram_mb": row.ram_mb,
                "disk_gb": row.disk_gb,
            }
        else:
            row = self.worker(worker_id, lock=True)
            pending = self.session.scalar(
                select(WorkerCommand.id)
                .where(
                    WorkerCommand.worker_id == row.id,
                    WorkerCommand.status.in_(["PENDING", "RUNNING"]),
                )
                .limit(1)
            )
            if pending:
                raise AgentError("worker_busy", 409)
            if row.status == "DESTROYED" and kind != "DESTROY":
                raise AgentError("worker_destroyed", 409)
            if kind == "EXECUTE" and row.status != "READY":
                raise AgentError("worker_not_ready", 409)
            if kind == "RESTORE":
                snapshot = self.session.get(WorkerSnapshot, UUID(str(payload["snapshot_id"])))
                if (
                    snapshot is None
                    or snapshot.worker_id != row.id
                    or snapshot.user_id != self.owner
                    or snapshot.status != "AVAILABLE"
                ):
                    raise AgentError("snapshot_not_found", 404)
        if kind == "SNAPSHOT":
            snapshot = WorkerSnapshot(user_id=self.owner, worker_id=row.id)
            self.session.add(snapshot)
            self.session.flush()
            payload["snapshot_id"] = str(snapshot.id)
        command = WorkerCommand(
            id=identifier,
            user_id=self.owner,
            worker_id=row.id,
            kind=kind,
            arguments=payload,
            signature=signature,
        )
        self.session.add(command)
        self.session.add(
            AuditLog(
                user_id=self.owner,
                event="worker.command_queued",
                details={"command_id": str(identifier), "worker_id": str(row.id), "kind": kind},
            )
        )
        self.session.flush()
        return command
