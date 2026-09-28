# android/app/src/main/java/br/com/vegasolucoes/agent/CallRejectReceiver.kt

Recebe recusa de chamada por PendingIntent privado, chama Core com dispositivo autenticado e fecha notificação após confirmação; falha de rede exige nova tentativa.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/CallRejectReceiver.kt) · 42 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [CallRejectReceiver](#L13) | Define o tipo CallRejectReceiver e reúne o estado/contrato descrito para este módulo. |
| [CallRejectReceiver.onReceive](#L16) | Trata o callback de CallRejectReceiver.onReceive, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.content.BroadcastReceiver</code> | Disponibiliza o símbolo Kotlin/Android android.content.BroadcastReceiver neste arquivo. |
| <a id="L4"></a>4 | <code>import android.content.Context</code> | Disponibiliza o símbolo Kotlin/Android android.content.Context neste arquivo. |
| <a id="L5"></a>5 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L6"></a>6 | <code>import kotlinx.coroutines.CoroutineScope</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.CoroutineScope neste arquivo. |
| <a id="L7"></a>7 | <code>import kotlinx.coroutines.Dispatchers</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.Dispatchers neste arquivo. |
| <a id="L8"></a>8 | <code>import kotlinx.coroutines.launch</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.launch neste arquivo. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L9"></a>9 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L11"></a>11 | <code>// Documentação: Define o tipo CallRejectReceiver e reúne o estado/contrato descrito para este</code> | Comentário de manutenção/documentação: Documentação: Define o tipo CallRejectReceiver e reúne o estado/contrato descrito para este |
| <a id="L12"></a>12 | <code>// módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L13"></a>13 | <code>class CallRejectReceiver : BroadcastReceiver() {</code> | Define o tipo CallRejectReceiver e reúne o estado/contrato descrito para este módulo. |
| <a id="L14"></a>14 | <code>    // Documentação: Trata o callback de CallRejectReceiver.onReceive, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de CallRejectReceiver.onReceive, segundo o contrato e as |
| <a id="L15"></a>15 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L16"></a>16 | <code>    override fun onReceive(context: Context, intent: Intent) {</code> | Trata o callback de CallRejectReceiver.onReceive, segundo o contrato e as verificações deste módulo. |
| <a id="L17"></a>17 | <code>        val id = intent.getStringExtra(&quot;event_id&quot;) ?: return</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê argumento textual do Intent para o fluxo indicado. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L18"></a>18 | <code>        val session = AgentRuntime.auth.session.value ?: return</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L19"></a>19 | <code>        val pending = goAsync()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L20"></a>20 | <code>        CoroutineScope(Dispatchers.IO).launch {</code> | Invoca/continua CoroutineScope com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L21"></a>21 | <code>            try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L22"></a>22 | <code>                AgentRuntime.auth.api(</code> | Invoca/continua AgentRuntime.auth.api com os argumentos declarados. |
| <a id="L23"></a>23 | <code>                    &quot;/calls/incoming/$id/reject&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L24"></a>24 | <code>                    &quot;POST&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L25"></a>25 | <code>                    JSONObject().put(&quot;device_id&quot;, session.deviceId),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L26"></a>26 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L27"></a>27 | <code>                val event =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L28"></a>28 | <code>                    outgoing(</code> | Invoca/continua outgoing com os argumentos declarados. |
| <a id="L29"></a>29 | <code>                        &quot;call.dismissed&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L30"></a>30 | <code>                        JSONObject().put(&quot;event_id&quot;, id).put(&quot;status&quot;, &quot;REJECTED&quot;),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L31"></a>31 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L32"></a>32 | <code>                AgentRuntime.events.save(event)</code> | Invoca/continua AgentRuntime.events.save com os argumentos declarados. |
| <a id="L33"></a>33 | <code>                AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L34"></a>34 | <code>                AgentNotifications(context).cancel(id)</code> | Invoca/continua AgentNotifications com os argumentos declarados. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L35"></a>35 | <code>            } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L36"></a>36 | <code>                AgentRuntime.voiceStatus.value = &quot;Abra o aplicativo para recusar novamente.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Abra o aplicativo para recusar novamente.&quot; ao bloco/chamada em construção. |
| <a id="L37"></a>37 | <code>            } finally {</code> | Fornece a expressão } finally { ao bloco/chamada em construção. |
| <a id="L38"></a>38 | <code>                pending.finish()</code> | Invoca/continua pending.finish com os argumentos declarados. |
| <a id="L39"></a>39 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L40"></a>40 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L41"></a>41 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L42"></a>42 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
