"""Real Core/manager readiness and guest execution; run only in worker-smoke test container."""

import json
import time
from uuid import uuid4

from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.models import User
from app.security import hash_password
from app.workers.client import ManagerClient
from app.workers.runner import execute_one, reconcile
from app.workers.service import WorkerService

settings = get_settings()
if settings.postgres_host != "postgres-test" or settings.postgres_db != "devlima_agent_test":
    raise SystemExit("Readiness smoke requires the isolated test database")
manager = ManagerClient(settings)
try:
    with Session(get_engine(), expire_on_commit=False) as session:
        user = User(
            username="worker-ready-" + uuid4().hex[:12],
            password_hash=hash_password(uuid4().hex),
            timezone="America/Sao_Paulo",
        )
        session.add(user)
        session.commit()
        service = WorkerService(session, user.id)
        create = service.queue(
            "CREATE", {"name": "core-ready-validation", "vcpu": 1, "ram_mb": 1024, "disk_gb": 10}
        )
        session.commit()
        try:
            assert execute_one(session, manager, create.id)
            assert create.status == "SUCCEEDED", create.error_code
            deadline = time.monotonic() + 480
            while time.monotonic() < deadline:
                reconcile(session, manager)
                session.expire_all()
                worker = service.worker(create.worker_id)
                if worker.status == "READY":
                    break
                if worker.status == "ERROR":
                    raise AssertionError(worker.error_code)
                time.sleep(5)
            assert worker.status == "READY" and worker.ip, "Readiness timed out"
            command = service.queue(
                "EXECUTE",
                {"script": "printf core-ready", "timeout": 30},
                worker_id=worker.id,
            )
            session.commit()
            assert execute_one(session, manager, command.id)
            assert command.status == "SUCCEEDED", command.error_code
            assert command.result["job"]["exit_code"] == 0
            assert command.result["job"]["output"] == "core-ready"
            print(json.dumps({"core_status": "READY", "guest_job": "passed"}), flush=True)
        finally:
            destroy = service.queue("DESTROY", {}, worker_id=create.worker_id)
            session.commit()
            assert execute_one(session, manager, destroy.id)
            assert destroy.status == "SUCCEEDED", destroy.error_code
            assert service.worker(create.worker_id).status == "DESTROYED"
            print(json.dumps({"worker_destroyed": True, "worker_id": str(create.worker_id)}))
finally:
    manager.close()
