# backend/app/llm/base.py

Define os tipos e a interface de provider, incluindo erros e a indicação de quais falhas técnicas permitem fallback.

[Arquivo fonte](../../../../../backend/app/llm/base.py) · 74 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [LLMMessage](#L10) | Define o tipo LLMMessage e reúne o estado/contrato descrito para este módulo. |
| [LLMCompletion](#L17) | Define o tipo LLMCompletion e reúne o estado/contrato descrito para este módulo. |
| [ProviderHealth](#L27) | Define o tipo ProviderHealth e reúne o estado/contrato descrito para este módulo. |
| [LLMError](#L37) | Define o tipo LLMError e reúne o estado/contrato descrito para este módulo. |
| [LLMError.__init__](#L41) | Inicializa LLMError com as dependências e estado declarados. |
| [LLMError.allows_fallback](#L49) | Implementa LLMError.allows_fallback como parte do fluxo descrito para este arquivo. |
| [LLMProvider](#L54) | Define o tipo LLMProvider e reúne o estado/contrato descrito para este módulo. |
| [LLMProvider.chat](#L60) | Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo. |
| [LLMProvider.health_check](#L68) | Implementa LLMProvider.health_check como parte do fluxo descrito para este arquivo. |
| [LLMProvider.close](#L73) | Libera LLMProvider.close, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from abc import ABC, abstractmethod</code> | Importa ABC, abstractmethod de abc. |
| <a id="L2"></a>2 | <code>from typing import Literal</code> | Importa Literal de typing. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from pydantic import BaseModel, ConfigDict, Field</code> | Importa BaseModel, ConfigDict, Field de pydantic. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>ProviderName = Literal[&quot;llama_cpp&quot;, &quot;groq&quot;]</code> | Define ProviderName com Literal[&#x27;llama_cpp&#x27;, &#x27;groq&#x27;]. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code># Documentação: Define o tipo LLMMessage e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMMessage e reúne o estado/contrato descrito para este módulo. |
| <a id="L10"></a>10 | <code>class LLMMessage(BaseModel):</code> | Define o tipo LLMMessage e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L12"></a>12 | <code>    role: Literal[&quot;system&quot;, &quot;user&quot;, &quot;assistant&quot;]</code> | Define role com None. |
| <a id="L13"></a>13 | <code>    content: str = Field(min_length=1, max_length=8000)</code> | Define content com Field(min_length=1, max_length=8000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=8000 |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L16"></a>16 | <code># Documentação: Define o tipo LLMCompletion e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMCompletion e reúne o estado/contrato descrito para este módulo. |
| <a id="L17"></a>17 | <code>class LLMCompletion(BaseModel):</code> | Define o tipo LLMCompletion e reúne o estado/contrato descrito para este módulo. |
| <a id="L18"></a>18 | <code>    content: str = Field(min_length=1, max_length=131072)</code> | Define content com Field(min_length=1, max_length=131072). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=131072 |
| <a id="L19"></a>19 | <code>    provider: ProviderName</code> | Define provider com None. |
| <a id="L20"></a>20 | <code>    model: str</code> | Define model com None. |
| <a id="L21"></a>21 | <code>    upstream_request_id: str &#124; None = None</code> | Define upstream_request_id com None. |
| <a id="L22"></a>22 | <code>    prompt_tokens: int &#124; None = Field(default=None, ge=0)</code> | Define prompt_tokens com Field(default=None, ge=0). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, ge=0 |
| <a id="L23"></a>23 | <code>    completion_tokens: int &#124; None = Field(default=None, ge=0)</code> | Define completion_tokens com Field(default=None, ge=0). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, ge=0 |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L26"></a>26 | <code># Documentação: Define o tipo ProviderHealth e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ProviderHealth e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>class ProviderHealth(BaseModel):</code> | Define o tipo ProviderHealth e reúne o estado/contrato descrito para este módulo. |
| <a id="L28"></a>28 | <code>    provider: ProviderName</code> | Define provider com None. |
| <a id="L29"></a>29 | <code>    configured: bool</code> | Define configured com None. |
| <a id="L30"></a>30 | <code>    healthy: bool</code> | Define healthy com None. |
| <a id="L31"></a>31 | <code>    model: str</code> | Define model com None. |
| <a id="L32"></a>32 | <code>    latency_ms: int</code> | Define latency_ms com None. |
| <a id="L33"></a>33 | <code>    error_code: str &#124; None = None</code> | Define error_code com None. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L35"></a>35 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L36"></a>36 | <code># Documentação: Define o tipo LLMError e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMError e reúne o estado/contrato descrito para este módulo. |
| <a id="L37"></a>37 | <code>class LLMError(Exception):</code> | Define o tipo LLMError e reúne o estado/contrato descrito para este módulo. |
| <a id="L38"></a>38 | <code>    &quot;&quot;&quot;Only stable error codes escape providers; upstream bodies/keys never do.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L39"></a>39 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L40"></a>40 | <code>    # Documentação: Inicializa LLMError com as dependências e estado declarados.</code> | Comentário: Documentação: Inicializa LLMError com as dependências e estado declarados. |
| <a id="L41"></a>41 | <code>    def __init__(self, code: str, *, status_code: int &#124; None = None):</code> | Inicializa LLMError com as dependências e estado declarados. |
| <a id="L42"></a>42 | <code>        super().__init__(code)</code> | Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: code |
| <a id="L43"></a>43 | <code>        self.code = code</code> | Define self.code com code. |
| <a id="L44"></a>44 | <code>        self.status_code = status_code</code> | Define self.status_code com status_code. |
| <a id="L45"></a>45 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L46"></a>46 | <code>    @property</code> | Aplica o decorator property à definição que segue. |
| <a id="L47"></a>47 | <code>    # Documentação: Implementa LLMError.allows_fallback como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa LLMError.allows_fallback como parte do fluxo descrito para este |
| <a id="L48"></a>48 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L49"></a>49 | <code>    def allows_fallback(self) -&gt; bool:</code> | Implementa LLMError.allows_fallback como parte do fluxo descrito para este arquivo. |
| <a id="L50"></a>50 | <code>        return self.code in {&quot;timeout&quot;, &quot;connection_error&quot;, &quot;server_error&quot;, &quot;model_unavailable&quot;}</code> | Retorna self.code in {&#x27;timeout&#x27;, &#x27;connection_error&#x27;, &#x27;server_error&#x27;, &#x27;model_unavailable&#x27;} ao chamador e encerra este caminho da função. |
| <a id="L51"></a>51 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L52"></a>52 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L53"></a>53 | <code># Documentação: Define o tipo LLMProvider e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMProvider e reúne o estado/contrato descrito para este módulo. |
| <a id="L54"></a>54 | <code>class LLMProvider(ABC):</code> | Define o tipo LLMProvider e reúne o estado/contrato descrito para este módulo. |
| <a id="L55"></a>55 | <code>    name: ProviderName</code> | Define name com None. |
| <a id="L56"></a>56 | <code>    model: str</code> | Define model com None. |
| <a id="L57"></a>57 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L58"></a>58 | <code>    @abstractmethod</code> | Aplica o decorator abstractmethod à definição que segue. |
| <a id="L59"></a>59 | <code>    # Documentação: Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo. |
| <a id="L60"></a>60 | <code>    def chat(</code> | Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo. |
| <a id="L61"></a>61 | <code>        self, messages: list[LLMMessage], *, max_tokens: int = 512, json_mode: bool = False</code> | Continua/fecha a instrução da linha 60. Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo. |
| <a id="L62"></a>62 | <code>    ) -&gt; LLMCompletion:</code> | Continua/fecha a instrução da linha 60. Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo. |
| <a id="L63"></a>63 | <code>        raise NotImplementedError</code> | Interrompe este caminho lançando NotImplementedError. |
| <a id="L64"></a>64 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L65"></a>65 | <code>    @abstractmethod</code> | Aplica o decorator abstractmethod à definição que segue. |
| <a id="L66"></a>66 | <code>    # Documentação: Implementa LLMProvider.health_check como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa LLMProvider.health_check como parte do fluxo descrito para este |
| <a id="L67"></a>67 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L68"></a>68 | <code>    def health_check(self) -&gt; ProviderHealth:</code> | Implementa LLMProvider.health_check como parte do fluxo descrito para este arquivo. |
| <a id="L69"></a>69 | <code>        raise NotImplementedError</code> | Interrompe este caminho lançando NotImplementedError. |
| <a id="L70"></a>70 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L71"></a>71 | <code>    @abstractmethod</code> | Aplica o decorator abstractmethod à definição que segue. |
| <a id="L72"></a>72 | <code>    # Documentação: Libera LLMProvider.close, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Libera LLMProvider.close, segundo o contrato e as verificações deste módulo. |
| <a id="L73"></a>73 | <code>    def close(self) -&gt; None:</code> | Libera LLMProvider.close, segundo o contrato e as verificações deste módulo. |
| <a id="L74"></a>74 | <code>        raise NotImplementedError</code> | Interrompe este caminho lançando NotImplementedError. |
