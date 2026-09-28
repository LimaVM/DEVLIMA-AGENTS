# vm-manager/systemd/devlima-worker-egress.xml

Define filtro libvirt de egress para workers, incluindo restrições de destinos privados/metadata; não altera a rede default existente por si só.

[Arquivo fonte](../../../../vm-manager/systemd/devlima-worker-egress.xml) · 18 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>&lt;filter name=&#x27;devlima-worker-egress&#x27;&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L2"></a>2 | <code>  &lt;filterref filter=&#x27;clean-traffic&#x27;/&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L3"></a>3 | <code>  &lt;rule action=&#x27;accept&#x27; direction=&#x27;out&#x27; priority=&#x27;600&#x27;&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L4"></a>4 | <code>    &lt;udp dstipaddr=&#x27;192.168.122.1&#x27; dstportstart=&#x27;53&#x27; state=&#x27;NEW&#x27;/&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L5"></a>5 | <code>  &lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L6"></a>6 | <code>  &lt;rule action=&#x27;accept&#x27; direction=&#x27;out&#x27; priority=&#x27;600&#x27;&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L7"></a>7 | <code>    &lt;tcp dstipaddr=&#x27;192.168.122.1&#x27; dstportstart=&#x27;53&#x27; state=&#x27;NEW&#x27;/&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L8"></a>8 | <code>  &lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L9"></a>9 | <code>  &lt;rule action=&#x27;accept&#x27; direction=&#x27;out&#x27; priority=&#x27;600&#x27;&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L10"></a>10 | <code>    &lt;udp srcportstart=&#x27;68&#x27; dstportstart=&#x27;67&#x27; state=&#x27;NEW&#x27;/&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L11"></a>11 | <code>  &lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L12"></a>12 | <code>  &lt;rule action=&#x27;drop&#x27; direction=&#x27;out&#x27; priority=&#x27;700&#x27;&gt;&lt;all dstipaddr=&#x27;10.0.0.0&#x27; dstipmask=&#x27;8&#x27; state=&#x27;NEW&#x27;/&gt;&lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L13"></a>13 | <code>  &lt;rule action=&#x27;drop&#x27; direction=&#x27;out&#x27; priority=&#x27;700&#x27;&gt;&lt;all dstipaddr=&#x27;172.16.0.0&#x27; dstipmask=&#x27;12&#x27; state=&#x27;NEW&#x27;/&gt;&lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L14"></a>14 | <code>  &lt;rule action=&#x27;drop&#x27; direction=&#x27;out&#x27; priority=&#x27;700&#x27;&gt;&lt;all dstipaddr=&#x27;192.168.0.0&#x27; dstipmask=&#x27;16&#x27; state=&#x27;NEW&#x27;/&gt;&lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L15"></a>15 | <code>  &lt;rule action=&#x27;drop&#x27; direction=&#x27;out&#x27; priority=&#x27;700&#x27;&gt;&lt;all dstipaddr=&#x27;100.64.0.0&#x27; dstipmask=&#x27;10&#x27; state=&#x27;NEW&#x27;/&gt;&lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L16"></a>16 | <code>  &lt;rule action=&#x27;drop&#x27; direction=&#x27;out&#x27; priority=&#x27;700&#x27;&gt;&lt;all dstipaddr=&#x27;169.254.0.0&#x27; dstipmask=&#x27;16&#x27; state=&#x27;NEW&#x27;/&gt;&lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L17"></a>17 | <code>  &lt;rule action=&#x27;drop&#x27; direction=&#x27;out&#x27; priority=&#x27;700&#x27;&gt;&lt;all dstipaddr=&#x27;147.15.33.140&#x27; dstipmask=&#x27;32&#x27; state=&#x27;NEW&#x27;/&gt;&lt;/rule&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
| <a id="L18"></a>18 | <code>&lt;/filter&gt;</code> | Declara elemento/atributo XML conforme o schema do componente indicado no contexto. |
