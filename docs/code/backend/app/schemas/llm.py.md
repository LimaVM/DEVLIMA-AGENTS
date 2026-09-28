# backend/app/schemas/llm.py

Define o pedido e a resposta de inferência e limita a quantidade/tamanho do contexto aceito pela rota de LLM.

[Arquivo fonte](../../../../../backend/app/schemas/llm.py) · 32 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [LLMChatRequest](#L9) | Define o tipo LLMChatRequest e reúne o estado/contrato descrito para este módulo. |
| [LLMChatRequest.bound_context](#L17) | Implementa LLMChatRequest.bound_context como parte do fluxo descrito para este arquivo. |
| [LLMChatResponse](#L26) | Define o tipo LLMChatResponse e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>from pydantic import BaseModel, ConfigDict, Field, model_validator</code> | Importa BaseModel, ConfigDict, Field, model_validator de pydantic. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L5"></a>5 | <code>from app.llm.base import LLMMessage, ProviderName</code> | Importa LLMMessage, ProviderName de app.llm.base. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code># Documentação: Define o tipo LLMChatRequest e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMChatRequest e reúne o estado/contrato descrito para este módulo. |
| <a id="L9"></a>9 | <code>class LLMChatRequest(BaseModel):</code> | Define o tipo LLMChatRequest e reúne o estado/contrato descrito para este módulo. |
| <a id="L10"></a>10 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L11"></a>11 | <code>    messages: list[LLMMessage] = Field(min_length=1, max_length=32)</code> | Define messages com Field(min_length=1, max_length=32). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=32 |
| <a id="L12"></a>12 | <code>    max_tokens: int = Field(default=512, ge=1, le=2048)</code> | Define max_tokens com Field(default=512, ge=1, le=2048). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=512, ge=1, le=2048 |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>    @model_validator(mode=&quot;after&quot;)</code> | Aplica o decorator model_validator(mode=&quot;after&quot;) à definição que segue. |
| <a id="L15"></a>15 | <code>    # Documentação: Implementa LLMChatRequest.bound_context como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa LLMChatRequest.bound_context como parte do fluxo descrito para este |
| <a id="L16"></a>16 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L17"></a>17 | <code>    def bound_context(self):</code> | Implementa LLMChatRequest.bound_context como parte do fluxo descrito para este arquivo. |
| <a id="L18"></a>18 | <code>        if sum(len(message.content) for message in self.messages) &gt; 16000:</code> | Executa este ramo somente se sum((len(message.content) for message in self.messages)) &gt; 16000; caso contrário, segue o ramo alternativo. |
| <a id="L19"></a>19 | <code>            raise ValueError(&quot;Contexto excede o limite de 16000 caracteres&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Contexto excede o limite de 16000 caracteres&#x27;). |
| <a id="L20"></a>20 | <code>        if not any(message.role == &quot;user&quot; for message in self.messages):</code> | Executa este ramo somente se not any((message.role == &#x27;user&#x27; for message in self.messages)); caso contrário, segue o ramo alternativo. |
| <a id="L21"></a>21 | <code>            raise ValueError(&quot;É necessária ao menos uma mensagem do usuário&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;É necessária ao menos uma mensagem do usuário&#x27;). |
| <a id="L22"></a>22 | <code>        return self</code> | Retorna self ao chamador e encerra este caminho da função. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code># Documentação: Define o tipo LLMChatResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMChatResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L26"></a>26 | <code>class LLMChatResponse(BaseModel):</code> | Define o tipo LLMChatResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>    request_id: UUID</code> | Define request_id com None. |
| <a id="L28"></a>28 | <code>    reply: str</code> | Define reply com None. |
| <a id="L29"></a>29 | <code>    provider: ProviderName</code> | Define provider com None. |
| <a id="L30"></a>30 | <code>    model: str</code> | Define model com None. |
| <a id="L31"></a>31 | <code>    fallback_used: bool</code> | Define fallback_used com None. |
| <a id="L32"></a>32 | <code>    latency_ms: int</code> | Define latency_ms com None. |
