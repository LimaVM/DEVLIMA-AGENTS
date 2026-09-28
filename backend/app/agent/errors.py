class AgentError(Exception):
    def __init__(self, code: str, status_code: int = 409):
        super().__init__(code)
        self.code = code
        self.status_code = status_code


class InvalidAgentResponse(AgentError):
    def __init__(self):
        super().__init__("invalid_agent_response", 502)
