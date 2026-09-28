from vm_manager.config import VMError
from vm_manager.provider import WorkerProvider
from vm_manager.registry import Registry


class WorkerService:
    def __init__(self, settings, provider: WorkerProvider):
        self.settings, self.provider = settings, provider
        self.registry = Registry(settings.state_root)

    def public(self, row):
        return {
            key: row.get(key)
            for key in (
                "id",
                "owner",
                "name",
                "vcpu",
                "ram_mb",
                "disk_gb",
                "status",
                "ip",
                "generation",
                "error_code",
                "updated_at",
            )
        }

    def status(self, identifier, owner):
        with self.registry.lock():
            row = self.registry.worker(identifier, owner)
            actual = self.provider.status(row)
            return self.public(self.registry.save(actual))

    def reconcile(self):
        with self.registry.lock():
            for row in self.registry.workers():
                try:
                    self.registry.save(self.provider.status(row))
                except VMError as error:
                    self.registry.save({**row, "error_code": error.code}, "ERROR")
            for operation in self.registry.incomplete():
                try:
                    row = self.registry.worker(operation["worker_id"], operation["owner"])
                    state = row["status"]
                    achieved = (
                        (operation["kind"] == "CREATE" and state in {"READY", "BOOTING"})
                        or (operation["kind"] == "DESTROY" and state == "DESTROYED")
                        or (operation["kind"] == "STOP" and state == "STOPPED")
                        or (operation["kind"] == "START" and state in {"READY", "BOOTING"})
                    )
                    if achieved:
                        self.registry.finish(
                            operation["id"],
                            row["id"],
                            operation["kind"],
                            {"worker": self.public(row)},
                        )
                    else:
                        self.registry.finish(
                            operation["id"],
                            row["id"],
                            operation["kind"],
                            {"code": "operation_recovery_required"},
                            "FAILED",
                        )
                except VMError:
                    self.registry.finish(
                        operation["id"],
                        operation["worker_id"],
                        operation["kind"],
                        {"code": "operation_recovery_required"},
                        "FAILED",
                    )

    def perform(self, request):
        data = request.model_dump(mode="json", exclude_none=True)
        identifier, owner, request_id, kind = (
            data["worker_id"],
            data["owner"],
            data["request_id"],
            data["kind"],
        )
        with self.registry.lock():
            cached = self.registry.begin(request_id, identifier, kind, data)
            if cached is not None:
                return cached
            created_new = False
            try:
                if kind == "CREATE":
                    if any(row["id"] == identifier for row in self.registry.workers()):
                        raise VMError("worker_already_exists")
                    desired = {
                        "id": identifier,
                        "owner": owner,
                        "name": data.get("name") or "Linux worker",
                        "vcpu": data["vcpu"],
                        "ram_mb": data["ram_mb"],
                        "disk_gb": data["disk_gb"],
                        "generation": request_id,
                        "ip": None,
                    }
                    row = self.registry.save(desired, "CREATING")
                    created_new = True
                    self.provider.check_resources(
                        [other for other in self.registry.workers() if other["id"] != identifier],
                        desired,
                    )
                    row = self.provider.create(row)
                    result = {"worker": self.public(self.registry.save(row))}
                else:
                    row = self.registry.worker(identifier, owner)
                    if row["status"] == "DESTROYED" and kind != "DESTROY":
                        raise VMError("worker_destroyed")
                    if kind == "DESTROY":
                        self.registry.save(row, "DESTROYING")
                        result = {
                            "worker": self.public(self.registry.save(self.provider.destroy(row)))
                        }
                        self.registry.delete_snapshots(identifier)
                    elif kind == "START":
                        actual = self.provider.status(row)
                        if actual["status"] == "STOPPED":
                            self.provider.check_resources(
                                [
                                    other
                                    for other in self.registry.workers()
                                    if other["id"] != identifier
                                ],
                                row,
                            )
                        result = {
                            "worker": self.public(self.registry.save(self.provider.start(row)))
                        }
                    elif kind == "STOP":
                        self.provider.stop(row)
                        result = {"worker": self.public(self.registry.save(row, "STOPPED"))}
                    elif kind == "RESET":
                        if self.provider.status(row)["status"] in {"STOPPED", "ERROR"}:
                            self.provider.check_resources(
                                [
                                    other
                                    for other in self.registry.workers()
                                    if other["id"] != identifier
                                ],
                                row,
                            )
                        self.registry.save(row, "RESETTING")
                        result = {
                            "worker": self.public(
                                self.registry.save(self.provider.reset(row, request_id))
                            )
                        }
                    elif kind == "SNAPSHOT":
                        with self.registry.connect() as db:
                            count = db.execute(
                                "SELECT COUNT(*) FROM snapshots "
                                "WHERE worker_id=? AND status='AVAILABLE'",
                                (identifier,),
                            ).fetchone()[0]
                        if count >= 5:
                            raise VMError("snapshot_quota_exceeded", 429)
                        snapshot, state = self.provider.snapshot(row, data["snapshot_id"])
                        self.registry.save_snapshot(data["snapshot_id"], identifier, snapshot)
                        result = {
                            "worker": self.public(self.registry.save(state)),
                            "snapshot": snapshot,
                        }
                    elif kind == "RESTORE":
                        snapshot = self.registry.snapshot(data["snapshot_id"], identifier)
                        result = {
                            "worker": self.public(
                                self.registry.save(self.provider.restore(row, snapshot))
                            )
                        }
                    elif kind == "EXECUTE":
                        execution = self.provider.execute(
                            row, request_id, data["script"], data["timeout"]
                        )
                        result = {"worker": self.public(row), "job": execution}
                    else:
                        raise VMError("operation_not_allowed", 422)
                self.registry.finish(request_id, identifier, kind, result)
                return result
            except VMError as error:
                if kind == "CREATE" and created_new:
                    try:
                        row = self.registry.worker(identifier, owner)
                        self.registry.save({**row, "error_code": error.code}, "ERROR")
                    except VMError:
                        pass
                self.registry.finish(request_id, identifier, kind, {"code": error.code}, "FAILED")
                raise
            except Exception:
                self.registry.finish(
                    request_id, identifier, kind, {"code": "manager_error"}, "FAILED"
                )
                raise VMError("manager_error", 503) from None
