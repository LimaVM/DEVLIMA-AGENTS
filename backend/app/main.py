import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.auth import router as auth_router
from app.api.calls import router as calls_router
from app.api.chat import router as chat_router
from app.api.devices import router as devices_router
from app.api.llm import router as llm_router
from app.api.memories import router as memories_router
from app.api.planning import router as planning_router
from app.api.websocket import router as websocket_router
from app.api.workers import router as workers_router
from app.config import get_settings
from app.db.session import get_engine

logger = logging.getLogger("devlima")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    get_engine().dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.8.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.enable_api_docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.enable_api_docs else None,
    )

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        request.state.request_id = str(uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError):
        # FastAPI's default includes rejected input, which can contain passwords.
        errors = [
            {"loc": item["loc"], "msg": item["msg"], "type": item["type"]}
            for item in error.errors()
        ]
        return JSONResponse(status_code=422, content={"detail": errors})

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, error: SQLAlchemyError):
        logger.error("Database failure request_id=%s", request.state.request_id)
        return JSONResponse(status_code=503, content={"detail": "Banco indisponível"})

    @app.get("/health/live", tags=["health"])
    def live():
        return {"status": "ok", "phase": 8}

    @app.get("/health/ready", tags=["health"])
    def ready():
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
            revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar()
        if revision != "0007_calls":
            return JSONResponse(status_code=503, content={"status": "schema_not_ready"})
        return {"status": "ready", "database": "ok", "schema": revision}

    app.include_router(calls_router)
    app.include_router(auth_router)
    app.include_router(llm_router)
    app.include_router(chat_router)
    app.include_router(memories_router)
    app.include_router(planning_router)
    app.include_router(workers_router)
    app.include_router(devices_router)
    app.include_router(websocket_router)
    return app


app = create_app()
