# backend/app/api/llm.py

Oferece diagnóstico e chat de inferência autenticados por meio do router; a rota não dá acesso arbitrário ao host.

[Arquivo fonte](../../../../../backend/app/api/llm.py) · 54 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [health](#L19) | Implementa health como parte do fluxo descrito para este arquivo. |
| [chat](#L30) | Implementa chat como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>from fastapi import APIRouter, Depends, HTTPException, Request</code> | Importa APIRouter, Depends, HTTPException, Request de fastapi. |
| <a id="L4"></a>4 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>from app.config import Settings, get_settings</code> | Importa Settings, get_settings de app.config. |
| <a id="L7"></a>7 | <code>from app.db.session import get_session</code> | Importa get_session de app.db.session. |
| <a id="L8"></a>8 | <code>from app.llm.base import LLMError</code> | Importa LLMError de app.llm.base. |
| <a id="L9"></a>9 | <code>from app.llm.service import build_router</code> | Importa build_router de app.llm.service. |
| <a id="L10"></a>10 | <code>from app.models import User</code> | Importa User de app.models. |
| <a id="L11"></a>11 | <code>from app.schemas.llm import LLMChatRequest, LLMChatResponse</code> | Importa LLMChatRequest, LLMChatResponse de app.schemas.llm. |
| <a id="L12"></a>12 | <code>from app.security import get_current_user</code> | Importa get_current_user de app.security. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>router = APIRouter(prefix=&quot;/llm&quot;, tags=[&quot;llm&quot;])</code> | Define router com APIRouter(prefix=&#x27;/llm&#x27;, tags=[&#x27;llm&#x27;]). Invoca APIRouter com os argumentos declarados nesta instrução. Argumentos: prefix=&#x27;/llm&#x27;, tags=[&#x27;llm&#x27;] |
| <a id="L15"></a>15 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L17"></a>17 | <code>@router.get(&quot;/health&quot;)</code> | Aplica o decorator router.get(&quot;/health&quot;) à definição que segue. |
| <a id="L18"></a>18 | <code># Documentação: Implementa health como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa health como parte do fluxo descrito para este arquivo. |
| <a id="L19"></a>19 | <code>def health(</code> | Implementa health como parte do fluxo descrito para este arquivo. |
| <a id="L20"></a>20 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 19. Implementa health como parte do fluxo descrito para este arquivo. |
| <a id="L21"></a>21 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 19. Implementa health como parte do fluxo descrito para este arquivo. |
| <a id="L22"></a>22 | <code>    settings: Settings = Depends(get_settings),</code> | Continua/fecha a instrução da linha 19. Implementa health como parte do fluxo descrito para este arquivo. |
| <a id="L23"></a>23 | <code>):</code> | Continua/fecha a instrução da linha 19. Implementa health como parte do fluxo descrito para este arquivo. |
| <a id="L24"></a>24 | <code>    with build_router(settings, session) as llm:</code> | Abre contexto(s) build_router(settings, session); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L25"></a>25 | <code>        return llm.health_check()</code> | Retorna llm.health_check() ao chamador e encerra este caminho da função. |
| <a id="L26"></a>26 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L27"></a>27 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L28"></a>28 | <code>@router.post(&quot;/chat&quot;, response_model=LLMChatResponse)</code> | Aplica o decorator router.post(&quot;/chat&quot;, response_model=LLMChatResponse) à definição que segue. |
| <a id="L29"></a>29 | <code># Documentação: Implementa chat como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L30"></a>30 | <code>def chat(</code> | Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L31"></a>31 | <code>    data: LLMChatRequest,</code> | Continua/fecha a instrução da linha 30. Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L32"></a>32 | <code>    request: Request,</code> | Continua/fecha a instrução da linha 30. Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L33"></a>33 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 30. Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L34"></a>34 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 30. Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L35"></a>35 | <code>    settings: Settings = Depends(get_settings),</code> | Continua/fecha a instrução da linha 30. Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L36"></a>36 | <code>) -&gt; LLMChatResponse:</code> | Continua/fecha a instrução da linha 30. Implementa chat como parte do fluxo descrito para este arquivo. |
| <a id="L37"></a>37 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L38"></a>38 | <code>        with build_router(settings, session) as llm:</code> | Abre contexto(s) build_router(settings, session); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L39"></a>39 | <code>            result = llm.chat(</code> | Define result com llm.chat(data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id |
| <a id="L40"></a>40 | <code>                data.messages,</code> | Continua/fecha a instrução da linha 39. Define result com llm.chat(data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id |
| <a id="L41"></a>41 | <code>                max_tokens=data.max_tokens,</code> | Continua/fecha a instrução da linha 39. Define result com llm.chat(data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id |
| <a id="L42"></a>42 | <code>                request_id=UUID(request.state.request_id),</code> | Continua/fecha a instrução da linha 39. Define result com llm.chat(data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id |
| <a id="L43"></a>43 | <code>                user_id=user.id,</code> | Continua/fecha a instrução da linha 39. Define result com llm.chat(data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id |
| <a id="L44"></a>44 | <code>            )</code> | Continua/fecha a instrução da linha 39. Define result com llm.chat(data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: data.messages, max_tokens=data.max_tokens, request_id=UUID(request.state.request_id), user_id=user.id |
| <a id="L45"></a>45 | <code>    except LLMError as error:</code> | Trata exceção LLMError como error. |
| <a id="L46"></a>46 | <code>        raise HTTPException(status_code=503, detail={&quot;code&quot;: error.code}) from None</code> | Interrompe este caminho lançando HTTPException(status_code=503, detail={&#x27;code&#x27;: error.code}). |
| <a id="L47"></a>47 | <code>    return LLMChatResponse(</code> | Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L48"></a>48 | <code>        request_id=result.request_id,</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L49"></a>49 | <code>        reply=result.completion.content,</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L50"></a>50 | <code>        provider=result.completion.provider,</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L51"></a>51 | <code>        model=result.completion.model,</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L52"></a>52 | <code>        fallback_used=result.fallback_used,</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L53"></a>53 | <code>        latency_ms=result.latency_ms,</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
| <a id="L54"></a>54 | <code>    )</code> | Continua/fecha a instrução da linha 47. Retorna LLMChatResponse(request_id=result.request_id, reply=result.completion.content, provider=result.completion.provider, model=result.completion.model, fallback_used=result.fallback_... ao chamador e encerra este caminho da função. |
