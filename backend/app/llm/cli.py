import argparse

from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.llm.base import LLMError, LLMMessage
from app.llm.service import build_router


# Documentação: Coordena a entrada de linha de comando deste arquivo: Executa diagnóstico do
# router e dos providers configurados, observando a política de fallback e sem imprimir API keys.
def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnóstico LLM no host autorizado")
    parser.add_argument("command", choices=["health", "smoke"])
    args = parser.parse_args()
    with Session(get_engine()) as session, build_router(get_settings(), session) as llm:
        if args.command == "health":
            print(llm.health_check())
            return
        try:
            result = llm.chat(
                [LLMMessage(role="user", content="Responda apenas: conexão confirmada.")],
                max_tokens=256,
            )
        except LLMError as error:
            parser.exit(1, f"Provider indisponível: {error.code}\n")
        print(
            {
                "provider": result.completion.provider,
                "fallback": result.fallback_used,
                "request_id": str(result.request_id),
                "latency_ms": result.latency_ms,
                "reply": result.completion.content,
            }
        )


if __name__ == "__main__":
    main()
