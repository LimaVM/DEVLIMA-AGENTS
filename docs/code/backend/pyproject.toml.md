# backend/pyproject.toml

Configura pytest/Ruff e as regras do projeto Python; não contém os valores privados de configuração do serviço.

[Arquivo fonte](../../../backend/pyproject.toml) · 15 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>[tool.pytest.ini_options]</code> | Abre seção/tabela [tool.pytest.ini_options]. |
| <a id="L2"></a>2 | <code>testpaths = [&quot;tests&quot;]</code> | Define a opção testpaths do build/ferramenta. |
| <a id="L3"></a>3 | <code>pythonpath = [&quot;.&quot;]</code> | Define a opção pythonpath do build/ferramenta. |
| <a id="L4"></a>4 | <code>filterwarnings = [&quot;error&quot;]</code> | Define a opção filterwarnings do build/ferramenta. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L6"></a>6 | <code>[tool.ruff]</code> | Abre seção/tabela [tool.ruff]. |
| <a id="L7"></a>7 | <code>target-version = &quot;py312&quot;</code> | Define a opção target-version do build/ferramenta. |
| <a id="L8"></a>8 | <code>line-length = 100</code> | Define a opção line-length do build/ferramenta. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L10"></a>10 | <code>[tool.ruff.lint]</code> | Abre seção/tabela [tool.ruff.lint]. |
| <a id="L11"></a>11 | <code>select = [&quot;E&quot;, &quot;F&quot;, &quot;I&quot;, &quot;UP&quot;, &quot;B&quot;]</code> | Define a opção select do build/ferramenta. |
| <a id="L12"></a>12 | <code>ignore = [&quot;B008&quot;]</code> | Define a opção ignore do build/ferramenta. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L14"></a>14 | <code>[tool.ruff.lint.isort]</code> | Abre seção/tabela [tool.ruff.lint.isort]. |
| <a id="L15"></a>15 | <code>known-first-party = [&quot;app&quot;, &quot;vm_manager&quot;]</code> | Define a opção known-first-party do build/ferramenta. |
