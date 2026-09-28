# android/app/src/androidTest/java/br/com/vegasolucoes/agent/QueueTest.kt

Conjunto de validações de QueueTest. Fixtures preparam o ambiente; asserts verificam o comportamento observado, e cleanup remove os recursos de teste.

[Arquivo fonte](../../../../../../../../../../../android/app/src/androidTest/java/br/com/vegasolucoes/agent/QueueTest.kt) · 88 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [QueueTest](#L13) | Define o tipo QueueTest e reúne o estado/contrato descrito para este módulo. |
| [QueueTest.voiceQueueUsesCallIdentityAndStopsAfterEnd](#L17) | Implementa QueueTest.voiceQueueUsesCallIdentityAndStopsAfterEnd como parte do fluxo descrito para este arquivo. |
| [QueueTest.reconnectRetainsIdentityAndReplyMapsNextTurnAtomically](#L43) | Implementa QueueTest.reconnectRetainsIdentityAndReplyMapsNextTurnAtomically como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import androidx.test.ext.junit.runners.AndroidJUnit4</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.ext.junit.runners.AndroidJUnit4 neste arquivo. |
| <a id="L4"></a>4 | <code>import androidx.test.platform.app.InstrumentationRegistry</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.platform.app.InstrumentationRegistry neste arquivo. |
| <a id="L5"></a>5 | <code>import java.util.UUID</code> | Disponibiliza o símbolo Kotlin/Android java.util.UUID neste arquivo. |
| <a id="L6"></a>6 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L7"></a>7 | <code>import org.junit.Assert.*</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Assert.* neste arquivo. |
| <a id="L8"></a>8 | <code>import org.junit.Test</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Test neste arquivo. |
| <a id="L9"></a>9 | <code>import org.junit.runner.RunWith</code> | Disponibiliza o símbolo Kotlin/Android org.junit.runner.RunWith neste arquivo. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L11"></a>11 | <code>@RunWith(AndroidJUnit4::class)</code> | Aplica a anotação @RunWith(AndroidJUnit4::class) à declaração seguinte. |
| <a id="L12"></a>12 | <code>// Documentação: Define o tipo QueueTest e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo QueueTest e reúne o estado/contrato descrito para este módulo. |
| <a id="L13"></a>13 | <code>class QueueTest {</code> | Define o tipo QueueTest e reúne o estado/contrato descrito para este módulo. |
| <a id="L14"></a>14 | <code>    @Test</code> | Aplica a anotação @Test à declaração seguinte. |
| <a id="L15"></a>15 | <code>    // Documentação: Implementa QueueTest.voiceQueueUsesCallIdentityAndStopsAfterEnd como parte do</code> | Comentário de manutenção/documentação: Documentação: Implementa QueueTest.voiceQueueUsesCallIdentityAndStopsAfterEnd como parte do |
| <a id="L16"></a>16 | <code>    // fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: fluxo descrito para este arquivo. |
| <a id="L17"></a>17 | <code>    fun voiceQueueUsesCallIdentityAndStopsAfterEnd() {</code> | Implementa QueueTest.voiceQueueUsesCallIdentityAndStopsAfterEnd como parte do fluxo descrito para este arquivo. |
| <a id="L18"></a>18 | <code>        val context = InstrumentationRegistry.getInstrumentation().targetContext</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L19"></a>19 | <code>        val db = EventStore(context, SecureStore(context))</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L20"></a>20 | <code>        db.ensureOwner(&quot;voice-queue-test&quot;)</code> | Invoca/continua db.ensureOwner com os argumentos declarados. |
| <a id="L21"></a>21 | <code>        val call =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L22"></a>22 | <code>            JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L23"></a>23 | <code>                .put(&quot;id&quot;, UUID.randomUUID().toString())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L24"></a>24 | <code>                .put(&quot;conversation_id&quot;, UUID.randomUUID().toString())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L25"></a>25 | <code>                .put(&quot;reason&quot;, &quot;test&quot;)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L26"></a>26 | <code>        val message = db.enqueueVoice(call, &quot;Olá por voz&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Grava transcrição na fila durável vinculada à chamada. |
| <a id="L27"></a>27 | <code>        val frame = db.nextFrame()!!</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L28"></a>28 | <code>        assertEquals(&quot;voice.transcript&quot;, frame.getString(&quot;type&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L29"></a>29 | <code>        assertEquals(message, frame.getString(&quot;event_id&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L30"></a>30 | <code>        assertEquals(</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L31"></a>31 | <code>            call.getString(&quot;id&quot;),</code> | Invoca/continua call.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L32"></a>32 | <code>            frame.getJSONObject(&quot;payload&quot;).getString(&quot;call_session_id&quot;),</code> | Invoca/continua frame.getJSONObject com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L33"></a>33 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L34"></a>34 | <code>        db.cancelVoice(call.getString(&quot;id&quot;))</code> | Invoca/continua db.cancelVoice com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L35"></a>35 | <code>        assertNull(db.nextFrame())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L36"></a>36 | <code>        db.clear()</code> | Invoca/continua db.clear com os argumentos declarados. |
| <a id="L37"></a>37 | <code>        db.close()</code> | Invoca/continua db.close com os argumentos declarados. |
| <a id="L38"></a>38 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L39"></a>39 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L40"></a>40 | <code>    @Test</code> | Aplica a anotação @Test à declaração seguinte. |
| <a id="L41"></a>41 | <code>    // Documentação: Implementa QueueTest.reconnectRetainsIdentityAndReplyMapsNextTurnAtomically</code> | Comentário de manutenção/documentação: Documentação: Implementa QueueTest.reconnectRetainsIdentityAndReplyMapsNextTurnAtomically |
| <a id="L42"></a>42 | <code>    // como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: como parte do fluxo descrito para este arquivo. |
| <a id="L43"></a>43 | <code>    fun reconnectRetainsIdentityAndReplyMapsNextTurnAtomically() {</code> | Implementa QueueTest.reconnectRetainsIdentityAndReplyMapsNextTurnAtomically como parte do fluxo descrito para este arquivo. |
| <a id="L44"></a>44 | <code>        val context = InstrumentationRegistry.getInstrumentation().targetContext</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L45"></a>45 | <code>        val vault = SecureStore(context)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L46"></a>46 | <code>        val db = EventStore(context, vault)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L47"></a>47 | <code>        db.ensureOwner(&quot;test-owner-a&quot;)</code> | Invoca/continua db.ensureOwner com os argumentos declarados. Associação ao proprietário no registry/contrato do manager. |
| <a id="L48"></a>48 | <code>        val thread = db.newThread()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L49"></a>49 | <code>        val first = db.enqueue(thread, &quot;primeiro&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L50"></a>50 | <code>        val second = db.enqueue(thread, &quot;segundo&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L51"></a>51 | <code>        assertEquals(first, db.nextFrame()!!.getString(&quot;event_id&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L52"></a>52 | <code>        db.sent(first)</code> | Invoca/continua db.sent com os argumentos declarados. |
| <a id="L53"></a>53 | <code>        assertNull(db.nextFrame())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L54"></a>54 | <code>        db.close()</code> | Invoca/continua db.close com os argumentos declarados. |
| <a id="L55"></a>55 | <code>        val reopened = EventStore(context, vault)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L56"></a>56 | <code>        reopened.reconnect()</code> | Invoca/continua reopened.reconnect com os argumentos declarados. |
| <a id="L57"></a>57 | <code>        assertEquals(first, reopened.nextFrame()!!.getString(&quot;event_id&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L58"></a>58 | <code>        val conversation = UUID.randomUUID().toString()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L59"></a>59 | <code>        val event =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L60"></a>60 | <code>            JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L61"></a>61 | <code>                .put(&quot;event_id&quot;, UUID.randomUUID().toString())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L62"></a>62 | <code>                .put(&quot;type&quot;, &quot;agent.message&quot;)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L63"></a>63 | <code>                .put(</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L64"></a>64 | <code>                    &quot;payload&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L65"></a>65 | <code>                    JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L66"></a>66 | <code>                        .put(&quot;client_message_id&quot;, first)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L67"></a>67 | <code>                        .put(&quot;conversation_id&quot;, conversation)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L68"></a>68 | <code>                        .put(&quot;user_message_id&quot;, UUID.randomUUID().toString())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L69"></a>69 | <code>                        .put(&quot;assistant_message_id&quot;, UUID.randomUUID().toString())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L70"></a>70 | <code>                        .put(&quot;reply&quot;, &quot;resposta&quot;),</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L71"></a>71 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L72"></a>72 | <code>        assertTrue(reopened.save(event))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L73"></a>73 | <code>        assertFalse(reopened.save(event))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L74"></a>74 | <code>        assertEquals(second, reopened.nextFrame()!!.getString(&quot;event_id&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L75"></a>75 | <code>        assertEquals(</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L76"></a>76 | <code>            conversation,</code> | Fornece a expressão conversation, ao bloco/chamada em construção. |
| <a id="L77"></a>77 | <code>            reopened.nextFrame()!!.getJSONObject(&quot;payload&quot;).getString(&quot;conversation_id&quot;),</code> | Invoca/continua reopened.nextFrame com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L78"></a>78 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L79"></a>79 | <code>        assertEquals(3, reopened.bubbles(reopened.threads().first()).size)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L80"></a>80 | <code>        reopened.ensureOwner(&quot;test-owner-a&quot;)</code> | Invoca/continua reopened.ensureOwner com os argumentos declarados. Associação ao proprietário no registry/contrato do manager. |
| <a id="L81"></a>81 | <code>        assertEquals(1, reopened.threads().size)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L82"></a>82 | <code>        reopened.ensureOwner(&quot;test-owner-b&quot;)</code> | Invoca/continua reopened.ensureOwner com os argumentos declarados. Associação ao proprietário no registry/contrato do manager. |
| <a id="L83"></a>83 | <code>        assertTrue(reopened.threads().isEmpty())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L84"></a>84 | <code>        assertTrue(reopened.recent().isEmpty())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L85"></a>85 | <code>        reopened.clear()</code> | Invoca/continua reopened.clear com os argumentos declarados. |
| <a id="L86"></a>86 | <code>        reopened.close()</code> | Invoca/continua reopened.close com os argumentos declarados. |
| <a id="L87"></a>87 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L88"></a>88 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
