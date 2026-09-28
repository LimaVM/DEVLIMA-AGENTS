import fcntl
import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime

from vm_manager.config import VMError


# Documentação: Implementa now como parte do fluxo descrito para este arquivo.
def now():
    return datetime.now(UTC).isoformat()


# Documentação: Define o tipo Registry e reúne o estado/contrato descrito para este módulo.
class Registry:
    # Documentação: Inicializa Registry com as dependências e estado declarados.
    def __init__(self, root):
        self.root = root
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.database = root / "registry.sqlite3"
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS workers (
                    id TEXT PRIMARY KEY, owner TEXT NOT NULL, data TEXT NOT NULL,
                    status TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS operations (
                    id TEXT PRIMARY KEY, worker_id TEXT NOT NULL,
                    owner TEXT NOT NULL, signature TEXT NOT NULL,
                    kind TEXT NOT NULL, arguments TEXT NOT NULL, status TEXT NOT NULL,
                    result TEXT, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS snapshots (
                    id TEXT PRIMARY KEY, worker_id TEXT NOT NULL, data TEXT NOT NULL,
                    status TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, worker_id TEXT,
                    operation TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
                );
            """)

    @contextmanager
    # Documentação: Implementa Registry.connect como parte do fluxo descrito para este arquivo.
    def connect(self):
        db = sqlite3.connect(self.database, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA foreign_keys=ON")
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    # Documentação: Serializa acesso ao estado operacional para evitar lifecycle concorrente no
    # manager.
    def lock(self):
        with (self.root / "operations.lock").open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    # Documentação: Implementa Registry.worker como parte do fluxo descrito para este arquivo.
    def worker(self, identifier, owner=None):
        with self.connect() as db:
            row = db.execute("SELECT * FROM workers WHERE id=?", (str(identifier),)).fetchone()
        if row is None or (owner is not None and row["owner"] != str(owner)):
            raise VMError("not_found", 404)
        return json.loads(row["data"]) | {
            "id": row["id"],
            "owner": row["owner"],
            "status": row["status"],
            "updated_at": row["updated_at"],
        }

    # Documentação: Implementa Registry.workers como parte do fluxo descrito para este arquivo.
    def workers(self, owner=None):
        with self.connect() as db:
            rows = db.execute("SELECT * FROM workers ORDER BY updated_at DESC").fetchall()
        return [
            json.loads(row["data"])
            | {"id": row["id"], "owner": row["owner"], "status": row["status"]}
            for row in rows
            if owner is None or row["owner"] == str(owner)
        ]

    # Documentação: Persiste Registry.save, segundo o contrato e as verificações deste módulo.
    def save(self, row, status=None):
        row = dict(row)
        identifier, owner = row.pop("id"), row.pop("owner")
        state = status or row.pop("status", "CREATING")
        row.pop("status", None)
        row.pop("updated_at", None)
        with self.connect() as db:
            db.execute(
                "INSERT INTO workers VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
                "data=excluded.data,status=excluded.status,updated_at=excluded.updated_at",
                (identifier, owner, json.dumps(row), state, now()),
            )
        return self.worker(identifier)

    # Documentação: Implementa Registry.begin como parte do fluxo descrito para este arquivo.
    def begin(self, request_id, worker_id, kind, arguments):
        signature = hashlib.sha256(
            json.dumps(
                {"worker_id": str(worker_id), "kind": kind, "arguments": arguments}, sort_keys=True
            ).encode()
        ).hexdigest()
        with self.connect() as db:
            row = db.execute("SELECT * FROM operations WHERE id=?", (str(request_id),)).fetchone()
            if row:
                if row["signature"] != signature:
                    raise VMError("idempotency_conflict")
                if row["status"] == "SUCCEEDED":
                    return json.loads(row["result"])
                # A crashed command may already have changed guest/host state.
                raise VMError("operation_recovery_required")
            db.execute(
                "INSERT INTO operations VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    str(request_id),
                    str(worker_id),
                    str(arguments["owner"]),
                    signature,
                    kind,
                    json.dumps(arguments),
                    "RUNNING",
                    None,
                    now(),
                ),
            )
        return None

    # Documentação: Implementa Registry.finish como parte do fluxo descrito para este arquivo.
    def finish(self, request_id, worker_id, kind, result, status="SUCCEEDED"):
        with self.connect() as db:
            db.execute(
                "UPDATE operations SET status=?,result=?,updated_at=? WHERE id=?",
                (status, json.dumps(result), now(), str(request_id)),
            )
            db.execute(
                "INSERT INTO audit(worker_id,operation,status,created_at) VALUES(?,?,?,?)",
                (str(worker_id), kind, status, now()),
            )

    # Documentação: Implementa Registry.snapshot como parte do fluxo descrito para este arquivo.
    def snapshot(self, identifier, worker_id):
        with self.connect() as db:
            row = db.execute(
                "SELECT * FROM snapshots WHERE id=? AND worker_id=? AND status='AVAILABLE'",
                (str(identifier), str(worker_id)),
            ).fetchone()
        if not row:
            raise VMError("snapshot_not_found", 404)
        return json.loads(row["data"])

    # Documentação: Persiste Registry.save_snapshot, segundo o contrato e as verificações deste
    # módulo.
    def save_snapshot(self, identifier, worker_id, data):
        with self.connect() as db:
            db.execute(
                "INSERT INTO snapshots VALUES(?,?,?,?,?)",
                (str(identifier), str(worker_id), json.dumps(data), "AVAILABLE", now()),
            )

    # Documentação: Remove Registry.delete_snapshots, segundo o contrato e as verificações deste
    # módulo.
    def delete_snapshots(self, worker_id):
        with self.connect() as db:
            db.execute("UPDATE snapshots SET status='DELETED' WHERE worker_id=?", (str(worker_id),))

    # Documentação: Implementa Registry.operation como parte do fluxo descrito para este arquivo.
    def operation(self, identifier, owner):
        with self.connect() as db:
            row = db.execute(
                "SELECT * FROM operations WHERE id=? AND owner=?", (str(identifier), str(owner))
            ).fetchone()
        if row is None:
            raise VMError("not_found", 404)
        return {
            "id": row["id"],
            "worker_id": row["worker_id"],
            "status": row["status"],
            "result": json.loads(row["result"]) if row["result"] else None,
        }

    # Documentação: Implementa Registry.incomplete como parte do fluxo descrito para este arquivo.
    def incomplete(self):
        with self.connect() as db:
            rows = db.execute("SELECT * FROM operations WHERE status='RUNNING'").fetchall()
        return [{**dict(row), "arguments": json.loads(row["arguments"])} for row in rows]
