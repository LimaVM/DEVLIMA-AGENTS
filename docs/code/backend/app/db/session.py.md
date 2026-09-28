# backend/app/db/session.py

Cria engine e sessões SQLAlchemy com timeouts, pool limitado, parâmetros ocultos e encerramento da sessão pela dependência FastAPI.

[Arquivo fonte](../../../../../backend/app/db/session.py) · 27 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [get_engine](#L12) | Cria e reutiliza engine PostgreSQL com pool/timeouts e parâmetros SQL ocultos. |
| [get_session](#L25) | Entrega sessão à rota e a fecha ao terminar o contexto da requisição. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from collections.abc import Generator</code> | Importa Generator de collections.abc. |
| <a id="L2"></a>2 | <code>from functools import lru_cache</code> | Importa lru_cache de functools. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from sqlalchemy import Engine, create_engine</code> | Importa Engine, create_engine de sqlalchemy. |
| <a id="L5"></a>5 | <code>from sqlalchemy.orm import Session, sessionmaker</code> | Importa Session, sessionmaker de sqlalchemy.orm. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code>@lru_cache</code> | Aplica o decorator lru_cache à definição que segue. |
| <a id="L11"></a>11 | <code># Documentação: Cria e reutiliza engine PostgreSQL com pool/timeouts e parâmetros SQL ocultos.</code> | Comentário: Documentação: Cria e reutiliza engine PostgreSQL com pool/timeouts e parâmetros SQL ocultos. |
| <a id="L12"></a>12 | <code>def get_engine() -&gt; Engine:</code> | Cria e reutiliza engine PostgreSQL com pool/timeouts e parâmetros SQL ocultos. |
| <a id="L13"></a>13 | <code>    return create_engine(</code> | Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L14"></a>14 | <code>        get_settings().database_url,</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L15"></a>15 | <code>        pool_pre_ping=True,</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L16"></a>16 | <code>        pool_size=5,</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L17"></a>17 | <code>        max_overflow=5,</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L18"></a>18 | <code>        pool_timeout=5,</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L19"></a>19 | <code>        connect_args={&quot;connect_timeout&quot;: 5, &quot;options&quot;: &quot;-c statement_timeout=10000&quot;},</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L20"></a>20 | <code>        hide_parameters=True,</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L21"></a>21 | <code>    )</code> | Continua/fecha a instrução da linha 13. Retorna create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_timeout=5, connect_args={&#x27;connect_timeout&#x27;: 5, &#x27;options&#x27;: &#x27;-c statement_timeout=... ao chamador e encerra este caminho da função. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code># Documentação: Entrega sessão à rota e a fecha ao terminar o contexto da requisição.</code> | Comentário: Documentação: Entrega sessão à rota e a fecha ao terminar o contexto da requisição. |
| <a id="L25"></a>25 | <code>def get_session() -&gt; Generator[Session, None, None]:</code> | Entrega sessão à rota e a fecha ao terminar o contexto da requisição. |
| <a id="L26"></a>26 | <code>    with sessionmaker(bind=get_engine(), expire_on_commit=False)() as session:</code> | Abre contexto(s) sessionmaker(bind=get_engine(), expire_on_commit=False)(); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L27"></a>27 | <code>        yield session</code> | Avalia a expressão (yield session). |
