import argparse
import getpass
import re
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.models import AuditLog, User
from app.security import hash_password


# Documentação: Implementa read_password como parte do fluxo descrito para este arquivo.
def read_password() -> str:
    first = getpass.getpass("Senha (mínimo 12 caracteres): ")
    second = getpass.getpass("Confirmar senha: ")
    if first != second:
        raise ValueError("As senhas não coincidem")
    return first


# Documentação: Coordena a entrada de linha de comando deste arquivo: Administra usuários pela
# linha de comando do ambiente operacional. Solicita senha sem eco, valida identidade/fuso e
# audita criação ou redefinição.
def main() -> None:
    parser = argparse.ArgumentParser(description="Administração DEVLIMA AGENT")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create-user")
    create.add_argument("username")
    create.add_argument("--timezone", default=get_settings().default_timezone)
    reset = commands.add_parser("reset-password")
    reset.add_argument("username")
    commands.add_parser("list-users")
    args = parser.parse_args()
    try:
        with Session(get_engine()) as session:
            if args.command == "list-users":
                for user in session.scalars(select(User).order_by(User.username)):
                    print(f"{user.id} {user.username} {user.timezone} active={user.is_active}")
                return
            username = args.username.lower()
            if not re.fullmatch(r"[a-z0-9_.-]{1,80}", username):
                raise ValueError("Nome de usuário inválido")
            user = session.scalar(select(User).where(User.username == username))
            if args.command == "create-user":
                if user:
                    raise ValueError("Usuário já existe")
                ZoneInfo(args.timezone)
                user = User(
                    username=username,
                    timezone=args.timezone,
                    password_hash=hash_password(read_password()),
                )
                session.add(user)
                session.flush()
                event = "admin.user_created"
            else:
                if user is None:
                    raise ValueError("Usuário não existe")
                user.password_hash = hash_password(read_password())
                user.token_version += 1
                event = "admin.password_reset"
            session.add(AuditLog(user_id=user.id, event=event, details={"source": "cli"}))
            session.commit()
            print(f"Operação concluída: {event}, usuário {username}")
    except ValueError as error:
        parser.exit(1, f"Erro: {error}\n")


if __name__ == "__main__":
    main()
