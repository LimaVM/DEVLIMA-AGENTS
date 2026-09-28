#!/usr/bin/env python3
"""Run inside the backend container after switching to runtime role."""

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from app.db.session import get_engine

with get_engine().connect() as db:
    role = db.execute(
        text(
            "SELECT current_user,rolsuper,rolcreatedb,rolcreaterole,rolbypassrls FROM pg_roles WHERE rolname=current_user"  # noqa: E501
        )
    ).one()
    assert role[0] == "agent_runtime" and all(value is False for value in role[1:])
    assert (
        db.execute(text("SELECT has_schema_privilege(current_user,'public','CREATE')")).scalar()
        is False
    )
    assert (
        db.execute(text("SELECT has_table_privilege(current_user,'users','INSERT')")).scalar()
        is True
    )
    assert (
        db.execute(text("SELECT has_table_privilege(current_user,'users','TRUNCATE')")).scalar()
        is False
    )
    assert (
        db.execute(
            text("SELECT has_table_privilege(current_user,'alembic_version','UPDATE')")
        ).scalar()
        is False
    )
    for statement in (
        "CREATE TABLE public.runtime_must_not_create(id integer)",
        "ALTER TABLE public.users ADD COLUMN runtime_must_not_alter integer",
        "TRUNCATE public.users CASCADE",
    ):
        transaction = db.begin_nested()
        try:
            db.execute(text(statement))
        except DBAPIError as error:
            assert getattr(error.orig, "sqlstate", None) == "42501"
            transaction.rollback()
        else:
            transaction.rollback()
            raise AssertionError("Runtime unexpectedly obtained administrative permission")
print("Runtime privilege guards passed; DDL and TRUNCATE denied.")
