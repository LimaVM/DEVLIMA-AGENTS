from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from vm_manager.app import Operation, create_app
from vm_manager.config import Settings, VMError
from vm_manager.linux import LinuxWorkerProvider, WindowsWorkerProvider
from vm_manager.service import WorkerService


# Documentação: Define o tipo FakeProvider e reúne o estado/contrato descrito para este módulo.
class FakeProvider:
    # Documentação: Inicializa FakeProvider com as dependências e estado declarados.
    def __init__(self):
        self.rows, self.calls = {}, []
        self.fail = None

    # Documentação: Libera FakeProvider.close, segundo o contrato e as verificações deste módulo.
    def close(self):
        pass

    # Documentação: Confere FakeProvider.check_resources, segundo o contrato e as verificações
    # deste módulo.
    def check_resources(self, rows, desired):
        if len([row for row in rows if row["status"] != "DESTROYED"]) >= 2:
            raise VMError("worker_quota_exceeded", 429)

    # Documentação: Cria FakeProvider.create, segundo o contrato e as verificações deste módulo.
    def create(self, row):
        self.calls.append("CREATE")
        if self.fail:
            raise VMError(self.fail)
        self.rows[row["id"]] = {**row, "status": "BOOTING"}
        return self.rows[row["id"]]

    # Documentação: Implementa FakeProvider.status como parte do fluxo descrito para este arquivo.
    def status(self, row):
        return self.rows.get(row["id"], {**row, "status": "ERROR"})

    # Documentação: Implementa FakeProvider.destroy como parte do fluxo descrito para este
    # arquivo.
    def destroy(self, row):
        self.calls.append("DESTROY")
        self.rows[row["id"]] = {**row, "status": "DESTROYED"}
        return self.rows[row["id"]]

    # Documentação: Interrompe FakeProvider.stop, segundo o contrato e as verificações deste
    # módulo.
    def stop(self, row):
        self.rows[row["id"]] = {**row, "status": "STOPPED"}

    # Documentação: Inicia FakeProvider.start, segundo o contrato e as verificações deste módulo.
    def start(self, row):
        self.rows[row["id"]] = {**row, "status": "BOOTING"}
        return self.rows[row["id"]]

    # Documentação: Implementa FakeProvider.reset como parte do fluxo descrito para este arquivo.
    def reset(self, row, generation):
        return self.create({**row, "generation": generation})

    # Documentação: Implementa FakeProvider.snapshot como parte do fluxo descrito para este
    # arquivo.
    def snapshot(self, row, identifier):
        return {"id": str(identifier), "worker_id": row["id"], "sha256": "a" * 64}, row

    # Documentação: Implementa FakeProvider.restore como parte do fluxo descrito para este
    # arquivo.
    def restore(self, row, snapshot):
        return row

    # Documentação: Implementa FakeProvider.execute como parte do fluxo descrito para este
    # arquivo.
    def execute(self, row, identifier, script, timeout):
        self.calls.append("EXECUTE")
        return {"exit_code": 0, "output": "done", "truncated": False}


@pytest.fixture
# Documentação: Implementa setup como parte do fluxo descrito para este arquivo.
def setup(tmp_path):
    config = Settings(token="t" * 40, state_root=tmp_path / "registry")
    provider = FakeProvider()
    return config, provider, WorkerService(config, provider)


# Documentação: Implementa operation como parte do fluxo descrito para este arquivo.
def operation(kind="CREATE", **args):
    return Operation(request_id=uuid4(), worker_id=uuid4(), owner=uuid4(), kind=kind, **args)


# Documentação: Verifica o cenário test_auth_and_private_contract; as condições e resultados
# esperados aparecem nos asserts.
def test_auth_and_private_contract(setup):
    config, provider, _ = setup
    with TestClient(create_app(config, provider)) as client:
        assert client.get("/health").status_code == 401
        headers = {"Authorization": "Bearer " + "t" * 40}
        assert client.get("/health", headers=headers).status_code == 200
        assert client.get("/docs", headers=headers).status_code == 404
        request = operation()
        response = client.post(
            "/v1/operations", headers=headers, json=request.model_dump(mode="json")
        )
        assert response.status_code == 200
        wrong = client.get(
            "/v1/workers/" + str(request.worker_id), headers=headers, params={"owner": str(uuid4())}
        )
        assert wrong.status_code == 404
        bad = client.post(
            "/v1/operations",
            headers=headers,
            json={
                **request.model_dump(mode="json"),
                "kind": "HOST_SHELL",
                "script": "secret-value",
            },
        )
        assert bad.status_code == 422
        assert "secret-value" not in bad.text


# Documentação: Verifica o cenário test_idempotency_and_argument_conflict; as condições e
# resultados esperados aparecem nos asserts.
def test_idempotency_and_argument_conflict(setup):
    _, provider, service = setup
    request = operation()
    first = service.perform(request)
    assert service.perform(request) == first
    assert provider.calls == ["CREATE"]
    with pytest.raises(VMError, match="idempotency_conflict"):
        service.perform(request.model_copy(update={"vcpu": 3}))
    with pytest.raises(VMError, match="worker_already_exists"):
        service.perform(request.model_copy(update={"request_id": uuid4()}))
    assert service.registry.worker(request.worker_id)["status"] == "BOOTING"


# Documentação: Verifica o cenário test_quota_owner_and_destroy_cleanup; as condições e resultados
# esperados aparecem nos asserts.
def test_quota_owner_and_destroy_cleanup(setup):
    _, provider, service = setup
    requests = [operation() for _ in range(3)]
    for request in requests[:2]:
        service.perform(request)
    with pytest.raises(VMError, match="worker_quota_exceeded"):
        service.perform(requests[2])
    row = service.registry.worker(requests[2].worker_id)
    assert row["status"] == "ERROR"
    victim = requests[0]
    with pytest.raises(VMError, match="not_found"):
        service.perform(operation("DESTROY").model_copy(update={"worker_id": victim.worker_id}))
    destroyed = service.perform(
        operation("DESTROY").model_copy(
            update={"worker_id": requests[2].worker_id, "owner": requests[2].owner}
        )
    )
    assert destroyed["worker"]["status"] == "DESTROYED"
    assert provider.calls.count("DESTROY") == 1


# Documentação: Verifica o cenário test_recovery_never_reexecutes_uncertain_job; as condições e
# resultados esperados aparecem nos asserts.
def test_recovery_never_reexecutes_uncertain_job(setup):
    _, provider, service = setup
    request = operation()
    service.perform(request)
    job = operation("EXECUTE", script="touch result").model_copy(
        update={"owner": request.owner, "worker_id": request.worker_id}
    )
    service.registry.begin(
        job.request_id, job.worker_id, job.kind, job.model_dump(mode="json", exclude_none=True)
    )
    service.reconcile()
    assert service.registry.operation(job.request_id, job.owner)["status"] == "FAILED"
    assert "EXECUTE" not in provider.calls
    with pytest.raises(VMError, match="operation_recovery_required"):
        service.perform(job)


# Documentação: Verifica o cenário test_reconcile_proves_create_from_actual_provider; as condições
# e resultados esperados aparecem nos asserts.
def test_reconcile_proves_create_from_actual_provider(setup):
    _, _, service = setup
    request = operation()
    service.perform(request)
    with service.registry.connect() as db:
        db.execute(
            "UPDATE operations SET status='RUNNING',result=NULL WHERE id=?",
            (str(request.request_id),),
        )
    service.reconcile()
    assert service.registry.operation(request.request_id, request.owner)["status"] == "SUCCEEDED"


# Documentação: Verifica o cenário test_snapshot_limit_and_cross_worker_restore; as condições e
# resultados esperados aparecem nos asserts.
def test_snapshot_limit_and_cross_worker_restore(setup):
    _, _, service = setup
    request = operation()
    service.perform(request)
    for _ in range(5):
        service.perform(
            operation("SNAPSHOT", snapshot_id=uuid4()).model_copy(
                update={"worker_id": request.worker_id, "owner": request.owner}
            )
        )
    with pytest.raises(VMError, match="snapshot_quota_exceeded"):
        service.perform(
            operation("SNAPSHOT", snapshot_id=uuid4()).model_copy(
                update={"worker_id": request.worker_id, "owner": request.owner}
            )
        )
    with pytest.raises(VMError, match="snapshot_not_found"):
        service.perform(
            operation("RESTORE", snapshot_id=uuid4()).model_copy(
                update={"worker_id": request.worker_id, "owner": request.owner}
            )
        )


# Documentação: Verifica o cenário test_linux_path_and_xml_protection; as condições e resultados
# esperados aparecem nos asserts.
def test_linux_path_and_xml_protection(tmp_path):
    provider = LinuxWorkerProvider.__new__(LinuxWorkerProvider)
    provider.root = tmp_path.resolve()
    identifier = uuid4()
    outside = tmp_path.parent / ("outside-" + str(uuid4()))
    outside.mkdir()
    (tmp_path / str(identifier)).symlink_to(outside, target_is_directory=True)
    with pytest.raises(VMError, match="unsafe_worker_path"):
        provider.directory(identifier)
    (tmp_path / str(identifier)).unlink()
    (tmp_path / str(identifier)).mkdir()
    (tmp_path / str(identifier) / "disk.qcow2").symlink_to(outside / "template")
    with pytest.raises(VMError, match="unsafe_worker_path"):
        provider.path(identifier, "disk.qcow2")
    with pytest.raises(VMError, match="unsafe_worker_path"):
        provider.path(identifier, "../template")


# Documentação: Verifica o cenário test_xml_labels_cannot_inject_host_paths; as condições e
# resultados esperados aparecem nos asserts.
def test_xml_labels_cannot_inject_host_paths(tmp_path):
    provider = LinuxWorkerProvider.__new__(LinuxWorkerProvider)
    provider.settings = Settings(token="t" * 40)
    row = {
        "id": str(uuid4()),
        "owner": str(uuid4()),
        "generation": str(uuid4()),
        "name": "label",
        "vcpu": 2,
        "ram_mb": 2048,
    }
    xml = provider.make_xml(row, tmp_path / "disk.qcow2", tmp_path / "seed.iso")
    assert "urn:devlima:worker:1" in xml
    assert "devlima-worker-egress" in xml
    assert "<filesystem" not in xml and "<hostdev" not in xml
    with pytest.raises(VMError, match="windows_not_available"):
        WindowsWorkerProvider().create()


@pytest.mark.parametrize("problem", ["metadata", "owner", "storage"])
# Documentação: Verifica o cenário test_foreign_domains_never_reach_lifecycle_commands; as
# condições e resultados esperados aparecem nos asserts.
def test_foreign_domains_never_reach_lifecycle_commands(tmp_path, problem):
    import xml.etree.ElementTree as ET
    from types import SimpleNamespace

    provider = LinuxWorkerProvider.__new__(LinuxWorkerProvider)
    provider.root = tmp_path.resolve()
    provider.settings = Settings(token="t" * 40)
    row = {
        "id": str(uuid4()),
        "owner": str(uuid4()),
        "generation": str(uuid4()),
        "vcpu": 2,
        "ram_mb": 2048,
    }
    disk = tmp_path / row["id"] / "disk.qcow2"
    xml = ET.fromstring(provider.make_xml(row, disk, tmp_path / "seed.iso"))
    metadata = xml.find("metadata/{urn:devlima:worker:1}worker")
    if problem == "metadata":
        xml.remove(xml.find("metadata"))
    elif problem == "owner":
        metadata.set("owner", str(uuid4()))
    else:
        xml.find("devices/disk[@device='disk']/source").set("file", str(tmp_path / "foreign.qcow2"))

    # Documentação: Define o tipo test_foreign_domains_never_reach_lifecycle_commands.Domain e
    # reúne o estado/contrato descrito para este módulo.
    class Domain:
        # Documentação: Implementa
        # test_foreign_domains_never_reach_lifecycle_commands.Domain.XMLDesc como parte do fluxo
        # descrito para este arquivo.
        def XMLDesc(self, _):
            return ET.tostring(xml, encoding="unicode")

    provider.conn = SimpleNamespace(lookupByUUIDString=lambda _: Domain())
    provider.libvirt = SimpleNamespace(libvirtError=RuntimeError)
    with pytest.raises(VMError) as issue:
        provider.domain(row)
    assert issue.value.status == 403
    assert issue.value.code in {"foreign_domain_protected", "foreign_storage_protected"}
