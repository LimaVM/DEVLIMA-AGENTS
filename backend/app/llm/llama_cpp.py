from app.llm.openai_compatible import OpenAICompatibleProvider


# Documentação: Define o tipo LlamaCppProvider e reúne o estado/contrato descrito para este
# módulo.
class LlamaCppProvider(OpenAICompatibleProvider):
    name = "llama_cpp"

    # Documentação: Implementa LlamaCppProvider.structured_options como parte do fluxo descrito
    # para este arquivo.
    def structured_options(self) -> dict:
        # Keep JSON turns/summaries within the output budget on thinking models.
        return {"reasoning_effort": "none", "chat_template_kwargs": {"enable_thinking": False}}
