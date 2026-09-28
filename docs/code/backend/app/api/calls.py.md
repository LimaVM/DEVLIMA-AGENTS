# backend/app/api/calls.py

Expõe listagem, atendimento, recusa, encerramento e transcrição de chamadas. Verifica o proprietário e a vinculação do dispositivo antes de alterar uma sessão.

[Arquivo fonte](../../../../../backend/app/api/calls.py) · 127 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [DeviceAction](#L24) | Define o tipo DeviceAction e reúne o estado/contrato descrito para este módulo. |
| [Transcript](#L30) | Define o tipo Transcript e reúne o estado/contrato descrito para este módulo. |
| [bind](#L36) | Implementa bind como parte do fluxo descrito para este arquivo. |
| [list_calls](#L47) | Lista list_calls, segundo o contrato e as verificações deste módulo. |
| [incoming](#L67) | Implementa incoming como parte do fluxo descrito para este arquivo. |
| [end](#L89) | Implementa end como parte do fluxo descrito para este arquivo. |
| [transcript](#L107) | Implementa transcript como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>from fastapi import APIRouter, Depends, HTTPException, Query</code> | Importa APIRouter, Depends, HTTPException, Query de fastapi. |
| <a id="L4"></a>4 | <code>from pydantic import BaseModel, ConfigDict, Field</code> | Importa BaseModel, ConfigDict, Field de pydantic. |
| <a id="L5"></a>5 | <code>from sqlalchemy import select</code> | Importa select de sqlalchemy. |
| <a id="L6"></a>6 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>from app.agent.core import AgentCore</code> | Importa AgentCore de app.agent.core. |
| <a id="L9"></a>9 | <code>from app.agent.errors import AgentError</code> | Importa AgentError de app.agent.errors. |
| <a id="L10"></a>10 | <code>from app.calls.service import CallService, state</code> | Importa CallService, state de app.calls.service. |
| <a id="L11"></a>11 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L12"></a>12 | <code>from app.db.session import get_session</code> | Importa get_session de app.db.session. |
| <a id="L13"></a>13 | <code>from app.llm.base import LLMError</code> | Importa LLMError de app.llm.base. |
| <a id="L14"></a>14 | <code>from app.models import User</code> | Importa User de app.models. |
| <a id="L15"></a>15 | <code>from app.models.calls import CallSession</code> | Importa CallSession de app.models.calls. |
| <a id="L16"></a>16 | <code>from app.models.devices import RefreshFamily</code> | Importa RefreshFamily de app.models.devices. |
| <a id="L17"></a>17 | <code>from app.schemas.chat import ChatSend</code> | Importa ChatSend de app.schemas.chat. |
| <a id="L18"></a>18 | <code>from app.security import bearer, decode_token, get_current_user</code> | Importa bearer, decode_token, get_current_user de app.security. |
| <a id="L19"></a>19 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L20"></a>20 | <code>router = APIRouter(prefix=&quot;/calls&quot;, tags=[&quot;calls&quot;])</code> | Define router com APIRouter(prefix=&#x27;/calls&#x27;, tags=[&#x27;calls&#x27;]). Invoca APIRouter com os argumentos declarados nesta instrução. Argumentos: prefix=&#x27;/calls&#x27;, tags=[&#x27;calls&#x27;] |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code># Documentação: Define o tipo DeviceAction e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo DeviceAction e reúne o estado/contrato descrito para este módulo. |
| <a id="L24"></a>24 | <code>class DeviceAction(BaseModel):</code> | Define o tipo DeviceAction e reúne o estado/contrato descrito para este módulo. |
| <a id="L25"></a>25 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L26"></a>26 | <code>    device_id: UUID</code> | Define device_id com None. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L27"></a>27 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L28"></a>28 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L29"></a>29 | <code># Documentação: Define o tipo Transcript e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Transcript e reúne o estado/contrato descrito para este módulo. |
| <a id="L30"></a>30 | <code>class Transcript(DeviceAction):</code> | Define o tipo Transcript e reúne o estado/contrato descrito para este módulo. |
| <a id="L31"></a>31 | <code>    client_message_id: UUID</code> | Define client_message_id com None. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L32"></a>32 | <code>    content: str = Field(min_length=1, max_length=4000)</code> | Define content com Field(min_length=1, max_length=4000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=4000 |
| <a id="L33"></a>33 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L35"></a>35 | <code># Documentação: Implementa bind como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa bind como parte do fluxo descrito para este arquivo. |
| <a id="L36"></a>36 | <code>def bind(session, user, data, credentials):</code> | Implementa bind como parte do fluxo descrito para este arquivo. |
| <a id="L37"></a>37 | <code>    claims = decode_token(credentials.credentials, get_settings())</code> | Define claims com decode_token(credentials.credentials, get_settings()). Invoca decode_token com os argumentos declarados nesta instrução. Argumentos: credentials.credentials, get_settings() |
| <a id="L38"></a>38 | <code>    if &quot;sid&quot; in claims:</code> | Executa este ramo somente se &#x27;sid&#x27; in claims; caso contrário, segue o ramo alternativo. |
| <a id="L39"></a>39 | <code>        family = session.get(RefreshFamily, UUID(claims[&quot;sid&quot;]))</code> | Define family com session.get(RefreshFamily, UUID(claims[&#x27;sid&#x27;])). Invoca session.get com os argumentos declarados nesta instrução. Argumentos: RefreshFamily, UUID(claims[&#x27;sid&#x27;]) |
| <a id="L40"></a>40 | <code>        if family.device_id != data.device_id:</code> | Executa este ramo somente se family.device_id != data.device_id; caso contrário, segue o ramo alternativo. |
| <a id="L41"></a>41 | <code>            raise HTTPException(403, &quot;device_session_mismatch&quot;)</code> | Interrompe este caminho lançando HTTPException(403, &#x27;device_session_mismatch&#x27;). |
| <a id="L42"></a>42 | <code>    return CallService(session, user.id, data.device_id)</code> | Retorna CallService(session, user.id, data.device_id) ao chamador e encerra este caminho da função. |
| <a id="L43"></a>43 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code>@router.get(&quot;&quot;)</code> | Aplica o decorator router.get(&quot;&quot;) à definição que segue. |
| <a id="L46"></a>46 | <code># Documentação: Lista list_calls, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L47"></a>47 | <code>def list_calls(</code> | Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L48"></a>48 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 47. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L49"></a>49 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 47. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L50"></a>50 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 47. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L51"></a>51 | <code>):</code> | Continua/fecha a instrução da linha 47. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L52"></a>52 | <code>    CallService(session, user.id).expire()</code> | Invoca CallService(session, user.id).expire com os argumentos declarados nesta instrução. |
| <a id="L53"></a>53 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L54"></a>54 | <code>    return [</code> | Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L55"></a>55 | <code>        state(row)</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L56"></a>56 | <code>        for row in session.scalars(</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L57"></a>57 | <code>            select(CallSession)</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L58"></a>58 | <code>            .where(CallSession.user_id == user.id)</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L59"></a>59 | <code>            .order_by(CallSession.started_at.desc())</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L60"></a>60 | <code>            .limit(limit)</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L61"></a>61 | <code>        )</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L62"></a>62 | <code>    ]</code> | Continua/fecha a instrução da linha 54. Retorna [state(row) for row in session.scalars(select(CallSession).where(CallSession.user_id == user.id).order_by(CallSession.started_at.desc()).limit(limit))] ao chamador e encerra este caminho da função. |
| <a id="L63"></a>63 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L64"></a>64 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L65"></a>65 | <code>@router.post(&quot;/incoming/{identifier}/{operation}&quot;)</code> | Aplica o decorator router.post(&quot;/incoming/{identifier}/{operation}&quot;) à definição que segue. |
| <a id="L66"></a>66 | <code># Documentação: Implementa incoming como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L67"></a>67 | <code>def incoming(</code> | Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L68"></a>68 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L69"></a>69 | <code>    operation: str,</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L70"></a>70 | <code>    data: DeviceAction,</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L71"></a>71 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L72"></a>72 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L73"></a>73 | <code>    credentials=Depends(bearer),</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L74"></a>74 | <code>):</code> | Continua/fecha a instrução da linha 67. Implementa incoming como parte do fluxo descrito para este arquivo. |
| <a id="L75"></a>75 | <code>    if operation not in {&quot;answer&quot;, &quot;reject&quot;}:</code> | Executa este ramo somente se operation not in {&#x27;answer&#x27;, &#x27;reject&#x27;}; caso contrário, segue o ramo alternativo. |
| <a id="L76"></a>76 | <code>        raise HTTPException(404, &quot;not_found&quot;)</code> | Interrompe este caminho lançando HTTPException(404, &#x27;not_found&#x27;). |
| <a id="L77"></a>77 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L78"></a>78 | <code>        service = bind(session, user, data, credentials)</code> | Define service com bind(session, user, data, credentials). Invoca bind com os argumentos declarados nesta instrução. Argumentos: session, user, data, credentials |
| <a id="L79"></a>79 | <code>        result = getattr(service, operation)(identifier)</code> | Define result com getattr(service, operation)(identifier). Invoca getattr(service, operation) com os argumentos declarados nesta instrução. Argumentos: identifier |
| <a id="L80"></a>80 | <code>        session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L81"></a>81 | <code>        return result</code> | Retorna result ao chamador e encerra este caminho da função. |
| <a id="L82"></a>82 | <code>    except AgentError as error:</code> | Trata exceção AgentError como error. |
| <a id="L83"></a>83 | <code>        session.rollback()</code> | Desfaz a transação atual antes de tratar a falha. |
| <a id="L84"></a>84 | <code>        raise HTTPException(error.status_code, error.code) from None</code> | Interrompe este caminho lançando HTTPException(error.status_code, error.code). |
| <a id="L85"></a>85 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L86"></a>86 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L87"></a>87 | <code>@router.post(&quot;/{identifier}/end&quot;)</code> | Aplica o decorator router.post(&quot;/{identifier}/end&quot;) à definição que segue. |
| <a id="L88"></a>88 | <code># Documentação: Implementa end como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L89"></a>89 | <code>def end(</code> | Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L90"></a>90 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 89. Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L91"></a>91 | <code>    data: DeviceAction,</code> | Continua/fecha a instrução da linha 89. Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L92"></a>92 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 89. Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L93"></a>93 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 89. Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L94"></a>94 | <code>    credentials=Depends(bearer),</code> | Continua/fecha a instrução da linha 89. Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L95"></a>95 | <code>):</code> | Continua/fecha a instrução da linha 89. Implementa end como parte do fluxo descrito para este arquivo. |
| <a id="L96"></a>96 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L97"></a>97 | <code>        result = bind(session, user, data, credentials).end(identifier)</code> | Define result com bind(session, user, data, credentials).end(identifier). Invoca bind(session, user, data, credentials).end com os argumentos declarados nesta instrução. Argumentos: identifier |
| <a id="L98"></a>98 | <code>        session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L99"></a>99 | <code>        return result</code> | Retorna result ao chamador e encerra este caminho da função. |
| <a id="L100"></a>100 | <code>    except AgentError as error:</code> | Trata exceção AgentError como error. |
| <a id="L101"></a>101 | <code>        session.rollback()</code> | Desfaz a transação atual antes de tratar a falha. |
| <a id="L102"></a>102 | <code>        raise HTTPException(error.status_code, error.code) from None</code> | Interrompe este caminho lançando HTTPException(error.status_code, error.code). |
| <a id="L103"></a>103 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L104"></a>104 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L105"></a>105 | <code>@router.post(&quot;/{identifier}/transcript&quot;)</code> | Aplica o decorator router.post(&quot;/{identifier}/transcript&quot;) à definição que segue. |
| <a id="L106"></a>106 | <code># Documentação: Implementa transcript como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L107"></a>107 | <code>def transcript(</code> | Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L108"></a>108 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 107. Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L109"></a>109 | <code>    data: Transcript,</code> | Continua/fecha a instrução da linha 107. Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L110"></a>110 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 107. Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L111"></a>111 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 107. Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L112"></a>112 | <code>    credentials=Depends(bearer),</code> | Continua/fecha a instrução da linha 107. Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L113"></a>113 | <code>):</code> | Continua/fecha a instrução da linha 107. Implementa transcript como parte do fluxo descrito para este arquivo. |
| <a id="L114"></a>114 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L115"></a>115 | <code>        conversation_id = bind(session, user, data, credentials).touch(identifier)</code> | Define conversation_id com bind(session, user, data, credentials).touch(identifier). Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. Invoca bind(session, user, data, credentials).touch com os argumentos declarados nesta instrução. Argumentos: identifier |
| <a id="L116"></a>116 | <code>        session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L117"></a>117 | <code>        return AgentCore(session, get_settings()).send(</code> | Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L118"></a>118 | <code>            user.id,</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L119"></a>119 | <code>            ChatSend(</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L120"></a>120 | <code>                conversation_id=conversation_id,</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L121"></a>121 | <code>                client_message_id=data.client_message_id,</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L122"></a>122 | <code>                content=data.content,</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L123"></a>123 | <code>            ),</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L124"></a>124 | <code>        )</code> | Continua/fecha a instrução da linha 117. Retorna AgentCore(session, get_settings()).send(user.id, ChatSend(conversation_id=conversation_id, client_message_id=data.client_message_id, content=data.content)) ao chamador e encerra este caminho da função. |
| <a id="L125"></a>125 | <code>    except (AgentError, LLMError) as error:</code> | Trata exceção (AgentError, LLMError) como error. |
| <a id="L126"></a>126 | <code>        session.rollback()</code> | Desfaz a transação atual antes de tratar a falha. |
| <a id="L127"></a>127 | <code>        raise HTTPException(getattr(error, &quot;status_code&quot;, 503), error.code) from None</code> | Interrompe este caminho lançando HTTPException(getattr(error, &#x27;status_code&#x27;, 503), error.code). |
