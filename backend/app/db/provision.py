import json
import sys

import psycopg
from psycopg import sql


def main():
    values = json.load(sys.stdin)
    try:
        with psycopg.connect(
            host="postgres",
            dbname=values["POSTGRES_DB"],
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            connect_timeout=10,
        ) as db:
            db.execute("SET LOCAL log_statement = 'none'")
            db.execute("SET LOCAL log_min_error_statement = 'PANIC'")
            for name, password in (
                (values["MIGRATION_POSTGRES_USER"], values["MIGRATION_POSTGRES_PASSWORD"]),
                (values["RUNTIME_POSTGRES_USER"], values["RUNTIME_POSTGRES_PASSWORD"]),
            ):
                if not db.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (name,)).fetchone():
                    db.execute(sql.SQL("CREATE ROLE {} LOGIN").format(sql.Identifier(name)))
                db.execute(
                    sql.SQL(
                        "ALTER ROLE {} WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE "
                        "NOREPLICATION NOBYPASSRLS PASSWORD {}"
                    ).format(sql.Identifier(name), sql.Literal(password))
                )
            migrate, runtime = map(
                sql.Identifier, (values["MIGRATION_POSTGRES_USER"], values["RUNTIME_POSTGRES_USER"])
            )
            database = sql.Identifier(values["POSTGRES_DB"])
            db.execute(sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(database))
            db.execute(
                sql.SQL("GRANT CONNECT ON DATABASE {} TO {}, {}").format(database, migrate, runtime)
            )
            db.execute("REVOKE ALL ON SCHEMA public FROM PUBLIC")
            db.execute(sql.SQL("ALTER SCHEMA public OWNER TO {}").format(migrate))
            for name, kind in db.execute(
                "SELECT c.relname,c.relkind FROM pg_class c JOIN pg_namespace n ON "
                "n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind IN "
                "('r','S')"
            ).fetchall():
                object_type = sql.SQL("SEQUENCE" if kind == "S" else "TABLE")
                db.execute(
                    sql.SQL("ALTER {} public.{} OWNER TO {}").format(
                        object_type, sql.Identifier(name), migrate
                    )
                )
            db.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {}").format(runtime))
            db.execute(sql.SQL("REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {}").format(runtime))
            db.execute(
                sql.SQL(
                    "GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO {}"
                ).format(runtime)
            )
            if db.execute("SELECT to_regclass('public.alembic_version')").fetchone()[0] is not None:
                db.execute(
                    sql.SQL("REVOKE INSERT,UPDATE,DELETE ON public.alembic_version FROM {}").format(
                        runtime
                    )
                )
            db.execute(
                sql.SQL("GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA public TO {}").format(
                    runtime
                )
            )
            db.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA public GRANT "
                    "SELECT,INSERT,UPDATE,DELETE ON TABLES TO {}"
                ).format(migrate, runtime)
            )
            db.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA public GRANT "
                    "USAGE,SELECT ON SEQUENCES TO {}"
                ).format(migrate, runtime)
            )
            db.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES FOR ROLE {} REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC"
                ).format(migrate)
            )
        print("Roles provisioned; runtime has CRUD, no DDL/admin privileges.")
    except Exception:
        print(
            "Role provisioning failed; details intentionally withheld to protect credentials.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
