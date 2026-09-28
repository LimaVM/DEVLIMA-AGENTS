# backend/app/api/memories.py

Expõe memórias aceitas e propostas pendentes, com criação, desativação, aceitação e rejeição restritas ao usuário autenticado.

[Arquivo fonte](../../../../../backend/app/api/memories.py) · 125 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [list_memories](#L20) | Lista list_memories, segundo o contrato e as verificações deste módulo. |
| [create_memory](#L37) | Cria create_memory, segundo o contrato e as verificações deste módulo. |
| [deactivate_memory](#L49) | Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| [list_candidates](#L69) | Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| [accept_candidate](#L87) | Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| [reject_candidate](#L102) | Implementa reject_candidate como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import UTC, datetime</code> | Importa UTC, datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from fastapi import APIRouter, Depends, HTTPException, Query, Response</code> | Importa APIRouter, Depends, HTTPException, Query, Response de fastapi. |
| <a id="L5"></a>5 | <code>from sqlalchemy import select</code> | Importa select de sqlalchemy. |
| <a id="L6"></a>6 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>from app.agent.errors import AgentError</code> | Importa AgentError de app.agent.errors. |
| <a id="L9"></a>9 | <code>from app.agent.memory_manager import MemoryManager</code> | Importa MemoryManager de app.agent.memory_manager. |
| <a id="L10"></a>10 | <code>from app.db.session import get_session</code> | Importa get_session de app.db.session. |
| <a id="L11"></a>11 | <code>from app.models import AuditLog, Memory, MemoryCandidate, User</code> | Importa AuditLog, Memory, MemoryCandidate, User de app.models. |
| <a id="L12"></a>12 | <code>from app.schemas.memories import CandidateResponse, MemoryCreate, MemoryResponse</code> | Importa CandidateResponse, MemoryCreate, MemoryResponse de app.schemas.memories. |
| <a id="L13"></a>13 | <code>from app.security import get_current_user</code> | Importa get_current_user de app.security. |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code>router = APIRouter(prefix=&quot;/memories&quot;, tags=[&quot;memories&quot;])</code> | Define router com APIRouter(prefix=&#x27;/memories&#x27;, tags=[&#x27;memories&#x27;]). Invoca APIRouter com os argumentos declarados nesta instrução. Argumentos: prefix=&#x27;/memories&#x27;, tags=[&#x27;memories&#x27;] |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L17"></a>17 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L18"></a>18 | <code>@router.get(&quot;&quot;, response_model=list[MemoryResponse])</code> | Aplica o decorator router.get(&quot;&quot;, response_model=list[MemoryResponse]) à definição que segue. |
| <a id="L19"></a>19 | <code># Documentação: Lista list_memories, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L20"></a>20 | <code>def list_memories(</code> | Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L21"></a>21 | <code>    offset: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 20. Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L22"></a>22 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 20. Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L23"></a>23 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 20. Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L24"></a>24 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 20. Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L25"></a>25 | <code>):</code> | Continua/fecha a instrução da linha 20. Lista list_memories, segundo o contrato e as verificações deste módulo. |
| <a id="L26"></a>26 | <code>    return session.scalars(</code> | Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L27"></a>27 | <code>        select(Memory)</code> | Continua/fecha a instrução da linha 26. Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L28"></a>28 | <code>        .where(Memory.user_id == user.id, Memory.is_active.is_(True))</code> | Continua/fecha a instrução da linha 26. Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L29"></a>29 | <code>        .order_by(Memory.updated_at.desc(), Memory.id)</code> | Continua/fecha a instrução da linha 26. Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L30"></a>30 | <code>        .offset(offset)</code> | Continua/fecha a instrução da linha 26. Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L31"></a>31 | <code>        .limit(limit)</code> | Continua/fecha a instrução da linha 26. Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L32"></a>32 | <code>    ).all()</code> | Continua/fecha a instrução da linha 26. Retorna session.scalars(select(Memory).where(Memory.user_id == user.id, Memory.is_active.is_(True)).order_by(Memory.updated_at.desc(), Memory.id).offset(offset).limit(limit)).all() ao chamador e encerra este caminho da função. |
| <a id="L33"></a>33 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L35"></a>35 | <code>@router.post(&quot;&quot;, response_model=MemoryResponse, status_code=201)</code> | Aplica o decorator router.post(&quot;&quot;, response_model=MemoryResponse, status_code=201) à definição que segue. |
| <a id="L36"></a>36 | <code># Documentação: Cria create_memory, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria create_memory, segundo o contrato e as verificações deste módulo. |
| <a id="L37"></a>37 | <code>def create_memory(</code> | Cria create_memory, segundo o contrato e as verificações deste módulo. |
| <a id="L38"></a>38 | <code>    data: MemoryCreate,</code> | Continua/fecha a instrução da linha 37. Cria create_memory, segundo o contrato e as verificações deste módulo. |
| <a id="L39"></a>39 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 37. Cria create_memory, segundo o contrato e as verificações deste módulo. |
| <a id="L40"></a>40 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 37. Cria create_memory, segundo o contrato e as verificações deste módulo. |
| <a id="L41"></a>41 | <code>):</code> | Continua/fecha a instrução da linha 37. Cria create_memory, segundo o contrato e as verificações deste módulo. |
| <a id="L42"></a>42 | <code>    row = MemoryManager(session, user.id).create(data.content, data.category)</code> | Define row com MemoryManager(session, user.id).create(data.content, data.category). Invoca MemoryManager(session, user.id).create com os argumentos declarados nesta instrução. Argumentos: data.content, data.category |
| <a id="L43"></a>43 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L44"></a>44 | <code>    return row</code> | Retorna row ao chamador e encerra este caminho da função. |
| <a id="L45"></a>45 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L46"></a>46 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L47"></a>47 | <code>@router.delete(&quot;/{identifier}&quot;, status_code=204)</code> | Aplica o decorator router.delete(&quot;/{identifier}&quot;, status_code=204) à definição que segue. |
| <a id="L48"></a>48 | <code># Documentação: Implementa deactivate_memory como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| <a id="L49"></a>49 | <code>def deactivate_memory(</code> | Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| <a id="L50"></a>50 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 49. Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| <a id="L51"></a>51 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 49. Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| <a id="L52"></a>52 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 49. Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| <a id="L53"></a>53 | <code>):</code> | Continua/fecha a instrução da linha 49. Implementa deactivate_memory como parte do fluxo descrito para este arquivo. |
| <a id="L54"></a>54 | <code>    row = session.scalar(</code> | Define row com session.scalar(select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update() |
| <a id="L55"></a>55 | <code>        select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update()</code> | Continua/fecha a instrução da linha 54. Define row com session.scalar(select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update() |
| <a id="L56"></a>56 | <code>    )</code> | Continua/fecha a instrução da linha 54. Define row com session.scalar(select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update() |
| <a id="L57"></a>57 | <code>    if row is None:</code> | Executa este ramo somente se row is None; caso contrário, segue o ramo alternativo. |
| <a id="L58"></a>58 | <code>        raise HTTPException(404, &quot;not_found&quot;)</code> | Interrompe este caminho lançando HTTPException(404, &#x27;not_found&#x27;). |
| <a id="L59"></a>59 | <code>    row.is_active, row.updated_at = False, datetime.now(UTC)</code> | Define (row.is_active, row.updated_at) com (False, datetime.now(UTC)). |
| <a id="L60"></a>60 | <code>    session.add(</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.deactivated&#x27;, details={&#x27;memory_id&#x27;: str(row.id)}) |
| <a id="L61"></a>61 | <code>        AuditLog(user_id=user.id, event=&quot;memory.deactivated&quot;, details={&quot;memory_id&quot;: str(row.id)})</code> | Continua/fecha a instrução da linha 60. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.deactivated&#x27;, details={&#x27;memory_id&#x27;: str(row.id)}) |
| <a id="L62"></a>62 | <code>    )</code> | Continua/fecha a instrução da linha 60. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.deactivated&#x27;, details={&#x27;memory_id&#x27;: str(row.id)}) |
| <a id="L63"></a>63 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L64"></a>64 | <code>    return Response(status_code=204)</code> | Retorna Response(status_code=204) ao chamador e encerra este caminho da função. |
| <a id="L65"></a>65 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L66"></a>66 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L67"></a>67 | <code>@router.get(&quot;/candidates&quot;, response_model=list[CandidateResponse])</code> | Aplica o decorator router.get(&quot;/candidates&quot;, response_model=list[CandidateResponse]) à definição que segue. |
| <a id="L68"></a>68 | <code># Documentação: Lista list_candidates, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L69"></a>69 | <code>def list_candidates(</code> | Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L70"></a>70 | <code>    status: str = Query(&quot;PENDING&quot;, pattern=&quot;^(PENDING&#124;ACCEPTED&#124;REJECTED)$&quot;),</code> | Continua/fecha a instrução da linha 69. Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L71"></a>71 | <code>    offset: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 69. Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L72"></a>72 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 69. Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L73"></a>73 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 69. Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L74"></a>74 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 69. Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L75"></a>75 | <code>):</code> | Continua/fecha a instrução da linha 69. Lista list_candidates, segundo o contrato e as verificações deste módulo. |
| <a id="L76"></a>76 | <code>    return session.scalars(</code> | Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L77"></a>77 | <code>        select(MemoryCandidate)</code> | Continua/fecha a instrução da linha 76. Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L78"></a>78 | <code>        .where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status)</code> | Continua/fecha a instrução da linha 76. Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L79"></a>79 | <code>        .order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.id)</code> | Continua/fecha a instrução da linha 76. Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L80"></a>80 | <code>        .offset(offset)</code> | Continua/fecha a instrução da linha 76. Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L81"></a>81 | <code>        .limit(limit)</code> | Continua/fecha a instrução da linha 76. Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L82"></a>82 | <code>    ).all()</code> | Continua/fecha a instrução da linha 76. Retorna session.scalars(select(MemoryCandidate).where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status).order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.i... ao chamador e encerra este caminho da função. |
| <a id="L83"></a>83 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L84"></a>84 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L85"></a>85 | <code>@router.post(&quot;/candidates/{identifier}/accept&quot;, response_model=MemoryResponse)</code> | Aplica o decorator router.post(&quot;/candidates/{identifier}/accept&quot;, response_model=MemoryResponse) à definição que segue. |
| <a id="L86"></a>86 | <code># Documentação: Implementa accept_candidate como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L87"></a>87 | <code>def accept_candidate(</code> | Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L88"></a>88 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 87. Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L89"></a>89 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 87. Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L90"></a>90 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 87. Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L91"></a>91 | <code>):</code> | Continua/fecha a instrução da linha 87. Implementa accept_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L92"></a>92 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L93"></a>93 | <code>        row = MemoryManager(session, user.id).accept(identifier)</code> | Define row com MemoryManager(session, user.id).accept(identifier). Invoca MemoryManager(session, user.id).accept com os argumentos declarados nesta instrução. Argumentos: identifier |
| <a id="L94"></a>94 | <code>        session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L95"></a>95 | <code>        return row</code> | Retorna row ao chamador e encerra este caminho da função. |
| <a id="L96"></a>96 | <code>    except AgentError as error:</code> | Trata exceção AgentError como error. |
| <a id="L97"></a>97 | <code>        raise HTTPException(error.status_code, error.code) from None</code> | Interrompe este caminho lançando HTTPException(error.status_code, error.code). |
| <a id="L98"></a>98 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L99"></a>99 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L100"></a>100 | <code>@router.post(&quot;/candidates/{identifier}/reject&quot;, status_code=204)</code> | Aplica o decorator router.post(&quot;/candidates/{identifier}/reject&quot;, status_code=204) à definição que segue. |
| <a id="L101"></a>101 | <code># Documentação: Implementa reject_candidate como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa reject_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L102"></a>102 | <code>def reject_candidate(</code> | Implementa reject_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L103"></a>103 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 102. Implementa reject_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L104"></a>104 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 102. Implementa reject_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L105"></a>105 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 102. Implementa reject_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L106"></a>106 | <code>):</code> | Continua/fecha a instrução da linha 102. Implementa reject_candidate como parte do fluxo descrito para este arquivo. |
| <a id="L107"></a>107 | <code>    row = session.scalar(</code> | Define row com session.scalar(select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update() |
| <a id="L108"></a>108 | <code>        select(MemoryCandidate)</code> | Continua/fecha a instrução da linha 107. Define row com session.scalar(select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update() |
| <a id="L109"></a>109 | <code>        .where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id)</code> | Continua/fecha a instrução da linha 107. Define row com session.scalar(select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update() |
| <a id="L110"></a>110 | <code>        .with_for_update()</code> | Continua/fecha a instrução da linha 107. Define row com session.scalar(select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update() |
| <a id="L111"></a>111 | <code>    )</code> | Continua/fecha a instrução da linha 107. Define row com session.scalar(select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update()). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(MemoryCandidate).where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id).with_for_update() |
| <a id="L112"></a>112 | <code>    if row is None:</code> | Executa este ramo somente se row is None; caso contrário, segue o ramo alternativo. |
| <a id="L113"></a>113 | <code>        raise HTTPException(404, &quot;not_found&quot;)</code> | Interrompe este caminho lançando HTTPException(404, &#x27;not_found&#x27;). |
| <a id="L114"></a>114 | <code>    if row.status == &quot;ACCEPTED&quot;:</code> | Executa este ramo somente se row.status == &#x27;ACCEPTED&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L115"></a>115 | <code>        raise HTTPException(409, &quot;candidate_already_accepted&quot;)</code> | Interrompe este caminho lançando HTTPException(409, &#x27;candidate_already_accepted&#x27;). |
| <a id="L116"></a>116 | <code>    row.status, row.rejection_reason = &quot;REJECTED&quot;, &quot;user_rejected&quot;</code> | Define (row.status, row.rejection_reason) com (&#x27;REJECTED&#x27;, &#x27;user_rejected&#x27;). |
| <a id="L117"></a>117 | <code>    session.add(</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L118"></a>118 | <code>        AuditLog(</code> | Continua/fecha a instrução da linha 117. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L119"></a>119 | <code>            user_id=user.id,</code> | Continua/fecha a instrução da linha 117. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L120"></a>120 | <code>            event=&quot;memory.candidate_rejected&quot;,</code> | Continua/fecha a instrução da linha 117. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L121"></a>121 | <code>            details={&quot;candidate_id&quot;: str(row.id)},</code> | Continua/fecha a instrução da linha 117. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L122"></a>122 | <code>        )</code> | Continua/fecha a instrução da linha 117. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L123"></a>123 | <code>    )</code> | Continua/fecha a instrução da linha 117. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;memory.candidate_rejected&#x27;, details={&#x27;candidate_id&#x27;: str(row.id)}) |
| <a id="L124"></a>124 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L125"></a>125 | <code>    return Response(status_code=204)</code> | Retorna Response(status_code=204) ao chamador e encerra este caminho da função. |
