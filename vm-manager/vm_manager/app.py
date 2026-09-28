import secrets
from contextlib import asynccontextmanager
from typing import Literal
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field, model_validator

from vm_manager.config import Settings, VMError
from vm_manager.linux import LinuxWorkerProvider
from vm_manager.service import WorkerService


# Documentação: Define o tipo Operation e reúne o estado/contrato descrito para este módulo.
class Operation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: UUID
    worker_id: UUID
    owner: UUID
    kind: Literal["CREATE", "DESTROY", "RESET", "START", "STOP", "SNAPSHOT", "RESTORE", "EXECUTE"]
    name: str | None = Field(None, min_length=1, max_length=64, pattern=r"^[a-z0-9-]+$")
    vcpu: int = Field(2, ge=1, le=4)
    ram_mb: int = Field(2048, ge=512, le=8192)
    disk_gb: int = Field(20, ge=10, le=80)
    snapshot_id: UUID | None = None
    script: str | None = Field(None, min_length=1, max_length=8000)
    timeout: int = Field(120, ge=1, le=300)

    @model_validator(mode="after")
    # Documentação: Implementa Operation.operation_arguments como parte do fluxo descrito para
    # este arquivo.
    def operation_arguments(self):
        if self.kind in {"SNAPSHOT", "RESTORE"} and self.snapshot_id is None:
            raise ValueError("snapshot_id required")
        if self.kind == "EXECUTE" and (self.script is None or not self.script.strip()):
            raise ValueError("script required")
        if self.kind != "EXECUTE" and self.script is not None:
            raise ValueError("script only allowed in worker execution")
        return self


# Documentação: Cria create_app, segundo o contrato e as verificações deste módulo.
def create_app(settings=None, provider=None):
    config = settings or Settings()
    bearer = HTTPBearer(auto_error=False)

    @asynccontextmanager
    # Documentação: Implementa create_app.lifespan como parte do fluxo descrito para este arquivo.
    async def lifespan(app):
        backend = provider or LinuxWorkerProvider(config)
        app.state.service = WorkerService(config, backend)
        app.state.service.reconcile()
        yield
        backend.close()

    app = FastAPI(
        title="DEVLIMA VM Manager",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    # Documentação: Implementa create_app.authenticated como parte do fluxo descrito para este
    # arquivo.
    def authenticated(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if credentials is None or not secrets.compare_digest(
            credentials.credentials, config.token.get_secret_value()
        ):
            raise HTTPException(401, "invalid_manager_token")

    # Documentação: Implementa create_app.service como parte do fluxo descrito para este arquivo.
    def service(request: Request, _: None = Depends(authenticated)):
        return request.app.state.service

    @app.exception_handler(VMError)
    # Documentação: Implementa create_app.vm_error como parte do fluxo descrito para este arquivo.
    async def vm_error(_, error):
        return JSONResponse(status_code=error.status, content={"detail": error.code})

    @app.exception_handler(RequestValidationError)
    # Documentação: Implementa create_app.validation_error como parte do fluxo descrito para este
    # arquivo.
    async def validation_error(_, error):
        return JSONResponse(
            status_code=422,
            content={
                "detail": [{"loc": item["loc"], "type": item["type"]} for item in error.errors()]
            },
        )

    @app.get("/health")
    # Documentação: Implementa create_app.health como parte do fluxo descrito para este arquivo.
    def health(manager: WorkerService = Depends(service)):
        return {"status": "ok", "template": "verified", "workers": len(manager.registry.workers())}

    @app.post("/v1/operations")
    # Documentação: Implementa create_app.perform como parte do fluxo descrito para este arquivo.
    def perform(data: Operation, manager: WorkerService = Depends(service)):
        return manager.perform(data)

    @app.get("/v1/operations/{identifier}")
    # Documentação: Implementa create_app.operation como parte do fluxo descrito para este
    # arquivo.
    def operation(
        identifier: UUID, owner: UUID = Query(), manager: WorkerService = Depends(service)
    ):
        return manager.registry.operation(identifier, owner)

    @app.get("/v1/workers/{identifier}")
    # Documentação: Implementa create_app.status como parte do fluxo descrito para este arquivo.
    def status(identifier: UUID, owner: UUID = Query(), manager: WorkerService = Depends(service)):
        return manager.status(identifier, owner)

    @app.get("/v1/workers")
    # Documentação: Implementa create_app.workers como parte do fluxo descrito para este arquivo.
    def workers(owner: UUID = Query(), manager: WorkerService = Depends(service)):
        return [manager.public(row) for row in manager.registry.workers(owner)]

    return app


# Documentação: Implementa app_factory como parte do fluxo descrito para este arquivo.
def app_factory():
    return create_app()
