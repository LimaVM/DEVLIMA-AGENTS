# backend/alembic.ini

Configura localização e logging do Alembic; a conexão real é obtida da configuração Python, sem senha versionada.

[Arquivo fonte](../../../backend/alembic.ini) · 30 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>[alembic]</code> | Abre seção/tabela [alembic]. |
| <a id="L2"></a>2 | <code>script_location = migrations</code> | Define a opção script_location do build/ferramenta. |
| <a id="L3"></a>3 | <code>prepend_sys_path = .</code> | Define a opção prepend_sys_path do build/ferramenta. |
| <a id="L4"></a>4 | <code>path_separator = os</code> | Define a opção path_separator do build/ferramenta. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L6"></a>6 | <code>[loggers]</code> | Abre seção/tabela [loggers]. |
| <a id="L7"></a>7 | <code>keys = root,sqlalchemy,alembic</code> | Define a opção keys do build/ferramenta. |
| <a id="L8"></a>8 | <code>[handlers]</code> | Abre seção/tabela [handlers]. |
| <a id="L9"></a>9 | <code>keys = console</code> | Define a opção keys do build/ferramenta. |
| <a id="L10"></a>10 | <code>[formatters]</code> | Abre seção/tabela [formatters]. |
| <a id="L11"></a>11 | <code>keys = generic</code> | Define a opção keys do build/ferramenta. |
| <a id="L12"></a>12 | <code>[logger_root]</code> | Abre seção/tabela [logger_root]. |
| <a id="L13"></a>13 | <code>level = WARNING</code> | Define a opção level do build/ferramenta. |
| <a id="L14"></a>14 | <code>handlers = console</code> | Define a opção handlers do build/ferramenta. |
| <a id="L15"></a>15 | <code>qualname =</code> | Define a opção qualname do build/ferramenta. |
| <a id="L16"></a>16 | <code>[logger_sqlalchemy]</code> | Abre seção/tabela [logger_sqlalchemy]. |
| <a id="L17"></a>17 | <code>level = WARNING</code> | Define a opção level do build/ferramenta. |
| <a id="L18"></a>18 | <code>handlers =</code> | Define a opção handlers do build/ferramenta. |
| <a id="L19"></a>19 | <code>qualname = sqlalchemy.engine</code> | Define a opção qualname do build/ferramenta. |
| <a id="L20"></a>20 | <code>[logger_alembic]</code> | Abre seção/tabela [logger_alembic]. |
| <a id="L21"></a>21 | <code>level = INFO</code> | Define a opção level do build/ferramenta. |
| <a id="L22"></a>22 | <code>handlers =</code> | Define a opção handlers do build/ferramenta. |
| <a id="L23"></a>23 | <code>qualname = alembic</code> | Define a opção qualname do build/ferramenta. |
| <a id="L24"></a>24 | <code>[handler_console]</code> | Abre seção/tabela [handler_console]. |
| <a id="L25"></a>25 | <code>class = StreamHandler</code> | Define a opção class do build/ferramenta. |
| <a id="L26"></a>26 | <code>args = (sys.stderr,)</code> | Define a opção args do build/ferramenta. |
| <a id="L27"></a>27 | <code>level = NOTSET</code> | Define a opção level do build/ferramenta. |
| <a id="L28"></a>28 | <code>formatter = generic</code> | Define a opção formatter do build/ferramenta. |
| <a id="L29"></a>29 | <code>[formatter_generic]</code> | Abre seção/tabela [formatter_generic]. |
| <a id="L30"></a>30 | <code>format = %(levelname)-5.5s [%(name)s] %(message)s</code> | Define a opção format do build/ferramenta. |
