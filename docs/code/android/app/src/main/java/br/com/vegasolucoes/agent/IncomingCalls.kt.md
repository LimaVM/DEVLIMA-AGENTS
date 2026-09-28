# android/app/src/main/java/br/com/vegasolucoes/agent/IncomingCalls.kt

Seleciona eventos de chamada ainda atendíveis e calcula tempo remanescente sem renovar a janela ao receber replay atrasado.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/IncomingCalls.kt) · 31 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [callRemainingMillis](#L10) | Calcula a janela restante de 120 segundos; valores inválidos, antigos ou muito futuros não tornam a chamada atendível. |
| [incomingCall](#L19) | Seleciona chamada ainda não resolvida, opcionalmente por event_id, dentro do prazo de atendimento. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import java.time.Duration</code> | Disponibiliza o símbolo Kotlin/Android java.time.Duration neste arquivo. |
| <a id="L4"></a>4 | <code>import java.time.Instant</code> | Disponibiliza o símbolo Kotlin/Android java.time.Instant neste arquivo. |
| <a id="L5"></a>5 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L7"></a>7 | <code>// Never ring a delayed outbox replay beyond the server&#x27;s answer window.</code> | Comentário de manutenção/documentação: Never ring a delayed outbox replay beyond the server&#x27;s answer window. |
| <a id="L8"></a>8 | <code>// Documentação: Calcula a janela restante de 120 segundos; valores inválidos, antigos ou muito</code> | Comentário de manutenção/documentação: Documentação: Calcula a janela restante de 120 segundos; valores inválidos, antigos ou muito |
| <a id="L9"></a>9 | <code>// futuros não tornam a chamada atendível.</code> | Comentário de manutenção/documentação: futuros não tornam a chamada atendível. |
| <a id="L10"></a>10 | <code>fun callRemainingMillis(timestamp: String, now: Instant = Instant.now()): Long = runCatching {</code> | Calcula a janela restante de 120 segundos; valores inválidos, antigos ou muito futuros não tornam a chamada atendível. |
| <a id="L11"></a>11 | <code>    val started = Instant.parse(timestamp)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L12"></a>12 | <code>    if (started.isAfter(now.plusSeconds(5))) 0L</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L13"></a>13 | <code>    else Duration.between(now, started.plusSeconds(120)).toMillis().coerceIn(0L, 120000L)</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L14"></a>14 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L15"></a>15 | <code>    .getOrDefault(0L)</code> | Invoca/continua getOrDefault com os argumentos declarados. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L17"></a>17 | <code>// Documentação: Seleciona chamada ainda não resolvida, opcionalmente por event_id, dentro do</code> | Comentário de manutenção/documentação: Documentação: Seleciona chamada ainda não resolvida, opcionalmente por event_id, dentro do |
| <a id="L18"></a>18 | <code>// prazo de atendimento.</code> | Comentário de manutenção/documentação: prazo de atendimento. |
| <a id="L19"></a>19 | <code>fun incomingCall(events: List&lt;JSONObject&gt;, id: String? = null): JSONObject? {</code> | Seleciona chamada ainda não resolvida, opcionalmente por event_id, dentro do prazo de atendimento. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L20"></a>20 | <code>    val resolved =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L21"></a>21 | <code>        events</code> | Fornece a expressão events ao bloco/chamada em construção. |
| <a id="L22"></a>22 | <code>            .filter { it.optString(&quot;type&quot;) in setOf(&quot;call.dismissed&quot;, &quot;call.state&quot;) }</code> | Invoca/continua it.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L23"></a>23 | <code>            .map { it.getJSONObject(&quot;payload&quot;).optString(&quot;event_id&quot;) }</code> | Invoca/continua it.getJSONObject com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L24"></a>24 | <code>            .toSet()</code> | Invoca/continua toSet com os argumentos declarados. |
| <a id="L25"></a>25 | <code>    return events.firstOrNull {</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L26"></a>26 | <code>        it.optString(&quot;type&quot;) == &quot;call.incoming&quot; &amp;&amp;</code> | Invoca/continua it.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L27"></a>27 | <code>            (id == null &#124;&#124; it.optString(&quot;event_id&quot;) == id) &amp;&amp;</code> | Invoca/continua it.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L28"></a>28 | <code>            it.optString(&quot;event_id&quot;) !in resolved &amp;&amp;</code> | Invoca/continua it.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L29"></a>29 | <code>            callRemainingMillis(it.optString(&quot;timestamp&quot;)) &gt; 0</code> | Invoca/continua callRemainingMillis com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L30"></a>30 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L31"></a>31 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
