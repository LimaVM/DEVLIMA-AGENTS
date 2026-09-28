# backend/app/models/calls.py

Mapeia call_sessions: conversa, proprietário, dispositivo, motivo, status e timestamps usados para controlar atendimento, encerramento e expiração.

[Arquivo fonte](../../../../../backend/app/models/calls.py) · 24 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [CallSession](#L11) | Define o tipo CallSession e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID, uuid4</code> | Importa UUID, uuid4 de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from sqlalchemy import DateTime, ForeignKey, String, func</code> | Importa DateTime, ForeignKey, String, func de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Mapped, mapped_column</code> | Importa Mapped, mapped_column de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.db.base import Base</code> | Importa Base de app.db.base. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code># Documentação: Define o tipo CallSession e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo CallSession e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>class CallSession(Base):</code> | Define o tipo CallSession e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>    __tablename__ = &quot;call_sessions&quot;</code> | Define __tablename__ com &#x27;call_sessions&#x27;. |
| <a id="L13"></a>13 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L14"></a>14 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L15"></a>15 | <code>    device_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;devices.id&quot;), index=True)</code> | Define device_id com mapped_column(ForeignKey(&#x27;devices.id&#x27;), index=True). Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;devices.id&#x27;), index=True |
| <a id="L16"></a>16 | <code>    incoming_event_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;outbox_events.id&quot;), unique=True)</code> | Define incoming_event_id com mapped_column(ForeignKey(&#x27;outbox_events.id&#x27;), unique=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;outbox_events.id&#x27;), unique=True |
| <a id="L17"></a>17 | <code>    conversation_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;conversations.id&quot;), index=True)</code> | Define conversation_id com mapped_column(ForeignKey(&#x27;conversations.id&#x27;), index=True). Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;conversations.id&#x27;), index=True |
| <a id="L18"></a>18 | <code>    reason: Mapped[str] = mapped_column(String(1000))</code> | Define reason com mapped_column(String(1000)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(1000) |
| <a id="L19"></a>19 | <code>    status: Mapped[str] = mapped_column(String(16), default=&quot;ACTIVE&quot;, index=True)</code> | Define status com mapped_column(String(16), default=&#x27;ACTIVE&#x27;, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), default=&#x27;ACTIVE&#x27;, index=True |
| <a id="L20"></a>20 | <code>    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define started_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L21"></a>21 | <code>    last_active_at: Mapped[datetime] = mapped_column(</code> | Define last_active_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L22"></a>22 | <code>        DateTime(timezone=True), server_default=func.now()</code> | Continua/fecha a instrução da linha 21. Define last_active_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L23"></a>23 | <code>    )</code> | Continua/fecha a instrução da linha 21. Define last_active_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L24"></a>24 | <code>    ended_at: Mapped[datetime &#124; None] = mapped_column(DateTime(timezone=True))</code> | Define ended_at com mapped_column(DateTime(timezone=True)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
