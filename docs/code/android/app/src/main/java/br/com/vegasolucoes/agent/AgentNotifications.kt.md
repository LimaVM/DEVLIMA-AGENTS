# android/app/src/main/java/br/com/vegasolucoes/agent/AgentNotifications.kt

Cria canais e notificações de conexão/lembrete/chamada, deduplica apresentação por evento e usa CallStyle/toque limitado à janela real de atendimento.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/AgentNotifications.kt) · 190 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [AgentNotifications](#L21) | Define o tipo AgentNotifications e reúne o estado/contrato descrito para este módulo. |
| [AgentNotifications.foreground](#L62) | Implementa AgentNotifications.foreground como parte do fluxo descrito para este arquivo. |
| [AgentNotifications.status](#L90) | Implementa AgentNotifications.status como parte do fluxo descrito para este arquivo. |
| [AgentNotifications.event](#L96) | Publica somente tipos notificáveis, cancela eventos resolvidos e limita toque de chamada ao tempo restante. |
| [AgentNotifications.cancel](#L187) | Cancela AgentNotifications.cancel, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.app.Notification</code> | Disponibiliza o símbolo Kotlin/Android android.app.Notification neste arquivo. |
| <a id="L5"></a>5 | <code>import android.app.NotificationChannel</code> | Disponibiliza o símbolo Kotlin/Android android.app.NotificationChannel neste arquivo. |
| <a id="L6"></a>6 | <code>import android.app.NotificationManager</code> | Disponibiliza o símbolo Kotlin/Android android.app.NotificationManager neste arquivo. |
| <a id="L7"></a>7 | <code>import android.app.PendingIntent</code> | Disponibiliza o símbolo Kotlin/Android android.app.PendingIntent neste arquivo. |
| <a id="L8"></a>8 | <code>import android.content.Context</code> | Disponibiliza o símbolo Kotlin/Android android.content.Context neste arquivo. |
| <a id="L9"></a>9 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L10"></a>10 | <code>import android.content.pm.PackageManager</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.PackageManager neste arquivo. |
| <a id="L11"></a>11 | <code>import android.media.AudioAttributes</code> | Disponibiliza o símbolo Kotlin/Android android.media.AudioAttributes neste arquivo. |
| <a id="L12"></a>12 | <code>import android.media.RingtoneManager</code> | Disponibiliza o símbolo Kotlin/Android android.media.RingtoneManager neste arquivo. |
| <a id="L13"></a>13 | <code>import android.os.Build</code> | Disponibiliza o símbolo Kotlin/Android android.os.Build neste arquivo. |
| <a id="L14"></a>14 | <code>import androidx.core.app.NotificationCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.app.NotificationCompat neste arquivo. |
| <a id="L15"></a>15 | <code>import androidx.core.app.Person</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.app.Person neste arquivo. |
| <a id="L16"></a>16 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L17"></a>17 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L18"></a>18 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L19"></a>19 | <code>// Documentação: Define o tipo AgentNotifications e reúne o estado/contrato descrito para este</code> | Comentário de manutenção/documentação: Documentação: Define o tipo AgentNotifications e reúne o estado/contrato descrito para este |
| <a id="L20"></a>20 | <code>// módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L21"></a>21 | <code>class AgentNotifications(private val context: Context) {</code> | Define o tipo AgentNotifications e reúne o estado/contrato descrito para este módulo. |
| <a id="L22"></a>22 | <code>    companion object {</code> | Fornece a expressão companion object { ao bloco/chamada em construção. |
| <a id="L23"></a>23 | <code>        const val CALL_CHANNEL = &quot;incoming_calls_v2&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L24"></a>24 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L26"></a>26 | <code>    private val manager = context.getSystemService(NotificationManager::class.java)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L27"></a>27 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L28"></a>28 | <code>    init {</code> | Fornece a expressão init { ao bloco/chamada em construção. |
| <a id="L29"></a>29 | <code>        manager.createNotificationChannel(</code> | Invoca/continua manager.createNotificationChannel com os argumentos declarados. |
| <a id="L30"></a>30 | <code>            NotificationChannel(</code> | Invoca/continua NotificationChannel com os argumentos declarados. |
| <a id="L31"></a>31 | <code>                &quot;connection&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L32"></a>32 | <code>                &quot;Conexão do agente&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L33"></a>33 | <code>                NotificationManager.IMPORTANCE_LOW,</code> | Fornece a expressão NotificationManager.IMPORTANCE_LOW, ao bloco/chamada em construção. |
| <a id="L34"></a>34 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L35"></a>35 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L36"></a>36 | <code>        manager.createNotificationChannel(</code> | Invoca/continua manager.createNotificationChannel com os argumentos declarados. |
| <a id="L37"></a>37 | <code>            NotificationChannel(&quot;reminders&quot;, &quot;Lembretes&quot;, NotificationManager.IMPORTANCE_HIGH)</code> | Invoca/continua NotificationChannel com os argumentos declarados. |
| <a id="L38"></a>38 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L39"></a>39 | <code>        manager.createNotificationChannel(</code> | Invoca/continua manager.createNotificationChannel com os argumentos declarados. |
| <a id="L40"></a>40 | <code>            NotificationChannel(</code> | Invoca/continua NotificationChannel com os argumentos declarados. |
| <a id="L41"></a>41 | <code>                    CALL_CHANNEL,</code> | Fornece a expressão CALL_CHANNEL, ao bloco/chamada em construção. |
| <a id="L42"></a>42 | <code>                    &quot;Chamadas internas&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L43"></a>43 | <code>                    NotificationManager.IMPORTANCE_HIGH,</code> | Fornece a expressão NotificationManager.IMPORTANCE_HIGH, ao bloco/chamada em construção. |
| <a id="L44"></a>44 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L45"></a>45 | <code>                .apply {</code> | Fornece a expressão .apply { ao bloco/chamada em construção. |
| <a id="L46"></a>46 | <code>                    description = &quot;Toque de chamadas recebidas do agente&quot;</code> | Fornece o valor de description no contexto desta expressão. |
| <a id="L47"></a>47 | <code>                    enableVibration(true)</code> | Invoca/continua enableVibration com os argumentos declarados. |
| <a id="L48"></a>48 | <code>                    setSound(</code> | Invoca/continua setSound com os argumentos declarados. Configura som do canal, respeitando alterações do usuário. |
| <a id="L49"></a>49 | <code>                        RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE),</code> | Invoca/continua RingtoneManager.getDefaultUri com os argumentos declarados. |
| <a id="L50"></a>50 | <code>                        AudioAttributes.Builder()</code> | Invoca/continua AudioAttributes.Builder com os argumentos declarados. |
| <a id="L51"></a>51 | <code>                            .setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE)</code> | Invoca/continua setUsage com os argumentos declarados. |
| <a id="L52"></a>52 | <code>                            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)</code> | Invoca/continua setContentType com os argumentos declarados. |
| <a id="L53"></a>53 | <code>                            .build(),</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L54"></a>54 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L55"></a>55 | <code>                    lockscreenVisibility = Notification.VISIBILITY_PRIVATE</code> | Fornece o valor de lockscreenVisibility no contexto desta expressão. |
| <a id="L56"></a>56 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L57"></a>57 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L58"></a>58 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L59"></a>59 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L60"></a>60 | <code>    // Documentação: Implementa AgentNotifications.foreground como parte do fluxo descrito para</code> | Comentário de manutenção/documentação: Documentação: Implementa AgentNotifications.foreground como parte do fluxo descrito para |
| <a id="L61"></a>61 | <code>    // este arquivo.</code> | Comentário de manutenção/documentação: este arquivo. |
| <a id="L62"></a>62 | <code>    fun foreground(text: String): Notification {</code> | Implementa AgentNotifications.foreground como parte do fluxo descrito para este arquivo. |
| <a id="L63"></a>63 | <code>        val open =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L64"></a>64 | <code>            PendingIntent.getActivity(</code> | Invoca/continua PendingIntent.getActivity com os argumentos declarados. |
| <a id="L65"></a>65 | <code>                context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L66"></a>66 | <code>                0,</code> | Fornece a expressão 0, ao bloco/chamada em construção. |
| <a id="L67"></a>67 | <code>                Intent(context, MainActivity::class.java),</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L68"></a>68 | <code>                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,</code> | Fornece a expressão PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT, ao bloco/chamada em construção. |
| <a id="L69"></a>69 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L70"></a>70 | <code>        val stop =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L71"></a>71 | <code>            PendingIntent.getService(</code> | Invoca/continua PendingIntent.getService com os argumentos declarados. |
| <a id="L72"></a>72 | <code>                context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L73"></a>73 | <code>                1,</code> | Fornece a expressão 1, ao bloco/chamada em construção. |
| <a id="L74"></a>74 | <code>                Intent(context, ConnectionService::class.java).setAction(ConnectionService.STOP),</code> | Invoca/continua Intent com os argumentos declarados. Define a ação que distingue este Intent/PendingIntent. |
| <a id="L75"></a>75 | <code>                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,</code> | Fornece a expressão PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT, ao bloco/chamada em construção. |
| <a id="L76"></a>76 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L77"></a>77 | <code>        return NotificationCompat.Builder(context, &quot;connection&quot;)</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L78"></a>78 | <code>            .setSmallIcon(R.drawable.ic_agent)</code> | Invoca/continua setSmallIcon com os argumentos declarados. |
| <a id="L79"></a>79 | <code>            .setContentTitle(&quot;DevLima Agent ativo&quot;)</code> | Invoca/continua setContentTitle com os argumentos declarados. |
| <a id="L80"></a>80 | <code>            .setContentText(text)</code> | Invoca/continua setContentText com os argumentos declarados. |
| <a id="L81"></a>81 | <code>            .setContentIntent(open)</code> | Invoca/continua setContentIntent com os argumentos declarados. Define destino aberto ao acionar o corpo da notificação. |
| <a id="L82"></a>82 | <code>            .setOngoing(true)</code> | Invoca/continua setOngoing com os argumentos declarados. Indica notificação associada a atividade/chamada em andamento. |
| <a id="L83"></a>83 | <code>            .setOnlyAlertOnce(true)</code> | Invoca/continua setOnlyAlertOnce com os argumentos declarados. Evita novo alerta sonoro ao atualizar a mesma notificação. |
| <a id="L84"></a>84 | <code>            .addAction(0, &quot;Desconectar&quot;, stop)</code> | Invoca/continua addAction com os argumentos declarados. |
| <a id="L85"></a>85 | <code>            .build()</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L86"></a>86 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L87"></a>87 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L88"></a>88 | <code>    // Documentação: Implementa AgentNotifications.status como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa AgentNotifications.status como parte do fluxo descrito para este |
| <a id="L89"></a>89 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L90"></a>90 | <code>    fun status(text: String) {</code> | Implementa AgentNotifications.status como parte do fluxo descrito para este arquivo. |
| <a id="L91"></a>91 | <code>        manager.notify(1, foreground(text))</code> | Invoca/continua manager.notify com os argumentos declarados. |
| <a id="L92"></a>92 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L93"></a>93 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L94"></a>94 | <code>    // Documentação: Publica somente tipos notificáveis, cancela eventos resolvidos e limita toque</code> | Comentário de manutenção/documentação: Documentação: Publica somente tipos notificáveis, cancela eventos resolvidos e limita toque |
| <a id="L95"></a>95 | <code>    // de chamada ao tempo restante.</code> | Comentário de manutenção/documentação: de chamada ao tempo restante. |
| <a id="L96"></a>96 | <code>    fun event(event: JSONObject) {</code> | Publica somente tipos notificáveis, cancela eventos resolvidos e limita toque de chamada ao tempo restante. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L97"></a>97 | <code>        val type = event.getString(&quot;type&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L98"></a>98 | <code>        if (type == &quot;call.dismissed&quot; &#124;&#124; type == &quot;call.state&quot;) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L99"></a>99 | <code>            cancel(event.getJSONObject(&quot;payload&quot;).getString(&quot;event_id&quot;))</code> | Invoca/continua cancel com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L100"></a>100 | <code>            return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L101"></a>101 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L102"></a>102 | <code>        if (type != &quot;reminder.triggered&quot; &amp;&amp; type != &quot;call.incoming&quot;) return</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L103"></a>103 | <code>        if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L104"></a>104 | <code>            Build.VERSION.SDK_INT &gt;= 33 &amp;&amp;</code> | Fornece a expressão Build.VERSION.SDK_INT &gt;= 33 &amp;&amp; ao bloco/chamada em construção. |
| <a id="L105"></a>105 | <code>                ContextCompat.checkSelfPermission(</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L106"></a>106 | <code>                    context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L107"></a>107 | <code>                    Manifest.permission.POST_NOTIFICATIONS,</code> | Fornece a expressão Manifest.permission.POST_NOTIFICATIONS, ao bloco/chamada em construção. |
| <a id="L108"></a>108 | <code>                ) != PackageManager.PERMISSION_GRANTED</code> | Fornece a expressão ) != PackageManager.PERMISSION_GRANTED ao bloco/chamada em construção. |
| <a id="L109"></a>109 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L110"></a>110 | <code>            return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L111"></a>111 | <code>        val call = type == &quot;call.incoming&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L112"></a>112 | <code>        val remaining = if (call) callRemainingMillis(event.optString(&quot;timestamp&quot;)) else 0L</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L113"></a>113 | <code>        if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L114"></a>114 | <code>            call &amp;&amp;</code> | Fornece a expressão call &amp;&amp; ao bloco/chamada em construção. |
| <a id="L115"></a>115 | <code>                (remaining == 0L &#124;&#124;</code> | Fornece a expressão (remaining == 0L &#124;&#124; ao bloco/chamada em construção. |
| <a id="L116"></a>116 | <code>                    incomingCall(AgentRuntime.received.value, event.getString(&quot;event_id&quot;)) == null)</code> | Invoca/continua incomingCall com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L117"></a>117 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L118"></a>118 | <code>            return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L119"></a>119 | <code>        val id = event.getString(&quot;event_id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L120"></a>120 | <code>        val payload = event.getJSONObject(&quot;payload&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L121"></a>121 | <code>        val open =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L122"></a>122 | <code>            PendingIntent.getActivity(</code> | Invoca/continua PendingIntent.getActivity com os argumentos declarados. |
| <a id="L123"></a>123 | <code>                context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L124"></a>124 | <code>                id.hashCode(),</code> | Invoca/continua id.hashCode com os argumentos declarados. |
| <a id="L125"></a>125 | <code>                Intent(</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L126"></a>126 | <code>                        context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L127"></a>127 | <code>                        if (call) IncomingCallActivity::class.java else MainActivity::class.java,</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L128"></a>128 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L129"></a>129 | <code>                    .setAction(&quot;event.$id&quot;)</code> | Invoca/continua setAction com os argumentos declarados. Define a ação que distingue este Intent/PendingIntent. |
| <a id="L130"></a>130 | <code>                    .putExtra(&quot;event_id&quot;, id),</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L131"></a>131 | <code>                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,</code> | Fornece a expressão PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT, ao bloco/chamada em construção. |
| <a id="L132"></a>132 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L133"></a>133 | <code>        val title = if (call) &quot;AGENTE ESTÁ LIGANDO&quot; else &quot;Lembrete do agente&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L134"></a>134 | <code>        val builder =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L135"></a>135 | <code>            NotificationCompat.Builder(context, if (call) CALL_CHANNEL else &quot;reminders&quot;)</code> | Invoca/continua NotificationCompat.Builder com os argumentos declarados. |
| <a id="L136"></a>136 | <code>                .setSmallIcon(R.drawable.ic_agent)</code> | Invoca/continua setSmallIcon com os argumentos declarados. |
| <a id="L137"></a>137 | <code>                .setContentTitle(title)</code> | Invoca/continua setContentTitle com os argumentos declarados. |
| <a id="L138"></a>138 | <code>                .setContentText(payload.optString(&quot;text&quot;, &quot;Abra o agente&quot;))</code> | Invoca/continua setContentText com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L139"></a>139 | <code>                .setStyle(NotificationCompat.BigTextStyle().bigText(payload.optString(&quot;text&quot;)))</code> | Invoca/continua setStyle com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L140"></a>140 | <code>                .setContentIntent(open)</code> | Invoca/continua setContentIntent com os argumentos declarados. Define destino aberto ao acionar o corpo da notificação. |
| <a id="L141"></a>141 | <code>                .setAutoCancel(!call)</code> | Invoca/continua setAutoCancel com os argumentos declarados. |
| <a id="L142"></a>142 | <code>                .setOnlyAlertOnce(true)</code> | Invoca/continua setOnlyAlertOnce com os argumentos declarados. Evita novo alerta sonoro ao atualizar a mesma notificação. |
| <a id="L143"></a>143 | <code>                .setVisibility(NotificationCompat.VISIBILITY_PRIVATE)</code> | Invoca/continua setVisibility com os argumentos declarados. Define a privacidade da notificação na tela bloqueada. |
| <a id="L144"></a>144 | <code>                .setCategory(</code> | Invoca/continua setCategory com os argumentos declarados. |
| <a id="L145"></a>145 | <code>                    if (call) NotificationCompat.CATEGORY_CALL</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L146"></a>146 | <code>                    else NotificationCompat.CATEGORY_REMINDER</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L147"></a>147 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L148"></a>148 | <code>        if (call) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L149"></a>149 | <code>            val answer =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L150"></a>150 | <code>                PendingIntent.getActivity(</code> | Invoca/continua PendingIntent.getActivity com os argumentos declarados. |
| <a id="L151"></a>151 | <code>                    context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L152"></a>152 | <code>                    id.hashCode() + 1,</code> | Invoca/continua id.hashCode com os argumentos declarados. |
| <a id="L153"></a>153 | <code>                    Intent(context, IncomingCallActivity::class.java)</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L154"></a>154 | <code>                        .setAction(&quot;answer.$id&quot;)</code> | Invoca/continua setAction com os argumentos declarados. Define a ação que distingue este Intent/PendingIntent. |
| <a id="L155"></a>155 | <code>                        .putExtra(&quot;event_id&quot;, id),</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L156"></a>156 | <code>                    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,</code> | Fornece a expressão PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT, ao bloco/chamada em construção. |
| <a id="L157"></a>157 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L158"></a>158 | <code>            val reject =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L159"></a>159 | <code>                PendingIntent.getBroadcast(</code> | Invoca/continua PendingIntent.getBroadcast com os argumentos declarados. |
| <a id="L160"></a>160 | <code>                    context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L161"></a>161 | <code>                    id.hashCode() + 2,</code> | Invoca/continua id.hashCode com os argumentos declarados. |
| <a id="L162"></a>162 | <code>                    Intent(context, CallRejectReceiver::class.java)</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L163"></a>163 | <code>                        .setAction(&quot;reject.$id&quot;)</code> | Invoca/continua setAction com os argumentos declarados. Define a ação que distingue este Intent/PendingIntent. |
| <a id="L164"></a>164 | <code>                        .putExtra(&quot;event_id&quot;, id),</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L165"></a>165 | <code>                    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,</code> | Fornece a expressão PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT, ao bloco/chamada em construção. |
| <a id="L166"></a>166 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L167"></a>167 | <code>            builder</code> | Fornece a expressão builder ao bloco/chamada em construção. |
| <a id="L168"></a>168 | <code>                .setStyle(</code> | Invoca/continua setStyle com os argumentos declarados. |
| <a id="L169"></a>169 | <code>                    NotificationCompat.CallStyle.forIncomingCall(</code> | Invoca/continua NotificationCompat.CallStyle.forIncomingCall com os argumentos declarados. |
| <a id="L170"></a>170 | <code>                        Person.Builder().setName(&quot;DevLima Agent&quot;).setImportant(true).build(),</code> | Invoca/continua Person.Builder com os argumentos declarados. |
| <a id="L171"></a>171 | <code>                        reject,</code> | Fornece a expressão reject, ao bloco/chamada em construção. |
| <a id="L172"></a>172 | <code>                        answer,</code> | Fornece a expressão answer, ao bloco/chamada em construção. |
| <a id="L173"></a>173 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L174"></a>174 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L175"></a>175 | <code>                .setOngoing(true)</code> | Invoca/continua setOngoing com os argumentos declarados. Indica notificação associada a atividade/chamada em andamento. |
| <a id="L176"></a>176 | <code>                .setTimeoutAfter(remaining)</code> | Invoca/continua setTimeoutAfter com os argumentos declarados. Limita permanência da notificação ao tempo indicado. |
| <a id="L177"></a>177 | <code>            if (Build.VERSION.SDK_INT &lt; 34 &#124;&#124; manager.canUseFullScreenIntent())</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Confere a autorização de tela cheia antes de solicitar apresentação da chamada. |
| <a id="L178"></a>178 | <code>                builder.setFullScreenIntent(open, true)</code> | Invoca/continua builder.setFullScreenIntent com os argumentos declarados. Solicita tela de chamada quando o sistema autorizar. |
| <a id="L179"></a>179 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L180"></a>180 | <code>        val notification = builder.build()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L181"></a>181 | <code>        if (call) notification.flags = notification.flags or Notification.FLAG_INSISTENT</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Solicita repetição do toque até cancelamento/timeout da notificação. |
| <a id="L182"></a>182 | <code>        manager.notify(id, 2, notification)</code> | Invoca/continua manager.notify com os argumentos declarados. |
| <a id="L183"></a>183 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L184"></a>184 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L185"></a>185 | <code>    // Documentação: Cancela AgentNotifications.cancel, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Cancela AgentNotifications.cancel, segundo o contrato e as verificações deste |
| <a id="L186"></a>186 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L187"></a>187 | <code>    fun cancel(id: String) {</code> | Cancela AgentNotifications.cancel, segundo o contrato e as verificações deste módulo. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L188"></a>188 | <code>        manager.cancel(id, 2)</code> | Invoca/continua manager.cancel com os argumentos declarados. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L189"></a>189 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L190"></a>190 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
