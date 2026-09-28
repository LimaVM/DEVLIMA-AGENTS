# android/app/src/main/java/br/com/vegasolucoes/agent/IncomingCallActivity.kt

Apresenta controles mínimos sobre tela bloqueada quando o Android permite e pede desbloqueio antes de encaminhar atendimento; não abre histórico nem liga microfone sozinha.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/IncomingCallActivity.kt) · 142 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [IncomingCallActivity](#L20) | Define o tipo IncomingCallActivity e reúne o estado/contrato descrito para este módulo. |
| [IncomingCallActivity.onCreate](#L25) | Trata o callback de IncomingCallActivity.onCreate, segundo o contrato e as verificações deste módulo. |
| [IncomingCallActivity.onPostResume](#L102) | Trata o callback de IncomingCallActivity.onPostResume, segundo o contrato e as verificações deste módulo. |
| [IncomingCallActivity.answer](#L112) | Solicita desbloqueio e encaminha internamente o event_id validado à interface principal. |
| [IncomingCallActivity.open](#L116) | Implementa IncomingCallActivity.open como parte do fluxo descrito para este arquivo. |
| [IncomingCallActivity.onDismissSucceeded](#L136) | Trata o callback de IncomingCallActivity.onDismissSucceeded, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.app.KeyguardManager</code> | Disponibiliza o símbolo Kotlin/Android android.app.KeyguardManager neste arquivo. |
| <a id="L4"></a>4 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L5"></a>5 | <code>import android.os.Bundle</code> | Disponibiliza o símbolo Kotlin/Android android.os.Bundle neste arquivo. |
| <a id="L6"></a>6 | <code>import androidx.activity.ComponentActivity</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.ComponentActivity neste arquivo. |
| <a id="L7"></a>7 | <code>import androidx.activity.compose.setContent</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.compose.setContent neste arquivo. |
| <a id="L8"></a>8 | <code>import androidx.activity.enableEdgeToEdge</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.enableEdgeToEdge neste arquivo. |
| <a id="L9"></a>9 | <code>import androidx.compose.foundation.layout.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.layout.* neste arquivo. |
| <a id="L10"></a>10 | <code>import androidx.compose.material3.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.material3.* neste arquivo. |
| <a id="L11"></a>11 | <code>import androidx.compose.runtime.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.runtime.* neste arquivo. |
| <a id="L12"></a>12 | <code>import androidx.compose.ui.Modifier</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.Modifier neste arquivo. |
| <a id="L13"></a>13 | <code>import androidx.compose.ui.unit.dp</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.unit.dp neste arquivo. |
| <a id="L14"></a>14 | <code>import androidx.lifecycle.compose.collectAsStateWithLifecycle</code> | Disponibiliza o símbolo Kotlin/Android androidx.lifecycle.compose.collectAsStateWithLifecycle neste arquivo. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L15"></a>15 | <code>import kotlinx.coroutines.delay</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.delay neste arquivo. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L17"></a>17 | <code>/** Minimal lock-screen surface. Chat, reason and microphone remain behind unlock. */</code> | Comentário de manutenção/documentação: Minimal lock-screen surface. Chat, reason and microphone remain behind unlock. */ |
| <a id="L18"></a>18 | <code>// Documentação: Define o tipo IncomingCallActivity e reúne o estado/contrato descrito para este</code> | Comentário de manutenção/documentação: Documentação: Define o tipo IncomingCallActivity e reúne o estado/contrato descrito para este |
| <a id="L19"></a>19 | <code>// módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L20"></a>20 | <code>class IncomingCallActivity : ComponentActivity() {</code> | Define o tipo IncomingCallActivity e reúne o estado/contrato descrito para este módulo. |
| <a id="L21"></a>21 | <code>    private var answerRequested = false</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L23"></a>23 | <code>    // Documentação: Trata o callback de IncomingCallActivity.onCreate, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de IncomingCallActivity.onCreate, segundo o contrato e as |
| <a id="L24"></a>24 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L25"></a>25 | <code>    override fun onCreate(state: Bundle?) {</code> | Trata o callback de IncomingCallActivity.onCreate, segundo o contrato e as verificações deste módulo. |
| <a id="L26"></a>26 | <code>        super.onCreate(state)</code> | Invoca/continua super.onCreate com os argumentos declarados. |
| <a id="L27"></a>27 | <code>        if (android.os.Build.VERSION.SDK_INT &gt;= 27) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L28"></a>28 | <code>            setShowWhenLocked(true)</code> | Invoca/continua setShowWhenLocked com os argumentos declarados. Autoriza esta janela a ser mostrada sobre bloqueio, sem desbloquear o aparelho. |
| <a id="L29"></a>29 | <code>            setTurnScreenOn(true)</code> | Invoca/continua setTurnScreenOn com os argumentos declarados. Solicita ligar a tela para apresentar a chamada, sujeito às regras do sistema. |
| <a id="L30"></a>30 | <code>        } else {</code> | Fornece a expressão } else { ao bloco/chamada em construção. |
| <a id="L31"></a>31 | <code>            @Suppress(&quot;DEPRECATION&quot;)</code> | Aplica a anotação @Suppress(&quot;DEPRECATION&quot;) à declaração seguinte. |
| <a id="L32"></a>32 | <code>            window.addFlags(</code> | Invoca/continua window.addFlags com os argumentos declarados. |
| <a id="L33"></a>33 | <code>                android.view.WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or</code> | Fornece a expressão android.view.WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or ao bloco/chamada em construção. |
| <a id="L34"></a>34 | <code>                    android.view.WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON</code> | Fornece a expressão android.view.WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON ao bloco/chamada em construção. |
| <a id="L35"></a>35 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L36"></a>36 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L37"></a>37 | <code>        answerRequested = intent.action?.startsWith(&quot;answer.&quot;) == true</code> | Invoca/continua startsWith com os argumentos declarados. |
| <a id="L38"></a>38 | <code>        enableEdgeToEdge()</code> | Invoca/continua enableEdgeToEdge com os argumentos declarados. |
| <a id="L39"></a>39 | <code>        val id =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L40"></a>40 | <code>            intent.getStringExtra(&quot;event_id&quot;)</code> | Invoca/continua intent.getStringExtra com os argumentos declarados. Lê argumento textual do Intent para o fluxo indicado. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L41"></a>41 | <code>                ?: run {</code> | Fornece a expressão ?: run { ao bloco/chamada em construção. |
| <a id="L42"></a>42 | <code>                    finish()</code> | Invoca/continua finish com os argumentos declarados. |
| <a id="L43"></a>43 | <code>                    return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L44"></a>44 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L45"></a>45 | <code>        setContent {</code> | Fornece a expressão setContent { ao bloco/chamada em construção. |
| <a id="L46"></a>46 | <code>            MaterialTheme(colorScheme = AgentColors) {</code> | Invoca/continua MaterialTheme com os argumentos declarados. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L47"></a>47 | <code>                val events by AgentRuntime.received.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L48"></a>48 | <code>                var tick by remember { mutableIntStateOf(0) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L49"></a>49 | <code>                LaunchedEffect(id) {</code> | Invoca/continua LaunchedEffect com os argumentos declarados. Executa coroutine vinculada às chaves e à presença do trecho na composição. |
| <a id="L50"></a>50 | <code>                    while (true) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L51"></a>51 | <code>                        delay(1000)</code> | Invoca/continua delay com os argumentos declarados. |
| <a id="L52"></a>52 | <code>                        tick++</code> | Fornece a expressão tick++ ao bloco/chamada em construção. |
| <a id="L53"></a>53 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L54"></a>54 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L55"></a>55 | <code>                val incoming = remember(events, tick) { incomingCall(events, id) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L56"></a>56 | <code>                LaunchedEffect(incoming) { if (incoming == null) finish() }</code> | Invoca/continua LaunchedEffect com os argumentos declarados. Executa coroutine vinculada às chaves e à presença do trecho na composição. |
| <a id="L57"></a>57 | <code>                Surface(Modifier.fillMaxSize()) {</code> | Invoca/continua Surface com os argumentos declarados. Define superfície visual usando cor/forma e componentes filhos. |
| <a id="L58"></a>58 | <code>                    Column(</code> | Invoca/continua Column com os argumentos declarados. Organiza componentes filhos verticalmente no layout. |
| <a id="L59"></a>59 | <code>                        Modifier.fillMaxSize().systemBarsPadding().padding(32.dp),</code> | Invoca/continua Modifier.fillMaxSize com os argumentos declarados. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L60"></a>60 | <code>                        verticalArrangement = Arrangement.spacedBy(24.dp),</code> | Invoca/continua Arrangement.spacedBy com os argumentos declarados. |
| <a id="L61"></a>61 | <code>                    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L62"></a>62 | <code>                        Spacer(Modifier.weight(1f))</code> | Invoca/continua Spacer com os argumentos declarados. |
| <a id="L63"></a>63 | <code>                        Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L64"></a>64 | <code>                            &quot;DEVLIMA AGENT&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L65"></a>65 | <code>                            style = MaterialTheme.typography.headlineMedium,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L66"></a>66 | <code>                            color = MaterialTheme.colorScheme.primary,</code> | Fornece o valor de color no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L67"></a>67 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L68"></a>68 | <code>                        Text(&quot;Agente está ligando&quot;, style = MaterialTheme.typography.headlineLarge)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L69"></a>69 | <code>                        Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L70"></a>70 | <code>                            &quot;Desbloqueie para conversar. O microfone só será ativado após atender.&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L71"></a>71 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L72"></a>72 | <code>                        Button(</code> | Invoca/continua Button com os argumentos declarados. Cria controle que executa onClick quando habilitado e acionado. |
| <a id="L73"></a>73 | <code>                            onClick = { answer(id) },</code> | Invoca/continua answer com os argumentos declarados. |
| <a id="L74"></a>74 | <code>                            enabled = incoming != null,</code> | Fornece o valor de enabled no contexto desta expressão. |
| <a id="L75"></a>75 | <code>                            modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L76"></a>76 | <code>                        ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L77"></a>77 | <code>                            Text(&quot;Atender&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L78"></a>78 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L79"></a>79 | <code>                        OutlinedButton(</code> | Invoca/continua OutlinedButton com os argumentos declarados. Cria controle com contorno e a ação onClick declarada. |
| <a id="L80"></a>80 | <code>                            onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L81"></a>81 | <code>                                sendBroadcast(</code> | Invoca/continua sendBroadcast com os argumentos declarados. |
| <a id="L82"></a>82 | <code>                                    Intent(</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L83"></a>83 | <code>                                            this@IncomingCallActivity,</code> | Fornece a expressão this@IncomingCallActivity, ao bloco/chamada em construção. |
| <a id="L84"></a>84 | <code>                                            CallRejectReceiver::class.java,</code> | Fornece a expressão CallRejectReceiver::class.java, ao bloco/chamada em construção. |
| <a id="L85"></a>85 | <code>                                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L86"></a>86 | <code>                                        .putExtra(&quot;event_id&quot;, id)</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L87"></a>87 | <code>                                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L88"></a>88 | <code>                            },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L89"></a>89 | <code>                            modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L90"></a>90 | <code>                        ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L91"></a>91 | <code>                            Text(&quot;Recusar&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L92"></a>92 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L93"></a>93 | <code>                        Spacer(Modifier.weight(1f))</code> | Invoca/continua Spacer com os argumentos declarados. |
| <a id="L94"></a>94 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L95"></a>95 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L96"></a>96 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L97"></a>97 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L98"></a>98 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L99"></a>99 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L100"></a>100 | <code>    // Documentação: Trata o callback de IncomingCallActivity.onPostResume, segundo o contrato e</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de IncomingCallActivity.onPostResume, segundo o contrato e |
| <a id="L101"></a>101 | <code>    // as verificações deste módulo.</code> | Comentário de manutenção/documentação: as verificações deste módulo. |
| <a id="L102"></a>102 | <code>    override fun onPostResume() {</code> | Trata o callback de IncomingCallActivity.onPostResume, segundo o contrato e as verificações deste módulo. |
| <a id="L103"></a>103 | <code>        super.onPostResume()</code> | Invoca/continua super.onPostResume com os argumentos declarados. |
| <a id="L104"></a>104 | <code>        if (answerRequested) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L105"></a>105 | <code>            answerRequested = false</code> | Fornece o valor de answerRequested no contexto desta expressão. |
| <a id="L106"></a>106 | <code>            intent.getStringExtra(&quot;event_id&quot;)?.let { answer(it) }</code> | Invoca/continua intent.getStringExtra com os argumentos declarados. Lê argumento textual do Intent para o fluxo indicado. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L107"></a>107 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L108"></a>108 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L109"></a>109 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L110"></a>110 | <code>    // Documentação: Solicita desbloqueio e encaminha internamente o event_id validado à interface</code> | Comentário de manutenção/documentação: Documentação: Solicita desbloqueio e encaminha internamente o event_id validado à interface |
| <a id="L111"></a>111 | <code>    // principal.</code> | Comentário de manutenção/documentação: principal. |
| <a id="L112"></a>112 | <code>    private fun answer(id: String) {</code> | Solicita desbloqueio e encaminha internamente o event_id validado à interface principal. |
| <a id="L113"></a>113 | <code>        val keyguard = getSystemService(KeyguardManager::class.java)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L114"></a>114 | <code>        // Documentação: Implementa IncomingCallActivity.open como parte do fluxo descrito para</code> | Comentário de manutenção/documentação: Documentação: Implementa IncomingCallActivity.open como parte do fluxo descrito para |
| <a id="L115"></a>115 | <code>        // este arquivo.</code> | Comentário de manutenção/documentação: este arquivo. |
| <a id="L116"></a>116 | <code>        fun open() {</code> | Implementa IncomingCallActivity.open como parte do fluxo descrito para este arquivo. |
| <a id="L117"></a>117 | <code>            if (incomingCall(AgentRuntime.received.value, id) == null) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L118"></a>118 | <code>                finish()</code> | Invoca/continua finish com os argumentos declarados. |
| <a id="L119"></a>119 | <code>                return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L120"></a>120 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L121"></a>121 | <code>            AgentRuntime.requestedAnswer.value = id</code> | Fornece a expressão AgentRuntime.requestedAnswer.value = id ao bloco/chamada em construção. |
| <a id="L122"></a>122 | <code>            startActivity(</code> | Invoca/continua startActivity com os argumentos declarados. |
| <a id="L123"></a>123 | <code>                Intent(this, MainActivity::class.java)</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L124"></a>124 | <code>                    .setAction(&quot;answer.$id&quot;)</code> | Invoca/continua setAction com os argumentos declarados. Define a ação que distingue este Intent/PendingIntent. |
| <a id="L125"></a>125 | <code>                    .addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)</code> | Invoca/continua addFlags com os argumentos declarados. |
| <a id="L126"></a>126 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L127"></a>127 | <code>            finish()</code> | Invoca/continua finish com os argumentos declarados. |
| <a id="L128"></a>128 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L129"></a>129 | <code>        if (!keyguard.isKeyguardLocked) open()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L130"></a>130 | <code>        else if (android.os.Build.VERSION.SDK_INT &gt;= 26)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L131"></a>131 | <code>            keyguard.requestDismissKeyguard(</code> | Invoca/continua keyguard.requestDismissKeyguard com os argumentos declarados. Pede ao Android desbloqueio; não contorna PIN/biometria do usuário. |
| <a id="L132"></a>132 | <code>                this,</code> | Fornece a expressão this, ao bloco/chamada em construção. |
| <a id="L133"></a>133 | <code>                object : KeyguardManager.KeyguardDismissCallback() {</code> | Invoca/continua KeyguardManager.KeyguardDismissCallback com os argumentos declarados. |
| <a id="L134"></a>134 | <code>                    // Documentação: Trata o callback de IncomingCallActivity.onDismissSucceeded,</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de IncomingCallActivity.onDismissSucceeded, |
| <a id="L135"></a>135 | <code>                    // segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: segundo o contrato e as verificações deste módulo. |
| <a id="L136"></a>136 | <code>                    override fun onDismissSucceeded() {</code> | Trata o callback de IncomingCallActivity.onDismissSucceeded, segundo o contrato e as verificações deste módulo. |
| <a id="L137"></a>137 | <code>                        open()</code> | Invoca/continua open com os argumentos declarados. |
| <a id="L138"></a>138 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L139"></a>139 | <code>                },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L140"></a>140 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L141"></a>141 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L142"></a>142 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
