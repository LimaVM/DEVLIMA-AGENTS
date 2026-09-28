# backend/app/agent/errors.py

Transporta códigos de erro de domínio e status HTTP sem expor conteúdo sensível em mensagens de exceção.

[Arquivo fonte](../../../../../backend/app/agent/errors.py) · 15 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [AgentError](#L2) | Define o tipo AgentError e reúne o estado/contrato descrito para este módulo. |
| [AgentError.__init__](#L4) | Inicializa AgentError com as dependências e estado declarados. |
| [InvalidAgentResponse](#L12) | Define o tipo InvalidAgentResponse e reúne o estado/contrato descrito para este módulo. |
| [InvalidAgentResponse.__init__](#L14) | Inicializa InvalidAgentResponse com as dependências e estado declarados. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code># Documentação: Define o tipo AgentError e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo AgentError e reúne o estado/contrato descrito para este módulo. |
| <a id="L2"></a>2 | <code>class AgentError(Exception):</code> | Define o tipo AgentError e reúne o estado/contrato descrito para este módulo. |
| <a id="L3"></a>3 | <code>    # Documentação: Inicializa AgentError com as dependências e estado declarados.</code> | Comentário: Documentação: Inicializa AgentError com as dependências e estado declarados. |
| <a id="L4"></a>4 | <code>    def __init__(self, code: str, status_code: int = 409):</code> | Inicializa AgentError com as dependências e estado declarados. |
| <a id="L5"></a>5 | <code>        super().__init__(code)</code> | Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: code |
| <a id="L6"></a>6 | <code>        self.code = code</code> | Define self.code com code. |
| <a id="L7"></a>7 | <code>        self.status_code = status_code</code> | Define self.status_code com status_code. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code># Documentação: Define o tipo InvalidAgentResponse e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo InvalidAgentResponse e reúne o estado/contrato descrito para este |
| <a id="L11"></a>11 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L12"></a>12 | <code>class InvalidAgentResponse(AgentError):</code> | Define o tipo InvalidAgentResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L13"></a>13 | <code>    # Documentação: Inicializa InvalidAgentResponse com as dependências e estado declarados.</code> | Comentário: Documentação: Inicializa InvalidAgentResponse com as dependências e estado declarados. |
| <a id="L14"></a>14 | <code>    def __init__(self):</code> | Inicializa InvalidAgentResponse com as dependências e estado declarados. |
| <a id="L15"></a>15 | <code>        super().__init__(&quot;invalid_agent_response&quot;, 502)</code> | Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;invalid_agent_response&#x27;, 502 |
