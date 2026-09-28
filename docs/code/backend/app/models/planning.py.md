# backend/app/models/planning.py

Mapeia tarefas, agendamentos/ocorrências, outbox e heartbeat do scheduler; a ocorrência e dedupe_key evitam disparos duplicados.

[Arquivo fonte](../../../../../backend/app/models/planning.py) · 78 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [Task](#L11) | Define o tipo Task e reúne o estado/contrato descrito para este módulo. |
| [Schedule](#L24) | Define o tipo Schedule e reúne o estado/contrato descrito para este módulo. |
| [ScheduledEvent](#L41) | Define o tipo ScheduledEvent e reúne o estado/contrato descrito para este módulo. |
| [OutboxEvent](#L58) | Define o tipo OutboxEvent e reúne o estado/contrato descrito para este módulo. |
| [SchedulerHeartbeat](#L74) | Define o tipo SchedulerHeartbeat e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID, uuid4</code> | Importa UUID, uuid4 de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func</code> | Importa JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Mapped, mapped_column</code> | Importa Mapped, mapped_column de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.db.base import Base</code> | Importa Base de app.db.base. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code># Documentação: Define o tipo Task e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Task e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>class Task(Base):</code> | Define o tipo Task e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>    __tablename__ = &quot;tasks&quot;</code> | Define __tablename__ com &#x27;tasks&#x27;. |
| <a id="L13"></a>13 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L14"></a>14 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L15"></a>15 | <code>    title: Mapped[str] = mapped_column(String(300))</code> | Define title com mapped_column(String(300)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(300) |
| <a id="L16"></a>16 | <code>    description: Mapped[str &#124; None] = mapped_column(Text)</code> | Define description com mapped_column(Text). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Text |
| <a id="L17"></a>17 | <code>    due_at: Mapped[datetime &#124; None] = mapped_column(DateTime(timezone=True), index=True)</code> | Define due_at com mapped_column(DateTime(timezone=True), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), index=True |
| <a id="L18"></a>18 | <code>    status: Mapped[str] = mapped_column(String(16), default=&quot;OPEN&quot;)</code> | Define status com mapped_column(String(16), default=&#x27;OPEN&#x27;). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), default=&#x27;OPEN&#x27; |
| <a id="L19"></a>19 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L20"></a>20 | <code>    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define updated_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code># Documentação: Define o tipo Schedule e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Schedule e reúne o estado/contrato descrito para este módulo. |
| <a id="L24"></a>24 | <code>class Schedule(Base):</code> | Define o tipo Schedule e reúne o estado/contrato descrito para este módulo. |
| <a id="L25"></a>25 | <code>    __tablename__ = &quot;schedules&quot;</code> | Define __tablename__ com &#x27;schedules&#x27;. |
| <a id="L26"></a>26 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L27"></a>27 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L28"></a>28 | <code>    kind: Mapped[str] = mapped_column(String(16), index=True)</code> | Define kind com mapped_column(String(16), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), index=True |
| <a id="L29"></a>29 | <code>    text: Mapped[str] = mapped_column(String(1000))</code> | Define text com mapped_column(String(1000)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(1000) |
| <a id="L30"></a>30 | <code>    timezone: Mapped[str] = mapped_column(String(80))</code> | Define timezone com mapped_column(String(80)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(80) |
| <a id="L31"></a>31 | <code>    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))</code> | Define start_at com mapped_column(DateTime(timezone=True)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L32"></a>32 | <code>    next_run_at: Mapped[datetime &#124; None] = mapped_column(DateTime(timezone=True), index=True)</code> | Define next_run_at com mapped_column(DateTime(timezone=True), index=True). Próximo disparo UTC calculado conforme timezone/regra do agendamento. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), index=True |
| <a id="L33"></a>33 | <code>    rrule: Mapped[str &#124; None] = mapped_column(String(500))</code> | Define rrule com mapped_column(String(500)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(500) |
| <a id="L34"></a>34 | <code>    status: Mapped[str] = mapped_column(String(16), default=&quot;SCHEDULED&quot;, index=True)</code> | Define status com mapped_column(String(16), default=&#x27;SCHEDULED&#x27;, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), default=&#x27;SCHEDULED&#x27;, index=True |
| <a id="L35"></a>35 | <code>    version: Mapped[int] = mapped_column(Integer, default=1)</code> | Define version com mapped_column(Integer, default=1). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer, default=1 |
| <a id="L36"></a>36 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L37"></a>37 | <code>    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define updated_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L38"></a>38 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L39"></a>39 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L40"></a>40 | <code># Documentação: Define o tipo ScheduledEvent e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ScheduledEvent e reúne o estado/contrato descrito para este módulo. |
| <a id="L41"></a>41 | <code>class ScheduledEvent(Base):</code> | Define o tipo ScheduledEvent e reúne o estado/contrato descrito para este módulo. |
| <a id="L42"></a>42 | <code>    __tablename__ = &quot;scheduled_events&quot;</code> | Define __tablename__ com &#x27;scheduled_events&#x27;. |
| <a id="L43"></a>43 | <code>    __table_args__ = (</code> | Define __table_args__ com (UniqueConstraint(&#x27;schedule_id&#x27;, &#x27;version&#x27;, &#x27;scheduled_at&#x27;, name=&#x27;uq_schedule_occurrence&#x27;),). |
| <a id="L44"></a>44 | <code>        UniqueConstraint(&quot;schedule_id&quot;, &quot;version&quot;, &quot;scheduled_at&quot;, name=&quot;uq_schedule_occurrence&quot;),</code> | Continua/fecha a instrução da linha 43. Define __table_args__ com (UniqueConstraint(&#x27;schedule_id&#x27;, &#x27;version&#x27;, &#x27;scheduled_at&#x27;, name=&#x27;uq_schedule_occurrence&#x27;),). |
| <a id="L45"></a>45 | <code>    )</code> | Continua/fecha a instrução da linha 43. Define __table_args__ com (UniqueConstraint(&#x27;schedule_id&#x27;, &#x27;version&#x27;, &#x27;scheduled_at&#x27;, name=&#x27;uq_schedule_occurrence&#x27;),). |
| <a id="L46"></a>46 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L47"></a>47 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L48"></a>48 | <code>    schedule_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;schedules.id&quot;), index=True)</code> | Define schedule_id com mapped_column(ForeignKey(&#x27;schedules.id&#x27;), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;schedules.id&#x27;), index=True |
| <a id="L49"></a>49 | <code>    version: Mapped[int] = mapped_column(Integer)</code> | Define version com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L50"></a>50 | <code>    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))</code> | Define scheduled_at com mapped_column(DateTime(timezone=True)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L51"></a>51 | <code>    executed_at: Mapped[datetime] = mapped_column(</code> | Define executed_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L52"></a>52 | <code>        DateTime(timezone=True), server_default=func.now()</code> | Continua/fecha a instrução da linha 51. Define executed_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L53"></a>53 | <code>    )</code> | Continua/fecha a instrução da linha 51. Define executed_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L54"></a>54 | <code>    status: Mapped[str] = mapped_column(String(16))</code> | Define status com mapped_column(String(16)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16) |
| <a id="L55"></a>55 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L56"></a>56 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L57"></a>57 | <code># Documentação: Define o tipo OutboxEvent e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo OutboxEvent e reúne o estado/contrato descrito para este módulo. |
| <a id="L58"></a>58 | <code>class OutboxEvent(Base):</code> | Define o tipo OutboxEvent e reúne o estado/contrato descrito para este módulo. |
| <a id="L59"></a>59 | <code>    __tablename__ = &quot;outbox_events&quot;</code> | Define __tablename__ com &#x27;outbox_events&#x27;. |
| <a id="L60"></a>60 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L61"></a>61 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L62"></a>62 | <code>    schedule_id: Mapped[UUID &#124; None] = mapped_column(ForeignKey(&quot;schedules.id&quot;), index=True)</code> | Define schedule_id com mapped_column(ForeignKey(&#x27;schedules.id&#x27;), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;schedules.id&#x27;), index=True |
| <a id="L63"></a>63 | <code>    type: Mapped[str] = mapped_column(String(64))</code> | Define type com mapped_column(String(64)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64) |
| <a id="L64"></a>64 | <code>    payload: Mapped[dict] = mapped_column(JSON)</code> | Define payload com mapped_column(JSON). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: JSON |
| <a id="L65"></a>65 | <code>    dedupe_key: Mapped[str] = mapped_column(String(160), unique=True)</code> | Define dedupe_key com mapped_column(String(160), unique=True). Chave que impede publicar a mesma ocorrência lógica novamente. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(160), unique=True |
| <a id="L66"></a>66 | <code>    status: Mapped[str] = mapped_column(String(16), default=&quot;PENDING&quot;, index=True)</code> | Define status com mapped_column(String(16), default=&#x27;PENDING&#x27;, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), default=&#x27;PENDING&#x27;, index=True |
| <a id="L67"></a>67 | <code>    created_at: Mapped[datetime] = mapped_column(</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), index=True |
| <a id="L68"></a>68 | <code>        DateTime(timezone=True), server_default=func.now(), index=True</code> | Continua/fecha a instrução da linha 67. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), index=True |
| <a id="L69"></a>69 | <code>    )</code> | Continua/fecha a instrução da linha 67. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), index=True |
| <a id="L70"></a>70 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L71"></a>71 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L72"></a>72 | <code># Documentação: Define o tipo SchedulerHeartbeat e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo SchedulerHeartbeat e reúne o estado/contrato descrito para este |
| <a id="L73"></a>73 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L74"></a>74 | <code>class SchedulerHeartbeat(Base):</code> | Define o tipo SchedulerHeartbeat e reúne o estado/contrato descrito para este módulo. |
| <a id="L75"></a>75 | <code>    __tablename__ = &quot;scheduler_heartbeats&quot;</code> | Define __tablename__ com &#x27;scheduler_heartbeats&#x27;. |
| <a id="L76"></a>76 | <code>    name: Mapped[str] = mapped_column(String(40), primary_key=True)</code> | Define name com mapped_column(String(40), primary_key=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(40), primary_key=True |
| <a id="L77"></a>77 | <code>    last_tick_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))</code> | Define last_tick_at com mapped_column(DateTime(timezone=True)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L78"></a>78 | <code>    processed: Mapped[int] = mapped_column(Integer)</code> | Define processed com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
