# backend/app/schemas/memories.py

Define memória e proposta públicas com validação de conteúdo, categorias e estados de confirmação.

[Arquivo fonte](../../../../../backend/app/schemas/memories.py) · 47 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [MemoryCreate](#L9) | Define o tipo MemoryCreate e reúne o estado/contrato descrito para este módulo. |
| [MemoryCreate.validate_content](#L18) | Valida MemoryCreate.validate_content, segundo o contrato e as verificações deste módulo. |
| [MemoryResponse](#L27) | Define o tipo MemoryResponse e reúne o estado/contrato descrito para este módulo. |
| [CandidateResponse](#L38) | Define o tipo CandidateResponse e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from typing import Literal</code> | Importa Literal de typing. |
| <a id="L3"></a>3 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L5"></a>5 | <code>from pydantic import BaseModel, ConfigDict, Field, field_validator</code> | Importa BaseModel, ConfigDict, Field, field_validator de pydantic. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code># Documentação: Define o tipo MemoryCreate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo MemoryCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L9"></a>9 | <code>class MemoryCreate(BaseModel):</code> | Define o tipo MemoryCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L10"></a>10 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L11"></a>11 | <code>    content: str = Field(min_length=1, max_length=1000)</code> | Define content com Field(min_length=1, max_length=1000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=1000 |
| <a id="L12"></a>12 | <code>    category: Literal[&quot;preference&quot;, &quot;fact&quot;] = &quot;fact&quot;</code> | Define category com &#x27;fact&#x27;. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>    @field_validator(&quot;content&quot;)</code> | Aplica o decorator field_validator(&quot;content&quot;) à definição que segue. |
| <a id="L15"></a>15 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L16"></a>16 | <code>    # Documentação: Valida MemoryCreate.validate_content, segundo o contrato e as verificações</code> | Comentário: Documentação: Valida MemoryCreate.validate_content, segundo o contrato e as verificações |
| <a id="L17"></a>17 | <code>    # deste módulo.</code> | Comentário: deste módulo. |
| <a id="L18"></a>18 | <code>    def validate_content(cls, value):</code> | Valida MemoryCreate.validate_content, segundo o contrato e as verificações deste módulo. |
| <a id="L19"></a>19 | <code>        from app.agent.memory_manager import safe_memory_content</code> | Importa safe_memory_content de app.agent.memory_manager. |
| <a id="L20"></a>20 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L21"></a>21 | <code>        if not safe_memory_content(value):</code> | Executa este ramo somente se not safe_memory_content(value); caso contrário, segue o ramo alternativo. |
| <a id="L22"></a>22 | <code>            raise ValueError(&quot;Conteúdo vazio ou sensível não permitido como memória&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Conteúdo vazio ou sensível não permitido como memória&#x27;). |
| <a id="L23"></a>23 | <code>        return value.strip()</code> | Retorna value.strip() ao chamador e encerra este caminho da função. |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L26"></a>26 | <code># Documentação: Define o tipo MemoryResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo MemoryResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>class MemoryResponse(BaseModel):</code> | Define o tipo MemoryResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L28"></a>28 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L29"></a>29 | <code>    id: UUID</code> | Define id com None. |
| <a id="L30"></a>30 | <code>    content: str</code> | Define content com None. |
| <a id="L31"></a>31 | <code>    category: str</code> | Define category com None. |
| <a id="L32"></a>32 | <code>    is_active: bool</code> | Define is_active com None. |
| <a id="L33"></a>33 | <code>    created_at: datetime</code> | Define created_at com None. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L35"></a>35 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L36"></a>36 | <code># Documentação: Define o tipo CandidateResponse e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo CandidateResponse e reúne o estado/contrato descrito para este |
| <a id="L37"></a>37 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L38"></a>38 | <code>class CandidateResponse(BaseModel):</code> | Define o tipo CandidateResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L39"></a>39 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L40"></a>40 | <code>    id: UUID</code> | Define id com None. |
| <a id="L41"></a>41 | <code>    content: str</code> | Define content com None. |
| <a id="L42"></a>42 | <code>    category: str</code> | Define category com None. |
| <a id="L43"></a>43 | <code>    confidence: float</code> | Define confidence com None. |
| <a id="L44"></a>44 | <code>    status: str</code> | Define status com None. |
| <a id="L45"></a>45 | <code>    rejection_reason: str &#124; None</code> | Define rejection_reason com None. |
| <a id="L46"></a>46 | <code>    accepted_memory_id: UUID &#124; None</code> | Define accepted_memory_id com None. |
| <a id="L47"></a>47 | <code>    created_at: datetime</code> | Define created_at com None. |
