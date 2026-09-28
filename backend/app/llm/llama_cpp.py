from app.llm.openai_compatible import OpenAICompatibleProvider


class LlamaCppProvider(OpenAICompatibleProvider):
    name = "llama_cpp"

    def structured_options(self) -> dict:
        # Keep JSON turns/summaries within the output budget on thinking models.
        return {"reasoning_effort": "none", "chat_template_kwargs": {"enable_thinking": False}}
