from app.llm.openai_compatible import OpenAICompatibleProvider


# Documentação: Define o tipo GroqProvider e reúne o estado/contrato descrito para este módulo.
class GroqProvider(OpenAICompatibleProvider):
    name = "groq"

    # Documentação: Inicializa GroqProvider com as dependências e estado declarados.
    def __init__(self, model: str, *, api_key: str, **kwargs):
        super().__init__(
            "https://api.groq.com/openai/v1",
            model,
            api_key=api_key,
            requires_key=True,
            **kwargs,
        )
