# backend/app/api/chat.py

Expõe conversas e mensagens com filtro de proprietário, histórico ordenado, arquivamento e envio pelo AgentCore.

[Arquivo fonte](../../../../../backend/app/api/chat.py) · 162 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [owned](#L28) | Implementa owned como parte do fluxo descrito para este arquivo. |
| [create_conversation](#L40) | Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| [list_conversations](#L59) | Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| [get_conversation](#L77) | Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| [archive_conversation](#L87) | Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| [list_messages](#L112) | Lista list_messages, segundo o contrato e as verificações deste módulo. |
| [list_summaries](#L134) | Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| [send_message](#L154) | Implementa send_message como parte do fluxo descrito para este arquivo. |

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
| <a id="L8"></a>8 | <code>from app.agent.core import AgentCore</code> | Importa AgentCore de app.agent.core. |
| <a id="L9"></a>9 | <code>from app.agent.errors import AgentError</code> | Importa AgentError de app.agent.errors. |
| <a id="L10"></a>10 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L11"></a>11 | <code>from app.db.session import get_session</code> | Importa get_session de app.db.session. |
| <a id="L12"></a>12 | <code>from app.llm.base import LLMError</code> | Importa LLMError de app.llm.base. |
| <a id="L13"></a>13 | <code>from app.models import AuditLog, Conversation, ConversationSummary, Message, User</code> | Importa AuditLog, Conversation, ConversationSummary, Message, User de app.models. |
| <a id="L14"></a>14 | <code>from app.schemas.chat import (</code> | Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L15"></a>15 | <code>    ChatReply,</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L16"></a>16 | <code>    ChatSend,</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L17"></a>17 | <code>    ConversationCreate,</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L18"></a>18 | <code>    ConversationResponse,</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L19"></a>19 | <code>    MessageResponse,</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L20"></a>20 | <code>    SummaryResponse,</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L21"></a>21 | <code>)</code> | Continua/fecha a instrução da linha 14. Importa ChatReply, ChatSend, ConversationCreate, ConversationResponse, MessageResponse, SummaryResponse de app.schemas.chat. |
| <a id="L22"></a>22 | <code>from app.security import get_current_user</code> | Importa get_current_user de app.security. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code>router = APIRouter(prefix=&quot;/chat&quot;, tags=[&quot;chat&quot;])</code> | Define router com APIRouter(prefix=&#x27;/chat&#x27;, tags=[&#x27;chat&#x27;]). Invoca APIRouter com os argumentos declarados nesta instrução. Argumentos: prefix=&#x27;/chat&#x27;, tags=[&#x27;chat&#x27;] |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L26"></a>26 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L27"></a>27 | <code># Documentação: Implementa owned como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa owned como parte do fluxo descrito para este arquivo. |
| <a id="L28"></a>28 | <code>def owned(session, user, identifier, lock=False):</code> | Implementa owned como parte do fluxo descrito para este arquivo. |
| <a id="L29"></a>29 | <code>    query = select(Conversation).where(</code> | Define query com select(Conversation).where(Conversation.id == identifier, Conversation.user_id == user.id). Acrescenta predicado que filtra os registros da consulta. Argumentos: Conversation.id == identifier, Conversation.user_id == user.id |
| <a id="L30"></a>30 | <code>        Conversation.id == identifier, Conversation.user_id == user.id</code> | Continua/fecha a instrução da linha 29. Define query com select(Conversation).where(Conversation.id == identifier, Conversation.user_id == user.id). Acrescenta predicado que filtra os registros da consulta. Argumentos: Conversation.id == identifier, Conversation.user_id == user.id |
| <a id="L31"></a>31 | <code>    )</code> | Continua/fecha a instrução da linha 29. Define query com select(Conversation).where(Conversation.id == identifier, Conversation.user_id == user.id). Acrescenta predicado que filtra os registros da consulta. Argumentos: Conversation.id == identifier, Conversation.user_id == user.id |
| <a id="L32"></a>32 | <code>    row = session.scalar(query.with_for_update() if lock else query)</code> | Define row com session.scalar(query.with_for_update() if lock else query). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: query.with_for_update() if lock else query |
| <a id="L33"></a>33 | <code>    if row is None:</code> | Executa este ramo somente se row is None; caso contrário, segue o ramo alternativo. |
| <a id="L34"></a>34 | <code>        raise HTTPException(404, &quot;not_found&quot;)</code> | Interrompe este caminho lançando HTTPException(404, &#x27;not_found&#x27;). |
| <a id="L35"></a>35 | <code>    return row</code> | Retorna row ao chamador e encerra este caminho da função. |
| <a id="L36"></a>36 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L38"></a>38 | <code>@router.post(&quot;/conversations&quot;, response_model=ConversationResponse, status_code=201)</code> | Aplica o decorator router.post(&quot;/conversations&quot;, response_model=ConversationResponse, status_code=201) à definição que segue. |
| <a id="L39"></a>39 | <code># Documentação: Cria create_conversation, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L40"></a>40 | <code>def create_conversation(</code> | Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L41"></a>41 | <code>    data: ConversationCreate,</code> | Continua/fecha a instrução da linha 40. Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L42"></a>42 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 40. Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L43"></a>43 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 40. Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L44"></a>44 | <code>):</code> | Continua/fecha a instrução da linha 40. Cria create_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L45"></a>45 | <code>    row = Conversation(user_id=user.id, title=data.title)</code> | Define row com Conversation(user_id=user.id, title=data.title). Invoca Conversation com os argumentos declarados nesta instrução. Argumentos: user_id=user.id, title=data.title |
| <a id="L46"></a>46 | <code>    session.add(row)</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: row |
| <a id="L47"></a>47 | <code>    session.flush()</code> | Envia alterações pendentes ao banco sem confirmar a transação. |
| <a id="L48"></a>48 | <code>    session.add(</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.created&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L49"></a>49 | <code>        AuditLog(</code> | Continua/fecha a instrução da linha 48. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.created&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L50"></a>50 | <code>            user_id=user.id, event=&quot;conversation.created&quot;, details={&quot;conversation_id&quot;: str(row.id)}</code> | Continua/fecha a instrução da linha 48. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.created&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L51"></a>51 | <code>        )</code> | Continua/fecha a instrução da linha 48. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.created&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L52"></a>52 | <code>    )</code> | Continua/fecha a instrução da linha 48. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.created&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L53"></a>53 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L54"></a>54 | <code>    return row</code> | Retorna row ao chamador e encerra este caminho da função. |
| <a id="L55"></a>55 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L56"></a>56 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L57"></a>57 | <code>@router.get(&quot;/conversations&quot;, response_model=list[ConversationResponse])</code> | Aplica o decorator router.get(&quot;/conversations&quot;, response_model=list[ConversationResponse]) à definição que segue. |
| <a id="L58"></a>58 | <code># Documentação: Lista list_conversations, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L59"></a>59 | <code>def list_conversations(</code> | Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L60"></a>60 | <code>    archived: bool = False,</code> | Continua/fecha a instrução da linha 59. Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L61"></a>61 | <code>    offset: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 59. Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L62"></a>62 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 59. Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L63"></a>63 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 59. Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L64"></a>64 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 59. Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L65"></a>65 | <code>):</code> | Continua/fecha a instrução da linha 59. Lista list_conversations, segundo o contrato e as verificações deste módulo. |
| <a id="L66"></a>66 | <code>    return session.scalars(</code> | Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L67"></a>67 | <code>        select(Conversation)</code> | Continua/fecha a instrução da linha 66. Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L68"></a>68 | <code>        .where(Conversation.user_id == user.id, Conversation.archived == archived)</code> | Continua/fecha a instrução da linha 66. Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L69"></a>69 | <code>        .order_by(Conversation.updated_at.desc(), Conversation.id)</code> | Continua/fecha a instrução da linha 66. Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L70"></a>70 | <code>        .offset(offset)</code> | Continua/fecha a instrução da linha 66. Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L71"></a>71 | <code>        .limit(limit)</code> | Continua/fecha a instrução da linha 66. Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L72"></a>72 | <code>    ).all()</code> | Continua/fecha a instrução da linha 66. Retorna session.scalars(select(Conversation).where(Conversation.user_id == user.id, Conversation.archived == archived).order_by(Conversation.updated_at.desc(), Conversation.id).offset(o... ao chamador e encerra este caminho da função. |
| <a id="L73"></a>73 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L74"></a>74 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L75"></a>75 | <code>@router.get(&quot;/conversations/{identifier}&quot;, response_model=ConversationResponse)</code> | Aplica o decorator router.get(&quot;/conversations/{identifier}&quot;, response_model=ConversationResponse) à definição que segue. |
| <a id="L76"></a>76 | <code># Documentação: Obtém get_conversation, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L77"></a>77 | <code>def get_conversation(</code> | Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L78"></a>78 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 77. Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L79"></a>79 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 77. Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L80"></a>80 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 77. Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L81"></a>81 | <code>):</code> | Continua/fecha a instrução da linha 77. Obtém get_conversation, segundo o contrato e as verificações deste módulo. |
| <a id="L82"></a>82 | <code>    return owned(session, user, identifier)</code> | Retorna owned(session, user, identifier) ao chamador e encerra este caminho da função. |
| <a id="L83"></a>83 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L84"></a>84 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L85"></a>85 | <code>@router.post(&quot;/conversations/{identifier}/archive&quot;, status_code=204)</code> | Aplica o decorator router.post(&quot;/conversations/{identifier}/archive&quot;, status_code=204) à definição que segue. |
| <a id="L86"></a>86 | <code># Documentação: Implementa archive_conversation como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| <a id="L87"></a>87 | <code>def archive_conversation(</code> | Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| <a id="L88"></a>88 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 87. Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| <a id="L89"></a>89 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 87. Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| <a id="L90"></a>90 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 87. Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| <a id="L91"></a>91 | <code>):</code> | Continua/fecha a instrução da linha 87. Implementa archive_conversation como parte do fluxo descrito para este arquivo. |
| <a id="L92"></a>92 | <code>    row = owned(session, user, identifier, lock=True)</code> | Define row com owned(session, user, identifier, lock=True). Invoca owned com os argumentos declarados nesta instrução. Argumentos: session, user, identifier, lock=True |
| <a id="L93"></a>93 | <code>    if row.lease_owner and row.lease_until &gt; datetime.now(UTC):</code> | Executa este ramo somente se row.lease_owner and row.lease_until &gt; datetime.now(UTC); caso contrário, segue o ramo alternativo. |
| <a id="L94"></a>94 | <code>        raise HTTPException(409, &quot;conversation_busy&quot;)</code> | Interrompe este caminho lançando HTTPException(409, &#x27;conversation_busy&#x27;). |
| <a id="L95"></a>95 | <code>    if row.pending_message_id:</code> | Executa este ramo somente se row.pending_message_id; caso contrário, segue o ramo alternativo. |
| <a id="L96"></a>96 | <code>        source = session.get(Message, row.pending_message_id)</code> | Define source com session.get(Message, row.pending_message_id). Invoca session.get com os argumentos declarados nesta instrução. Argumentos: Message, row.pending_message_id |
| <a id="L97"></a>97 | <code>        source.status, source.error_code = &quot;FAILED&quot;, &quot;processing_lease_expired&quot;</code> | Define (source.status, source.error_code) com (&#x27;FAILED&#x27;, &#x27;processing_lease_expired&#x27;). |
| <a id="L98"></a>98 | <code>    row.lease_owner = row.lease_until = row.pending_message_id = None</code> | Define row.lease_owner, row.lease_until, row.pending_message_id com None. Identifica quem reivindicou o processamento; resultado só é aceito se o lease ainda pertencer à execução. Prazo da reivindicação; permite detectar processamento abandonado sem manter lock durante toda a inferência. |
| <a id="L99"></a>99 | <code>    row.archived = True</code> | Define row.archived com True. |
| <a id="L100"></a>100 | <code>    row.updated_at = datetime.now(UTC)</code> | Define row.updated_at com datetime.now(UTC). Invoca datetime.now com os argumentos declarados nesta instrução. Argumentos: UTC |
| <a id="L101"></a>101 | <code>    session.add(</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.archived&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L102"></a>102 | <code>        AuditLog(</code> | Continua/fecha a instrução da linha 101. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.archived&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L103"></a>103 | <code>            user_id=user.id, event=&quot;conversation.archived&quot;, details={&quot;conversation_id&quot;: str(row.id)}</code> | Continua/fecha a instrução da linha 101. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.archived&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L104"></a>104 | <code>        )</code> | Continua/fecha a instrução da linha 101. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.archived&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L105"></a>105 | <code>    )</code> | Continua/fecha a instrução da linha 101. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=&#x27;conversation.archived&#x27;, details={&#x27;conversation_id&#x27;: str(row.id)}) |
| <a id="L106"></a>106 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L107"></a>107 | <code>    return Response(status_code=204)</code> | Retorna Response(status_code=204) ao chamador e encerra este caminho da função. |
| <a id="L108"></a>108 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L109"></a>109 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L110"></a>110 | <code>@router.get(&quot;/conversations/{identifier}/messages&quot;, response_model=list[MessageResponse])</code> | Aplica o decorator router.get(&quot;/conversations/{identifier}/messages&quot;, response_model=list[MessageResponse]) à definição que segue. |
| <a id="L111"></a>111 | <code># Documentação: Lista list_messages, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L112"></a>112 | <code>def list_messages(</code> | Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L113"></a>113 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 112. Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L114"></a>114 | <code>    after_sequence: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 112. Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L115"></a>115 | <code>    limit: int = Query(100, ge=1, le=200),</code> | Continua/fecha a instrução da linha 112. Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L116"></a>116 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 112. Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L117"></a>117 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 112. Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L118"></a>118 | <code>):</code> | Continua/fecha a instrução da linha 112. Lista list_messages, segundo o contrato e as verificações deste módulo. |
| <a id="L119"></a>119 | <code>    owned(session, user, identifier)</code> | Invoca owned com os argumentos declarados nesta instrução. Argumentos: session, user, identifier |
| <a id="L120"></a>120 | <code>    return session.scalars(</code> | Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L121"></a>121 | <code>        select(Message)</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L122"></a>122 | <code>        .where(</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L123"></a>123 | <code>            Message.conversation_id == identifier,</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L124"></a>124 | <code>            Message.user_id == user.id,</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L125"></a>125 | <code>            Message.sequence &gt; after_sequence,</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L126"></a>126 | <code>        )</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L127"></a>127 | <code>        .order_by(Message.sequence)</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L128"></a>128 | <code>        .limit(limit)</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L129"></a>129 | <code>    ).all()</code> | Continua/fecha a instrução da linha 120. Retorna session.scalars(select(Message).where(Message.conversation_id == identifier, Message.user_id == user.id, Message.sequence &gt; after_sequence).order_by(Message.sequence).limit(limi... ao chamador e encerra este caminho da função. |
| <a id="L130"></a>130 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L131"></a>131 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L132"></a>132 | <code>@router.get(&quot;/conversations/{identifier}/summaries&quot;, response_model=list[SummaryResponse])</code> | Aplica o decorator router.get(&quot;/conversations/{identifier}/summaries&quot;, response_model=list[SummaryResponse]) à definição que segue. |
| <a id="L133"></a>133 | <code># Documentação: Lista list_summaries, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L134"></a>134 | <code>def list_summaries(</code> | Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L135"></a>135 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 134. Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L136"></a>136 | <code>    limit: int = Query(20, ge=1, le=100),</code> | Continua/fecha a instrução da linha 134. Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L137"></a>137 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 134. Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L138"></a>138 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 134. Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L139"></a>139 | <code>):</code> | Continua/fecha a instrução da linha 134. Lista list_summaries, segundo o contrato e as verificações deste módulo. |
| <a id="L140"></a>140 | <code>    owned(session, user, identifier)</code> | Invoca owned com os argumentos declarados nesta instrução. Argumentos: session, user, identifier |
| <a id="L141"></a>141 | <code>    return session.scalars(</code> | Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L142"></a>142 | <code>        select(ConversationSummary)</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L143"></a>143 | <code>        .where(</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L144"></a>144 | <code>            ConversationSummary.conversation_id == identifier,</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L145"></a>145 | <code>            ConversationSummary.user_id == user.id,</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L146"></a>146 | <code>        )</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L147"></a>147 | <code>        .order_by(ConversationSummary.through_sequence.desc())</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L148"></a>148 | <code>        .limit(limit)</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L149"></a>149 | <code>    ).all()</code> | Continua/fecha a instrução da linha 141. Retorna session.scalars(select(ConversationSummary).where(ConversationSummary.conversation_id == identifier, ConversationSummary.user_id == user.id).order_by(ConversationSummary.through... ao chamador e encerra este caminho da função. |
| <a id="L150"></a>150 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L151"></a>151 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L152"></a>152 | <code>@router.post(&quot;/messages&quot;, response_model=ChatReply)</code> | Aplica o decorator router.post(&quot;/messages&quot;, response_model=ChatReply) à definição que segue. |
| <a id="L153"></a>153 | <code># Documentação: Implementa send_message como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa send_message como parte do fluxo descrito para este arquivo. |
| <a id="L154"></a>154 | <code>def send_message(</code> | Implementa send_message como parte do fluxo descrito para este arquivo. |
| <a id="L155"></a>155 | <code>    data: ChatSend, user: User = Depends(get_current_user), session: Session = Depends(get_session)</code> | Continua/fecha a instrução da linha 154. Implementa send_message como parte do fluxo descrito para este arquivo. |
| <a id="L156"></a>156 | <code>):</code> | Continua/fecha a instrução da linha 154. Implementa send_message como parte do fluxo descrito para este arquivo. |
| <a id="L157"></a>157 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L158"></a>158 | <code>        return AgentCore(session, get_settings()).send(user.id, data)</code> | Retorna AgentCore(session, get_settings()).send(user.id, data) ao chamador e encerra este caminho da função. |
| <a id="L159"></a>159 | <code>    except AgentError as error:</code> | Trata exceção AgentError como error. |
| <a id="L160"></a>160 | <code>        raise HTTPException(error.status_code, error.code) from None</code> | Interrompe este caminho lançando HTTPException(error.status_code, error.code). |
| <a id="L161"></a>161 | <code>    except LLMError as error:</code> | Trata exceção LLMError como error. |
| <a id="L162"></a>162 | <code>        raise HTTPException(503, error.code) from None</code> | Interrompe este caminho lançando HTTPException(503, error.code). |
