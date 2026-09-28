# android/build.gradle.kts

Declara plugins e versões compartilhadas do build Android, sem aplicá-los a módulos que não os usam.

[Arquivo fonte](../../../android/build.gradle.kts) · 5 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>plugins {</code> | Fornece a expressão plugins { ao bloco/chamada em construção. |
| <a id="L2"></a>2 | <code>    id(&quot;com.android.application&quot;) version &quot;8.13.2&quot; apply false</code> | Invoca/continua id com os argumentos declarados. |
| <a id="L3"></a>3 | <code>    id(&quot;org.jetbrains.kotlin.android&quot;) version &quot;2.3.10&quot; apply false</code> | Invoca/continua id com os argumentos declarados. |
| <a id="L4"></a>4 | <code>    id(&quot;org.jetbrains.kotlin.plugin.compose&quot;) version &quot;2.3.10&quot; apply false</code> | Invoca/continua id com os argumentos declarados. |
| <a id="L5"></a>5 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
