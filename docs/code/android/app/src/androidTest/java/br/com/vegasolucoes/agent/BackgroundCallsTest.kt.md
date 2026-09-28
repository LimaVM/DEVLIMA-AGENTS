# android/app/src/androidTest/java/br/com/vegasolucoes/agent/BackgroundCallsTest.kt

Conjunto de validações de BackgroundCallsTest. Fixtures preparam o ambiente; asserts verificam o comportamento observado, e cleanup remove os recursos de teste.

[Arquivo fonte](../../../../../../../../../../../android/app/src/androidTest/java/br/com/vegasolucoes/agent/BackgroundCallsTest.kt) · 154 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [BackgroundCallsTest](#L26) | Define o tipo BackgroundCallsTest e reúne o estado/contrato descrito para este módulo. |
| [BackgroundCallsTest.await](#L32) | Implementa BackgroundCallsTest.await como parte do fluxo descrito para este arquivo. |
| [BackgroundCallsTest.connect](#L43) | Implementa BackgroundCallsTest.connect como parte do fluxo descrito para este arquivo. |
| [BackgroundCallsTest.loginAndConnectForExternalIdleProbe](#L79) | Implementa BackgroundCallsTest.loginAndConnectForExternalIdleProbe como parte do fluxo descrito para este arquivo. |
| [BackgroundCallsTest.removedTaskAndLockedScreenReceiveCall](#L86) | Implementa BackgroundCallsTest.removedTaskAndLockedScreenReceiveCall como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.app.ActivityManager</code> | Disponibiliza o símbolo Kotlin/Android android.app.ActivityManager neste arquivo. |
| <a id="L5"></a>5 | <code>import android.app.Notification</code> | Disponibiliza o símbolo Kotlin/Android android.app.Notification neste arquivo. |
| <a id="L6"></a>6 | <code>import android.app.NotificationManager</code> | Disponibiliza o símbolo Kotlin/Android android.app.NotificationManager neste arquivo. |
| <a id="L7"></a>7 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L8"></a>8 | <code>import android.os.SystemClock</code> | Disponibiliza o símbolo Kotlin/Android android.os.SystemClock neste arquivo. |
| <a id="L9"></a>9 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L10"></a>10 | <code>import androidx.test.ext.junit.runners.AndroidJUnit4</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.ext.junit.runners.AndroidJUnit4 neste arquivo. |
| <a id="L11"></a>11 | <code>import androidx.test.platform.app.InstrumentationRegistry</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.platform.app.InstrumentationRegistry neste arquivo. |
| <a id="L12"></a>12 | <code>import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry neste arquivo. |
| <a id="L13"></a>13 | <code>import androidx.test.runner.lifecycle.Stage</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.runner.lifecycle.Stage neste arquivo. |
| <a id="L14"></a>14 | <code>import java.io.File</code> | Disponibiliza o símbolo Kotlin/Android java.io.File neste arquivo. |
| <a id="L15"></a>15 | <code>import java.time.Instant</code> | Disponibiliza o símbolo Kotlin/Android java.time.Instant neste arquivo. |
| <a id="L16"></a>16 | <code>import kotlinx.coroutines.runBlocking</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.runBlocking neste arquivo. |
| <a id="L17"></a>17 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L18"></a>18 | <code>import org.junit.Assert.*</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Assert.* neste arquivo. |
| <a id="L19"></a>19 | <code>import org.junit.Assume.assumeTrue</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Assume.assumeTrue neste arquivo. |
| <a id="L20"></a>20 | <code>import org.junit.Test</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Test neste arquivo. |
| <a id="L21"></a>21 | <code>import org.junit.runner.RunWith</code> | Disponibiliza o símbolo Kotlin/Android org.junit.runner.RunWith neste arquivo. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L23"></a>23 | <code>@RunWith(AndroidJUnit4::class)</code> | Aplica a anotação @RunWith(AndroidJUnit4::class) à declaração seguinte. |
| <a id="L24"></a>24 | <code>// Documentação: Define o tipo BackgroundCallsTest e reúne o estado/contrato descrito para este</code> | Comentário de manutenção/documentação: Documentação: Define o tipo BackgroundCallsTest e reúne o estado/contrato descrito para este |
| <a id="L25"></a>25 | <code>// módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L26"></a>26 | <code>class BackgroundCallsTest {</code> | Define o tipo BackgroundCallsTest e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>    private val instrumentation = InstrumentationRegistry.getInstrumentation()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L28"></a>28 | <code>    private val context = instrumentation.targetContext</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L29"></a>29 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L30"></a>30 | <code>    // Documentação: Implementa BackgroundCallsTest.await como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa BackgroundCallsTest.await como parte do fluxo descrito para este |
| <a id="L31"></a>31 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L32"></a>32 | <code>    private fun await(label: String, condition: () -&gt; Boolean) {</code> | Implementa BackgroundCallsTest.await como parte do fluxo descrito para este arquivo. |
| <a id="L33"></a>33 | <code>        val deadline = SystemClock.elapsedRealtime() + 45000</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L34"></a>34 | <code>        while (SystemClock.elapsedRealtime() &lt; deadline) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L35"></a>35 | <code>            if (condition()) return</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L36"></a>36 | <code>            Thread.sleep(250)</code> | Invoca/continua Thread.sleep com os argumentos declarados. |
| <a id="L37"></a>37 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L38"></a>38 | <code>        throw AssertionError(&quot;Timeout: $label&quot;)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L39"></a>39 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L40"></a>40 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L41"></a>41 | <code>    // Documentação: Implementa BackgroundCallsTest.connect como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa BackgroundCallsTest.connect como parte do fluxo descrito para este |
| <a id="L42"></a>42 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L43"></a>43 | <code>    private fun connect() {</code> | Implementa BackgroundCallsTest.connect como parte do fluxo descrito para este arquivo. |
| <a id="L44"></a>44 | <code>        val file = File(context.noBackupFilesDir, &quot;e2e-private.json&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L45"></a>45 | <code>        assumeTrue(&quot;Isolated, private configuration required&quot;, file.exists())</code> | Invoca/continua assumeTrue com os argumentos declarados. |
| <a id="L46"></a>46 | <code>        val credentials = JSONObject(file.readText())</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L47"></a>47 | <code>        require(credentials.getString(&quot;username&quot;).startsWith(&quot;devlima-v1-validation&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L48"></a>48 | <code>        runBlocking {</code> | Fornece a expressão runBlocking { ao bloco/chamada em construção. |
| <a id="L49"></a>49 | <code>            AgentRuntime.auth.login(</code> | Invoca/continua AgentRuntime.auth.login com os argumentos declarados. |
| <a id="L50"></a>50 | <code>                credentials.getString(&quot;server&quot;),</code> | Invoca/continua credentials.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L51"></a>51 | <code>                credentials.getString(&quot;username&quot;),</code> | Invoca/continua credentials.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L52"></a>52 | <code>                credentials.getString(&quot;password&quot;),</code> | Invoca/continua credentials.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L53"></a>53 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L54"></a>54 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L55"></a>55 | <code>        file.delete()</code> | Invoca/continua file.delete com os argumentos declarados. |
| <a id="L56"></a>56 | <code>        instrumentation.uiAutomation</code> | Fornece a expressão instrumentation.uiAutomation ao bloco/chamada em construção. |
| <a id="L57"></a>57 | <code>            .executeShellCommand(</code> | Invoca/continua executeShellCommand com os argumentos declarados. |
| <a id="L58"></a>58 | <code>                &quot;pm grant ${context.packageName} ${Manifest.permission.POST_NOTIFICATIONS}&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L59"></a>59 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L60"></a>60 | <code>            .close()</code> | Invoca/continua close com os argumentos declarados. |
| <a id="L61"></a>61 | <code>        instrumentation.runOnMainSync {</code> | Fornece a expressão instrumentation.runOnMainSync { ao bloco/chamada em construção. |
| <a id="L62"></a>62 | <code>            context.startActivity(</code> | Invoca/continua context.startActivity com os argumentos declarados. |
| <a id="L63"></a>63 | <code>                Intent(context, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L64"></a>64 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L65"></a>65 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L66"></a>66 | <code>        Thread.sleep(1000)</code> | Invoca/continua Thread.sleep com os argumentos declarados. |
| <a id="L67"></a>67 | <code>        instrumentation.runOnMainSync {</code> | Fornece a expressão instrumentation.runOnMainSync { ao bloco/chamada em construção. |
| <a id="L68"></a>68 | <code>            ContextCompat.startForegroundService(</code> | Invoca/continua ContextCompat.startForegroundService com os argumentos declarados. Solicita início do serviço; as restrições de background do Android continuam valendo. |
| <a id="L69"></a>69 | <code>                context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L70"></a>70 | <code>                Intent(context, ConnectionService::class.java),</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L71"></a>71 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L72"></a>72 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L73"></a>73 | <code>        await(&quot;connected&quot;) { AgentRuntime.connection.value == &quot;Conectado&quot; }</code> | Invoca/continua await com os argumentos declarados. |
| <a id="L74"></a>74 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L75"></a>75 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L76"></a>76 | <code>    @Test</code> | Aplica a anotação @Test à declaração seguinte. |
| <a id="L77"></a>77 | <code>    // Documentação: Implementa BackgroundCallsTest.loginAndConnectForExternalIdleProbe como parte</code> | Comentário de manutenção/documentação: Documentação: Implementa BackgroundCallsTest.loginAndConnectForExternalIdleProbe como parte |
| <a id="L78"></a>78 | <code>    // do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: do fluxo descrito para este arquivo. |
| <a id="L79"></a>79 | <code>    fun loginAndConnectForExternalIdleProbe() {</code> | Implementa BackgroundCallsTest.loginAndConnectForExternalIdleProbe como parte do fluxo descrito para este arquivo. |
| <a id="L80"></a>80 | <code>        connect()</code> | Invoca/continua connect com os argumentos declarados. |
| <a id="L81"></a>81 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L82"></a>82 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L83"></a>83 | <code>    @Test</code> | Aplica a anotação @Test à declaração seguinte. |
| <a id="L84"></a>84 | <code>    // Documentação: Implementa BackgroundCallsTest.removedTaskAndLockedScreenReceiveCall como</code> | Comentário de manutenção/documentação: Documentação: Implementa BackgroundCallsTest.removedTaskAndLockedScreenReceiveCall como |
| <a id="L85"></a>85 | <code>    // parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: parte do fluxo descrito para este arquivo. |
| <a id="L86"></a>86 | <code>    fun removedTaskAndLockedScreenReceiveCall() {</code> | Implementa BackgroundCallsTest.removedTaskAndLockedScreenReceiveCall como parte do fluxo descrito para este arquivo. |
| <a id="L87"></a>87 | <code>        connect()</code> | Invoca/continua connect com os argumentos declarados. |
| <a id="L88"></a>88 | <code>        val schedule = runBlocking {</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L89"></a>89 | <code>            JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L90"></a>90 | <code>                AgentRuntime.auth.api(</code> | Invoca/continua AgentRuntime.auth.api com os argumentos declarados. |
| <a id="L91"></a>91 | <code>                    &quot;/scheduled-calls&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L92"></a>92 | <code>                    &quot;POST&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L93"></a>93 | <code>                    JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L94"></a>94 | <code>                        .put(&quot;reason&quot;, &quot;Teste de chamada com interface fechada&quot;)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L95"></a>95 | <code>                        .put(&quot;datetime&quot;, Instant.now().plusSeconds(12).toString()),</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L96"></a>96 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L97"></a>97 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L98"></a>98 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L99"></a>99 | <code>        instrumentation.runOnMainSync {</code> | Fornece a expressão instrumentation.runOnMainSync { ao bloco/chamada em construção. |
| <a id="L100"></a>100 | <code>            context.getSystemService(ActivityManager::class.java).appTasks.forEach {</code> | Invoca/continua context.getSystemService com os argumentos declarados. |
| <a id="L101"></a>101 | <code>                it.finishAndRemoveTask()</code> | Invoca/continua it.finishAndRemoveTask com os argumentos declarados. |
| <a id="L102"></a>102 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L103"></a>103 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L104"></a>104 | <code>        instrumentation.uiAutomation.executeShellCommand(&quot;input keyevent 223&quot;).close()</code> | Invoca/continua instrumentation.uiAutomation.executeShellCommand com os argumentos declarados. |
| <a id="L105"></a>105 | <code>        try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L106"></a>106 | <code>            await(&quot;incoming after task removal&quot;) {</code> | Invoca/continua await com os argumentos declarados. |
| <a id="L107"></a>107 | <code>                AgentRuntime.received.value.any {</code> | Fornece a expressão AgentRuntime.received.value.any { ao bloco/chamada em construção. |
| <a id="L108"></a>108 | <code>                    it.optString(&quot;type&quot;) == &quot;call.incoming&quot; &amp;&amp;</code> | Invoca/continua it.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L109"></a>109 | <code>                        it.getJSONObject(&quot;payload&quot;).optString(&quot;schedule_id&quot;) ==</code> | Invoca/continua it.getJSONObject com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L110"></a>110 | <code>                            schedule.getString(&quot;id&quot;)</code> | Invoca/continua schedule.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L111"></a>111 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L112"></a>112 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L113"></a>113 | <code>            val event =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L114"></a>114 | <code>                AgentRuntime.received.value.first {</code> | Fornece a expressão AgentRuntime.received.value.first { ao bloco/chamada em construção. |
| <a id="L115"></a>115 | <code>                    it.optString(&quot;type&quot;) == &quot;call.incoming&quot; &amp;&amp;</code> | Invoca/continua it.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L116"></a>116 | <code>                        it.getJSONObject(&quot;payload&quot;).optString(&quot;schedule_id&quot;) ==</code> | Invoca/continua it.getJSONObject com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L117"></a>117 | <code>                            schedule.getString(&quot;id&quot;)</code> | Invoca/continua schedule.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L118"></a>118 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L119"></a>119 | <code>            val id = event.getString(&quot;event_id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L120"></a>120 | <code>            val manager = context.getSystemService(NotificationManager::class.java)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L121"></a>121 | <code>            await(&quot;ringing notification&quot;) { manager.activeNotifications.any { it.tag == id } }</code> | Invoca/continua await com os argumentos declarados. |
| <a id="L122"></a>122 | <code>            val notification = manager.activeNotifications.first { it.tag == id }.notification</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L123"></a>123 | <code>            assertEquals(Notification.CATEGORY_CALL, notification.category)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L124"></a>124 | <code>            assertTrue(notification.flags and Notification.FLAG_INSISTENT != 0)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Solicita repetição do toque até cancelamento/timeout da notificação. |
| <a id="L125"></a>125 | <code>            assertNotNull(notification.fullScreenIntent)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L126"></a>126 | <code>            assertEquals(</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L127"></a>127 | <code>                &quot;android.app.Notification\$CallStyle&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L128"></a>128 | <code>                notification.extras.getString(Notification.EXTRA_TEMPLATE),</code> | Invoca/continua notification.extras.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L129"></a>129 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L130"></a>130 | <code>            assertNotNull(&quot;Persistent connection survives closing its task&quot;, AgentRuntime.sender)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L131"></a>131 | <code>            await(&quot;incoming UI above lock screen&quot;) {</code> | Invoca/continua await com os argumentos declarados. |
| <a id="L132"></a>132 | <code>                var visible = false</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L133"></a>133 | <code>                instrumentation.runOnMainSync {</code> | Fornece a expressão instrumentation.runOnMainSync { ao bloco/chamada em construção. |
| <a id="L134"></a>134 | <code>                    visible =</code> | Fornece o valor de visible no contexto desta expressão. |
| <a id="L135"></a>135 | <code>                        ActivityLifecycleMonitorRegistry.getInstance()</code> | Invoca/continua ActivityLifecycleMonitorRegistry.getInstance com os argumentos declarados. |
| <a id="L136"></a>136 | <code>                            .getActivitiesInStage(Stage.RESUMED)</code> | Invoca/continua getActivitiesInStage com os argumentos declarados. |
| <a id="L137"></a>137 | <code>                            .any { it is IncomingCallActivity }</code> | Fornece a expressão .any { it is IncomingCallActivity } ao bloco/chamada em construção. |
| <a id="L138"></a>138 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L139"></a>139 | <code>                visible</code> | Fornece a expressão visible ao bloco/chamada em construção. |
| <a id="L140"></a>140 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L141"></a>141 | <code>            assertNull(</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L142"></a>142 | <code>                &quot;Incoming call must not activate microphone before answer&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L143"></a>143 | <code>                AgentRuntime.voice.value,</code> | Fornece a expressão AgentRuntime.voice.value, ao bloco/chamada em construção. |
| <a id="L144"></a>144 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L145"></a>145 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L146"></a>146 | <code>            context.sendBroadcast(</code> | Invoca/continua context.sendBroadcast com os argumentos declarados. |
| <a id="L147"></a>147 | <code>                Intent(context, CallRejectReceiver::class.java).putExtra(&quot;event_id&quot;, id)</code> | Invoca/continua Intent com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L148"></a>148 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L149"></a>149 | <code>            await(&quot;reject stops ringing&quot;) { manager.activeNotifications.none { it.tag == id } }</code> | Invoca/continua await com os argumentos declarados. |
| <a id="L150"></a>150 | <code>        } finally {</code> | Fornece a expressão } finally { ao bloco/chamada em construção. |
| <a id="L151"></a>151 | <code>            instrumentation.uiAutomation.executeShellCommand(&quot;input keyevent 224&quot;).close()</code> | Invoca/continua instrumentation.uiAutomation.executeShellCommand com os argumentos declarados. |
| <a id="L152"></a>152 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L153"></a>153 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L154"></a>154 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
