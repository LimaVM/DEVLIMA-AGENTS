# backend/app/models/llm_request.py

Mapeia metadados de tentativas de inferência: provider, duração, resultado e vínculo ao usuário/requisição.

[Arquivo fonte](../../../../../backend/app/models/llm_request.py) · 29 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [LLMRequest](#L11) | Define o tipo LLMRequest e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID, uuid4</code> | Importa UUID, uuid4 de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func</code> | Importa Boolean, DateTime, ForeignKey, Integer, String, func de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Mapped, mapped_column</code> | Importa Mapped, mapped_column de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.db.base import Base</code> | Importa Base de app.db.base. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code># Documentação: Define o tipo LLMRequest e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LLMRequest e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>class LLMRequest(Base):</code> | Define o tipo LLMRequest e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>    __tablename__ = &quot;llm_requests&quot;</code> | Define __tablename__ com &#x27;llm_requests&#x27;. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L15"></a>15 | <code>    request_id: Mapped[UUID] = mapped_column(nullable=False, index=True)</code> | Define request_id com mapped_column(nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: nullable=False, index=True |
| <a id="L16"></a>16 | <code>    user_id: Mapped[UUID &#124; None] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L17"></a>17 | <code>    provider: Mapped[str] = mapped_column(String(32), nullable=False)</code> | Define provider com mapped_column(String(32), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(32), nullable=False |
| <a id="L18"></a>18 | <code>    model: Mapped[str] = mapped_column(String(512), nullable=False)</code> | Define model com mapped_column(String(512), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(512), nullable=False |
| <a id="L19"></a>19 | <code>    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)</code> | Define latency_ms com mapped_column(Integer, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer, nullable=False |
| <a id="L20"></a>20 | <code>    success: Mapped[bool] = mapped_column(Boolean, nullable=False)</code> | Define success com mapped_column(Boolean, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Boolean, nullable=False |
| <a id="L21"></a>21 | <code>    fallback: Mapped[bool] = mapped_column(Boolean, nullable=False)</code> | Define fallback com mapped_column(Boolean, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Boolean, nullable=False |
| <a id="L22"></a>22 | <code>    error_code: Mapped[str &#124; None] = mapped_column(String(64))</code> | Define error_code com mapped_column(String(64)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64) |
| <a id="L23"></a>23 | <code>    status_code: Mapped[int &#124; None] = mapped_column(Integer)</code> | Define status_code com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L24"></a>24 | <code>    upstream_request_id: Mapped[str &#124; None] = mapped_column(String(255))</code> | Define upstream_request_id com mapped_column(String(255)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(255) |
| <a id="L25"></a>25 | <code>    prompt_tokens: Mapped[int &#124; None] = mapped_column(Integer)</code> | Define prompt_tokens com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L26"></a>26 | <code>    completion_tokens: Mapped[int &#124; None] = mapped_column(Integer)</code> | Define completion_tokens com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L27"></a>27 | <code>    created_at: Mapped[datetime] = mapped_column(</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False, index=True |
| <a id="L28"></a>28 | <code>        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True</code> | Continua/fecha a instrução da linha 27. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False, index=True |
| <a id="L29"></a>29 | <code>    )</code> | Continua/fecha a instrução da linha 27. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False, index=True |
