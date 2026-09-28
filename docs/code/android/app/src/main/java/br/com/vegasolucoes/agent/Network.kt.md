# android/app/src/main/java/br/com/vegasolucoes/agent/Network.kt

Normaliza servidor HTTPS, serializa renovação de sessão, chama API por OkHttp e conserva sessão cifrada sem persistir a senha de login.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/Network.kt) · 213 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [ApiFailure](#L18) | Define o tipo ApiFailure e reúne o estado/contrato descrito para este módulo. |
| [LoginRequired](#L21) | Define o tipo LoginRequired e reúne o estado/contrato descrito para este módulo. |
| [normalizedServer](#L25) | Aceita somente base HTTPS válida, sem credenciais/query/fragment e normaliza barra final. |
| [Backoff](#L43) | Define o tipo Backoff e reúne o estado/contrato descrito para este módulo. |
| [Backoff.reset](#L47) | Implementa Backoff.reset como parte do fluxo descrito para este arquivo. |
| [Backoff.nextDelay](#L52) | Implementa Backoff.nextDelay como parte do fluxo descrito para este arquivo. |
| [AuthRepository](#L60) | Define o tipo AuthRepository e reúne o estado/contrato descrito para este módulo. |
| [AuthRepository.request](#L73) | Executa a requisição de AuthRepository.request, segundo o contrato e as verificações deste módulo. |
| [AuthRepository.login](#L99) | Autentica, obtém identidade/timezone, associa cache ao proprietário e grava sessão cifrada. |
| [AuthRepository.access](#L138) | Renova token próximo da expiração sob mutex e exige login novamente somente para rejeição de autenticação. |
| [AuthRepository.invalidateAccess](#L175) | Implementa AuthRepository.invalidateAccess como parte do fluxo descrito para este arquivo. |
| [AuthRepository.api](#L187) | Executa HTTP autenticado e tenta renovação uma vez após rejeição do access token. |
| [AuthRepository.logout](#L201) | Tenta revogar a família no Core e remove sessão/dispositivo locais. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import java.util.concurrent.TimeUnit</code> | Disponibiliza o símbolo Kotlin/Android java.util.concurrent.TimeUnit neste arquivo. |
| <a id="L4"></a>4 | <code>import kotlin.random.Random</code> | Disponibiliza o símbolo Kotlin/Android kotlin.random.Random neste arquivo. |
| <a id="L5"></a>5 | <code>import kotlinx.coroutines.Dispatchers</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.Dispatchers neste arquivo. |
| <a id="L6"></a>6 | <code>import kotlinx.coroutines.flow.MutableStateFlow</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.flow.MutableStateFlow neste arquivo. |
| <a id="L7"></a>7 | <code>import kotlinx.coroutines.sync.Mutex</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.sync.Mutex neste arquivo. |
| <a id="L8"></a>8 | <code>import kotlinx.coroutines.sync.withLock</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.sync.withLock neste arquivo. Serializa esta seção para impedir renovação/alteração concorrente do estado. |
| <a id="L9"></a>9 | <code>import kotlinx.coroutines.withContext</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.withContext neste arquivo. Executa trabalho no dispatcher declarado sem bloquear o chamador de UI. |
| <a id="L10"></a>10 | <code>import okhttp3.HttpUrl.Companion.toHttpUrlOrNull</code> | Disponibiliza o símbolo Kotlin/Android okhttp3.HttpUrl.Companion.toHttpUrlOrNull neste arquivo. |
| <a id="L11"></a>11 | <code>import okhttp3.MediaType.Companion.toMediaType</code> | Disponibiliza o símbolo Kotlin/Android okhttp3.MediaType.Companion.toMediaType neste arquivo. |
| <a id="L12"></a>12 | <code>import okhttp3.OkHttpClient</code> | Disponibiliza o símbolo Kotlin/Android okhttp3.OkHttpClient neste arquivo. |
| <a id="L13"></a>13 | <code>import okhttp3.Request</code> | Disponibiliza o símbolo Kotlin/Android okhttp3.Request neste arquivo. |
| <a id="L14"></a>14 | <code>import okhttp3.RequestBody.Companion.toRequestBody</code> | Disponibiliza o símbolo Kotlin/Android okhttp3.RequestBody.Companion.toRequestBody neste arquivo. |
| <a id="L15"></a>15 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L17"></a>17 | <code>// Documentação: Define o tipo ApiFailure e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo ApiFailure e reúne o estado/contrato descrito para este módulo. |
| <a id="L18"></a>18 | <code>class ApiFailure(val status: Int, val code: String) : Exception(code)</code> | Define o tipo ApiFailure e reúne o estado/contrato descrito para este módulo. |
| <a id="L19"></a>19 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L20"></a>20 | <code>// Documentação: Define o tipo LoginRequired e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo LoginRequired e reúne o estado/contrato descrito para este módulo. |
| <a id="L21"></a>21 | <code>class LoginRequired : Exception(&quot;login_required&quot;)</code> | Define o tipo LoginRequired e reúne o estado/contrato descrito para este módulo. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L23"></a>23 | <code>// Documentação: Aceita somente base HTTPS válida, sem credenciais/query/fragment e normaliza</code> | Comentário de manutenção/documentação: Documentação: Aceita somente base HTTPS válida, sem credenciais/query/fragment e normaliza |
| <a id="L24"></a>24 | <code>// barra final.</code> | Comentário de manutenção/documentação: barra final. |
| <a id="L25"></a>25 | <code>fun normalizedServer(value: String): String {</code> | Aceita somente base HTTPS válida, sem credenciais/query/fragment e normaliza barra final. |
| <a id="L26"></a>26 | <code>    val url =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L27"></a>27 | <code>        value.trim().toHttpUrlOrNull()</code> | Invoca/continua value.trim com os argumentos declarados. |
| <a id="L28"></a>28 | <code>            ?: throw IllegalArgumentException(&quot;Informe uma URL HTTPS válida&quot;)</code> | Invoca/continua IllegalArgumentException com os argumentos declarados. |
| <a id="L29"></a>29 | <code>    require(</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L30"></a>30 | <code>        url.scheme == &quot;https&quot; &amp;&amp;</code> | Fornece a expressão url.scheme == &quot;https&quot; &amp;&amp; ao bloco/chamada em construção. |
| <a id="L31"></a>31 | <code>            url.username.isEmpty() &amp;&amp;</code> | Invoca/continua url.username.isEmpty com os argumentos declarados. |
| <a id="L32"></a>32 | <code>            url.password.isEmpty() &amp;&amp;</code> | Invoca/continua url.password.isEmpty com os argumentos declarados. |
| <a id="L33"></a>33 | <code>            url.query == null &amp;&amp;</code> | Fornece a expressão url.query == null &amp;&amp; ao bloco/chamada em construção. |
| <a id="L34"></a>34 | <code>            url.fragment == null &amp;&amp;</code> | Fornece a expressão url.fragment == null &amp;&amp; ao bloco/chamada em construção. |
| <a id="L35"></a>35 | <code>            url.encodedPath == &quot;/&quot;</code> | Fornece a expressão url.encodedPath == &quot;/&quot; ao bloco/chamada em construção. |
| <a id="L36"></a>36 | <code>    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L37"></a>37 | <code>        &quot;Use HTTPS e apenas o domínio, sem credenciais ou caminho&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L38"></a>38 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L39"></a>39 | <code>    return url.toString().removeSuffix(&quot;/&quot;)</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L40"></a>40 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L41"></a>41 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L42"></a>42 | <code>// Documentação: Define o tipo Backoff e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo Backoff e reúne o estado/contrato descrito para este módulo. |
| <a id="L43"></a>43 | <code>class Backoff {</code> | Define o tipo Backoff e reúne o estado/contrato descrito para este módulo. |
| <a id="L44"></a>44 | <code>    private var attempt = 0</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L45"></a>45 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L46"></a>46 | <code>    // Documentação: Implementa Backoff.reset como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa Backoff.reset como parte do fluxo descrito para este arquivo. |
| <a id="L47"></a>47 | <code>    fun reset() {</code> | Implementa Backoff.reset como parte do fluxo descrito para este arquivo. |
| <a id="L48"></a>48 | <code>        attempt = 0</code> | Fornece o valor de attempt no contexto desta expressão. |
| <a id="L49"></a>49 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L50"></a>50 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L51"></a>51 | <code>    // Documentação: Implementa Backoff.nextDelay como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa Backoff.nextDelay como parte do fluxo descrito para este arquivo. |
| <a id="L52"></a>52 | <code>    fun nextDelay(): Long {</code> | Implementa Backoff.nextDelay como parte do fluxo descrito para este arquivo. |
| <a id="L53"></a>53 | <code>        val base = (1000L shl attempt.coerceAtMost(6)).coerceAtMost(60000)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L54"></a>54 | <code>        attempt = (attempt + 1).coerceAtMost(6)</code> | Invoca/continua coerceAtMost com os argumentos declarados. |
| <a id="L55"></a>55 | <code>        return (base * Random.nextDouble(0.8, 1.2)).toLong().coerceIn(1000, 60000)</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L56"></a>56 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L57"></a>57 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L58"></a>58 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L59"></a>59 | <code>// Documentação: Define o tipo AuthRepository e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo AuthRepository e reúne o estado/contrato descrito para este módulo. |
| <a id="L60"></a>60 | <code>class AuthRepository(private val secure: SecureStore, private val events: EventStore) {</code> | Define o tipo AuthRepository e reúne o estado/contrato descrito para este módulo. |
| <a id="L61"></a>61 | <code>    val session = MutableStateFlow(secure.load())</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L62"></a>62 | <code>    private val refreshLock = Mutex()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L63"></a>63 | <code>    val http =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L64"></a>64 | <code>        OkHttpClient.Builder()</code> | Invoca/continua OkHttpClient.Builder com os argumentos declarados. |
| <a id="L65"></a>65 | <code>            .connectTimeout(10, TimeUnit.SECONDS)</code> | Invoca/continua connectTimeout com os argumentos declarados. |
| <a id="L66"></a>66 | <code>            .readTimeout(130, TimeUnit.SECONDS)</code> | Invoca/continua readTimeout com os argumentos declarados. |
| <a id="L67"></a>67 | <code>            .writeTimeout(20, TimeUnit.SECONDS)</code> | Invoca/continua writeTimeout com os argumentos declarados. |
| <a id="L68"></a>68 | <code>            .pingInterval(20, TimeUnit.SECONDS)</code> | Invoca/continua pingInterval com os argumentos declarados. |
| <a id="L69"></a>69 | <code>            .build()</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L70"></a>70 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L71"></a>71 | <code>    // Documentação: Executa a requisição de AuthRepository.request, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Executa a requisição de AuthRepository.request, segundo o contrato e as |
| <a id="L72"></a>72 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L73"></a>73 | <code>    private fun request(</code> | Executa a requisição de AuthRepository.request, segundo o contrato e as verificações deste módulo. |
| <a id="L74"></a>74 | <code>        server: String,</code> | Fornece a expressão server: String, ao bloco/chamada em construção. |
| <a id="L75"></a>75 | <code>        path: String,</code> | Fornece a expressão path: String, ao bloco/chamada em construção. |
| <a id="L76"></a>76 | <code>        data: JSONObject? = null,</code> | Fornece a expressão data: JSONObject? = null, ao bloco/chamada em construção. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L77"></a>77 | <code>        token: String? = null,</code> | Fornece a expressão token: String? = null, ao bloco/chamada em construção. |
| <a id="L78"></a>78 | <code>        method: String = if (data == null) &quot;GET&quot; else &quot;POST&quot;,</code> | Invoca/continua if com os argumentos declarados. |
| <a id="L79"></a>79 | <code>    ): String {</code> | Fornece a expressão ): String { ao bloco/chamada em construção. |
| <a id="L80"></a>80 | <code>        val builder = Request.Builder().url(server + path)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L81"></a>81 | <code>        token?.let { builder.header(&quot;Authorization&quot;, &quot;Bearer $it&quot;) }</code> | Invoca/continua builder.header com os argumentos declarados. |
| <a id="L82"></a>82 | <code>        builder.method(</code> | Invoca/continua builder.method com os argumentos declarados. |
| <a id="L83"></a>83 | <code>            method,</code> | Fornece a expressão method, ao bloco/chamada em construção. |
| <a id="L84"></a>84 | <code>            data?.toString()?.toRequestBody(&quot;application/json; charset=utf-8&quot;.toMediaType()),</code> | Invoca/continua toString com os argumentos declarados. |
| <a id="L85"></a>85 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L86"></a>86 | <code>        http</code> | Fornece a expressão http ao bloco/chamada em construção. |
| <a id="L87"></a>87 | <code>            .newCall(builder.build())</code> | Invoca/continua newCall com os argumentos declarados. |
| <a id="L88"></a>88 | <code>            .apply { timeout().timeout(20, TimeUnit.SECONDS) }</code> | Invoca/continua timeout com os argumentos declarados. |
| <a id="L89"></a>89 | <code>            .execute()</code> | Invoca/continua execute com os argumentos declarados. |
| <a id="L90"></a>90 | <code>            .use { response -&gt;</code> | Fornece a expressão .use { response -&gt; ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L91"></a>91 | <code>                val body = response.body?.string() ?: &quot;&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L92"></a>92 | <code>                if (!response.isSuccessful) throw ApiFailure(response.code, &quot;http_${response.code}&quot;)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L93"></a>93 | <code>                return body</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L94"></a>94 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L95"></a>95 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L96"></a>96 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L97"></a>97 | <code>    // Documentação: Autentica, obtém identidade/timezone, associa cache ao proprietário e grava</code> | Comentário de manutenção/documentação: Documentação: Autentica, obtém identidade/timezone, associa cache ao proprietário e grava |
| <a id="L98"></a>98 | <code>    // sessão cifrada.</code> | Comentário de manutenção/documentação: sessão cifrada. |
| <a id="L99"></a>99 | <code>    suspend fun login(serverInput: String, username: String, password: String) =</code> | Autentica, obtém identidade/timezone, associa cache ao proprietário e grava sessão cifrada. |
| <a id="L100"></a>100 | <code>        withContext(Dispatchers.IO) {</code> | Invoca/continua withContext com os argumentos declarados. Executa trabalho no dispatcher declarado sem bloquear o chamador de UI. |
| <a id="L101"></a>101 | <code>            refreshLock.withLock {</code> | Fornece a expressão refreshLock.withLock { ao bloco/chamada em construção. Serializa esta seção para impedir renovação/alteração concorrente do estado. |
| <a id="L102"></a>102 | <code>                val server = normalizedServer(serverInput)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L103"></a>103 | <code>                val id = secure.deviceId()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L104"></a>104 | <code>                val answer =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L105"></a>105 | <code>                    JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L106"></a>106 | <code>                        request(</code> | Invoca/continua request com os argumentos declarados. |
| <a id="L107"></a>107 | <code>                            server,</code> | Fornece a expressão server, ao bloco/chamada em construção. |
| <a id="L108"></a>108 | <code>                            &quot;/auth/login&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L109"></a>109 | <code>                            JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L110"></a>110 | <code>                                .put(&quot;username&quot;, username.trim())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L111"></a>111 | <code>                                .put(&quot;password&quot;, password)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L112"></a>112 | <code>                                .put(&quot;device_id&quot;, id),</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L113"></a>113 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L114"></a>114 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L115"></a>115 | <code>                val me =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L116"></a>116 | <code>                    JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L117"></a>117 | <code>                        request(server, &quot;/auth/me&quot;, token = answer.getString(&quot;access_token&quot;))</code> | Invoca/continua request com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L118"></a>118 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L119"></a>119 | <code>                events.ensureOwner(server + &quot;&#124;&quot; + me.getString(&quot;id&quot;))</code> | Invoca/continua events.ensureOwner com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L120"></a>120 | <code>                val data =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L121"></a>121 | <code>                    SessionData(</code> | Invoca/continua SessionData com os argumentos declarados. |
| <a id="L122"></a>122 | <code>                        server,</code> | Fornece a expressão server, ao bloco/chamada em construção. |
| <a id="L123"></a>123 | <code>                        answer.getString(&quot;access_token&quot;),</code> | Invoca/continua answer.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L124"></a>124 | <code>                        answer.getString(&quot;refresh_token&quot;),</code> | Invoca/continua answer.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L125"></a>125 | <code>                        System.currentTimeMillis() + answer.getLong(&quot;expires_in&quot;) * 1000,</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L126"></a>126 | <code>                        id,</code> | Fornece a expressão id, ao bloco/chamada em construção. |
| <a id="L127"></a>127 | <code>                        me.getString(&quot;username&quot;),</code> | Invoca/continua me.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L128"></a>128 | <code>                        me.getString(&quot;id&quot;),</code> | Invoca/continua me.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L129"></a>129 | <code>                        me.getString(&quot;timezone&quot;),</code> | Invoca/continua me.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L130"></a>130 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L131"></a>131 | <code>                secure.save(data)</code> | Invoca/continua secure.save com os argumentos declarados. |
| <a id="L132"></a>132 | <code>                session.value = data</code> | Fornece a expressão session.value = data ao bloco/chamada em construção. |
| <a id="L133"></a>133 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L134"></a>134 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L135"></a>135 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L136"></a>136 | <code>    // Documentação: Renova token próximo da expiração sob mutex e exige login novamente somente</code> | Comentário de manutenção/documentação: Documentação: Renova token próximo da expiração sob mutex e exige login novamente somente |
| <a id="L137"></a>137 | <code>    // para rejeição de autenticação.</code> | Comentário de manutenção/documentação: para rejeição de autenticação. |
| <a id="L138"></a>138 | <code>    suspend fun access(): SessionData =</code> | Renova token próximo da expiração sob mutex e exige login novamente somente para rejeição de autenticação. |
| <a id="L139"></a>139 | <code>        withContext(Dispatchers.IO) {</code> | Invoca/continua withContext com os argumentos declarados. Executa trabalho no dispatcher declarado sem bloquear o chamador de UI. |
| <a id="L140"></a>140 | <code>            refreshLock.withLock {</code> | Fornece a expressão refreshLock.withLock { ao bloco/chamada em construção. Serializa esta seção para impedir renovação/alteração concorrente do estado. |
| <a id="L141"></a>141 | <code>                val current = session.value ?: throw LoginRequired()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L142"></a>142 | <code>                if (current.expiresAt - System.currentTimeMillis() &gt; 60000) return@withLock current</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Serializa esta seção para impedir renovação/alteração concorrente do estado. |
| <a id="L143"></a>143 | <code>                try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L144"></a>144 | <code>                    val answer =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L145"></a>145 | <code>                        JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L146"></a>146 | <code>                            request(</code> | Invoca/continua request com os argumentos declarados. |
| <a id="L147"></a>147 | <code>                                current.server,</code> | Fornece a expressão current.server, ao bloco/chamada em construção. |
| <a id="L148"></a>148 | <code>                                &quot;/auth/refresh&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L149"></a>149 | <code>                                JSONObject().put(&quot;refresh_token&quot;, current.refresh),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L150"></a>150 | <code>                            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L151"></a>151 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L152"></a>152 | <code>                    val updated =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L153"></a>153 | <code>                        current.copy(</code> | Invoca/continua current.copy com os argumentos declarados. |
| <a id="L154"></a>154 | <code>                            access = answer.getString(&quot;access_token&quot;),</code> | Invoca/continua answer.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L155"></a>155 | <code>                            refresh = answer.getString(&quot;refresh_token&quot;),</code> | Invoca/continua answer.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L156"></a>156 | <code>                            expiresAt =</code> | Fornece o valor de expiresAt no contexto desta expressão. |
| <a id="L157"></a>157 | <code>                                System.currentTimeMillis() + answer.getLong(&quot;expires_in&quot;) * 1000,</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L158"></a>158 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L159"></a>159 | <code>                    secure.save(updated)</code> | Invoca/continua secure.save com os argumentos declarados. |
| <a id="L160"></a>160 | <code>                    session.value = updated</code> | Fornece a expressão session.value = updated ao bloco/chamada em construção. |
| <a id="L161"></a>161 | <code>                    updated</code> | Fornece a expressão updated ao bloco/chamada em construção. |
| <a id="L162"></a>162 | <code>                } catch (issue: ApiFailure) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L163"></a>163 | <code>                    if (issue.status == 401 &#124;&#124; issue.status == 403) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L164"></a>164 | <code>                        secure.clear()</code> | Invoca/continua secure.clear com os argumentos declarados. |
| <a id="L165"></a>165 | <code>                        session.value = null</code> | Fornece a expressão session.value = null ao bloco/chamada em construção. |
| <a id="L166"></a>166 | <code>                        throw LoginRequired()</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L167"></a>167 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L168"></a>168 | <code>                    throw issue</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L169"></a>169 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L170"></a>170 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L171"></a>171 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L172"></a>172 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L173"></a>173 | <code>    // Documentação: Implementa AuthRepository.invalidateAccess como parte do fluxo descrito para</code> | Comentário de manutenção/documentação: Documentação: Implementa AuthRepository.invalidateAccess como parte do fluxo descrito para |
| <a id="L174"></a>174 | <code>    // este arquivo.</code> | Comentário de manutenção/documentação: este arquivo. |
| <a id="L175"></a>175 | <code>    suspend fun invalidateAccess() {</code> | Implementa AuthRepository.invalidateAccess como parte do fluxo descrito para este arquivo. |
| <a id="L176"></a>176 | <code>        refreshLock.withLock {</code> | Fornece a expressão refreshLock.withLock { ao bloco/chamada em construção. Serializa esta seção para impedir renovação/alteração concorrente do estado. |
| <a id="L177"></a>177 | <code>            session.value?.let {</code> | Fornece a expressão session.value?.let { ao bloco/chamada em construção. |
| <a id="L178"></a>178 | <code>                val data = it.copy(expiresAt = 0)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L179"></a>179 | <code>                secure.save(data)</code> | Invoca/continua secure.save com os argumentos declarados. |
| <a id="L180"></a>180 | <code>                session.value = data</code> | Fornece a expressão session.value = data ao bloco/chamada em construção. |
| <a id="L181"></a>181 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L182"></a>182 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L183"></a>183 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L184"></a>184 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L185"></a>185 | <code>    // Documentação: Executa HTTP autenticado e tenta renovação uma vez após rejeição do access</code> | Comentário de manutenção/documentação: Documentação: Executa HTTP autenticado e tenta renovação uma vez após rejeição do access |
| <a id="L186"></a>186 | <code>    // token.</code> | Comentário de manutenção/documentação: token. |
| <a id="L187"></a>187 | <code>    suspend fun api(path: String, method: String = &quot;GET&quot;, data: JSONObject? = null): String =</code> | Executa HTTP autenticado e tenta renovação uma vez após rejeição do access token. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L188"></a>188 | <code>        withContext(Dispatchers.IO) {</code> | Invoca/continua withContext com os argumentos declarados. Executa trabalho no dispatcher declarado sem bloquear o chamador de UI. |
| <a id="L189"></a>189 | <code>            val current = access()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L190"></a>190 | <code>            try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L191"></a>191 | <code>                request(current.server, path, data, current.access, method)</code> | Invoca/continua request com os argumentos declarados. |
| <a id="L192"></a>192 | <code>            } catch (issue: ApiFailure) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L193"></a>193 | <code>                if (issue.status != 401) throw issue</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L194"></a>194 | <code>                invalidateAccess()</code> | Invoca/continua invalidateAccess com os argumentos declarados. |
| <a id="L195"></a>195 | <code>                val updated = access()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L196"></a>196 | <code>                request(updated.server, path, data, updated.access, method)</code> | Invoca/continua request com os argumentos declarados. |
| <a id="L197"></a>197 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L198"></a>198 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L199"></a>199 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L200"></a>200 | <code>    // Documentação: Tenta revogar a família no Core e remove sessão/dispositivo locais.</code> | Comentário de manutenção/documentação: Documentação: Tenta revogar a família no Core e remove sessão/dispositivo locais. |
| <a id="L201"></a>201 | <code>    suspend fun logout() =</code> | Tenta revogar a família no Core e remove sessão/dispositivo locais. |
| <a id="L202"></a>202 | <code>        withContext(Dispatchers.IO) {</code> | Invoca/continua withContext com os argumentos declarados. Executa trabalho no dispatcher declarado sem bloquear o chamador de UI. |
| <a id="L203"></a>203 | <code>            refreshLock.withLock {</code> | Fornece a expressão refreshLock.withLock { ao bloco/chamada em construção. Serializa esta seção para impedir renovação/alteração concorrente do estado. |
| <a id="L204"></a>204 | <code>                session.value?.let {</code> | Fornece a expressão session.value?.let { ao bloco/chamada em construção. |
| <a id="L205"></a>205 | <code>                    try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L206"></a>206 | <code>                        request(it.server, &quot;/auth/logout&quot;, JSONObject(), it.access)</code> | Invoca/continua request com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L207"></a>207 | <code>                    } catch (_: Exception) {}</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L208"></a>208 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L209"></a>209 | <code>                secure.clear()</code> | Invoca/continua secure.clear com os argumentos declarados. |
| <a id="L210"></a>210 | <code>                session.value = null</code> | Fornece a expressão session.value = null ao bloco/chamada em construção. |
| <a id="L211"></a>211 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L212"></a>212 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L213"></a>213 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
