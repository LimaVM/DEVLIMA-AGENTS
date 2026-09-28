# android/gradle.properties

Define memória e comportamento de Gradle/Kotlin/Android para compilação reproduzível dentro dos limites da VPS.

[Arquivo fonte](../../../android/gradle.properties) · 5 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>org.gradle.jvmargs=-Xmx3g -Dfile.encoding=UTF-8</code> | Define a opção org.gradle.jvmargs do build/ferramenta. |
| <a id="L2"></a>2 | <code>org.gradle.workers.max=2</code> | Define a opção org.gradle.workers.max do build/ferramenta. |
| <a id="L3"></a>3 | <code>org.gradle.parallel=false</code> | Define a opção org.gradle.parallel do build/ferramenta. |
| <a id="L4"></a>4 | <code>android.useAndroidX=true</code> | Define a opção android.useAndroidX do build/ferramenta. |
| <a id="L5"></a>5 | <code>kotlin.code.style=official</code> | Define a opção kotlin.code.style do build/ferramenta. |
