# backend/app/models/devices.py

Mapeia dispositivos, famílias/tokens de refresh e entregas de outbox com tentativas, envio e ACK por dispositivo.

[Arquivo fonte](../../../../../backend/app/models/devices.py) · 53 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [Device](#L11) | Define o tipo Device e reúne o estado/contrato descrito para este módulo. |
| [RefreshFamily](#L25) | Define o tipo RefreshFamily e reúne o estado/contrato descrito para este módulo. |
| [RefreshToken](#L37) | Define o tipo RefreshToken e reúne o estado/contrato descrito para este módulo. |
| [EventDelivery](#L46) | Define o tipo EventDelivery e reúne o estado/contrato descrito para este módulo. |

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
| <a id="L10"></a>10 | <code># Documentação: Define o tipo Device e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Device e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>class Device(Base):</code> | Define o tipo Device e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>    __tablename__ = &quot;devices&quot;</code> | Define __tablename__ com &#x27;devices&#x27;. |
| <a id="L13"></a>13 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True)</code> | Define id com mapped_column(primary_key=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True |
| <a id="L14"></a>14 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L15"></a>15 | <code>    name: Mapped[str] = mapped_column(String(64), default=&quot;Android&quot;)</code> | Define name com mapped_column(String(64), default=&#x27;Android&#x27;). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64), default=&#x27;Android&#x27; |
| <a id="L16"></a>16 | <code>    revoked: Mapped[bool] = mapped_column(Boolean, default=False)</code> | Define revoked com mapped_column(Boolean, default=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Boolean, default=False |
| <a id="L17"></a>17 | <code>    connection_id: Mapped[UUID &#124; None] = mapped_column()</code> | Define connection_id com mapped_column(). Invoca mapped_column com os argumentos declarados nesta instrução. |
| <a id="L18"></a>18 | <code>    last_seen_at: Mapped[datetime] = mapped_column(</code> | Define last_seen_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L19"></a>19 | <code>        DateTime(timezone=True), server_default=func.now()</code> | Continua/fecha a instrução da linha 18. Define last_seen_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L20"></a>20 | <code>    )</code> | Continua/fecha a instrução da linha 18. Define last_seen_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L21"></a>21 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code># Documentação: Define o tipo RefreshFamily e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo RefreshFamily e reúne o estado/contrato descrito para este módulo. |
| <a id="L25"></a>25 | <code>class RefreshFamily(Base):</code> | Define o tipo RefreshFamily e reúne o estado/contrato descrito para este módulo. |
| <a id="L26"></a>26 | <code>    __tablename__ = &quot;refresh_families&quot;</code> | Define __tablename__ com &#x27;refresh_families&#x27;. |
| <a id="L27"></a>27 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L28"></a>28 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L29"></a>29 | <code>    device_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;devices.id&quot;), index=True)</code> | Define device_id com mapped_column(ForeignKey(&#x27;devices.id&#x27;), index=True). Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;devices.id&#x27;), index=True |
| <a id="L30"></a>30 | <code>    token_version: Mapped[int] = mapped_column(Integer)</code> | Define token_version com mapped_column(Integer). Contador de revogação comparado com o JWT para invalidar tokens antigos. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L31"></a>31 | <code>    revoked: Mapped[bool] = mapped_column(Boolean, default=False)</code> | Define revoked com mapped_column(Boolean, default=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Boolean, default=False |
| <a id="L32"></a>32 | <code>    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))</code> | Define expires_at com mapped_column(DateTime(timezone=True)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L33"></a>33 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L35"></a>35 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L36"></a>36 | <code># Documentação: Define o tipo RefreshToken e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo RefreshToken e reúne o estado/contrato descrito para este módulo. |
| <a id="L37"></a>37 | <code>class RefreshToken(Base):</code> | Define o tipo RefreshToken e reúne o estado/contrato descrito para este módulo. |
| <a id="L38"></a>38 | <code>    __tablename__ = &quot;refresh_tokens&quot;</code> | Define __tablename__ com &#x27;refresh_tokens&#x27;. |
| <a id="L39"></a>39 | <code>    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)</code> | Define token_hash com mapped_column(String(64), primary_key=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64), primary_key=True |
| <a id="L40"></a>40 | <code>    family_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;refresh_families.id&quot;), index=True)</code> | Define family_id com mapped_column(ForeignKey(&#x27;refresh_families.id&#x27;), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;refresh_families.id&#x27;), index=True |
| <a id="L41"></a>41 | <code>    used: Mapped[bool] = mapped_column(Boolean, default=False)</code> | Define used com mapped_column(Boolean, default=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Boolean, default=False |
| <a id="L42"></a>42 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L43"></a>43 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code># Documentação: Define o tipo EventDelivery e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo EventDelivery e reúne o estado/contrato descrito para este módulo. |
| <a id="L46"></a>46 | <code>class EventDelivery(Base):</code> | Define o tipo EventDelivery e reúne o estado/contrato descrito para este módulo. |
| <a id="L47"></a>47 | <code>    __tablename__ = &quot;event_deliveries&quot;</code> | Define __tablename__ com &#x27;event_deliveries&#x27;. |
| <a id="L48"></a>48 | <code>    device_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;devices.id&quot;), primary_key=True)</code> | Define device_id com mapped_column(ForeignKey(&#x27;devices.id&#x27;), primary_key=True). Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;devices.id&#x27;), primary_key=True |
| <a id="L49"></a>49 | <code>    event_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;outbox_events.id&quot;), primary_key=True)</code> | Define event_id com mapped_column(ForeignKey(&#x27;outbox_events.id&#x27;), primary_key=True). Identificador estável do evento usado por replay, deduplicação, notificação e ACK. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;outbox_events.id&#x27;), primary_key=True |
| <a id="L50"></a>50 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L51"></a>51 | <code>    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))</code> | Define sent_at com mapped_column(DateTime(timezone=True)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L52"></a>52 | <code>    acknowledged_at: Mapped[datetime &#124; None] = mapped_column(DateTime(timezone=True))</code> | Define acknowledged_at com mapped_column(DateTime(timezone=True)). Momento de confirmação de entrega ao dispositivo; envio isolado não equivale a ACK. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L53"></a>53 | <code>    attempts: Mapped[int] = mapped_column(Integer, default=1)</code> | Define attempts com mapped_column(Integer, default=1). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer, default=1 |
