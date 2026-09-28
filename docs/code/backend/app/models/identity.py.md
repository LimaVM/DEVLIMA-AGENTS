# backend/app/models/identity.py

Mapeia usuário, auditoria e throttle de login. A senha é representada por hash e token_version permite invalidar sessões.

[Arquivo fonte](../../../../../backend/app/models/identity.py) · 45 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [User](#L11) | Define o tipo User e reúne o estado/contrato descrito para este módulo. |
| [AuditLog](#L26) | Define o tipo AuditLog e reúne o estado/contrato descrito para este módulo. |
| [LoginThrottle](#L40) | Define o tipo LoginThrottle e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID, uuid4</code> | Importa UUID, uuid4 de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, func</code> | Importa JSON, Boolean, DateTime, ForeignKey, Integer, String, func de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Mapped, mapped_column</code> | Importa Mapped, mapped_column de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.db.base import Base</code> | Importa Base de app.db.base. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code># Documentação: Define o tipo User e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo User e reúne o estado/contrato descrito para este módulo. |
| <a id="L11"></a>11 | <code>class User(Base):</code> | Define o tipo User e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>    __tablename__ = &quot;users&quot;</code> | Define __tablename__ com &#x27;users&#x27;. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L15"></a>15 | <code>    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)</code> | Define username com mapped_column(String(80), unique=True, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(80), unique=True, nullable=False |
| <a id="L16"></a>16 | <code>    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)</code> | Define password_hash com mapped_column(String(255), nullable=False). Armazena verificador Argon2; não é a senha original do usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(255), nullable=False |
| <a id="L17"></a>17 | <code>    timezone: Mapped[str] = mapped_column(String(80), nullable=False)</code> | Define timezone com mapped_column(String(80), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(80), nullable=False |
| <a id="L18"></a>18 | <code>    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)</code> | Define is_active com mapped_column(Boolean, default=True, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Boolean, default=True, nullable=False |
| <a id="L19"></a>19 | <code>    token_version: Mapped[int] = mapped_column(Integer, default=0, nullable=False)</code> | Define token_version com mapped_column(Integer, default=0, nullable=False). Contador de revogação comparado com o JWT para invalidar tokens antigos. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer, default=0, nullable=False |
| <a id="L20"></a>20 | <code>    created_at: Mapped[datetime] = mapped_column(</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False |
| <a id="L21"></a>21 | <code>        DateTime(timezone=True), server_default=func.now(), nullable=False</code> | Continua/fecha a instrução da linha 20. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False |
| <a id="L22"></a>22 | <code>    )</code> | Continua/fecha a instrução da linha 20. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code># Documentação: Define o tipo AuditLog e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo AuditLog e reúne o estado/contrato descrito para este módulo. |
| <a id="L26"></a>26 | <code>class AuditLog(Base):</code> | Define o tipo AuditLog e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>    __tablename__ = &quot;audit_log&quot;</code> | Define __tablename__ com &#x27;audit_log&#x27;. |
| <a id="L28"></a>28 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L29"></a>29 | <code>    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)</code> | Define id com mapped_column(primary_key=True, default=uuid4). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: primary_key=True, default=uuid4 |
| <a id="L30"></a>30 | <code>    user_id: Mapped[UUID &#124; None] = mapped_column(ForeignKey(&quot;users.id&quot;), index=True)</code> | Define user_id com mapped_column(ForeignKey(&#x27;users.id&#x27;), index=True). Vincula o registro ao proprietário; consultas e alterações devem filtrar esse usuário. Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: ForeignKey(&#x27;users.id&#x27;), index=True |
| <a id="L31"></a>31 | <code>    event: Mapped[str] = mapped_column(String(80), nullable=False, index=True)</code> | Define event com mapped_column(String(80), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(80), nullable=False, index=True |
| <a id="L32"></a>32 | <code>    request_id: Mapped[str &#124; None] = mapped_column(String(36))</code> | Define request_id com mapped_column(String(36)). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(36) |
| <a id="L33"></a>33 | <code>    details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)</code> | Define details com mapped_column(JSON, default=dict, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: JSON, default=dict, nullable=False |
| <a id="L34"></a>34 | <code>    created_at: Mapped[datetime] = mapped_column(</code> | Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False, index=True |
| <a id="L35"></a>35 | <code>        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True</code> | Continua/fecha a instrução da linha 34. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False, index=True |
| <a id="L36"></a>36 | <code>    )</code> | Continua/fecha a instrução da linha 34. Define created_at com mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), server_default=func.now(), nullable=False, index=True |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L38"></a>38 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L39"></a>39 | <code># Documentação: Define o tipo LoginThrottle e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo LoginThrottle e reúne o estado/contrato descrito para este módulo. |
| <a id="L40"></a>40 | <code>class LoginThrottle(Base):</code> | Define o tipo LoginThrottle e reúne o estado/contrato descrito para este módulo. |
| <a id="L41"></a>41 | <code>    __tablename__ = &quot;login_throttles&quot;</code> | Define __tablename__ com &#x27;login_throttles&#x27;. |
| <a id="L42"></a>42 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L43"></a>43 | <code>    bucket: Mapped[str] = mapped_column(String(64), primary_key=True)</code> | Define bucket com mapped_column(String(64), primary_key=True). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: String(64), primary_key=True |
| <a id="L44"></a>44 | <code>    attempts: Mapped[int] = mapped_column(Integer, nullable=False)</code> | Define attempts com mapped_column(Integer, nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: Integer, nullable=False |
| <a id="L45"></a>45 | <code>    window_started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)</code> | Define window_started_at com mapped_column(DateTime(timezone=True), nullable=False). Invoca mapped_column com os argumentos declarados nesta instrução. Argumentos: DateTime(timezone=True), nullable=False |
