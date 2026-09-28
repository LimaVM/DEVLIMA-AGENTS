# backend/app/main.py

Constrói FastAPI, registra rotas/middlewares, padroniza erros e expõe liveness/readiness com verificação do banco e revisão do schema.

[Arquivo fonte](../../../../backend/app/main.py) · 100 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [lifespan](#L28) | Implementa lifespan como parte do fluxo descrito para este arquivo. |
| [create_app](#L34) | Cria create_app, segundo o contrato e as verificações deste módulo. |
| [create_app.request_id](#L48) | Executa a requisição de create_app.request_id, segundo o contrato e as verificações deste módulo. |
| [create_app.validation_error](#L58) | Implementa create_app.validation_error como parte do fluxo descrito para este arquivo. |
| [create_app.database_error](#L69) | Implementa create_app.database_error como parte do fluxo descrito para este arquivo. |
| [create_app.live](#L75) | Implementa create_app.live como parte do fluxo descrito para este arquivo. |
| [create_app.ready](#L80) | Implementa create_app.ready como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import logging</code> | Importa módulo(s) logging. |
| <a id="L2"></a>2 | <code>from contextlib import asynccontextmanager</code> | Importa asynccontextmanager de contextlib. |
| <a id="L3"></a>3 | <code>from uuid import uuid4</code> | Importa uuid4 de uuid. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L5"></a>5 | <code>from fastapi import FastAPI, Request</code> | Importa FastAPI, Request de fastapi. |
| <a id="L6"></a>6 | <code>from fastapi.exceptions import RequestValidationError</code> | Importa RequestValidationError de fastapi.exceptions. |
| <a id="L7"></a>7 | <code>from fastapi.responses import JSONResponse</code> | Importa JSONResponse de fastapi.responses. |
| <a id="L8"></a>8 | <code>from sqlalchemy import text</code> | Importa text de sqlalchemy. |
| <a id="L9"></a>9 | <code>from sqlalchemy.exc import SQLAlchemyError</code> | Importa SQLAlchemyError de sqlalchemy.exc. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L11"></a>11 | <code>from app.api.auth import router as auth_router</code> | Importa router de app.api.auth. |
| <a id="L12"></a>12 | <code>from app.api.calls import router as calls_router</code> | Importa router de app.api.calls. |
| <a id="L13"></a>13 | <code>from app.api.chat import router as chat_router</code> | Importa router de app.api.chat. |
| <a id="L14"></a>14 | <code>from app.api.devices import router as devices_router</code> | Importa router de app.api.devices. |
| <a id="L15"></a>15 | <code>from app.api.llm import router as llm_router</code> | Importa router de app.api.llm. |
| <a id="L16"></a>16 | <code>from app.api.memories import router as memories_router</code> | Importa router de app.api.memories. |
| <a id="L17"></a>17 | <code>from app.api.planning import router as planning_router</code> | Importa router de app.api.planning. |
| <a id="L18"></a>18 | <code>from app.api.websocket import router as websocket_router</code> | Importa router de app.api.websocket. |
| <a id="L19"></a>19 | <code>from app.api.workers import router as workers_router</code> | Importa router de app.api.workers. |
| <a id="L20"></a>20 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L21"></a>21 | <code>from app.db.session import get_engine</code> | Importa get_engine de app.db.session. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code>logger = logging.getLogger(&quot;devlima&quot;)</code> | Define logger com logging.getLogger(&#x27;devlima&#x27;). Invoca logging.getLogger com os argumentos declarados nesta instrução. Argumentos: &#x27;devlima&#x27; |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L26"></a>26 | <code>@asynccontextmanager</code> | Aplica o decorator asynccontextmanager à definição que segue. |
| <a id="L27"></a>27 | <code># Documentação: Implementa lifespan como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa lifespan como parte do fluxo descrito para este arquivo. |
| <a id="L28"></a>28 | <code>async def lifespan(app: FastAPI):</code> | Implementa lifespan como parte do fluxo descrito para este arquivo. |
| <a id="L29"></a>29 | <code>    yield</code> | Avalia a expressão (yield). |
| <a id="L30"></a>30 | <code>    get_engine().dispose()</code> | Invoca get_engine().dispose com os argumentos declarados nesta instrução. |
| <a id="L31"></a>31 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L32"></a>32 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L33"></a>33 | <code># Documentação: Cria create_app, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria create_app, segundo o contrato e as verificações deste módulo. |
| <a id="L34"></a>34 | <code>def create_app() -&gt; FastAPI:</code> | Cria create_app, segundo o contrato e as verificações deste módulo. |
| <a id="L35"></a>35 | <code>    settings = get_settings()</code> | Define settings com get_settings(). Invoca get_settings com os argumentos declarados nesta instrução. |
| <a id="L36"></a>36 | <code>    app = FastAPI(</code> | Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L37"></a>37 | <code>        title=settings.app_name,</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L38"></a>38 | <code>        version=&quot;1.0.1&quot;,</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L39"></a>39 | <code>        lifespan=lifespan,</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L40"></a>40 | <code>        docs_url=&quot;/docs&quot; if settings.enable_api_docs else None,</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L41"></a>41 | <code>        redoc_url=None,</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L42"></a>42 | <code>        openapi_url=&quot;/openapi.json&quot; if settings.enable_api_docs else None,</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L43"></a>43 | <code>    )</code> | Continua/fecha a instrução da linha 36. Define app com FastAPI(title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if setti.... Invoca FastAPI com os argumentos declarados nesta instrução. Argumentos: title=settings.app_name, version=&#x27;1.0.1&#x27;, lifespan=lifespan, docs_url=&#x27;/docs&#x27; if settings.enable_api_docs else None, redoc_url=None, openapi_url=&#x27;/openapi.json&#x27; if settings.enable_api_docs else None |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code>    @app.middleware(&quot;http&quot;)</code> | Aplica o decorator app.middleware(&quot;http&quot;) à definição que segue. |
| <a id="L46"></a>46 | <code>    # Documentação: Executa a requisição de create_app.request_id, segundo o contrato e as</code> | Comentário: Documentação: Executa a requisição de create_app.request_id, segundo o contrato e as |
| <a id="L47"></a>47 | <code>    # verificações deste módulo.</code> | Comentário: verificações deste módulo. |
| <a id="L48"></a>48 | <code>    async def request_id(request: Request, call_next):</code> | Executa a requisição de create_app.request_id, segundo o contrato e as verificações deste módulo. |
| <a id="L49"></a>49 | <code>        request.state.request_id = str(uuid4())</code> | Define request.state.request_id com str(uuid4()). Invoca str com os argumentos declarados nesta instrução. Argumentos: uuid4() |
| <a id="L50"></a>50 | <code>        response = await call_next(request)</code> | Define response com await call_next(request). |
| <a id="L51"></a>51 | <code>        response.headers[&quot;X-Request-ID&quot;] = request.state.request_id</code> | Define response.headers[&#x27;X-Request-ID&#x27;] com request.state.request_id. |
| <a id="L52"></a>52 | <code>        response.headers[&quot;Cache-Control&quot;] = &quot;no-store&quot;</code> | Define response.headers[&#x27;Cache-Control&#x27;] com &#x27;no-store&#x27;. |
| <a id="L53"></a>53 | <code>        return response</code> | Retorna response ao chamador e encerra este caminho da função. |
| <a id="L54"></a>54 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L55"></a>55 | <code>    @app.exception_handler(RequestValidationError)</code> | Aplica o decorator app.exception_handler(RequestValidationError) à definição que segue. |
| <a id="L56"></a>56 | <code>    # Documentação: Implementa create_app.validation_error como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa create_app.validation_error como parte do fluxo descrito para este |
| <a id="L57"></a>57 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L58"></a>58 | <code>    async def validation_error(request: Request, error: RequestValidationError):</code> | Implementa create_app.validation_error como parte do fluxo descrito para este arquivo. |
| <a id="L59"></a>59 | <code>        # FastAPI&#x27;s default includes rejected input, which can contain passwords.</code> | Comentário: FastAPI&#x27;s default includes rejected input, which can contain passwords. |
| <a id="L60"></a>60 | <code>        errors = [</code> | Define errors com [{&#x27;loc&#x27;: item[&#x27;loc&#x27;], &#x27;msg&#x27;: item[&#x27;msg&#x27;], &#x27;type&#x27;: item[&#x27;type&#x27;]} for item in error.errors()]. |
| <a id="L61"></a>61 | <code>            {&quot;loc&quot;: item[&quot;loc&quot;], &quot;msg&quot;: item[&quot;msg&quot;], &quot;type&quot;: item[&quot;type&quot;]}</code> | Continua/fecha a instrução da linha 60. Define errors com [{&#x27;loc&#x27;: item[&#x27;loc&#x27;], &#x27;msg&#x27;: item[&#x27;msg&#x27;], &#x27;type&#x27;: item[&#x27;type&#x27;]} for item in error.errors()]. |
| <a id="L62"></a>62 | <code>            for item in error.errors()</code> | Continua/fecha a instrução da linha 60. Define errors com [{&#x27;loc&#x27;: item[&#x27;loc&#x27;], &#x27;msg&#x27;: item[&#x27;msg&#x27;], &#x27;type&#x27;: item[&#x27;type&#x27;]} for item in error.errors()]. |
| <a id="L63"></a>63 | <code>        ]</code> | Continua/fecha a instrução da linha 60. Define errors com [{&#x27;loc&#x27;: item[&#x27;loc&#x27;], &#x27;msg&#x27;: item[&#x27;msg&#x27;], &#x27;type&#x27;: item[&#x27;type&#x27;]} for item in error.errors()]. |
| <a id="L64"></a>64 | <code>        return JSONResponse(status_code=422, content={&quot;detail&quot;: errors})</code> | Retorna JSONResponse(status_code=422, content={&#x27;detail&#x27;: errors}) ao chamador e encerra este caminho da função. |
| <a id="L65"></a>65 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L66"></a>66 | <code>    @app.exception_handler(SQLAlchemyError)</code> | Aplica o decorator app.exception_handler(SQLAlchemyError) à definição que segue. |
| <a id="L67"></a>67 | <code>    # Documentação: Implementa create_app.database_error como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa create_app.database_error como parte do fluxo descrito para este |
| <a id="L68"></a>68 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L69"></a>69 | <code>    async def database_error(request: Request, error: SQLAlchemyError):</code> | Implementa create_app.database_error como parte do fluxo descrito para este arquivo. |
| <a id="L70"></a>70 | <code>        logger.error(&quot;Database failure request_id=%s&quot;, request.state.request_id)</code> | Invoca logger.error com os argumentos declarados nesta instrução. Argumentos: &#x27;Database failure request_id=%s&#x27;, request.state.request_id |
| <a id="L71"></a>71 | <code>        return JSONResponse(status_code=503, content={&quot;detail&quot;: &quot;Banco indisponível&quot;})</code> | Retorna JSONResponse(status_code=503, content={&#x27;detail&#x27;: &#x27;Banco indisponível&#x27;}) ao chamador e encerra este caminho da função. |
| <a id="L72"></a>72 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L73"></a>73 | <code>    @app.get(&quot;/health/live&quot;, tags=[&quot;health&quot;])</code> | Aplica o decorator app.get(&quot;/health/live&quot;, tags=[&quot;health&quot;]) à definição que segue. |
| <a id="L74"></a>74 | <code>    # Documentação: Implementa create_app.live como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa create_app.live como parte do fluxo descrito para este arquivo. |
| <a id="L75"></a>75 | <code>    def live():</code> | Implementa create_app.live como parte do fluxo descrito para este arquivo. |
| <a id="L76"></a>76 | <code>        return {&quot;status&quot;: &quot;ok&quot;, &quot;phase&quot;: 9}</code> | Retorna {&#x27;status&#x27;: &#x27;ok&#x27;, &#x27;phase&#x27;: 9} ao chamador e encerra este caminho da função. |
| <a id="L77"></a>77 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L78"></a>78 | <code>    @app.get(&quot;/health/ready&quot;, tags=[&quot;health&quot;])</code> | Aplica o decorator app.get(&quot;/health/ready&quot;, tags=[&quot;health&quot;]) à definição que segue. |
| <a id="L79"></a>79 | <code>    # Documentação: Implementa create_app.ready como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa create_app.ready como parte do fluxo descrito para este arquivo. |
| <a id="L80"></a>80 | <code>    def ready():</code> | Implementa create_app.ready como parte do fluxo descrito para este arquivo. |
| <a id="L81"></a>81 | <code>        with get_engine().connect() as connection:</code> | Abre contexto(s) get_engine().connect(); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L82"></a>82 | <code>            connection.execute(text(&quot;SELECT 1&quot;))</code> | Invoca execute; o receptor e os argumentos abaixo determinam SQL ou operação permitida. Argumentos: text(&#x27;SELECT 1&#x27;) |
| <a id="L83"></a>83 | <code>            revision = connection.execute(text(&quot;SELECT version_num FROM alembic_version&quot;)).scalar()</code> | Define revision com connection.execute(text(&#x27;SELECT version_num FROM alembic_version&#x27;)).scalar(). Invoca connection.execute(text(&#x27;SELECT version_num FROM alembic_version&#x27;)).scalar com os argumentos declarados nesta instrução. |
| <a id="L84"></a>84 | <code>        if revision != &quot;0007_calls&quot;:</code> | Executa este ramo somente se revision != &#x27;0007_calls&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L85"></a>85 | <code>            return JSONResponse(status_code=503, content={&quot;status&quot;: &quot;schema_not_ready&quot;})</code> | Retorna JSONResponse(status_code=503, content={&#x27;status&#x27;: &#x27;schema_not_ready&#x27;}) ao chamador e encerra este caminho da função. |
| <a id="L86"></a>86 | <code>        return {&quot;status&quot;: &quot;ready&quot;, &quot;database&quot;: &quot;ok&quot;, &quot;schema&quot;: revision}</code> | Retorna {&#x27;status&#x27;: &#x27;ready&#x27;, &#x27;database&#x27;: &#x27;ok&#x27;, &#x27;schema&#x27;: revision} ao chamador e encerra este caminho da função. |
| <a id="L87"></a>87 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L88"></a>88 | <code>    app.include_router(calls_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: calls_router |
| <a id="L89"></a>89 | <code>    app.include_router(auth_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: auth_router |
| <a id="L90"></a>90 | <code>    app.include_router(llm_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: llm_router |
| <a id="L91"></a>91 | <code>    app.include_router(chat_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: chat_router |
| <a id="L92"></a>92 | <code>    app.include_router(memories_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: memories_router |
| <a id="L93"></a>93 | <code>    app.include_router(planning_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: planning_router |
| <a id="L94"></a>94 | <code>    app.include_router(workers_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: workers_router |
| <a id="L95"></a>95 | <code>    app.include_router(devices_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: devices_router |
| <a id="L96"></a>96 | <code>    app.include_router(websocket_router)</code> | Invoca app.include_router com os argumentos declarados nesta instrução. Argumentos: websocket_router |
| <a id="L97"></a>97 | <code>    return app</code> | Retorna app ao chamador e encerra este caminho da função. |
| <a id="L98"></a>98 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L99"></a>99 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L100"></a>100 | <code>app = create_app()</code> | Define app com create_app(). Invoca create_app com os argumentos declarados nesta instrução. |
