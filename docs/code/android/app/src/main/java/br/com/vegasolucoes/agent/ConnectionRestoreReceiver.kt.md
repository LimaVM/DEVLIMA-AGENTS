# android/app/src/main/java/br/com/vegasolucoes/agent/ConnectionRestoreReceiver.kt

Tenta restaurar conexão desejada após boot/desbloqueio ou atualização, verificando sessão e histórico de parada pelo usuário; nunca inicia microfone.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/ConnectionRestoreReceiver.kt) · 46 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [ConnectionRestoreReceiver](#L13) | Define o tipo ConnectionRestoreReceiver e reúne o estado/contrato descrito para este módulo. |
| [ConnectionRestoreReceiver.onReceive](#L16) | Restaura somente conexão desejada com sessão válida, sem ignorar parada explícita pelo usuário. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.app.ActivityManager</code> | Disponibiliza o símbolo Kotlin/Android android.app.ActivityManager neste arquivo. |
| <a id="L4"></a>4 | <code>import android.app.ApplicationExitInfo</code> | Disponibiliza o símbolo Kotlin/Android android.app.ApplicationExitInfo neste arquivo. |
| <a id="L5"></a>5 | <code>import android.content.BroadcastReceiver</code> | Disponibiliza o símbolo Kotlin/Android android.content.BroadcastReceiver neste arquivo. |
| <a id="L6"></a>6 | <code>import android.content.Context</code> | Disponibiliza o símbolo Kotlin/Android android.content.Context neste arquivo. |
| <a id="L7"></a>7 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L8"></a>8 | <code>import android.os.Build</code> | Disponibiliza o símbolo Kotlin/Android android.os.Build neste arquivo. |
| <a id="L9"></a>9 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L11"></a>11 | <code>// Documentação: Define o tipo ConnectionRestoreReceiver e reúne o estado/contrato descrito para</code> | Comentário de manutenção/documentação: Documentação: Define o tipo ConnectionRestoreReceiver e reúne o estado/contrato descrito para |
| <a id="L12"></a>12 | <code>// este módulo.</code> | Comentário de manutenção/documentação: este módulo. |
| <a id="L13"></a>13 | <code>class ConnectionRestoreReceiver : BroadcastReceiver() {</code> | Define o tipo ConnectionRestoreReceiver e reúne o estado/contrato descrito para este módulo. |
| <a id="L14"></a>14 | <code>    // Documentação: Restaura somente conexão desejada com sessão válida, sem ignorar parada</code> | Comentário de manutenção/documentação: Documentação: Restaura somente conexão desejada com sessão válida, sem ignorar parada |
| <a id="L15"></a>15 | <code>    // explícita pelo usuário.</code> | Comentário de manutenção/documentação: explícita pelo usuário. |
| <a id="L16"></a>16 | <code>    override fun onReceive(context: Context, intent: Intent) {</code> | Restaura somente conexão desejada com sessão válida, sem ignorar parada explícita pelo usuário. |
| <a id="L17"></a>17 | <code>        if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L18"></a>18 | <code>            intent.action !in setOf(Intent.ACTION_BOOT_COMPLETED, Intent.ACTION_MY_PACKAGE_REPLACED)</code> | Invoca/continua setOf com os argumentos declarados. |
| <a id="L19"></a>19 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L20"></a>20 | <code>            return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L21"></a>21 | <code>        val prefs = context.getSharedPreferences(&quot;connection&quot;, Context.MODE_PRIVATE)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Acessa preferências privadas do aplicativo para conservar escolha/estado. |
| <a id="L22"></a>22 | <code>        if (!prefs.getBoolean(&quot;wanted&quot;, false)) return</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Preferência de manter conexão ativa; desconectar deve impedir restauração automática. |
| <a id="L23"></a>23 | <code>        if (Build.VERSION.SDK_INT &gt;= 30) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L24"></a>24 | <code>            val stopped =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L25"></a>25 | <code>                context</code> | Fornece a expressão context ao bloco/chamada em construção. |
| <a id="L26"></a>26 | <code>                    .getSystemService(ActivityManager::class.java)</code> | Invoca/continua getSystemService com os argumentos declarados. |
| <a id="L27"></a>27 | <code>                    .getHistoricalProcessExitReasons(context.packageName, 0, 10)</code> | Invoca/continua getHistoricalProcessExitReasons com os argumentos declarados. |
| <a id="L28"></a>28 | <code>                    .any {</code> | Fornece a expressão .any { ao bloco/chamada em construção. |
| <a id="L29"></a>29 | <code>                        it.reason == ApplicationExitInfo.REASON_USER_REQUESTED &amp;&amp;</code> | Fornece a expressão it.reason == ApplicationExitInfo.REASON_USER_REQUESTED &amp;&amp; ao bloco/chamada em construção. |
| <a id="L30"></a>30 | <code>                            it.timestamp &gt;= prefs.getLong(&quot;enabled_at&quot;, 0L)</code> | Invoca/continua prefs.getLong com os argumentos declarados. Timestamp da ativação usado para comparar histórico posterior de parada explícita. |
| <a id="L31"></a>31 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L32"></a>32 | <code>            if (stopped) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L33"></a>33 | <code>                prefs.edit().putBoolean(&quot;wanted&quot;, false).apply()</code> | Invoca/continua prefs.edit com os argumentos declarados. Preferência de manter conexão ativa; desconectar deve impedir restauração automática. |
| <a id="L34"></a>34 | <code>                return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L35"></a>35 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L36"></a>36 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L37"></a>37 | <code>        if (AgentRuntime.auth.session.value == null) return</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L38"></a>38 | <code>        // Credential storage is available after boot/unlock. Never start the microphone here.</code> | Comentário de manutenção/documentação: Credential storage is available after boot/unlock. Never start the microphone here. |
| <a id="L39"></a>39 | <code>        runCatching {</code> | Fornece a expressão runCatching { ao bloco/chamada em construção. |
| <a id="L40"></a>40 | <code>            ContextCompat.startForegroundService(</code> | Invoca/continua ContextCompat.startForegroundService com os argumentos declarados. Solicita início do serviço; as restrições de background do Android continuam valendo. |
| <a id="L41"></a>41 | <code>                context,</code> | Fornece a expressão context, ao bloco/chamada em construção. |
| <a id="L42"></a>42 | <code>                Intent(context, ConnectionService::class.java),</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L43"></a>43 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L44"></a>44 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L45"></a>45 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L46"></a>46 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
