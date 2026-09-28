# Documentação: Define o tipo AgentError e reúne o estado/contrato descrito para este módulo.
class AgentError(Exception):
    # Documentação: Inicializa AgentError com as dependências e estado declarados.
    def __init__(self, code: str, status_code: int = 409):
        super().__init__(code)
        self.code = code
        self.status_code = status_code


# Documentação: Define o tipo InvalidAgentResponse e reúne o estado/contrato descrito para este
# módulo.
class InvalidAgentResponse(AgentError):
    # Documentação: Inicializa InvalidAgentResponse com as dependências e estado declarados.
    def __init__(self):
        super().__init__("invalid_agent_response", 502)
