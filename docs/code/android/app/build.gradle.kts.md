# android/app/build.gradle.kts

Configura SDK, versões, variantes debug/release, dependências e assinatura externa na VPS. A senha/keystore de assinatura não é embutida no script.

[Arquivo fonte](../../../../android/app/build.gradle.kts) · 72 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import java.util.Properties</code> | Disponibiliza o símbolo Kotlin/Android java.util.Properties neste arquivo. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>plugins {</code> | Fornece a expressão plugins { ao bloco/chamada em construção. |
| <a id="L4"></a>4 | <code>    id(&quot;com.android.application&quot;)</code> | Invoca/continua id com os argumentos declarados. |
| <a id="L5"></a>5 | <code>    id(&quot;org.jetbrains.kotlin.android&quot;)</code> | Invoca/continua id com os argumentos declarados. |
| <a id="L6"></a>6 | <code>    id(&quot;org.jetbrains.kotlin.plugin.compose&quot;)</code> | Invoca/continua id com os argumentos declarados. |
| <a id="L7"></a>7 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L9"></a>9 | <code>android {</code> | Fornece a expressão android { ao bloco/chamada em construção. |
| <a id="L10"></a>10 | <code>    namespace = &quot;br.com.vegasolucoes.agent&quot;</code> | Fornece o valor de namespace no contexto desta expressão. |
| <a id="L11"></a>11 | <code>    compileSdk = 36</code> | Fornece o valor de compileSdk no contexto desta expressão. |
| <a id="L12"></a>12 | <code>    buildToolsVersion = &quot;36.0.0&quot;</code> | Fornece o valor de buildToolsVersion no contexto desta expressão. |
| <a id="L13"></a>13 | <code>    defaultConfig {</code> | Fornece a expressão defaultConfig { ao bloco/chamada em construção. |
| <a id="L14"></a>14 | <code>        applicationId = &quot;br.com.vegasolucoes.agent&quot;</code> | Fornece o valor de applicationId no contexto desta expressão. |
| <a id="L15"></a>15 | <code>        minSdk = 26</code> | Fornece o valor de minSdk no contexto desta expressão. |
| <a id="L16"></a>16 | <code>        targetSdk = 36</code> | Fornece o valor de targetSdk no contexto desta expressão. |
| <a id="L17"></a>17 | <code>        versionCode = 103</code> | Fornece o valor de versionCode no contexto desta expressão. |
| <a id="L18"></a>18 | <code>        versionName = &quot;1.0.3&quot;</code> | Fornece o valor de versionName no contexto desta expressão. |
| <a id="L19"></a>19 | <code>        testInstrumentationRunner = &quot;androidx.test.runner.AndroidJUnitRunner&quot;</code> | Fornece o valor de testInstrumentationRunner no contexto desta expressão. |
| <a id="L20"></a>20 | <code>        buildConfigField(&quot;String&quot;, &quot;DEFAULT_SERVER&quot;, &quot;\&quot;https://agent.vegasolucoes.com.br\&quot;&quot;)</code> | Invoca/continua buildConfigField com os argumentos declarados. |
| <a id="L21"></a>21 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L22"></a>22 | <code>    val signingFile = file(&quot;/srv/devlima-build-tools/signing.properties&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L23"></a>23 | <code>    if (signingFile.exists()) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L24"></a>24 | <code>        val values = Properties().apply { signingFile.inputStream().use { load(it) } }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L25"></a>25 | <code>        signingConfigs.create(&quot;production&quot;) {</code> | Invoca/continua signingConfigs.create com os argumentos declarados. |
| <a id="L26"></a>26 | <code>            storeFile = file(values.getProperty(&quot;storeFile&quot;))</code> | Invoca/continua file com os argumentos declarados. |
| <a id="L27"></a>27 | <code>            storePassword = values.getProperty(&quot;storePassword&quot;)</code> | Invoca/continua values.getProperty com os argumentos declarados. |
| <a id="L28"></a>28 | <code>            keyAlias = values.getProperty(&quot;keyAlias&quot;)</code> | Invoca/continua values.getProperty com os argumentos declarados. |
| <a id="L29"></a>29 | <code>            keyPassword = values.getProperty(&quot;keyPassword&quot;)</code> | Invoca/continua values.getProperty com os argumentos declarados. |
| <a id="L30"></a>30 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L31"></a>31 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L32"></a>32 | <code>    buildTypes {</code> | Fornece a expressão buildTypes { ao bloco/chamada em construção. |
| <a id="L33"></a>33 | <code>        debug {</code> | Fornece a expressão debug { ao bloco/chamada em construção. |
| <a id="L34"></a>34 | <code>            applicationIdSuffix = &quot;.debug&quot;</code> | Fornece o valor de applicationIdSuffix no contexto desta expressão. |
| <a id="L35"></a>35 | <code>            versionNameSuffix = &quot;-debug&quot;</code> | Fornece o valor de versionNameSuffix no contexto desta expressão. |
| <a id="L36"></a>36 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L37"></a>37 | <code>        release {</code> | Fornece a expressão release { ao bloco/chamada em construção. |
| <a id="L38"></a>38 | <code>            isMinifyEnabled = false</code> | Fornece o valor de isMinifyEnabled no contexto desta expressão. |
| <a id="L39"></a>39 | <code>            if (signingFile.exists()) signingConfig = signingConfigs.getByName(&quot;production&quot;)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L40"></a>40 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L41"></a>41 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L42"></a>42 | <code>    compileOptions {</code> | Fornece a expressão compileOptions { ao bloco/chamada em construção. |
| <a id="L43"></a>43 | <code>        sourceCompatibility = JavaVersion.VERSION_17</code> | Fornece o valor de sourceCompatibility no contexto desta expressão. |
| <a id="L44"></a>44 | <code>        targetCompatibility = JavaVersion.VERSION_17</code> | Fornece o valor de targetCompatibility no contexto desta expressão. |
| <a id="L45"></a>45 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L46"></a>46 | <code>    buildFeatures {</code> | Fornece a expressão buildFeatures { ao bloco/chamada em construção. |
| <a id="L47"></a>47 | <code>        compose = true</code> | Fornece o valor de compose no contexto desta expressão. |
| <a id="L48"></a>48 | <code>        buildConfig = true</code> | Fornece o valor de buildConfig no contexto desta expressão. |
| <a id="L49"></a>49 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L50"></a>50 | <code>    packaging { resources.excludes += &quot;/META-INF/{AL2.0,LGPL2.1}&quot; }</code> | Fornece a expressão packaging { resources.excludes += &quot;/META-INF/{AL2.0,LGPL2.1}&quot; } ao bloco/chamada em construção. |
| <a id="L51"></a>51 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L52"></a>52 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L53"></a>53 | <code>kotlin { compilerOptions { jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17) } }</code> | Invoca/continua jvmTarget.set com os argumentos declarados. |
| <a id="L54"></a>54 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L55"></a>55 | <code>dependencies {</code> | Fornece a expressão dependencies { ao bloco/chamada em construção. |
| <a id="L56"></a>56 | <code>    implementation(platform(&quot;androidx.compose:compose-bom:2026.02.01&quot;))</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L57"></a>57 | <code>    implementation(&quot;androidx.activity:activity-compose:1.12.4&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L58"></a>58 | <code>    implementation(&quot;androidx.core:core-ktx:1.17.0&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L59"></a>59 | <code>    implementation(&quot;androidx.lifecycle:lifecycle-runtime-ktx:2.10.0&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L60"></a>60 | <code>    implementation(&quot;androidx.lifecycle:lifecycle-runtime-compose:2.10.0&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L61"></a>61 | <code>    implementation(&quot;androidx.compose.ui:ui&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L62"></a>62 | <code>    implementation(&quot;androidx.compose.foundation:foundation&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L63"></a>63 | <code>    implementation(&quot;androidx.compose.material3:material3&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L64"></a>64 | <code>    implementation(&quot;com.squareup.okhttp3:okhttp:4.12.0&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L65"></a>65 | <code>    implementation(&quot;org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2&quot;)</code> | Invoca/continua implementation com os argumentos declarados. |
| <a id="L66"></a>66 | <code>    testImplementation(&quot;junit:junit:4.13.2&quot;)</code> | Invoca/continua testImplementation com os argumentos declarados. |
| <a id="L67"></a>67 | <code>    androidTestImplementation(&quot;androidx.test:runner:1.7.0&quot;)</code> | Invoca/continua androidTestImplementation com os argumentos declarados. |
| <a id="L68"></a>68 | <code>    androidTestImplementation(&quot;androidx.test.ext:junit:1.3.0&quot;)</code> | Invoca/continua androidTestImplementation com os argumentos declarados. |
| <a id="L69"></a>69 | <code>    androidTestImplementation(platform(&quot;androidx.compose:compose-bom:2026.02.01&quot;))</code> | Invoca/continua androidTestImplementation com os argumentos declarados. |
| <a id="L70"></a>70 | <code>    androidTestImplementation(&quot;androidx.compose.ui:ui-test-junit4&quot;)</code> | Invoca/continua androidTestImplementation com os argumentos declarados. |
| <a id="L71"></a>71 | <code>    debugImplementation(&quot;androidx.compose.ui:ui-test-manifest&quot;)</code> | Invoca/continua debugImplementation com os argumentos declarados. |
| <a id="L72"></a>72 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
