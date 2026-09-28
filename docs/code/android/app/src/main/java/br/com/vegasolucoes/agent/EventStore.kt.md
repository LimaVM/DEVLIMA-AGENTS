# android/app/src/main/java/br/com/vegasolucoes/agent/EventStore.kt

Mantém SQLite local com conteúdo cifrado: eventos deduplicados, threads, mensagens pendentes, cache e associação ao proprietário; ordem e estados controlam replay.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/EventStore.kt) · 463 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [LocalThread](#L12) | Define o tipo LocalThread e reúne o estado/contrato descrito para este módulo. |
| [PendingMessage](#L15) | Define o tipo PendingMessage e reúne o estado/contrato descrito para este módulo. |
| [Bubble](#L26) | Define o tipo Bubble e reúne o estado/contrato descrito para este módulo. |
| [EventStore](#L34) | Define o tipo EventStore e reúne o estado/contrato descrito para este módulo. |
| [EventStore.onCreate](#L38) | Trata o callback de EventStore.onCreate, segundo o contrato e as verificações deste módulo. |
| [EventStore.createQueue](#L47) | Cria EventStore.createQueue, segundo o contrato e as verificações deste módulo. |
| [EventStore.onUpgrade](#L60) | Trata o callback de EventStore.onUpgrade, segundo o contrato e as verificações deste módulo. |
| [EventStore.ensureOwner](#L68) | Apaga cache/fila de outro proprietário antes de associar armazenamento ao usuário autenticado. |
| [EventStore.save](#L86) | Persiste evento por UUID com deduplicação e atualiza mensagem/thread quando a resposta chega. |
| [EventStore.shouldNotify](#L146) | Implementa EventStore.shouldNotify como parte do fluxo descrito para este arquivo. |
| [EventStore.notified](#L154) | Implementa EventStore.notified como parte do fluxo descrito para este arquivo. |
| [EventStore.recent](#L160) | Implementa EventStore.recent como parte do fluxo descrito para este arquivo. |
| [EventStore.threads](#L177) | Implementa EventStore.threads como parte do fluxo descrito para este arquivo. |
| [EventStore.newThread](#L195) | Implementa EventStore.newThread como parte do fluxo descrito para este arquivo. |
| [EventStore.importThreads](#L206) | Importa EventStore.importThreads, segundo o contrato e as verificações deste módulo. |
| [EventStore.enqueue](#L230) | Enfileira EventStore.enqueue, segundo o contrato e as verificações deste módulo. |
| [EventStore.pending](#L247) | Implementa EventStore.pending como parte do fluxo descrito para este arquivo. |
| [EventStore.nextFrame](#L274) | Escolhe o próximo envio durável respeitando ordem global, bloqueio por falha e retry_at. |
| [EventStore.enqueueVoice](#L309) | Enfileira EventStore.enqueueVoice, segundo o contrato e as verificações deste módulo. |
| [EventStore.cancelVoice](#L331) | Cancela EventStore.cancelVoice, segundo o contrato e as verificações deste módulo. |
| [EventStore.sent](#L340) | Implementa EventStore.sent como parte do fluxo descrito para este arquivo. |
| [EventStore.response](#L350) | Implementa EventStore.response como parte do fluxo descrito para este arquivo. |
| [EventStore.reconnect](#L378) | Implementa EventStore.reconnect como parte do fluxo descrito para este arquivo. |
| [EventStore.retry](#L387) | Tenta novamente EventStore.retry, segundo o contrato e as verificações deste módulo. |
| [EventStore.cacheHistory](#L397) | Implementa EventStore.cacheHistory como parte do fluxo descrito para este arquivo. |
| [EventStore.bubbles](#L406) | Implementa EventStore.bubbles como parte do fluxo descrito para este arquivo. |
| [EventStore.clear](#L455) | Limpa EventStore.clear, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.content.ContentValues</code> | Disponibiliza o símbolo Kotlin/Android android.content.ContentValues neste arquivo. |
| <a id="L4"></a>4 | <code>import android.content.Context</code> | Disponibiliza o símbolo Kotlin/Android android.content.Context neste arquivo. |
| <a id="L5"></a>5 | <code>import android.database.sqlite.SQLiteDatabase</code> | Disponibiliza o símbolo Kotlin/Android android.database.sqlite.SQLiteDatabase neste arquivo. |
| <a id="L6"></a>6 | <code>import android.database.sqlite.SQLiteOpenHelper</code> | Disponibiliza o símbolo Kotlin/Android android.database.sqlite.SQLiteOpenHelper neste arquivo. |
| <a id="L7"></a>7 | <code>import java.util.UUID</code> | Disponibiliza o símbolo Kotlin/Android java.util.UUID neste arquivo. |
| <a id="L8"></a>8 | <code>import org.json.JSONArray</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONArray neste arquivo. |
| <a id="L9"></a>9 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L11"></a>11 | <code>// Documentação: Define o tipo LocalThread e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo LocalThread e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>data class LocalThread(val id: String, val serverId: String?, val title: String)</code> | Define o tipo LocalThread e reúne o estado/contrato descrito para este módulo. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L14"></a>14 | <code>// Documentação: Define o tipo PendingMessage e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo PendingMessage e reúne o estado/contrato descrito para este módulo. |
| <a id="L15"></a>15 | <code>data class PendingMessage(</code> | Define o tipo PendingMessage e reúne o estado/contrato descrito para este módulo. |
| <a id="L16"></a>16 | <code>    val id: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L17"></a>17 | <code>    val threadId: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L18"></a>18 | <code>    val content: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L19"></a>19 | <code>    val status: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L20"></a>20 | <code>    val result: JSONObject?,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L21"></a>21 | <code>    val attempts: Int,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L22"></a>22 | <code>    val callId: String? = null,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L23"></a>23 | <code>)</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L25"></a>25 | <code>// Documentação: Define o tipo Bubble e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo Bubble e reúne o estado/contrato descrito para este módulo. |
| <a id="L26"></a>26 | <code>data class Bubble(</code> | Define o tipo Bubble e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>    val text: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L28"></a>28 | <code>    val mine: Boolean,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L29"></a>29 | <code>    val state: String = &quot;&quot;,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L30"></a>30 | <code>    val retryId: String? = null,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L31"></a>31 | <code>)</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L32"></a>32 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L33"></a>33 | <code>// Documentação: Define o tipo EventStore e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo EventStore e reúne o estado/contrato descrito para este módulo. |
| <a id="L34"></a>34 | <code>class EventStore(context: Context, private val secure: SecureStore) :</code> | Define o tipo EventStore e reúne o estado/contrato descrito para este módulo. |
| <a id="L35"></a>35 | <code>    SQLiteOpenHelper(context, &quot;events.db&quot;, null, 3) {</code> | Invoca/continua SQLiteOpenHelper com os argumentos declarados. |
| <a id="L36"></a>36 | <code>    // Documentação: Trata o callback de EventStore.onCreate, segundo o contrato e as verificações</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de EventStore.onCreate, segundo o contrato e as verificações |
| <a id="L37"></a>37 | <code>    // deste módulo.</code> | Comentário de manutenção/documentação: deste módulo. |
| <a id="L38"></a>38 | <code>    override fun onCreate(db: SQLiteDatabase) {</code> | Trata o callback de EventStore.onCreate, segundo o contrato e as verificações deste módulo. |
| <a id="L39"></a>39 | <code>        db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L40"></a>40 | <code>            &quot;CREATE TABLE events(id TEXT PRIMARY KEY,type TEXT NOT NULL,payload TEXT NOT NULL,received_at INTEGER NOT NULL,notified INTEGER NOT NULL DEFAULT 0)&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L41"></a>41 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L42"></a>42 | <code>        createQueue(db)</code> | Invoca/continua createQueue com os argumentos declarados. |
| <a id="L43"></a>43 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L45"></a>45 | <code>    // Documentação: Cria EventStore.createQueue, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Cria EventStore.createQueue, segundo o contrato e as verificações deste |
| <a id="L46"></a>46 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L47"></a>47 | <code>    private fun createQueue(db: SQLiteDatabase) {</code> | Cria EventStore.createQueue, segundo o contrato e as verificações deste módulo. |
| <a id="L48"></a>48 | <code>        db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L49"></a>49 | <code>            &quot;CREATE TABLE threads(id TEXT PRIMARY KEY,server_id TEXT UNIQUE,title TEXT NOT NULL,updated INTEGER NOT NULL)&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L50"></a>50 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L51"></a>51 | <code>        db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L52"></a>52 | <code>            &quot;CREATE TABLE pending(id TEXT PRIMARY KEY,thread_id TEXT NOT NULL,content TEXT NOT NULL,status TEXT NOT NULL,result TEXT,attempts INTEGER NOT NULL DEFAULT 0,retry_at INTEGER NOT NULL DEFAULT 0,created INTEGER NOT NULL,call_id TEXT)&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L53"></a>53 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L54"></a>54 | <code>        db.execSQL(&quot;CREATE TABLE history(conversation_id TEXT PRIMARY KEY,payload TEXT NOT NULL)&quot;)</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L55"></a>55 | <code>        db.execSQL(&quot;CREATE TABLE metadata(name TEXT PRIMARY KEY,value TEXT NOT NULL)&quot;)</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L56"></a>56 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L57"></a>57 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L58"></a>58 | <code>    // Documentação: Trata o callback de EventStore.onUpgrade, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de EventStore.onUpgrade, segundo o contrato e as |
| <a id="L59"></a>59 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L60"></a>60 | <code>    override fun onUpgrade(db: SQLiteDatabase, old: Int, new: Int) {</code> | Trata o callback de EventStore.onUpgrade, segundo o contrato e as verificações deste módulo. |
| <a id="L61"></a>61 | <code>        if (old &lt; 2) createQueue(db)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L62"></a>62 | <code>        else if (old &lt; 3) db.execSQL(&quot;ALTER TABLE pending ADD COLUMN call_id TEXT&quot;)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. Associa transcrição/fila à sessão de chamada correta. |
| <a id="L63"></a>63 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L64"></a>64 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L65"></a>65 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L66"></a>66 | <code>    // Documentação: Apaga cache/fila de outro proprietário antes de associar armazenamento ao</code> | Comentário de manutenção/documentação: Documentação: Apaga cache/fila de outro proprietário antes de associar armazenamento ao |
| <a id="L67"></a>67 | <code>    // usuário autenticado.</code> | Comentário de manutenção/documentação: usuário autenticado. |
| <a id="L68"></a>68 | <code>    fun ensureOwner(owner: String) {</code> | Apaga cache/fila de outro proprietário antes de associar armazenamento ao usuário autenticado. Associação ao proprietário no registry/contrato do manager. |
| <a id="L69"></a>69 | <code>        val db = writableDatabase</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L70"></a>70 | <code>        val previous =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L71"></a>71 | <code>            db.rawQuery(&quot;SELECT value FROM metadata WHERE name=&#x27;owner&#x27;&quot;, null).use {</code> | Invoca/continua db.rawQuery com os argumentos declarados. Garante fechamento do recurso ao terminar este bloco, incluindo falha. Associação ao proprietário no registry/contrato do manager. |
| <a id="L72"></a>72 | <code>                if (it.moveToFirst()) secure.decrypt(it.getString(0)) else null</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L73"></a>73 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L74"></a>74 | <code>        if (previous != owner) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Associação ao proprietário no registry/contrato do manager. |
| <a id="L75"></a>75 | <code>            clear()</code> | Invoca/continua clear com os argumentos declarados. |
| <a id="L76"></a>76 | <code>            db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L77"></a>77 | <code>                &quot;INSERT INTO metadata(name,value) VALUES(&#x27;owner&#x27;,?)&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. Associação ao proprietário no registry/contrato do manager. |
| <a id="L78"></a>78 | <code>                arrayOf&lt;Any&gt;(secure.encrypt(owner)),</code> | Invoca/continua secure.encrypt com os argumentos declarados. Associação ao proprietário no registry/contrato do manager. |
| <a id="L79"></a>79 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L80"></a>80 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L81"></a>81 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L82"></a>82 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L83"></a>83 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L84"></a>84 | <code>    // Documentação: Persiste evento por UUID com deduplicação e atualiza mensagem/thread quando a</code> | Comentário de manutenção/documentação: Documentação: Persiste evento por UUID com deduplicação e atualiza mensagem/thread quando a |
| <a id="L85"></a>85 | <code>    // resposta chega.</code> | Comentário de manutenção/documentação: resposta chega. |
| <a id="L86"></a>86 | <code>    fun save(event: JSONObject): Boolean {</code> | Persiste evento por UUID com deduplicação e atualiza mensagem/thread quando a resposta chega. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L87"></a>87 | <code>        val id = UUID.fromString(event.getString(&quot;event_id&quot;)).toString()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Identificador estável do evento usado por replay, deduplicação, notificação e ACK. |
| <a id="L88"></a>88 | <code>        val db = writableDatabase</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L89"></a>89 | <code>        db.beginTransaction()</code> | Invoca/continua db.beginTransaction com os argumentos declarados. Abre transação SQLite para alterações associadas. |
| <a id="L90"></a>90 | <code>        try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L91"></a>91 | <code>            val values =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L92"></a>92 | <code>                ContentValues().apply {</code> | Invoca/continua ContentValues com os argumentos declarados. |
| <a id="L93"></a>93 | <code>                    put(&quot;id&quot;, id)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L94"></a>94 | <code>                    put(&quot;type&quot;, event.getString(&quot;type&quot;))</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L95"></a>95 | <code>                    put(&quot;payload&quot;, secure.encrypt(event.toString()))</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L96"></a>96 | <code>                    put(&quot;received_at&quot;, System.currentTimeMillis())</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L97"></a>97 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L98"></a>98 | <code>            val added =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L99"></a>99 | <code>                db.insertWithOnConflict(&quot;events&quot;, null, values, SQLiteDatabase.CONFLICT_IGNORE) !=</code> | Invoca/continua db.insertWithOnConflict com os argumentos declarados. |
| <a id="L100"></a>100 | <code>                    -1L</code> | Fornece a expressão -1L ao bloco/chamada em construção. |
| <a id="L101"></a>101 | <code>            if (event.getString(&quot;type&quot;) == &quot;agent.message&quot;) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L102"></a>102 | <code>                val reply = event.getJSONObject(&quot;payload&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L103"></a>103 | <code>                val client = reply.optString(&quot;client_message_id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê texto opcional, aplicando fallback declarado quando necessário. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L104"></a>104 | <code>                val source =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L105"></a>105 | <code>                    db.rawQuery(&quot;SELECT thread_id FROM pending WHERE id=?&quot;, arrayOf(client)).use {</code> | Invoca/continua db.rawQuery com os argumentos declarados. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L106"></a>106 | <code>                        if (it.moveToFirst()) it.getString(0) else null</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L107"></a>107 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L108"></a>108 | <code>                if (source != null) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L109"></a>109 | <code>                    val duplicate =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L110"></a>110 | <code>                        db.rawQuery(</code> | Invoca/continua db.rawQuery com os argumentos declarados. Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura. |
| <a id="L111"></a>111 | <code>                                &quot;SELECT id FROM threads WHERE server_id=? AND id!=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L112"></a>112 | <code>                                arrayOf(reply.getString(&quot;conversation_id&quot;), source),</code> | Invoca/continua arrayOf com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L113"></a>113 | <code>                            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L114"></a>114 | <code>                            .use { if (it.moveToFirst()) it.getString(0) else null }</code> | Invoca/continua if com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L115"></a>115 | <code>                    if (duplicate != null) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L116"></a>116 | <code>                        db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L117"></a>117 | <code>                            &quot;UPDATE pending SET thread_id=? WHERE thread_id=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L118"></a>118 | <code>                            arrayOf(source, duplicate),</code> | Invoca/continua arrayOf com os argumentos declarados. |
| <a id="L119"></a>119 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L120"></a>120 | <code>                        db.delete(&quot;threads&quot;, &quot;id=?&quot;, arrayOf(duplicate))</code> | Invoca/continua db.delete com os argumentos declarados. |
| <a id="L121"></a>121 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L122"></a>122 | <code>                    db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L123"></a>123 | <code>                        &quot;UPDATE threads SET server_id=?,updated=? WHERE id=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L124"></a>124 | <code>                        arrayOf&lt;Any&gt;(</code> | Fornece a expressão arrayOf&lt;Any&gt;( ao bloco/chamada em construção. |
| <a id="L125"></a>125 | <code>                            reply.getString(&quot;conversation_id&quot;),</code> | Invoca/continua reply.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L126"></a>126 | <code>                            System.currentTimeMillis(),</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L127"></a>127 | <code>                            source,</code> | Fornece a expressão source, ao bloco/chamada em construção. |
| <a id="L128"></a>128 | <code>                        ),</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L129"></a>129 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L130"></a>130 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L131"></a>131 | <code>                db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L132"></a>132 | <code>                    &quot;UPDATE pending SET status=&#x27;COMPLETED&#x27;,result=? WHERE id=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L133"></a>133 | <code>                    arrayOf&lt;Any&gt;(secure.encrypt(reply.toString()), client),</code> | Invoca/continua secure.encrypt com os argumentos declarados. |
| <a id="L134"></a>134 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L135"></a>135 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L136"></a>136 | <code>            db.setTransactionSuccessful()</code> | Invoca/continua db.setTransactionSuccessful com os argumentos declarados. Marca transação SQLite para confirmar no encerramento. |
| <a id="L137"></a>137 | <code>            return added</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L138"></a>138 | <code>        } finally {</code> | Fornece a expressão } finally { ao bloco/chamada em construção. |
| <a id="L139"></a>139 | <code>            db.endTransaction()</code> | Invoca/continua db.endTransaction com os argumentos declarados. Finaliza transação SQLite, confirmando se marcada como válida. |
| <a id="L140"></a>140 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L141"></a>141 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L142"></a>142 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L143"></a>143 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L144"></a>144 | <code>    // Documentação: Implementa EventStore.shouldNotify como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.shouldNotify como parte do fluxo descrito para este |
| <a id="L145"></a>145 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L146"></a>146 | <code>    fun shouldNotify(id: String): Boolean =</code> | Implementa EventStore.shouldNotify como parte do fluxo descrito para este arquivo. |
| <a id="L147"></a>147 | <code>        readableDatabase.rawQuery(&quot;SELECT notified FROM events WHERE id=?&quot;, arrayOf(id)).use {</code> | Invoca/continua readableDatabase.rawQuery com os argumentos declarados. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L148"></a>148 | <code>            it.moveToFirst() &amp;&amp; it.getInt(0) == 0</code> | Invoca/continua it.moveToFirst com os argumentos declarados. |
| <a id="L149"></a>149 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L150"></a>150 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L151"></a>151 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L152"></a>152 | <code>    // Documentação: Implementa EventStore.notified como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.notified como parte do fluxo descrito para este |
| <a id="L153"></a>153 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L154"></a>154 | <code>    fun notified(id: String) {</code> | Implementa EventStore.notified como parte do fluxo descrito para este arquivo. |
| <a id="L155"></a>155 | <code>        writableDatabase.execSQL(&quot;UPDATE events SET notified=1 WHERE id=?&quot;, arrayOf&lt;Any&gt;(id))</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L156"></a>156 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L157"></a>157 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L158"></a>158 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L159"></a>159 | <code>    // Documentação: Implementa EventStore.recent como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.recent como parte do fluxo descrito para este arquivo. |
| <a id="L160"></a>160 | <code>    fun recent(limit: Int = 100): List&lt;JSONObject&gt; {</code> | Implementa EventStore.recent como parte do fluxo descrito para este arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L161"></a>161 | <code>        val result = mutableListOf&lt;JSONObject&gt;()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L162"></a>162 | <code>        readableDatabase</code> | Fornece a expressão readableDatabase ao bloco/chamada em construção. |
| <a id="L163"></a>163 | <code>            .rawQuery(</code> | Invoca/continua rawQuery com os argumentos declarados. Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura. |
| <a id="L164"></a>164 | <code>                &quot;SELECT payload FROM events ORDER BY received_at DESC LIMIT ?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L165"></a>165 | <code>                arrayOf(limit.coerceIn(1, 1000).toString()),</code> | Invoca/continua arrayOf com os argumentos declarados. |
| <a id="L166"></a>166 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L167"></a>167 | <code>            .use { rows -&gt;</code> | Fornece a expressão .use { rows -&gt; ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L168"></a>168 | <code>                while (rows.moveToNext()) runCatching {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L169"></a>169 | <code>                    result.add(JSONObject(secure.decrypt(rows.getString(0))))</code> | Invoca/continua result.add com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L170"></a>170 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L171"></a>171 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L172"></a>172 | <code>        return result</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L173"></a>173 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L174"></a>174 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L175"></a>175 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L176"></a>176 | <code>    // Documentação: Implementa EventStore.threads como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.threads como parte do fluxo descrito para este arquivo. |
| <a id="L177"></a>177 | <code>    fun threads(): List&lt;LocalThread&gt; =</code> | Implementa EventStore.threads como parte do fluxo descrito para este arquivo. |
| <a id="L178"></a>178 | <code>        readableDatabase</code> | Fornece a expressão readableDatabase ao bloco/chamada em construção. |
| <a id="L179"></a>179 | <code>            .rawQuery(&quot;SELECT id,server_id,title FROM threads ORDER BY updated DESC&quot;, null)</code> | Invoca/continua rawQuery com os argumentos declarados. Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura. |
| <a id="L180"></a>180 | <code>            .use { c -&gt;</code> | Fornece a expressão .use { c -&gt; ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L181"></a>181 | <code>                buildList {</code> | Fornece a expressão buildList { ao bloco/chamada em construção. |
| <a id="L182"></a>182 | <code>                    while (c.moveToNext()) add(</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L183"></a>183 | <code>                        LocalThread(</code> | Invoca/continua LocalThread com os argumentos declarados. |
| <a id="L184"></a>184 | <code>                            c.getString(0),</code> | Invoca/continua c.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L185"></a>185 | <code>                            if (c.isNull(1)) null else c.getString(1),</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L186"></a>186 | <code>                            secure.decrypt(c.getString(2)),</code> | Invoca/continua secure.decrypt com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L187"></a>187 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L188"></a>188 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L189"></a>189 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L190"></a>190 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L191"></a>191 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L192"></a>192 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L193"></a>193 | <code>    // Documentação: Implementa EventStore.newThread como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.newThread como parte do fluxo descrito para este |
| <a id="L194"></a>194 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L195"></a>195 | <code>    fun newThread(): String =</code> | Implementa EventStore.newThread como parte do fluxo descrito para este arquivo. |
| <a id="L196"></a>196 | <code>        UUID.randomUUID().toString().also {</code> | Invoca/continua UUID.randomUUID com os argumentos declarados. |
| <a id="L197"></a>197 | <code>            writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L198"></a>198 | <code>                &quot;INSERT INTO threads VALUES(?,NULL,?,?)&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L199"></a>199 | <code>                arrayOf&lt;Any&gt;(it, secure.encrypt(&quot;Nova conversa&quot;), System.currentTimeMillis()),</code> | Invoca/continua secure.encrypt com os argumentos declarados. |
| <a id="L200"></a>200 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L201"></a>201 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L202"></a>202 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L203"></a>203 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L204"></a>204 | <code>    // Documentação: Importa EventStore.importThreads, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Importa EventStore.importThreads, segundo o contrato e as verificações deste |
| <a id="L205"></a>205 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L206"></a>206 | <code>    fun importThreads(rows: JSONArray) {</code> | Importa EventStore.importThreads, segundo o contrato e as verificações deste módulo. |
| <a id="L207"></a>207 | <code>        val db = writableDatabase</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L208"></a>208 | <code>        for (i in 0 until rows.length()) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L209"></a>209 | <code>            val row = rows.getJSONObject(i)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L210"></a>210 | <code>            val id = row.getString(&quot;id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L211"></a>211 | <code>            db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L212"></a>212 | <code>                &quot;INSERT OR IGNORE INTO threads VALUES(?,?,?,?)&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L213"></a>213 | <code>                arrayOf&lt;Any&gt;(</code> | Fornece a expressão arrayOf&lt;Any&gt;( ao bloco/chamada em construção. |
| <a id="L214"></a>214 | <code>                    id,</code> | Fornece a expressão id, ao bloco/chamada em construção. |
| <a id="L215"></a>215 | <code>                    id,</code> | Fornece a expressão id, ao bloco/chamada em construção. |
| <a id="L216"></a>216 | <code>                    secure.encrypt(row.getString(&quot;title&quot;)),</code> | Invoca/continua secure.encrypt com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L217"></a>217 | <code>                    System.currentTimeMillis() - i,</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L218"></a>218 | <code>                ),</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L219"></a>219 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L220"></a>220 | <code>            db.execSQL(</code> | Invoca/continua db.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L221"></a>221 | <code>                &quot;UPDATE threads SET title=? WHERE server_id=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L222"></a>222 | <code>                arrayOf&lt;Any&gt;(secure.encrypt(row.getString(&quot;title&quot;)), id),</code> | Invoca/continua secure.encrypt com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L223"></a>223 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L224"></a>224 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L225"></a>225 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L226"></a>226 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L227"></a>227 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L228"></a>228 | <code>    // Documentação: Enfileira EventStore.enqueue, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Enfileira EventStore.enqueue, segundo o contrato e as verificações deste |
| <a id="L229"></a>229 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L230"></a>230 | <code>    fun enqueue(thread: String, text: String): String {</code> | Enfileira EventStore.enqueue, segundo o contrato e as verificações deste módulo. |
| <a id="L231"></a>231 | <code>        require(text.isNotBlank() &amp;&amp; text.length &lt;= 4000)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L232"></a>232 | <code>        require(threads().any { it.id == thread })</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L233"></a>233 | <code>        val id = UUID.randomUUID().toString()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L234"></a>234 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L235"></a>235 | <code>            &quot;INSERT INTO pending(id,thread_id,content,status,created) VALUES(?,?,?,&#x27;QUEUED&#x27;,?)&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L236"></a>236 | <code>            arrayOf&lt;Any&gt;(id, thread, secure.encrypt(text), System.currentTimeMillis()),</code> | Invoca/continua secure.encrypt com os argumentos declarados. |
| <a id="L237"></a>237 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L238"></a>238 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L239"></a>239 | <code>            &quot;UPDATE threads SET updated=?,title=CASE WHEN server_id IS NULL THEN ? ELSE title END WHERE id=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L240"></a>240 | <code>            arrayOf&lt;Any&gt;(System.currentTimeMillis(), secure.encrypt(text.take(60)), thread),</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L241"></a>241 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L242"></a>242 | <code>        return id</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L243"></a>243 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L244"></a>244 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L245"></a>245 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L246"></a>246 | <code>    // Documentação: Implementa EventStore.pending como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.pending como parte do fluxo descrito para este arquivo. |
| <a id="L247"></a>247 | <code>    fun pending(thread: String? = null): List&lt;PendingMessage&gt; =</code> | Implementa EventStore.pending como parte do fluxo descrito para este arquivo. |
| <a id="L248"></a>248 | <code>        readableDatabase</code> | Fornece a expressão readableDatabase ao bloco/chamada em construção. |
| <a id="L249"></a>249 | <code>            .rawQuery(</code> | Invoca/continua rawQuery com os argumentos declarados. Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura. |
| <a id="L250"></a>250 | <code>                &quot;SELECT id,thread_id,content,status,result,attempts,call_id FROM pending&quot; +</code> | Fornece a expressão &quot;SELECT id,thread_id,content,status,result,attempts,call_id FROM pending&quot; + ao bloco/chamada em construção. Associa transcrição/fila à sessão de chamada correta. |
| <a id="L251"></a>251 | <code>                    (if (thread == null) &quot;&quot; else &quot; WHERE thread_id=?&quot;) +</code> | Invoca/continua if com os argumentos declarados. |
| <a id="L252"></a>252 | <code>                    &quot; ORDER BY created,rowid&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L253"></a>253 | <code>                thread?.let { arrayOf(it) },</code> | Invoca/continua arrayOf com os argumentos declarados. |
| <a id="L254"></a>254 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L255"></a>255 | <code>            .use { c -&gt;</code> | Fornece a expressão .use { c -&gt; ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L256"></a>256 | <code>                buildList {</code> | Fornece a expressão buildList { ao bloco/chamada em construção. |
| <a id="L257"></a>257 | <code>                    while (c.moveToNext()) add(</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L258"></a>258 | <code>                        PendingMessage(</code> | Invoca/continua PendingMessage com os argumentos declarados. |
| <a id="L259"></a>259 | <code>                            c.getString(0),</code> | Invoca/continua c.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L260"></a>260 | <code>                            c.getString(1),</code> | Invoca/continua c.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L261"></a>261 | <code>                            secure.decrypt(c.getString(2)),</code> | Invoca/continua secure.decrypt com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L262"></a>262 | <code>                            c.getString(3),</code> | Invoca/continua c.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L263"></a>263 | <code>                            if (c.isNull(4)) null else JSONObject(secure.decrypt(c.getString(4))),</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L264"></a>264 | <code>                            c.getInt(5),</code> | Invoca/continua c.getInt com os argumentos declarados. |
| <a id="L265"></a>265 | <code>                            if (c.isNull(6)) null else c.getString(6),</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L266"></a>266 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L267"></a>267 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L268"></a>268 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L269"></a>269 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L270"></a>270 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L271"></a>271 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L272"></a>272 | <code>    // Documentação: Escolhe o próximo envio durável respeitando ordem global, bloqueio por falha</code> | Comentário de manutenção/documentação: Documentação: Escolhe o próximo envio durável respeitando ordem global, bloqueio por falha |
| <a id="L273"></a>273 | <code>    // e retry_at.</code> | Comentário de manutenção/documentação: e retry_at. |
| <a id="L274"></a>274 | <code>    fun nextFrame(): JSONObject? {</code> | Escolhe o próximo envio durável respeitando ordem global, bloqueio por falha e retry_at. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L275"></a>275 | <code>        // One outstanding turn globally; a failed turn blocks its thread until explicit retry.</code> | Comentário de manutenção/documentação: One outstanding turn globally; a failed turn blocks its thread until explicit retry. |
| <a id="L276"></a>276 | <code>        val next =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L277"></a>277 | <code>            pending().firstOrNull { it.status !in setOf(&quot;COMPLETED&quot;, &quot;CANCELLED&quot;) } ?: return null</code> | Invoca/continua pending com os argumentos declarados. |
| <a id="L278"></a>278 | <code>        if (next.status == &quot;FAILED&quot;) return null</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L279"></a>279 | <code>        val due =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L280"></a>280 | <code>            readableDatabase</code> | Fornece a expressão readableDatabase ao bloco/chamada em construção. |
| <a id="L281"></a>281 | <code>                .rawQuery(&quot;SELECT retry_at FROM pending WHERE id=?&quot;, arrayOf(next.id))</code> | Invoca/continua rawQuery com os argumentos declarados. Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura. Momento mínimo para novo envio, evitando loop de retry imediato. |
| <a id="L282"></a>282 | <code>                .use {</code> | Fornece a expressão .use { ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L283"></a>283 | <code>                    it.moveToFirst()</code> | Invoca/continua it.moveToFirst com os argumentos declarados. |
| <a id="L284"></a>284 | <code>                    it.getLong(0)</code> | Invoca/continua it.getLong com os argumentos declarados. |
| <a id="L285"></a>285 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L286"></a>286 | <code>        if (due &gt; System.currentTimeMillis()) return null</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L287"></a>287 | <code>        val thread = threads().first { it.id == next.threadId }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L288"></a>288 | <code>        if (next.callId != null)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L289"></a>289 | <code>            return outgoing(</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L290"></a>290 | <code>                &quot;voice.transcript&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L291"></a>291 | <code>                JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L292"></a>292 | <code>                    .put(&quot;call_session_id&quot;, next.callId)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L293"></a>293 | <code>                    .put(&quot;client_message_id&quot;, next.id)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L294"></a>294 | <code>                    .put(&quot;content&quot;, next.content),</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L295"></a>295 | <code>                next.id,</code> | Fornece a expressão next.id, ao bloco/chamada em construção. |
| <a id="L296"></a>296 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L297"></a>297 | <code>        return outgoing(</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L298"></a>298 | <code>            &quot;chat.message&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L299"></a>299 | <code>            JSONObject().put(&quot;client_message_id&quot;, next.id).put(&quot;content&quot;, next.content).apply {</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L300"></a>300 | <code>                thread.serverId?.let { put(&quot;conversation_id&quot;, it) }</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L301"></a>301 | <code>            },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L302"></a>302 | <code>            next.id,</code> | Fornece a expressão next.id, ao bloco/chamada em construção. |
| <a id="L303"></a>303 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L304"></a>304 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L305"></a>305 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L306"></a>306 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L307"></a>307 | <code>    // Documentação: Enfileira EventStore.enqueueVoice, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Enfileira EventStore.enqueueVoice, segundo o contrato e as verificações deste |
| <a id="L308"></a>308 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L309"></a>309 | <code>    fun enqueueVoice(call: JSONObject, text: String): String {</code> | Enfileira EventStore.enqueueVoice, segundo o contrato e as verificações deste módulo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L310"></a>310 | <code>        val conversation = call.getString(&quot;conversation_id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L311"></a>311 | <code>        importThreads(</code> | Invoca/continua importThreads com os argumentos declarados. |
| <a id="L312"></a>312 | <code>            JSONArray()</code> | Invoca/continua JSONArray com os argumentos declarados. |
| <a id="L313"></a>313 | <code>                .put(</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L314"></a>314 | <code>                    JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L315"></a>315 | <code>                        .put(&quot;id&quot;, conversation)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L316"></a>316 | <code>                        .put(&quot;title&quot;, &quot;Chamada: &quot; + call.optString(&quot;reason&quot;))</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L317"></a>317 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L318"></a>318 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L319"></a>319 | <code>        val thread = threads().first { it.serverId == conversation }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L320"></a>320 | <code>        return enqueue(thread.id, text).also {</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L321"></a>321 | <code>            writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L322"></a>322 | <code>                &quot;UPDATE pending SET call_id=? WHERE id=?&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. Associa transcrição/fila à sessão de chamada correta. |
| <a id="L323"></a>323 | <code>                arrayOf(call.getString(&quot;id&quot;), it),</code> | Invoca/continua arrayOf com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L324"></a>324 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L325"></a>325 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L326"></a>326 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L327"></a>327 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L328"></a>328 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L329"></a>329 | <code>    // Documentação: Cancela EventStore.cancelVoice, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Cancela EventStore.cancelVoice, segundo o contrato e as verificações deste |
| <a id="L330"></a>330 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L331"></a>331 | <code>    fun cancelVoice(callId: String) {</code> | Cancela EventStore.cancelVoice, segundo o contrato e as verificações deste módulo. |
| <a id="L332"></a>332 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L333"></a>333 | <code>            &quot;UPDATE pending SET status=&#x27;CANCELLED&#x27; WHERE call_id=? AND status!=&#x27;COMPLETED&#x27;&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. Associa transcrição/fila à sessão de chamada correta. |
| <a id="L334"></a>334 | <code>            arrayOf(callId),</code> | Invoca/continua arrayOf com os argumentos declarados. |
| <a id="L335"></a>335 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L336"></a>336 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L337"></a>337 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L338"></a>338 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L339"></a>339 | <code>    // Documentação: Implementa EventStore.sent como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.sent como parte do fluxo descrito para este arquivo. |
| <a id="L340"></a>340 | <code>    fun sent(id: String) {</code> | Implementa EventStore.sent como parte do fluxo descrito para este arquivo. |
| <a id="L341"></a>341 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L342"></a>342 | <code>            &quot;UPDATE pending SET status=&#x27;SENDING&#x27;,attempts=attempts+1,retry_at=? WHERE id=? AND status!=&#x27;COMPLETED&#x27;&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. Momento mínimo para novo envio, evitando loop de retry imediato. |
| <a id="L343"></a>343 | <code>            arrayOf&lt;Any&gt;(System.currentTimeMillis() + 180000, id),</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L344"></a>344 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L345"></a>345 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L346"></a>346 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L347"></a>347 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L348"></a>348 | <code>    // Documentação: Implementa EventStore.response como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.response como parte do fluxo descrito para este |
| <a id="L349"></a>349 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L350"></a>350 | <code>    fun response(event: JSONObject) {</code> | Implementa EventStore.response como parte do fluxo descrito para este arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L351"></a>351 | <code>        val body = event.getJSONObject(&quot;payload&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L352"></a>352 | <code>        val id = body.optString(&quot;client_message_id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê texto opcional, aplicando fallback declarado quando necessário. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L353"></a>353 | <code>        if (id.isEmpty()) return</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L354"></a>354 | <code>        if (event.getString(&quot;type&quot;) == &quot;error&quot;) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L355"></a>355 | <code>            val retry =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L356"></a>356 | <code>                body.optString(&quot;code&quot;) in</code> | Invoca/continua body.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L357"></a>357 | <code>                    setOf(</code> | Invoca/continua setOf com os argumentos declarados. |
| <a id="L358"></a>358 | <code>                        &quot;device_busy&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L359"></a>359 | <code>                        &quot;conversation_busy&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L360"></a>360 | <code>                        &quot;processing_lease_expired&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L361"></a>361 | <code>                        &quot;processing_lease_lost&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L362"></a>362 | <code>                        &quot;service_unavailable&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L363"></a>363 | <code>                        &quot;provider_timeout&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L364"></a>364 | <code>                        &quot;provider_connection_failed&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L365"></a>365 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L366"></a>366 | <code>            val current = pending().firstOrNull { it.id == id } ?: return</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L367"></a>367 | <code>            val state = if (retry &amp;&amp; current.attempts &lt; 5) &quot;QUEUED&quot; else &quot;FAILED&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L368"></a>368 | <code>            writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L369"></a>369 | <code>                &quot;UPDATE pending SET status=?,retry_at=? WHERE id=? AND status!=&#x27;COMPLETED&#x27;&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. Momento mínimo para novo envio, evitando loop de retry imediato. |
| <a id="L370"></a>370 | <code>                arrayOf&lt;Any&gt;(state, System.currentTimeMillis() + 15000, id),</code> | Invoca/continua System.currentTimeMillis com os argumentos declarados. |
| <a id="L371"></a>371 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L372"></a>372 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L373"></a>373 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L374"></a>374 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L375"></a>375 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L376"></a>376 | <code>    // Documentação: Implementa EventStore.reconnect como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.reconnect como parte do fluxo descrito para este |
| <a id="L377"></a>377 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L378"></a>378 | <code>    fun reconnect() {</code> | Implementa EventStore.reconnect como parte do fluxo descrito para este arquivo. |
| <a id="L379"></a>379 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L380"></a>380 | <code>            &quot;UPDATE pending SET status=&#x27;QUEUED&#x27;,retry_at=0 WHERE status=&#x27;SENDING&#x27;&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L381"></a>381 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L382"></a>382 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L383"></a>383 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L384"></a>384 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L385"></a>385 | <code>    // Documentação: Tenta novamente EventStore.retry, segundo o contrato e as verificações deste</code> | Comentário de manutenção/documentação: Documentação: Tenta novamente EventStore.retry, segundo o contrato e as verificações deste |
| <a id="L386"></a>386 | <code>    // módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L387"></a>387 | <code>    fun retry(id: String) {</code> | Tenta novamente EventStore.retry, segundo o contrato e as verificações deste módulo. |
| <a id="L388"></a>388 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L389"></a>389 | <code>            &quot;UPDATE pending SET status=&#x27;QUEUED&#x27;,attempts=0,retry_at=0 WHERE id=? AND status=&#x27;FAILED&#x27;&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. Momento mínimo para novo envio, evitando loop de retry imediato. |
| <a id="L390"></a>390 | <code>            arrayOf&lt;Any&gt;(id),</code> | Fornece a expressão arrayOf&lt;Any&gt;(id), ao bloco/chamada em construção. |
| <a id="L391"></a>391 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L392"></a>392 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L393"></a>393 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L394"></a>394 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L395"></a>395 | <code>    // Documentação: Implementa EventStore.cacheHistory como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.cacheHistory como parte do fluxo descrito para este |
| <a id="L396"></a>396 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L397"></a>397 | <code>    fun cacheHistory(id: String, rows: JSONArray) {</code> | Implementa EventStore.cacheHistory como parte do fluxo descrito para este arquivo. |
| <a id="L398"></a>398 | <code>        writableDatabase.execSQL(</code> | Invoca/continua writableDatabase.execSQL com os argumentos declarados. Executa SQL local; placeholders são preenchidos pelos argumentos declarados. |
| <a id="L399"></a>399 | <code>            &quot;INSERT OR REPLACE INTO history VALUES(?,?)&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L400"></a>400 | <code>            arrayOf&lt;Any&gt;(id, secure.encrypt(rows.toString())),</code> | Invoca/continua secure.encrypt com os argumentos declarados. |
| <a id="L401"></a>401 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L402"></a>402 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L403"></a>403 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L404"></a>404 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L405"></a>405 | <code>    // Documentação: Implementa EventStore.bubbles como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa EventStore.bubbles como parte do fluxo descrito para este arquivo. |
| <a id="L406"></a>406 | <code>    fun bubbles(thread: LocalThread): List&lt;Bubble&gt; {</code> | Implementa EventStore.bubbles como parte do fluxo descrito para este arquivo. |
| <a id="L407"></a>407 | <code>        val history =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L408"></a>408 | <code>            thread.serverId?.let { id -&gt;</code> | Fornece a expressão thread.serverId?.let { id -&gt; ao bloco/chamada em construção. |
| <a id="L409"></a>409 | <code>                readableDatabase</code> | Fornece a expressão readableDatabase ao bloco/chamada em construção. |
| <a id="L410"></a>410 | <code>                    .rawQuery(&quot;SELECT payload FROM history WHERE conversation_id=?&quot;, arrayOf(id))</code> | Invoca/continua rawQuery com os argumentos declarados. Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L411"></a>411 | <code>                    .use {</code> | Fornece a expressão .use { ao bloco/chamada em construção. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L412"></a>412 | <code>                        if (it.moveToFirst()) JSONArray(secure.decrypt(it.getString(0)))</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L413"></a>413 | <code>                        else JSONArray()</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L414"></a>414 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L415"></a>415 | <code>            } ?: JSONArray()</code> | Invoca/continua JSONArray com os argumentos declarados. |
| <a id="L416"></a>416 | <code>        val ids = mutableSetOf&lt;String&gt;()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L417"></a>417 | <code>        val result = mutableListOf&lt;Bubble&gt;()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L418"></a>418 | <code>        for (i in 0 until history.length()) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L419"></a>419 | <code>            val row = history.getJSONObject(i)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L420"></a>420 | <code>            ids.add(row.getString(&quot;id&quot;))</code> | Invoca/continua ids.add com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L421"></a>421 | <code>            result.add(</code> | Invoca/continua result.add com os argumentos declarados. |
| <a id="L422"></a>422 | <code>                Bubble(</code> | Invoca/continua Bubble com os argumentos declarados. |
| <a id="L423"></a>423 | <code>                    row.getString(&quot;content&quot;),</code> | Invoca/continua row.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L424"></a>424 | <code>                    row.getString(&quot;role&quot;) == &quot;user&quot;,</code> | Invoca/continua row.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L425"></a>425 | <code>                    if (row.optString(&quot;status&quot;) == &quot;FAILED&quot;) &quot;Falha no envio&quot; else &quot;&quot;,</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L426"></a>426 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L427"></a>427 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L428"></a>428 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L429"></a>429 | <code>        for (row in pending(thread.id)) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L430"></a>430 | <code>            if (row.result == null &#124;&#124; row.result.optString(&quot;user_message_id&quot;) !in ids)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L431"></a>431 | <code>                result.add(</code> | Invoca/continua result.add com os argumentos declarados. |
| <a id="L432"></a>432 | <code>                    Bubble(</code> | Invoca/continua Bubble com os argumentos declarados. |
| <a id="L433"></a>433 | <code>                        row.content,</code> | Fornece a expressão row.content, ao bloco/chamada em construção. |
| <a id="L434"></a>434 | <code>                        true,</code> | Fornece a expressão true, ao bloco/chamada em construção. |
| <a id="L435"></a>435 | <code>                        when (row.status) {</code> | Despacha o valor/condição para os ramos declarados abaixo. |
| <a id="L436"></a>436 | <code>                            &quot;QUEUED&quot; -&gt; &quot;Na fila&quot;</code> | Fornece a expressão &quot;QUEUED&quot; -&gt; &quot;Na fila&quot; ao bloco/chamada em construção. |
| <a id="L437"></a>437 | <code>                            &quot;SENDING&quot; -&gt; &quot;Aguardando agente…&quot;</code> | Fornece a expressão &quot;SENDING&quot; -&gt; &quot;Aguardando agente…&quot; ao bloco/chamada em construção. |
| <a id="L438"></a>438 | <code>                            &quot;CANCELLED&quot; -&gt; &quot;Chamada encerrada&quot;</code> | Fornece a expressão &quot;CANCELLED&quot; -&gt; &quot;Chamada encerrada&quot; ao bloco/chamada em construção. |
| <a id="L439"></a>439 | <code>                            &quot;FAILED&quot; -&gt; &quot;Falha — toque para tentar novamente&quot;</code> | Fornece a expressão &quot;FAILED&quot; -&gt; &quot;Falha — toque para tentar novamente&quot; ao bloco/chamada em construção. |
| <a id="L440"></a>440 | <code>                            else -&gt; &quot;&quot;</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L441"></a>441 | <code>                        },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L442"></a>442 | <code>                        if (row.status == &quot;FAILED&quot;) row.id else null,</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L443"></a>443 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L444"></a>444 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L445"></a>445 | <code>            row.result?.let {</code> | Fornece a expressão row.result?.let { ao bloco/chamada em construção. |
| <a id="L446"></a>446 | <code>                if (it.optString(&quot;assistant_message_id&quot;) !in ids)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L447"></a>447 | <code>                    result.add(Bubble(it.getString(&quot;reply&quot;), false))</code> | Invoca/continua result.add com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L448"></a>448 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L449"></a>449 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L450"></a>450 | <code>        return result</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L451"></a>451 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L452"></a>452 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L453"></a>453 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L454"></a>454 | <code>    // Documentação: Limpa EventStore.clear, segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: Documentação: Limpa EventStore.clear, segundo o contrato e as verificações deste módulo. |
| <a id="L455"></a>455 | <code>    fun clear() {</code> | Limpa EventStore.clear, segundo o contrato e as verificações deste módulo. |
| <a id="L456"></a>456 | <code>        for (table in</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L457"></a>457 | <code>            listOf(&quot;events&quot;, &quot;pending&quot;, &quot;threads&quot;, &quot;history&quot;, &quot;metadata&quot;)) writableDatabase.delete(</code> | Invoca/continua listOf com os argumentos declarados. |
| <a id="L458"></a>458 | <code>            table,</code> | Fornece a expressão table, ao bloco/chamada em construção. |
| <a id="L459"></a>459 | <code>            null,</code> | Fornece a expressão null, ao bloco/chamada em construção. |
| <a id="L460"></a>460 | <code>            null,</code> | Fornece a expressão null, ao bloco/chamada em construção. |
| <a id="L461"></a>461 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L462"></a>462 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L463"></a>463 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
