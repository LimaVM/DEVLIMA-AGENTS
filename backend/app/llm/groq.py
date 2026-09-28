from app.llm.openai_compatible import OpenAICompatibleProvider


class GroqProvider(OpenAICompatibleProvider):
    name = "groq"

    def __init__(self, model: str, *, api_key: str, **kwargs):
        super().__init__(
            "https://api.groq.com/openai/v1",
            model,
            api_key=api_key,
            requires_key=True,
            **kwargs,
        )
