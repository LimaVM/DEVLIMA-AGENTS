# backend/app/llm/groq.py

Especializa o provider compatível com chat completions para Groq; API key e modelo vêm da configuração externa.

[Arquivo fonte](../../../../../backend/app/llm/groq.py) · 16 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [GroqProvider](#L5) | Define o tipo GroqProvider e reúne o estado/contrato descrito para este módulo. |
| [GroqProvider.__init__](#L9) | Inicializa GroqProvider com as dependências e estado declarados. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from app.llm.openai_compatible import OpenAICompatibleProvider</code> | Importa OpenAICompatibleProvider de app.llm.openai_compatible. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code># Documentação: Define o tipo GroqProvider e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo GroqProvider e reúne o estado/contrato descrito para este módulo. |
| <a id="L5"></a>5 | <code>class GroqProvider(OpenAICompatibleProvider):</code> | Define o tipo GroqProvider e reúne o estado/contrato descrito para este módulo. |
| <a id="L6"></a>6 | <code>    name = &quot;groq&quot;</code> | Define name com &#x27;groq&#x27;. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>    # Documentação: Inicializa GroqProvider com as dependências e estado declarados.</code> | Comentário: Documentação: Inicializa GroqProvider com as dependências e estado declarados. |
| <a id="L9"></a>9 | <code>    def __init__(self, model: str, *, api_key: str, **kwargs):</code> | Inicializa GroqProvider com as dependências e estado declarados. |
| <a id="L10"></a>10 | <code>        super().__init__(</code> | Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
| <a id="L11"></a>11 | <code>            &quot;https://api.groq.com/openai/v1&quot;,</code> | Continua/fecha a instrução da linha 10. Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
| <a id="L12"></a>12 | <code>            model,</code> | Continua/fecha a instrução da linha 10. Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
| <a id="L13"></a>13 | <code>            api_key=api_key,</code> | Continua/fecha a instrução da linha 10. Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
| <a id="L14"></a>14 | <code>            requires_key=True,</code> | Continua/fecha a instrução da linha 10. Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
| <a id="L15"></a>15 | <code>            **kwargs,</code> | Continua/fecha a instrução da linha 10. Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
| <a id="L16"></a>16 | <code>        )</code> | Continua/fecha a instrução da linha 10. Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: &#x27;https://api.groq.com/openai/v1&#x27;, model, api_key=api_key, requires_key=True, **=kwargs |
