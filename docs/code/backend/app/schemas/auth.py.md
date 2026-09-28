# backend/app/schemas/auth.py

Define contratos HTTP de login, token e identidade, incluindo limites de campos e separação de resposta pública e hash de senha.

[Arquivo fonte](../../../../../backend/app/schemas/auth.py) · 29 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [LoginRequest](#L8) | Define o tipo LoginRequest e reúne o estado/contrato descrito para este módulo. |
| [TokenResponse](#L16) | Define o tipo TokenResponse e reúne o estado/contrato descrito para este módulo. |
| [UserResponse](#L24) | Define o tipo UserResponse e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from pydantic import BaseModel, ConfigDict, Field, SecretStr</code> | Importa BaseModel, ConfigDict, Field, SecretStr de pydantic. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code># Documentação: Define o tipo LoginRequest e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LoginRequest e reúne o estado/contrato descrito para este módulo. |
| <a id="L8"></a>8 | <code>class LoginRequest(BaseModel):</code> | Define o tipo LoginRequest e reúne o estado/contrato descrito para este módulo. |
| <a id="L9"></a>9 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;, hide_input_in_errors=True)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;, hide_input_in_errors=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27;, hide_input_in_errors=True |
| <a id="L10"></a>10 | <code>    username: str = Field(min_length=1, max_length=80, pattern=r&quot;^[a-zA-Z0-9_.-]+$&quot;)</code> | Define username com Field(min_length=1, max_length=80, pattern=&#x27;^[a-zA-Z0-9_.-]+$&#x27;). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=80, pattern=&#x27;^[a-zA-Z0-9_.-]+$&#x27; |
| <a id="L11"></a>11 | <code>    password: SecretStr = Field(min_length=1, max_length=1024)</code> | Define password com Field(min_length=1, max_length=1024). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=1024 |
| <a id="L12"></a>12 | <code>    device_id: UUID &#124; None = None</code> | Define device_id com None. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code># Documentação: Define o tipo TokenResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo TokenResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L16"></a>16 | <code>class TokenResponse(BaseModel):</code> | Define o tipo TokenResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L17"></a>17 | <code>    access_token: str</code> | Define access_token com None. |
| <a id="L18"></a>18 | <code>    token_type: str = &quot;bearer&quot;</code> | Define token_type com &#x27;bearer&#x27;. |
| <a id="L19"></a>19 | <code>    expires_in: int</code> | Define expires_in com None. |
| <a id="L20"></a>20 | <code>    refresh_token: str &#124; None = None</code> | Define refresh_token com None. |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code># Documentação: Define o tipo UserResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo UserResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L24"></a>24 | <code>class UserResponse(BaseModel):</code> | Define o tipo UserResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L25"></a>25 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L26"></a>26 | <code>    id: UUID</code> | Define id com None. |
| <a id="L27"></a>27 | <code>    username: str</code> | Define username com None. |
| <a id="L28"></a>28 | <code>    timezone: str</code> | Define timezone com None. |
| <a id="L29"></a>29 | <code>    created_at: datetime</code> | Define created_at com None. |
