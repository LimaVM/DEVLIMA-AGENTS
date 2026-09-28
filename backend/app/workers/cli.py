"""Real manager/queue smoke; restricted to the isolated test database."""

import json
from uuid import uuid4

from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.models import User
from app.security import hash_password
from app.workers.client import ManagerClient
from app.workers.runner import execute_one
from app.workers.service import WorkerService


def main():
    settings = get_settings()
    if settings.postgres_host != "postgres-test" or settings.postgres_db != "devlima_agent_test":
        raise SystemExit("Smoke requires the isolated test database")
    manager = ManagerClient(settings)
    assert manager.request("GET", "/health")["status"] == "ok"
    try:
        with Session(get_engine(), expire_on_commit=False) as session:
            user = User(
                username="worker-smoke-" + uuid4().hex[:12],
                password_hash=hash_password(uuid4().hex),
                timezone="America/Sao_Paulo",
            )
            session.add(user)
            session.commit()
            service = WorkerService(session, user.id)
            create = service.queue(
                "CREATE", {"name": "core-queue-smoke", "vcpu": 1, "ram_mb": 1024, "disk_gb": 10}
            )
            session.commit()
            try:
                assert execute_one(session, manager, create.id)
                assert create.status == "SUCCEEDED", create.error_code
                assert service.worker(create.worker_id).status == "BOOTING"
            finally:
                if create.status != "PENDING":
                    destroy = service.queue("DESTROY", {}, worker_id=create.worker_id)
                    session.commit()
                    assert execute_one(session, manager, destroy.id)
                    assert destroy.status == "SUCCEEDED", destroy.error_code
                    assert service.worker(create.worker_id).status == "DESTROYED"
            print(
                json.dumps(
                    {
                        "result": "passed",
                        "core_queue": True,
                        "manager_uid": 10001,
                        "worker_id": str(create.worker_id),
                    }
                )
            )
    finally:
        manager.close()


if __name__ == "__main__":
    main()
