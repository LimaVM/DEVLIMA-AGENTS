from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from test_planning import headers

from app.agent.action_engine import ActionEngine
from app.agent.action_parser import ActionProposal
from app.agent.errors import AgentError
from app.models import OutboxEvent, User, Worker, WorkerSnapshot
from app.workers.client import ManagerError
from app.workers.runner import claim, execute_one
from app.workers.service import WorkerService


class FakeManager:
    def __init__(self):
        self.calls = 0
        self.previous = None
        self.error = None

    def operation(self, *_):
        if self.previous:
            return self.previous
        raise ManagerError("not_found")

    def perform(self, command):
        self.calls += 1
        if self.error:
            raise self.error
        return {
            "worker": {"id": str(command.worker_id), "status": "BOOTING", "ip": None},
            "job": {"exit_code": 0, "output": "ok"},
        }


def test_worker_api_queue_idempotency_and_tenant(client, session, user):
    data = {"request_id": str(uuid4()), "name": "test-worker"}
    response = client.post("/workers", headers=headers(user), json=data)
    assert response.status_code == 202
    assert response.json()["status"] == "PENDING"
    identifier = response.json()["worker_id"]
    assert (
        client.post("/workers", headers=headers(user), json=data).json()["id"]
        == response.json()["id"]
    )
    assert session.scalar(select(func.count()).select_from(Worker)) == 1
    assert (
        client.post("/workers", headers=headers(user), json={**data, "name": "changed"}).status_code
        == 409
    )
    other = User(username="other", password_hash=user.password_hash, timezone=user.timezone)
    session.add(other)
    session.commit()
    assert client.get("/workers/" + identifier, headers=headers(other)).status_code == 404
    assert (
        client.get("/workers/" + identifier + "/commands", headers=headers(other)).status_code
        == 404
    )
    assert (
        client.post(
            "/workers/" + identifier + "/commands",
            headers=headers(user),
            json={"request_id": str(uuid4()), "kind": "DESTROY"},
        ).status_code
        == 409
    )
    assert (
        client.post(
            "/workers", headers=headers(user), json={**data, "host_path": "/root"}
        ).status_code
        == 422
    )


def test_runner_commits_queue_before_host_call_and_finishes_once(session, user):
    command = WorkerService(session, user.id).queue("CREATE", {})
    session.commit()
    manager = FakeManager()
    assert execute_one(session, manager)
    assert command.status == "SUCCEEDED"
    assert session.get(Worker, command.worker_id).status == "BOOTING"
    assert not execute_one(session, manager)
    assert manager.calls == 1
    assert session.scalar(select(func.count()).select_from(OutboxEvent)) == 1


def test_runner_recovers_cached_operation_without_repeating_side_effect(session, user):
    command = WorkerService(session, user.id).queue("CREATE", {})
    session.commit()
    acquired = claim(session, datetime.now(UTC) - timedelta(seconds=601))
    assert acquired.id == command.id
    manager = FakeManager()
    manager.previous = {
        "status": "SUCCEEDED",
        "result": {"worker": {"status": "READY", "ip": "192.168.122.10"}},
    }
    assert execute_one(session, manager)
    assert command.status == "SUCCEEDED"
    assert manager.calls == 0


def test_uncertain_connection_retries_query_not_job(session, user):
    command = WorkerService(session, user.id).queue("CREATE", {})
    session.commit()
    manager = FakeManager()
    manager.error = ManagerError("manager_unreachable", uncertain=True)
    execute_one(session, manager)
    assert command.status == "PENDING"
    assert not execute_one(session, manager)
    command.lease_until = datetime.now(UTC) - timedelta(seconds=1)
    session.commit()
    manager.previous = {"status": "RUNNING"}
    execute_one(session, manager)
    assert manager.calls == 1
    assert command.status == "PENDING"
    command.lease_until = datetime.now(UTC) - timedelta(seconds=1)
    session.commit()
    manager.previous = {"status": "FAILED", "result": {"code": "operation_recovery_required"}}
    execute_one(session, manager)
    assert command.status == "FAILED"
    assert manager.calls == 1


def test_snapshot_and_execution_guards(session, user):
    service = WorkerService(session, user.id)
    create = service.queue("CREATE", {})
    session.commit()
    manager = FakeManager()
    execute_one(session, manager)
    with pytest.raises(AgentError, match="worker_not_ready"):
        service.queue("EXECUTE", {"script": "id"}, worker_id=create.worker_id)
    session.rollback()
    worker = service.worker(create.worker_id)
    worker.status = "READY"
    session.commit()
    snapshot = service.queue("SNAPSHOT", {}, worker_id=worker.id)
    session.commit()
    assert session.get(WorkerSnapshot, snapshot.arguments["snapshot_id"]).status == "PENDING"
    manager.error = ManagerError("host_disk_reserve")
    execute_one(session, manager)
    assert session.get(WorkerSnapshot, snapshot.arguments["snapshot_id"]).status == "FAILED"
    with pytest.raises(AgentError, match="snapshot_not_found"):
        service.queue("RESTORE", {"snapshot_id": str(uuid4())}, worker_id=worker.id)


def test_action_queue_is_truthful_and_json_serializable(session, user):
    from test_context import history

    _, source = history(session, user, ["Crie um worker Linux"])
    results = ActionEngine(session).process(
        [ActionProposal(type="create_linux_worker", arguments={"name": "worker-chat"})], source[-1]
    )
    session.commit()
    assert results[0]["status"] == "SUCCEEDED"
    assert results[0]["data"]["status"] == "PENDING"
    assert "solicitada" in results[0]["message"]
