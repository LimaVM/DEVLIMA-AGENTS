# android/app/src/androidTest/java/br/com/vegasolucoes/agent/StorageTest.kt

Conjunto de validações de StorageTest. Fixtures preparam o ambiente; asserts verificam o comportamento observado, e cleanup remove os recursos de teste.

[Arquivo fonte](../../../../../../../../../../../android/app/src/androidTest/java/br/com/vegasolucoes/agent/StorageTest.kt) · 61 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [StorageTest](#L14) | Define o tipo StorageTest e reúne o estado/contrato descrito para este módulo. |
| [StorageTest.credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate](#L19) | Implementa StorageTest.credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import androidx.test.ext.junit.runners.AndroidJUnit4</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.ext.junit.runners.AndroidJUnit4 neste arquivo. |
| <a id="L4"></a>4 | <code>import androidx.test.platform.app.InstrumentationRegistry</code> | Disponibiliza o símbolo Kotlin/Android androidx.test.platform.app.InstrumentationRegistry neste arquivo. |
| <a id="L5"></a>5 | <code>import java.io.File</code> | Disponibiliza o símbolo Kotlin/Android java.io.File neste arquivo. |
| <a id="L6"></a>6 | <code>import java.util.UUID</code> | Disponibiliza o símbolo Kotlin/Android java.util.UUID neste arquivo. |
| <a id="L7"></a>7 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L8"></a>8 | <code>import org.junit.Assert.*</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Assert.* neste arquivo. |
| <a id="L9"></a>9 | <code>import org.junit.Test</code> | Disponibiliza o símbolo Kotlin/Android org.junit.Test neste arquivo. |
| <a id="L10"></a>10 | <code>import org.junit.runner.RunWith</code> | Disponibiliza o símbolo Kotlin/Android org.junit.runner.RunWith neste arquivo. |
| <a id="L11"></a>11 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L12"></a>12 | <code>@RunWith(AndroidJUnit4::class)</code> | Aplica a anotação @RunWith(AndroidJUnit4::class) à declaração seguinte. |
| <a id="L13"></a>13 | <code>// Documentação: Define o tipo StorageTest e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo StorageTest e reúne o estado/contrato descrito para este módulo. |
| <a id="L14"></a>14 | <code>class StorageTest {</code> | Define o tipo StorageTest e reúne o estado/contrato descrito para este módulo. |
| <a id="L15"></a>15 | <code>    @Test</code> | Aplica a anotação @Test à declaração seguinte. |
| <a id="L16"></a>16 | <code>    // Documentação: Implementa</code> | Comentário de manutenção/documentação: Documentação: Implementa |
| <a id="L17"></a>17 | <code>    // StorageTest.credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate como parte do</code> | Comentário de manutenção/documentação: StorageTest.credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate como parte do |
| <a id="L18"></a>18 | <code>    // fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: fluxo descrito para este arquivo. |
| <a id="L19"></a>19 | <code>    fun credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate() {</code> | Implementa StorageTest.credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate como parte do fluxo descrito para este arquivo. |
| <a id="L20"></a>20 | <code>        val context = InstrumentationRegistry.getInstrumentation().targetContext</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L21"></a>21 | <code>        val vault = SecureStore(context)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L22"></a>22 | <code>        val device = vault.deviceId()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L23"></a>23 | <code>        val data =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L24"></a>24 | <code>            SessionData(</code> | Invoca/continua SessionData com os argumentos declarados. |
| <a id="L25"></a>25 | <code>                &quot;https://agent.vegasolucoes.com.br&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L26"></a>26 | <code>                &quot;fake-test-access-not-a-real-token&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L27"></a>27 | <code>                &quot;fake-test-refresh-not-a-real-token&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L28"></a>28 | <code>                1234567890L,</code> | Fornece a expressão 1234567890L, ao bloco/chamada em construção. |
| <a id="L29"></a>29 | <code>                device,</code> | Fornece a expressão device, ao bloco/chamada em construção. |
| <a id="L30"></a>30 | <code>                &quot;test&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L31"></a>31 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L32"></a>32 | <code>        vault.save(data)</code> | Invoca/continua vault.save com os argumentos declarados. |
| <a id="L33"></a>33 | <code>        assertEquals(data, vault.load())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L34"></a>34 | <code>        assertFalse(File(context.noBackupFilesDir, &quot;session.bin&quot;).readText().contains(data.access))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L35"></a>35 | <code>        val event =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L36"></a>36 | <code>            JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L37"></a>37 | <code>                .put(&quot;event_id&quot;, UUID.randomUUID().toString())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L38"></a>38 | <code>                .put(&quot;type&quot;, &quot;reminder.triggered&quot;)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L39"></a>39 | <code>                .put(&quot;payload&quot;, JSONObject().put(&quot;text&quot;, &quot;storage-test-coffee&quot;))</code> | Invoca/continua put com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L40"></a>40 | <code>        val store = EventStore(context, vault)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L41"></a>41 | <code>        assertTrue(store.save(event))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L42"></a>42 | <code>        assertFalse(store.save(event))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L43"></a>43 | <code>        store.notified(event.getString(&quot;event_id&quot;))</code> | Invoca/continua store.notified com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L44"></a>44 | <code>        store.close()</code> | Invoca/continua store.close com os argumentos declarados. |
| <a id="L45"></a>45 | <code>        val reopened = EventStore(context, SecureStore(context))</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L46"></a>46 | <code>        assertTrue(</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L47"></a>47 | <code>            reopened.recent().any { it.getString(&quot;event_id&quot;) == event.getString(&quot;event_id&quot;) }</code> | Invoca/continua reopened.recent com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L48"></a>48 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L49"></a>49 | <code>        assertFalse(reopened.shouldNotify(event.getString(&quot;event_id&quot;)))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L50"></a>50 | <code>        reopened.readableDatabase</code> | Fornece a expressão reopened.readableDatabase ao bloco/chamada em construção. |
| <a id="L51"></a>51 | <code>            .rawQuery(&quot;SELECT payload FROM events WHERE id=?&quot;, arrayOf(event.getString(&quot;event_id&quot;)))</code> | Invoca/continua rawQuery com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L52"></a>52 | <code>            .use {</code> | Fornece a expressão .use { ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L53"></a>53 | <code>                assertTrue(it.moveToFirst())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L54"></a>54 | <code>                assertFalse(it.getString(0).contains(&quot;storage-test-coffee&quot;))</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L55"></a>55 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L56"></a>56 | <code>        reopened.clear()</code> | Invoca/continua reopened.clear com os argumentos declarados. |
| <a id="L57"></a>57 | <code>        reopened.close()</code> | Invoca/continua reopened.close com os argumentos declarados. |
| <a id="L58"></a>58 | <code>        vault.clear()</code> | Invoca/continua vault.clear com os argumentos declarados. |
| <a id="L59"></a>59 | <code>        assertNotEquals(device, vault.deviceId())</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. Verifica comportamento esperado pelo teste; não constitui funcionalidade de produção. |
| <a id="L60"></a>60 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L61"></a>61 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
