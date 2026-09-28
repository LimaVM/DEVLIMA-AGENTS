# backend/app/api/devices.py

Lista dispositivos do usuário autenticado e permite revogar dispositivo/famílias de sessão do mesmo proprietário.

[Arquivo fonte](../../../../../backend/app/api/devices.py) · 50 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [devices](#L17) | Implementa devices como parte do fluxo descrito para este arquivo. |
| [revoke](#L31) | Revoga revoke, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>from fastapi import APIRouter, Depends, HTTPException, Response</code> | Importa APIRouter, Depends, HTTPException, Response de fastapi. |
| <a id="L4"></a>4 | <code>from sqlalchemy import select</code> | Importa select de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.db.session import get_session</code> | Importa get_session de app.db.session. |
| <a id="L8"></a>8 | <code>from app.models import AuditLog, User</code> | Importa AuditLog, User de app.models. |
| <a id="L9"></a>9 | <code>from app.models.devices import Device, RefreshFamily</code> | Importa Device, RefreshFamily de app.models.devices. |
| <a id="L10"></a>10 | <code>from app.security import get_current_user</code> | Importa get_current_user de app.security. |
| <a id="L11"></a>11 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L12"></a>12 | <code>router = APIRouter(prefix=&quot;/devices&quot;, tags=[&quot;devices&quot;])</code> | Define router com APIRouter(prefix=&#x27;/devices&#x27;, tags=[&#x27;devices&#x27;]). Invoca APIRouter com os argumentos declarados nesta instrução. Argumentos: prefix=&#x27;/devices&#x27;, tags=[&#x27;devices&#x27;] |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code>@router.get(&quot;&quot;)</code> | Aplica o decorator router.get(&quot;&quot;) à definição que segue. |
| <a id="L16"></a>16 | <code># Documentação: Implementa devices como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa devices como parte do fluxo descrito para este arquivo. |
| <a id="L17"></a>17 | <code>def devices(session: Session = Depends(get_session), user: User = Depends(get_current_user)):</code> | Implementa devices como parte do fluxo descrito para este arquivo. |
| <a id="L18"></a>18 | <code>    return [</code> | Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L19"></a>19 | <code>        {&quot;id&quot;: row.id, &quot;name&quot;: row.name, &quot;revoked&quot;: row.revoked, &quot;last_seen_at&quot;: row.last_seen_at}</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L20"></a>20 | <code>        for row in session.scalars(</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L21"></a>21 | <code>            select(Device)</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L22"></a>22 | <code>            .where(Device.user_id == user.id)</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L23"></a>23 | <code>            .order_by(Device.created_at.desc())</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L24"></a>24 | <code>            .limit(100)</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L25"></a>25 | <code>        )</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L26"></a>26 | <code>    ]</code> | Continua/fecha a instrução da linha 18. Retorna [{&#x27;id&#x27;: row.id, &#x27;name&#x27;: row.name, &#x27;revoked&#x27;: row.revoked, &#x27;last_seen_at&#x27;: row.last_seen_at} for row in session.scalars(select(Device).where(Device.user_id == user.id).order_by(D... ao chamador e encerra este caminho da função. |
| <a id="L27"></a>27 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L28"></a>28 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L29"></a>29 | <code>@router.post(&quot;/{identifier}/revoke&quot;, status_code=204)</code> | Aplica o decorator router.post(&quot;/{identifier}/revoke&quot;, status_code=204) à definição que segue. |
| <a id="L30"></a>30 | <code># Documentação: Revoga revoke, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Revoga revoke, segundo o contrato e as verificações deste módulo. |
| <a id="L31"></a>31 | <code>def revoke(</code> | Revoga revoke, segundo o contrato e as verificações deste módulo. |
| <a id="L32"></a>32 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 31. Revoga revoke, segundo o contrato e as verificações deste módulo. |
| <a id="L33"></a>33 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 31. Revoga revoke, segundo o contrato e as verificações deste módulo. |
| <a id="L34"></a>34 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 31. Revoga revoke, segundo o contrato e as verificações deste módulo. |
| <a id="L35"></a>35 | <code>):</code> | Continua/fecha a instrução da linha 31. Revoga revoke, segundo o contrato e as verificações deste módulo. |
| <a id="L36"></a>36 | <code>    row = session.scalar(</code> | Define row com session.scalar(select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update() |
| <a id="L37"></a>37 | <code>        select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update()</code> | Continua/fecha a instrução da linha 36. Define row com session.scalar(select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update() |
| <a id="L38"></a>38 | <code>    )</code> | Continua/fecha a instrução da linha 36. Define row com session.scalar(select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update() |
| <a id="L39"></a>39 | <code>    if row is None:</code> | Executa este ramo somente se row is None; caso contrário, segue o ramo alternativo. |
| <a id="L40"></a>40 | <code>        raise HTTPException(404, &quot;not_found&quot;)</code> | Interrompe este caminho lançando HTTPException(404, &#x27;not_found&#x27;). |
| <a id="L41"></a>41 | <code>    row.revoked = True</code> | Define row.revoked com True. |
| <a id="L42"></a>42 | <code>    for family in session.scalars(</code> | Percorre session.scalars(select(RefreshFamily).where(RefreshFamily.device_id == row.id).with_for_update()), atribuindo cada elemento a family. |
| <a id="L43"></a>43 | <code>        select(RefreshFamily).where(RefreshFamily.device_id == row.id).with_for_update()</code> | Continua/fecha a instrução da linha 42. Percorre session.scalars(select(RefreshFamily).where(RefreshFamily.device_id == row.id).with_for_update()), atribuindo cada elemento a family. |
| <a id="L44"></a>44 | <code>    ):</code> | Continua/fecha a instrução da linha 42. Percorre session.scalars(select(RefreshFamily).where(RefreshFamily.device_id == row.id).with_for_update()), atribuindo cada elemento a family. |
| <a id="L45"></a>45 | <code>        family.revoked = True</code> | Define family.revoked com True. |
| <a id="L46"></a>46 | <code>    session.add(</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;device.revoked&#x27;, details={&#x27;device_id&#x27;: str(row.id)}) |
| <a id="L47"></a>47 | <code>        AuditLog(user_id=user.id, event=&quot;device.revoked&quot;, details={&quot;device_id&quot;: str(row.id)})</code> | Continua/fecha a instrução da linha 46. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;device.revoked&#x27;, details={&#x27;device_id&#x27;: str(row.id)}) |
| <a id="L48"></a>48 | <code>    )</code> | Continua/fecha a instrução da linha 46. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;device.revoked&#x27;, details={&#x27;device_id&#x27;: str(row.id)}) |
| <a id="L49"></a>49 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L50"></a>50 | <code>    return Response(status_code=204)</code> | Retorna Response(status_code=204) ao chamador e encerra este caminho da função. |
