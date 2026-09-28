import argparse
import logging
import signal
import threading
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.models import AuditLog, OutboxEvent, SchedulerHeartbeat
from app.models.workers import Worker, WorkerCommand, WorkerSnapshot
from app.workers.client import ManagerClient, ManagerError

logger = logging.getLogger("worker-runner")


# Documentação: Implementa claim como parte do fluxo descrito para este arquivo.
def claim(session, now=None, command_id=None):
    now = now or datetime.now(UTC)
    row = session.scalar(
        select(WorkerCommand)
        .where(
            WorkerCommand.id == command_id if command_id is not None else True,
            or_(
                (WorkerCommand.status == "PENDING")
                & (or_(WorkerCommand.lease_until.is_(None), WorkerCommand.lease_until <= now)),
                (WorkerCommand.status == "RUNNING") & (WorkerCommand.lease_until <= now),
            ),
        )
        .order_by(WorkerCommand.created_at)
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    if row is None:
        session.rollback()
        return None
    row.status, row.lease_id, row.lease_until = "RUNNING", uuid4(), now + timedelta(seconds=600)
    row.attempts += 1
    row.updated_at = now
    session.commit()
    return row


# Documentação: Implementa apply_status como parte do fluxo descrito para este arquivo.
def apply_status(worker, data):
    worker.status = data["status"]
    worker.ip = data.get("ip")
    worker.error_code = data.get("error_code")
    worker.updated_at = datetime.now(UTC)


# Documentação: Reivindica e executa comando de worker com lease e registra seu resultado no Core.
def execute_one(session, client, command_id=None):
    command = claim(session, command_id=command_id)
    if command is None:
        return False
    lease = command.lease_id
    result, error, uncertain = None, None, False
    try:
        try:
            previous = client.operation(command.id, command.user_id)
        except ManagerError as issue:
            if issue.code != "not_found":
                raise
            previous = None
        if previous is None:
            result = client.perform(command)
        elif previous["status"] == "RUNNING":
            raise ManagerError("manager_operation_running", uncertain=True)
        elif previous["status"] == "SUCCEEDED":
            result = previous["result"]
        else:
            raise ManagerError(
                (previous.get("result") or {}).get("code", "operation_recovery_required")
            )
    except ManagerError as issue:
        error, uncertain = issue.code, issue.uncertain
    session.expire_all()
    row = session.scalar(
        select(WorkerCommand).where(WorkerCommand.id == command.id).with_for_update()
    )
    if row.lease_id != lease:
        session.rollback()
        return True
    row.updated_at = datetime.now(UTC)
    row.lease_id = None
    row.error_code = error
    if uncertain:
        row.status = "PENDING"
        row.lease_until = row.updated_at + timedelta(seconds=10)
        session.commit()
        return True
    row.lease_until = None
    row.status = "FAILED" if error else "SUCCEEDED"
    row.result = result or {}
    worker = session.get(Worker, row.worker_id)
    if result and result.get("worker"):
        apply_status(worker, result["worker"])
    elif error and row.kind == "CREATE":
        worker.status, worker.error_code = "ERROR", error
    if row.kind == "SNAPSHOT":
        snapshot = session.get(WorkerSnapshot, row.arguments["snapshot_id"])
        snapshot.status = "FAILED" if error else "AVAILABLE"
        snapshot.sha256 = (result or {}).get("snapshot", {}).get("sha256")
    if row.kind == "DESTROY" and not error:
        for snapshot in session.scalars(
            select(WorkerSnapshot).where(WorkerSnapshot.worker_id == worker.id)
        ):
            snapshot.status = "DELETED"
    session.add(
        AuditLog(
            user_id=row.user_id,
            event="worker.command_finished",
            details={
                "command_id": str(row.id),
                "kind": row.kind,
                "status": row.status,
                "error_code": error,
            },
        )
    )
    session.add(
        OutboxEvent(
            user_id=row.user_id,
            type="worker.updated",
            payload={
                "worker_id": str(row.worker_id),
                "command_id": str(row.id),
                "status": row.status,
            },
            dedupe_key=f"worker-command:{row.id}",
        )
    )
    session.commit()
    return True


# Documentação: Implementa reconcile como parte do fluxo descrito para este arquivo.
def reconcile(session, client):
    identifiers = [
        (row.id, row.user_id)
        for row in session.scalars(select(Worker).where(Worker.status != "DESTROYED").limit(100))
    ]
    session.commit()
    for identifier, owner in identifiers:
        try:
            data = client.status(identifier, owner)
        except ManagerError:
            continue
        worker = session.get(Worker, identifier)
        if (
            worker.status == "BOOTING"
            and datetime.now(UTC) - worker.created_at > timedelta(minutes=15)
            and data["status"] == "BOOTING"
        ):
            data = {**data, "error_code": "boot_taking_long"}
        apply_status(worker, data)
        session.commit()
    heartbeat = session.get(SchedulerHeartbeat, "worker-runner")
    if heartbeat is None:
        session.add(
            SchedulerHeartbeat(name="worker-runner", last_tick_at=datetime.now(UTC), processed=0)
        )
    else:
        heartbeat.last_tick_at = datetime.now(UTC)
    session.commit()


# Documentação: Coordena a entrada de linha de comando deste arquivo: Reivindica comandos duráveis
# com lease/locks, executa operação idempotente no manager, atualiza Core e reconcilia operações
# interrompidas.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["run", "once", "health"])
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.command == "health":
        with Session(get_engine()) as session:
            heartbeat = session.get(SchedulerHeartbeat, "worker-runner")
            if heartbeat is None or datetime.now(UTC) - heartbeat.last_tick_at > timedelta(
                minutes=10
            ):
                raise SystemExit(1)
        return
    settings = get_settings()
    if len(settings.vm_manager_token.get_secret_value()) < 32:
        raise SystemExit("VM Manager token not configured")
    client = ManagerClient(settings)
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    try:
        while not stop.is_set():
            try:
                with Session(get_engine(), expire_on_commit=False) as session:
                    execute_one(session, client)
                    reconcile(session, client)
            except Exception:
                logger.error("worker_runner_tick_failed")
            if args.command == "once":
                break
            stop.wait(5)
    finally:
        client.close()
        get_engine().dispose()


if __name__ == "__main__":
    main()
