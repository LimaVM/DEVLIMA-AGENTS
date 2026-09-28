from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    return create_engine(
        get_settings().database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        pool_timeout=5,
        connect_args={"connect_timeout": 5, "options": "-c statement_timeout=10000"},
        hide_parameters=True,
    )


def get_session() -> Generator[Session, None, None]:
    with sessionmaker(bind=get_engine(), expire_on_commit=False)() as session:
        yield session
