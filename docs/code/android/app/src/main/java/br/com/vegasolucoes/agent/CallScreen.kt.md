# android/app/src/main/java/br/com/vegasolucoes/agent/CallScreen.kt

Apresenta chamada recebida/ativa, pede microfone somente com interface visível, atende pelo Core e oferece voz, texto, mute, saída e encerramento.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/CallScreen.kt) · 300 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [CallOverlay](#L25) | Implementa CallOverlay como parte do fluxo descrito para este arquivo. |
| [startVoice](#L45) | Inicia startVoice, segundo o contrato e as verificações deste módulo. |
| [accept](#L61) | Implementa accept como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L5"></a>5 | <code>import android.content.pm.PackageManager</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.PackageManager neste arquivo. |
| <a id="L6"></a>6 | <code>import androidx.activity.compose.rememberLauncherForActivityResult</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.compose.rememberLauncherForActivityResult neste arquivo. |
| <a id="L7"></a>7 | <code>import androidx.activity.result.contract.ActivityResultContracts</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.result.contract.ActivityResultContracts neste arquivo. |
| <a id="L8"></a>8 | <code>import androidx.compose.foundation.layout.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.layout.* neste arquivo. |
| <a id="L9"></a>9 | <code>import androidx.compose.material3.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.material3.* neste arquivo. |
| <a id="L10"></a>10 | <code>import androidx.compose.runtime.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.runtime.* neste arquivo. |
| <a id="L11"></a>11 | <code>import androidx.compose.ui.Modifier</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.Modifier neste arquivo. |
| <a id="L12"></a>12 | <code>import androidx.compose.ui.unit.dp</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.unit.dp neste arquivo. |
| <a id="L13"></a>13 | <code>import androidx.compose.ui.window.Dialog</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.window.Dialog neste arquivo. Apresenta conteúdo modal segundo propriedades e callback de fechamento. |
| <a id="L14"></a>14 | <code>import androidx.compose.ui.window.DialogProperties</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.window.DialogProperties neste arquivo. |
| <a id="L15"></a>15 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L16"></a>16 | <code>import androidx.lifecycle.Lifecycle</code> | Disponibiliza o símbolo Kotlin/Android androidx.lifecycle.Lifecycle neste arquivo. |
| <a id="L17"></a>17 | <code>import androidx.lifecycle.compose.collectAsStateWithLifecycle</code> | Disponibiliza o símbolo Kotlin/Android androidx.lifecycle.compose.collectAsStateWithLifecycle neste arquivo. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L18"></a>18 | <code>import java.time.Instant</code> | Disponibiliza o símbolo Kotlin/Android java.time.Instant neste arquivo. |
| <a id="L19"></a>19 | <code>import kotlinx.coroutines.delay</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.delay neste arquivo. |
| <a id="L20"></a>20 | <code>import kotlinx.coroutines.launch</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.launch neste arquivo. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L21"></a>21 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L23"></a>23 | <code>@Composable</code> | Aplica a anotação @Composable à declaração seguinte. |
| <a id="L24"></a>24 | <code>// Documentação: Implementa CallOverlay como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa CallOverlay como parte do fluxo descrito para este arquivo. |
| <a id="L25"></a>25 | <code>fun CallOverlay(activity: MainActivity, session: SessionData) {</code> | Implementa CallOverlay como parte do fluxo descrito para este arquivo. |
| <a id="L26"></a>26 | <code>    val received by AgentRuntime.received.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L27"></a>27 | <code>    val call by AgentRuntime.call.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L28"></a>28 | <code>    val voice by AgentRuntime.voice.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L29"></a>29 | <code>    val status by AgentRuntime.voiceStatus.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L30"></a>30 | <code>    val mute by AgentRuntime.mute.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L31"></a>31 | <code>    val speaker by AgentRuntime.speaker.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L32"></a>32 | <code>    val scope = rememberCoroutineScope()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L33"></a>33 | <code>    var error by remember { mutableStateOf&lt;String?&gt;(null) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L34"></a>34 | <code>    var busy by remember { mutableStateOf(false) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L35"></a>35 | <code>    var selected by remember { mutableStateOf&lt;String?&gt;(null) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L36"></a>36 | <code>    var now by remember { mutableStateOf(Instant.now()) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L37"></a>37 | <code>    LaunchedEffect(Unit) {</code> | Invoca/continua LaunchedEffect com os argumentos declarados. Executa coroutine vinculada às chaves e à presença do trecho na composição. |
| <a id="L38"></a>38 | <code>        while (true) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L39"></a>39 | <code>            now = Instant.now()</code> | Invoca/continua Instant.now com os argumentos declarados. |
| <a id="L40"></a>40 | <code>            delay(1000)</code> | Invoca/continua delay com os argumentos declarados. |
| <a id="L41"></a>41 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L42"></a>42 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L43"></a>43 | <code>    val incoming = remember(received, now) { incomingCall(received) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L44"></a>44 | <code>    // Documentação: Inicia startVoice, segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: Documentação: Inicia startVoice, segundo o contrato e as verificações deste módulo. |
| <a id="L45"></a>45 | <code>    fun startVoice() {</code> | Inicia startVoice, segundo o contrato e as verificações deste módulo. |
| <a id="L46"></a>46 | <code>        try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L47"></a>47 | <code>            if (!activity.lifecycle.currentState.isAtLeast(Lifecycle.State.RESUMED)) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L48"></a>48 | <code>                error = &quot;Volte ao aplicativo para ativar o áudio.&quot;</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L49"></a>49 | <code>                return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L50"></a>50 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L51"></a>51 | <code>            activity.connect()</code> | Invoca/continua activity.connect com os argumentos declarados. |
| <a id="L52"></a>52 | <code>            ContextCompat.startForegroundService(</code> | Invoca/continua ContextCompat.startForegroundService com os argumentos declarados. Solicita início do serviço; as restrições de background do Android continuam valendo. |
| <a id="L53"></a>53 | <code>                activity,</code> | Fornece a expressão activity, ao bloco/chamada em construção. |
| <a id="L54"></a>54 | <code>                Intent(activity, VoiceService::class.java),</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L55"></a>55 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L56"></a>56 | <code>        } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L57"></a>57 | <code>            error = &quot;Não foi possível ativar o áudio. Continue por texto ou tente novamente.&quot;</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L58"></a>58 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L59"></a>59 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L60"></a>60 | <code>    // Documentação: Implementa accept como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa accept como parte do fluxo descrito para este arquivo. |
| <a id="L61"></a>61 | <code>    fun accept(id: String) {</code> | Implementa accept como parte do fluxo descrito para este arquivo. |
| <a id="L62"></a>62 | <code>        scope.launch {</code> | Fornece a expressão scope.launch { ao bloco/chamada em construção. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L63"></a>63 | <code>            busy = true</code> | Fornece o valor de busy no contexto desta expressão. |
| <a id="L64"></a>64 | <code>            try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L65"></a>65 | <code>                val row =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L66"></a>66 | <code>                    JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L67"></a>67 | <code>                        AgentRuntime.auth.api(</code> | Invoca/continua AgentRuntime.auth.api com os argumentos declarados. |
| <a id="L68"></a>68 | <code>                            &quot;/calls/incoming/$id/answer&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L69"></a>69 | <code>                            &quot;POST&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L70"></a>70 | <code>                            JSONObject().put(&quot;device_id&quot;, session.deviceId),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L71"></a>71 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L72"></a>72 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L73"></a>73 | <code>                AgentRuntime.call.value = row</code> | Fornece a expressão AgentRuntime.call.value = row ao bloco/chamada em construção. |
| <a id="L74"></a>74 | <code>                AgentNotifications(activity).cancel(id)</code> | Invoca/continua AgentNotifications com os argumentos declarados. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L75"></a>75 | <code>                val event =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L76"></a>76 | <code>                    outgoing(&quot;call.state&quot;, JSONObject().put(&quot;event_id&quot;, id).put(&quot;session&quot;, row))</code> | Invoca/continua outgoing com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L77"></a>77 | <code>                AgentRuntime.events.save(event)</code> | Invoca/continua AgentRuntime.events.save com os argumentos declarados. |
| <a id="L78"></a>78 | <code>                AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L79"></a>79 | <code>                startVoice()</code> | Invoca/continua startVoice com os argumentos declarados. |
| <a id="L80"></a>80 | <code>                error = null</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L81"></a>81 | <code>            } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L82"></a>82 | <code>                error = &quot;Esta chamada expirou ou não pôde ser atendida. Atualize a conexão.&quot;</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L83"></a>83 | <code>            } finally {</code> | Fornece a expressão } finally { ao bloco/chamada em construção. |
| <a id="L84"></a>84 | <code>                busy = false</code> | Fornece o valor de busy no contexto desta expressão. |
| <a id="L85"></a>85 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L86"></a>86 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L87"></a>87 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L88"></a>88 | <code>    val microphone =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L89"></a>89 | <code>        rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) {</code> | Invoca/continua rememberLauncherForActivityResult com os argumentos declarados. |
| <a id="L90"></a>90 | <code>            if (selected != null) accept(selected!!) else startVoice()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L91"></a>91 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L92"></a>92 | <code>    val requestedAnswer by AgentRuntime.requestedAnswer.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L93"></a>93 | <code>    val lifecycleState by activity.lifecycle.currentStateFlow.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L94"></a>94 | <code>    LaunchedEffect(requestedAnswer, incoming, lifecycleState) {</code> | Invoca/continua LaunchedEffect com os argumentos declarados. Executa coroutine vinculada às chaves e à presença do trecho na composição. |
| <a id="L95"></a>95 | <code>        val requested = requestedAnswer</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L96"></a>96 | <code>        if (requested != null &amp;&amp; lifecycleState == Lifecycle.State.RESUMED) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L97"></a>97 | <code>            AgentRuntime.requestedAnswer.value = null</code> | Fornece a expressão AgentRuntime.requestedAnswer.value = null ao bloco/chamada em construção. |
| <a id="L98"></a>98 | <code>            if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L99"></a>99 | <code>                incomingCall(received, requested) != null &amp;&amp; call?.optString(&quot;status&quot;) != &quot;ACTIVE&quot;</code> | Invoca/continua incomingCall com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L100"></a>100 | <code>            ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L101"></a>101 | <code>                selected = requested</code> | Fornece o valor de selected no contexto desta expressão. |
| <a id="L102"></a>102 | <code>                if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L103"></a>103 | <code>                    ContextCompat.checkSelfPermission(activity, Manifest.permission.RECORD_AUDIO) !=</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L104"></a>104 | <code>                        PackageManager.PERMISSION_GRANTED</code> | Fornece a expressão PackageManager.PERMISSION_GRANTED ao bloco/chamada em construção. |
| <a id="L105"></a>105 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L106"></a>106 | <code>                    microphone.launch(Manifest.permission.RECORD_AUDIO)</code> | Invoca/continua microphone.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L107"></a>107 | <code>                else accept(requested)</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L108"></a>108 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L109"></a>109 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L110"></a>110 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L111"></a>111 | <code>    LaunchedEffect(session.deviceId) {</code> | Invoca/continua LaunchedEffect com os argumentos declarados. Executa coroutine vinculada às chaves e à presença do trecho na composição. |
| <a id="L112"></a>112 | <code>        try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L113"></a>113 | <code>            val rows = arrayRows(AgentRuntime.auth.api(&quot;/calls&quot;))</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L114"></a>114 | <code>            AgentRuntime.call.value = rows.firstOrNull {</code> | Fornece a expressão AgentRuntime.call.value = rows.firstOrNull { ao bloco/chamada em construção. |
| <a id="L115"></a>115 | <code>                it.getString(&quot;status&quot;) == &quot;ACTIVE&quot; &amp;&amp; it.getString(&quot;device_id&quot;) == session.deviceId</code> | Invoca/continua it.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L116"></a>116 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L117"></a>117 | <code>        } catch (_: Exception) {}</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L118"></a>118 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L119"></a>119 | <code>    if (call?.optString(&quot;status&quot;) == &quot;ACTIVE&quot;) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L120"></a>120 | <code>        var duration by remember { mutableLongStateOf(0) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L121"></a>121 | <code>        var text by remember { mutableStateOf(&quot;&quot;) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L122"></a>122 | <code>        LaunchedEffect(call?.optString(&quot;id&quot;)) {</code> | Invoca/continua LaunchedEffect com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L123"></a>123 | <code>            while (true) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L124"></a>124 | <code>                duration =</code> | Fornece o valor de duration no contexto desta expressão. |
| <a id="L125"></a>125 | <code>                    runCatching {</code> | Fornece a expressão runCatching { ao bloco/chamada em construção. |
| <a id="L126"></a>126 | <code>                            java.time.Duration.between(</code> | Invoca/continua java.time.Duration.between com os argumentos declarados. |
| <a id="L127"></a>127 | <code>                                    Instant.parse(call!!.getString(&quot;started_at&quot;)),</code> | Invoca/continua Instant.parse com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L128"></a>128 | <code>                                    Instant.now(),</code> | Invoca/continua Instant.now com os argumentos declarados. |
| <a id="L129"></a>129 | <code>                                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L130"></a>130 | <code>                                .seconds</code> | Fornece a expressão .seconds ao bloco/chamada em construção. |
| <a id="L131"></a>131 | <code>                                .coerceAtLeast(0)</code> | Invoca/continua coerceAtLeast com os argumentos declarados. |
| <a id="L132"></a>132 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L133"></a>133 | <code>                        .getOrDefault(0)</code> | Invoca/continua getOrDefault com os argumentos declarados. |
| <a id="L134"></a>134 | <code>                delay(1000)</code> | Invoca/continua delay com os argumentos declarados. |
| <a id="L135"></a>135 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L136"></a>136 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L137"></a>137 | <code>        Dialog(</code> | Invoca/continua Dialog com os argumentos declarados. Apresenta conteúdo modal segundo propriedades e callback de fechamento. |
| <a id="L138"></a>138 | <code>            onDismissRequest = {},</code> | Fornece o valor de onDismissRequest no contexto desta expressão. |
| <a id="L139"></a>139 | <code>            properties = DialogProperties(usePlatformDefaultWidth = false),</code> | Invoca/continua DialogProperties com os argumentos declarados. |
| <a id="L140"></a>140 | <code>        ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L141"></a>141 | <code>            Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {</code> | Invoca/continua Surface com os argumentos declarados. Define superfície visual usando cor/forma e componentes filhos. |
| <a id="L142"></a>142 | <code>                Column(</code> | Invoca/continua Column com os argumentos declarados. Organiza componentes filhos verticalmente no layout. |
| <a id="L143"></a>143 | <code>                    Modifier.fillMaxSize().systemBarsPadding().imePadding().padding(24.dp),</code> | Invoca/continua Modifier.fillMaxSize com os argumentos declarados. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L144"></a>144 | <code>                    verticalArrangement = Arrangement.spacedBy(20.dp),</code> | Invoca/continua Arrangement.spacedBy com os argumentos declarados. |
| <a id="L145"></a>145 | <code>                ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L146"></a>146 | <code>                    Spacer(Modifier.height(24.dp))</code> | Invoca/continua Spacer com os argumentos declarados. |
| <a id="L147"></a>147 | <code>                    Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L148"></a>148 | <code>                        &quot;DEVLIMA AGENT&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L149"></a>149 | <code>                        color = MaterialTheme.colorScheme.primary,</code> | Fornece o valor de color no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L150"></a>150 | <code>                        style = MaterialTheme.typography.headlineMedium,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L151"></a>151 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L152"></a>152 | <code>                    Text(&quot;Chamada interna · %02d:%02d&quot;.format(duration / 60, duration % 60))</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L153"></a>153 | <code>                    Text(call!!.getString(&quot;reason&quot;))</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L154"></a>154 | <code>                    Text(status)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L155"></a>155 | <code>                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {</code> | Invoca/continua Row com os argumentos declarados. Organiza componentes filhos horizontalmente no layout. |
| <a id="L156"></a>156 | <code>                        OutlinedButton(onClick = { voice?.toggleMute() }) {</code> | Invoca/continua OutlinedButton com os argumentos declarados. Cria controle com contorno e a ação onClick declarada. |
| <a id="L157"></a>157 | <code>                            Text(if (mute) &quot;Ativar mic&quot; else &quot;Silenciar&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L158"></a>158 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L159"></a>159 | <code>                        OutlinedButton(onClick = { voice?.toggleSpeaker() }) {</code> | Invoca/continua OutlinedButton com os argumentos declarados. Cria controle com contorno e a ação onClick declarada. |
| <a id="L160"></a>160 | <code>                            Text(if (speaker) &quot;Alto-falante&quot; else &quot;Auricular&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L161"></a>161 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L162"></a>162 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L163"></a>163 | <code>                    Button(</code> | Invoca/continua Button com os argumentos declarados. Cria controle que executa onClick quando habilitado e acionado. |
| <a id="L164"></a>164 | <code>                        onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L165"></a>165 | <code>                            if (voice == null) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L166"></a>166 | <code>                                selected = null</code> | Fornece o valor de selected no contexto desta expressão. |
| <a id="L167"></a>167 | <code>                                if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L168"></a>168 | <code>                                    ContextCompat.checkSelfPermission(</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L169"></a>169 | <code>                                        activity,</code> | Fornece a expressão activity, ao bloco/chamada em construção. |
| <a id="L170"></a>170 | <code>                                        Manifest.permission.RECORD_AUDIO,</code> | Fornece a expressão Manifest.permission.RECORD_AUDIO, ao bloco/chamada em construção. |
| <a id="L171"></a>171 | <code>                                    ) != PackageManager.PERMISSION_GRANTED</code> | Fornece a expressão ) != PackageManager.PERMISSION_GRANTED ao bloco/chamada em construção. |
| <a id="L172"></a>172 | <code>                                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L173"></a>173 | <code>                                    microphone.launch(Manifest.permission.RECORD_AUDIO)</code> | Invoca/continua microphone.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L174"></a>174 | <code>                                else startVoice()</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L175"></a>175 | <code>                            } else voice?.listen()</code> | Invoca/continua listen com os argumentos declarados. |
| <a id="L176"></a>176 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L177"></a>177 | <code>                    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L178"></a>178 | <code>                        Text(if (voice == null) &quot;Ativar áudio&quot; else &quot;Falar&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L179"></a>179 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L180"></a>180 | <code>                    Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L181"></a>181 | <code>                        &quot;O reconhecimento de fala pode usar o serviço instalado no Android. Confira suas configurações de voz.&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L182"></a>182 | <code>                        style = MaterialTheme.typography.bodySmall,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L183"></a>183 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L184"></a>184 | <code>                    OutlinedTextField(</code> | Invoca/continua OutlinedTextField com os argumentos declarados. Liga entrada de texto ao valor e callback de alteração. |
| <a id="L185"></a>185 | <code>                        text,</code> | Fornece a expressão text, ao bloco/chamada em construção. |
| <a id="L186"></a>186 | <code>                        { if (it.length &lt;= 4000) text = it },</code> | Invoca/continua if com os argumentos declarados. |
| <a id="L187"></a>187 | <code>                        label = { Text(&quot;Alternativa por texto&quot;) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L188"></a>188 | <code>                        modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L189"></a>189 | <code>                        maxLines = 4,</code> | Fornece o valor de maxLines no contexto desta expressão. |
| <a id="L190"></a>190 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L191"></a>191 | <code>                    TextButton(</code> | Invoca/continua TextButton com os argumentos declarados. Cria ação textual com a condição enabled declarada. |
| <a id="L192"></a>192 | <code>                        onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L193"></a>193 | <code>                            if (voice != null) voice?.sendText(text)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Encaminha texto pela fila/contrato da chamada ativa. |
| <a id="L194"></a>194 | <code>                            else {</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L195"></a>195 | <code>                                AgentRuntime.events.enqueueVoice(call!!, text)</code> | Invoca/continua AgentRuntime.events.enqueueVoice com os argumentos declarados. Grava transcrição na fila durável vinculada à chamada. |
| <a id="L196"></a>196 | <code>                                AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L197"></a>197 | <code>                                activity.connect()</code> | Invoca/continua activity.connect com os argumentos declarados. |
| <a id="L198"></a>198 | <code>                            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L199"></a>199 | <code>                            text = &quot;&quot;</code> | Fornece o valor de text no contexto desta expressão. |
| <a id="L200"></a>200 | <code>                        },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L201"></a>201 | <code>                        enabled = text.isNotBlank(),</code> | Invoca/continua text.isNotBlank com os argumentos declarados. |
| <a id="L202"></a>202 | <code>                    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L203"></a>203 | <code>                        Text(&quot;Enviar texto&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L204"></a>204 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L205"></a>205 | <code>                    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L206"></a>206 | <code>                    Spacer(Modifier.weight(1f))</code> | Invoca/continua Spacer com os argumentos declarados. |
| <a id="L207"></a>207 | <code>                    Button(</code> | Invoca/continua Button com os argumentos declarados. Cria controle que executa onClick quando habilitado e acionado. |
| <a id="L208"></a>208 | <code>                        onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L209"></a>209 | <code>                            if (voice != null) voice?.end()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L210"></a>210 | <code>                            else</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L211"></a>211 | <code>                                scope.launch {</code> | Fornece a expressão scope.launch { ao bloco/chamada em construção. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L212"></a>212 | <code>                                    try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L213"></a>213 | <code>                                        AgentRuntime.call.value =</code> | Fornece a expressão AgentRuntime.call.value = ao bloco/chamada em construção. |
| <a id="L214"></a>214 | <code>                                            JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L215"></a>215 | <code>                                                AgentRuntime.auth.api(</code> | Invoca/continua AgentRuntime.auth.api com os argumentos declarados. |
| <a id="L216"></a>216 | <code>                                                    &quot;/calls/${call!!.getString(&quot;id&quot;)}/end&quot;,</code> | Fornece a expressão &quot;/calls/${call!!.getString(&quot;id&quot;)}/end&quot;, ao bloco/chamada em construção. |
| <a id="L217"></a>217 | <code>                                                    &quot;POST&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L218"></a>218 | <code>                                                    JSONObject().put(&quot;device_id&quot;, session.deviceId),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L219"></a>219 | <code>                                                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L220"></a>220 | <code>                                            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L221"></a>221 | <code>                                        AgentRuntime.events.cancelVoice(call!!.getString(&quot;id&quot;))</code> | Invoca/continua AgentRuntime.events.cancelVoice com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L222"></a>222 | <code>                                        AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L223"></a>223 | <code>                                    } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L224"></a>224 | <code>                                        error = &quot;Não foi possível encerrar. Tente novamente.&quot;</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L225"></a>225 | <code>                                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L226"></a>226 | <code>                                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L227"></a>227 | <code>                        },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L228"></a>228 | <code>                        colors =</code> | Fornece o valor de colors no contexto desta expressão. |
| <a id="L229"></a>229 | <code>                            ButtonDefaults.buttonColors(</code> | Invoca/continua ButtonDefaults.buttonColors com os argumentos declarados. |
| <a id="L230"></a>230 | <code>                                containerColor = MaterialTheme.colorScheme.error</code> | Fornece o valor de containerColor no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L231"></a>231 | <code>                            ),</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L232"></a>232 | <code>                        modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L233"></a>233 | <code>                    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L234"></a>234 | <code>                        Text(&quot;Encerrar chamada&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L235"></a>235 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L236"></a>236 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L237"></a>237 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L238"></a>238 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L239"></a>239 | <code>    } else if (incoming != null)</code> | Invoca/continua if com os argumentos declarados. |
| <a id="L240"></a>240 | <code>        AlertDialog(</code> | Invoca/continua AlertDialog com os argumentos declarados. Apresenta confirmação/recusa com os botões e mensagens declarados. |
| <a id="L241"></a>241 | <code>            onDismissRequest = {},</code> | Fornece o valor de onDismissRequest no contexto desta expressão. |
| <a id="L242"></a>242 | <code>            title = { Text(&quot;AGENTE ESTÁ LIGANDO&quot;) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L243"></a>243 | <code>            text = {</code> | Fornece o valor de text no contexto desta expressão. |
| <a id="L244"></a>244 | <code>                Column {</code> | Fornece a expressão Column { ao bloco/chamada em construção. Organiza componentes filhos verticalmente no layout. |
| <a id="L245"></a>245 | <code>                    Text(incoming.getJSONObject(&quot;payload&quot;).optString(&quot;text&quot;))</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L246"></a>246 | <code>                    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L247"></a>247 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L248"></a>248 | <code>            },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L249"></a>249 | <code>            confirmButton = {</code> | Fornece o valor de confirmButton no contexto desta expressão. |
| <a id="L250"></a>250 | <code>                TextButton(</code> | Invoca/continua TextButton com os argumentos declarados. Cria ação textual com a condição enabled declarada. |
| <a id="L251"></a>251 | <code>                    enabled = !busy,</code> | Fornece o valor de enabled no contexto desta expressão. |
| <a id="L252"></a>252 | <code>                    onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L253"></a>253 | <code>                        selected = incoming.getString(&quot;event_id&quot;)</code> | Invoca/continua incoming.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L254"></a>254 | <code>                        if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L255"></a>255 | <code>                            ContextCompat.checkSelfPermission(</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L256"></a>256 | <code>                                activity,</code> | Fornece a expressão activity, ao bloco/chamada em construção. |
| <a id="L257"></a>257 | <code>                                Manifest.permission.RECORD_AUDIO,</code> | Fornece a expressão Manifest.permission.RECORD_AUDIO, ao bloco/chamada em construção. |
| <a id="L258"></a>258 | <code>                            ) != PackageManager.PERMISSION_GRANTED</code> | Fornece a expressão ) != PackageManager.PERMISSION_GRANTED ao bloco/chamada em construção. |
| <a id="L259"></a>259 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L260"></a>260 | <code>                            microphone.launch(Manifest.permission.RECORD_AUDIO)</code> | Invoca/continua microphone.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L261"></a>261 | <code>                        else accept(selected!!)</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L262"></a>262 | <code>                    },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L263"></a>263 | <code>                ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L264"></a>264 | <code>                    Text(&quot;Atender&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L265"></a>265 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L266"></a>266 | <code>            },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L267"></a>267 | <code>            dismissButton = {</code> | Fornece o valor de dismissButton no contexto desta expressão. |
| <a id="L268"></a>268 | <code>                TextButton(</code> | Invoca/continua TextButton com os argumentos declarados. Cria ação textual com a condição enabled declarada. |
| <a id="L269"></a>269 | <code>                    enabled = !busy,</code> | Fornece o valor de enabled no contexto desta expressão. |
| <a id="L270"></a>270 | <code>                    onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L271"></a>271 | <code>                        scope.launch {</code> | Fornece a expressão scope.launch { ao bloco/chamada em construção. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L272"></a>272 | <code>                            busy = true</code> | Fornece o valor de busy no contexto desta expressão. |
| <a id="L273"></a>273 | <code>                            try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L274"></a>274 | <code>                                val id = incoming.getString(&quot;event_id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L275"></a>275 | <code>                                AgentRuntime.auth.api(</code> | Invoca/continua AgentRuntime.auth.api com os argumentos declarados. |
| <a id="L276"></a>276 | <code>                                    &quot;/calls/incoming/$id/reject&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L277"></a>277 | <code>                                    &quot;POST&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L278"></a>278 | <code>                                    JSONObject().put(&quot;device_id&quot;, session.deviceId),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L279"></a>279 | <code>                                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L280"></a>280 | <code>                                AgentRuntime.events.save(</code> | Invoca/continua AgentRuntime.events.save com os argumentos declarados. |
| <a id="L281"></a>281 | <code>                                    outgoing(</code> | Invoca/continua outgoing com os argumentos declarados. |
| <a id="L282"></a>282 | <code>                                        &quot;call.dismissed&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L283"></a>283 | <code>                                        JSONObject().put(&quot;event_id&quot;, id).put(&quot;status&quot;, &quot;REJECTED&quot;),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L284"></a>284 | <code>                                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L285"></a>285 | <code>                                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L286"></a>286 | <code>                                AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L287"></a>287 | <code>                                AgentNotifications(activity).cancel(id)</code> | Invoca/continua AgentNotifications com os argumentos declarados. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L288"></a>288 | <code>                            } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L289"></a>289 | <code>                                error = &quot;Não foi possível recusar. Tente novamente.&quot;</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L290"></a>290 | <code>                            } finally {</code> | Fornece a expressão } finally { ao bloco/chamada em construção. |
| <a id="L291"></a>291 | <code>                                busy = false</code> | Fornece o valor de busy no contexto desta expressão. |
| <a id="L292"></a>292 | <code>                            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L293"></a>293 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L294"></a>294 | <code>                    },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L295"></a>295 | <code>                ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L296"></a>296 | <code>                    Text(&quot;Recusar&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L297"></a>297 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L298"></a>298 | <code>            },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L299"></a>299 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L300"></a>300 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
