# backend/app/models/workers.py

Mapeia workers, comandos duráveis e snapshots com vínculo ao proprietário e estados utilizados pelo runner.

[Arquivo fonte](../../../../../backend/app/models/workers.py) · 55 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [Worker](#L11) | Define o tipo Worker e reúne o estado/contrato descrito para este módulo. |
| [WorkerCommand](#L28) | Define o tipo WorkerCommand e reúne o estado/contrato descrito para este módulo. |
| [WorkerSnapshot](#L47) | Define o tipo WorkerSnapshot e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID, uuid4</code> | Importa UUID, uuid4 de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func</code> | Importa JSON, DateTime, ForeignKey, Integer, String, Text, func de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Mapped, mapped_column</code> | Importa Mapped, mapped_column de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.db.base import Base</code> | Importa Base de app.db.base. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code># Documentação: Define o tipo Worker e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Worker e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>class Worker(Base):</code> | Define o tipo Worker e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>    __tablename__ = &quot;workers&quot;</code> | Define __tablename__ com &#x27;workers&#x27;. |
| <a id="L13"></a>13 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L14"></a>14 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L15"></a>15 | <code>    name: Mapped[str] = mapped_column(String(64))</code> | Define name com mapped_column(String(64)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64) |
| <a id="L16"></a>16 | <code>    provider: Mapped[str] = mapped_column(String(16), default=&quot;LINUX&quot;)</code> | Define provider com mapped_column(String(16), default=&#x27;LINUX&#x27;). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), default=&#x27;LINUX&#x27; |
| <a id="L17"></a>17 | <code>    vcpu: Mapped[int] = mapped_column(Integer)</code> | Define vcpu com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L18"></a>18 | <code>    ram_mb: Mapped[int] = mapped_column(Integer)</code> | Define ram_mb com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L19"></a>19 | <code>    disk_gb: Mapped[int] = mapped_column(Integer)</code> | Define disk_gb com mapped_column(Integer). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer |
| <a id="L20"></a>20 | <code>    status: Mapped[str] = mapped_column(String(24), default=&quot;QUEUED&quot;, index=True)</code> | Define status com mapped_column(String(24), default=&#x27;QUEUED&#x27;, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(24), default=&#x27;QUEUED&#x27;, index=True |
| <a id="L21"></a>21 | <code>    ip: Mapped[str &#124; None] = mapped_column(String(45))</code> | Define ip com mapped_column(String(45)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(45) |
| <a id="L22"></a>22 | <code>    error_code: Mapped[str &#124; None] = mapped_column(String(80))</code> | Define error_code com mapped_column(String(80)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(80) |
| <a id="L23"></a>23 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L24"></a>24 | <code>    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define updated_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L26"></a>26 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L27"></a>27 | <code># Documentação: Define o tipo WorkerCommand e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerCommand e reúne o estado/contrato descrito para este módulo. |
| <a id="L28"></a>28 | <code>class WorkerCommand(Base):</code> | Define o tipo WorkerCommand e reúne o estado/contrato descrito para este módulo. |
| <a id="L29"></a>29 | <code>    __tablename__ = &quot;worker_commands&quot;</code> | Define __tablename__ com &#x27;worker_commands&#x27;. |
| <a id="L30"></a>30 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L31"></a>31 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L32"></a>32 | <code>    worker_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;workers.id&quot;), index=True)</code> | Define worker_id com mapped_column(ForeignKey(&#x27;workers.id&#x27;), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;workers.id&#x27;), index=True |
| <a id="L33"></a>33 | <code>    kind: Mapped[str] = mapped_column(String(16))</code> | Define kind com mapped_column(String(16)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16) |
| <a id="L34"></a>34 | <code>    arguments: Mapped[dict] = mapped_column(JSON)</code> | Define arguments com mapped_column(JSON). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: JSON |
| <a id="L35"></a>35 | <code>    status: Mapped[str] = mapped_column(String(24), default=&quot;PENDING&quot;, index=True)</code> | Define status com mapped_column(String(24), default=&#x27;PENDING&#x27;, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(24), default=&#x27;PENDING&#x27;, index=True |
| <a id="L36"></a>36 | <code>    lease_id: Mapped[UUID &#124; None] = mapped_column()</code> | Define lease_id com mapped_column(). Invoca mapped_column com os argumentos declarados nesta instrução. |
| <a id="L37"></a>37 | <code>    lease_until: Mapped[datetime &#124; None] = mapped_column(DateTime(timezone=True))</code> | Define lease_until com mapped_column(DateTime(timezone=True)). Prazo da reivindicação; permite detectar processamento abandonado sem manter lock durante toda a inferência. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True) |
| <a id="L38"></a>38 | <code>    attempts: Mapped[int] = mapped_column(Integer, default=0)</code> | Define attempts com mapped_column(Integer, default=0). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer, default=0 |
| <a id="L39"></a>39 | <code>    result: Mapped[dict] = mapped_column(JSON, default=dict)</code> | Define result com mapped_column(JSON, default=dict). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: JSON, default=dict |
| <a id="L40"></a>40 | <code>    error_code: Mapped[str &#124; None] = mapped_column(String(80))</code> | Define error_code com mapped_column(String(80)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(80) |
| <a id="L41"></a>41 | <code>    signature: Mapped[str] = mapped_column(String(64))</code> | Define signature com mapped_column(String(64)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64) |
| <a id="L42"></a>42 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L43"></a>43 | <code>    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define updated_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L46"></a>46 | <code># Documentação: Define o tipo WorkerSnapshot e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerSnapshot e reúne o estado/contrato descrito para este módulo. |
| <a id="L47"></a>47 | <code>class WorkerSnapshot(Base):</code> | Define o tipo WorkerSnapshot e reúne o estado/contrato descrito para este módulo. |
| <a id="L48"></a>48 | <code>    __tablename__ = &quot;worker_snapshots&quot;</code> | Define __tablename__ com &#x27;worker_snapshots&#x27;. |
| <a id="L49"></a>49 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L50"></a>50 | <code>    user_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L51"></a>51 | <code>    worker_id: Mapped[UUID] = mapped_column(ForeignKey(&quot;workers.id&quot;), index=True)</code> | Define worker_id com mapped_column(ForeignKey(&#x27;workers.id&#x27;), index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;workers.id&#x27;), index=True |
| <a id="L52"></a>52 | <code>    status: Mapped[str] = mapped_column(String(16), default=&quot;PENDING&quot;)</code> | Define status com mapped_column(String(16), default=&#x27;PENDING&#x27;). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(16), default=&#x27;PENDING&#x27; |
| <a id="L53"></a>53 | <code>    sha256: Mapped[str &#124; None] = mapped_column(String(64))</code> | Define sha256 com mapped_column(String(64)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64) |
| <a id="L54"></a>54 | <code>    description: Mapped[str &#124; None] = mapped_column(Text)</code> | Define description com mapped_column(Text). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Text |
| <a id="L55"></a>55 | <code>    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now()). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now() |
