# android/app/src/main/java/br/com/vegasolucoes/agent/CallDeliverySettings.kt

Mostra condições reais de entrega e atalhos oficiais para notificações, tela cheia e bateria; a escolha das permissões continua com o usuário.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/CallDeliverySettings.kt) · 95 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [CallDeliverySettings](#L22) | Implementa CallDeliverySettings como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.app.NotificationManager</code> | Disponibiliza o símbolo Kotlin/Android android.app.NotificationManager neste arquivo. |
| <a id="L5"></a>5 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L6"></a>6 | <code>import android.content.pm.PackageManager</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.PackageManager neste arquivo. |
| <a id="L7"></a>7 | <code>import android.net.Uri</code> | Disponibiliza o símbolo Kotlin/Android android.net.Uri neste arquivo. |
| <a id="L8"></a>8 | <code>import android.os.Build</code> | Disponibiliza o símbolo Kotlin/Android android.os.Build neste arquivo. |
| <a id="L9"></a>9 | <code>import android.os.PowerManager</code> | Disponibiliza o símbolo Kotlin/Android android.os.PowerManager neste arquivo. |
| <a id="L10"></a>10 | <code>import android.provider.Settings</code> | Disponibiliza o símbolo Kotlin/Android android.provider.Settings neste arquivo. |
| <a id="L11"></a>11 | <code>import androidx.activity.compose.rememberLauncherForActivityResult</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.compose.rememberLauncherForActivityResult neste arquivo. |
| <a id="L12"></a>12 | <code>import androidx.activity.result.contract.ActivityResultContracts</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.result.contract.ActivityResultContracts neste arquivo. |
| <a id="L13"></a>13 | <code>import androidx.compose.foundation.layout.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.layout.* neste arquivo. |
| <a id="L14"></a>14 | <code>import androidx.compose.material3.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.material3.* neste arquivo. |
| <a id="L15"></a>15 | <code>import androidx.compose.runtime.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.runtime.* neste arquivo. |
| <a id="L16"></a>16 | <code>import androidx.compose.ui.Modifier</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.Modifier neste arquivo. |
| <a id="L17"></a>17 | <code>import androidx.compose.ui.unit.dp</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.unit.dp neste arquivo. |
| <a id="L18"></a>18 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L19"></a>19 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L20"></a>20 | <code>@Composable</code> | Aplica a anotação @Composable à declaração seguinte. |
| <a id="L21"></a>21 | <code>// Documentação: Implementa CallDeliverySettings como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa CallDeliverySettings como parte do fluxo descrito para este arquivo. |
| <a id="L22"></a>22 | <code>fun CallDeliverySettings(activity: MainActivity) {</code> | Implementa CallDeliverySettings como parte do fluxo descrito para este arquivo. |
| <a id="L23"></a>23 | <code>    var revision by remember { mutableIntStateOf(0) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L24"></a>24 | <code>    val settings =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L25"></a>25 | <code>        rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) {</code> | Invoca/continua rememberLauncherForActivityResult com os argumentos declarados. |
| <a id="L26"></a>26 | <code>            revision++</code> | Fornece a expressão revision++ ao bloco/chamada em construção. |
| <a id="L27"></a>27 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L28"></a>28 | <code>    val manager = activity.getSystemService(NotificationManager::class.java)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L29"></a>29 | <code>    val power = activity.getSystemService(PowerManager::class.java)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L30"></a>30 | <code>    val enabled =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L31"></a>31 | <code>        remember(revision) {</code> | Invoca/continua remember com os argumentos declarados. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L32"></a>32 | <code>            manager.areNotificationsEnabled() &amp;&amp;</code> | Invoca/continua manager.areNotificationsEnabled com os argumentos declarados. |
| <a id="L33"></a>33 | <code>                (Build.VERSION.SDK_INT &lt; 33 &#124;&#124;</code> | Fornece a expressão (Build.VERSION.SDK_INT &lt; 33 &#124;&#124; ao bloco/chamada em construção. |
| <a id="L34"></a>34 | <code>                    ContextCompat.checkSelfPermission(</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L35"></a>35 | <code>                        activity,</code> | Fornece a expressão activity, ao bloco/chamada em construção. |
| <a id="L36"></a>36 | <code>                        Manifest.permission.POST_NOTIFICATIONS,</code> | Fornece a expressão Manifest.permission.POST_NOTIFICATIONS, ao bloco/chamada em construção. |
| <a id="L37"></a>37 | <code>                    ) == PackageManager.PERMISSION_GRANTED) &amp;&amp;</code> | Fornece a expressão ) == PackageManager.PERMISSION_GRANTED) &amp;&amp; ao bloco/chamada em construção. |
| <a id="L38"></a>38 | <code>                (manager.getNotificationChannel(AgentNotifications.CALL_CHANNEL)?.importance</code> | Invoca/continua manager.getNotificationChannel com os argumentos declarados. |
| <a id="L39"></a>39 | <code>                    ?: 0) &gt;= NotificationManager.IMPORTANCE_HIGH</code> | Fornece a expressão ?: 0) &gt;= NotificationManager.IMPORTANCE_HIGH ao bloco/chamada em construção. |
| <a id="L40"></a>40 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L41"></a>41 | <code>    val fullscreen =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L42"></a>42 | <code>        remember(revision) { Build.VERSION.SDK_INT &lt; 34 &#124;&#124; manager.canUseFullScreenIntent() }</code> | Invoca/continua remember com os argumentos declarados. Confere a autorização de tela cheia antes de solicitar apresentação da chamada. |
| <a id="L43"></a>43 | <code>    val battery = remember(revision) { power.isIgnoringBatteryOptimizations(activity.packageName) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L44"></a>44 | <code>    Text(&quot;Receber chamadas com a tela bloqueada&quot;, style = MaterialTheme.typography.titleLarge)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L45"></a>45 | <code>    Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L46"></a>46 | <code>        &quot;Você pode fechar a tela do app. Mantenha DevLima Agent ativo na notificação para receber chamadas. Ao conectar, ele também tentará reconectar após reiniciar e desbloquear o celular.&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L47"></a>47 | <code>    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L48"></a>48 | <code>    Text(&quot;Notificações de chamada: &quot; + if (enabled) &quot;permitidas&quot; else &quot;precisam de configuração&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L49"></a>49 | <code>    OutlinedButton(</code> | Invoca/continua OutlinedButton com os argumentos declarados. Cria controle com contorno e a ação onClick declarada. |
| <a id="L50"></a>50 | <code>        onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L51"></a>51 | <code>            settings.launch(</code> | Invoca/continua settings.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L52"></a>52 | <code>                Intent(Settings.ACTION_CHANNEL_NOTIFICATION_SETTINGS)</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L53"></a>53 | <code>                    .putExtra(Settings.EXTRA_APP_PACKAGE, activity.packageName)</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. |
| <a id="L54"></a>54 | <code>                    .putExtra(Settings.EXTRA_CHANNEL_ID, AgentNotifications.CALL_CHANNEL)</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. |
| <a id="L55"></a>55 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L56"></a>56 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L57"></a>57 | <code>    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L58"></a>58 | <code>        Text(&quot;Configurar toque e notificações&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L59"></a>59 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L60"></a>60 | <code>    if (Build.VERSION.SDK_INT &gt;= 34) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L61"></a>61 | <code>        Text(&quot;Tela de chamada: &quot; + if (fullscreen) &quot;permitida&quot; else &quot;toque para permitir&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L62"></a>62 | <code>        OutlinedButton(</code> | Invoca/continua OutlinedButton com os argumentos declarados. Cria controle com contorno e a ação onClick declarada. |
| <a id="L63"></a>63 | <code>            onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L64"></a>64 | <code>                settings.launch(</code> | Invoca/continua settings.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L65"></a>65 | <code>                    Intent(</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L66"></a>66 | <code>                        Settings.ACTION_MANAGE_APP_USE_FULL_SCREEN_INTENT,</code> | Fornece a expressão Settings.ACTION_MANAGE_APP_USE_FULL_SCREEN_INTENT, ao bloco/chamada em construção. |
| <a id="L67"></a>67 | <code>                        Uri.parse(&quot;package:&quot; + activity.packageName),</code> | Invoca/continua Uri.parse com os argumentos declarados. |
| <a id="L68"></a>68 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L69"></a>69 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L70"></a>70 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L71"></a>71 | <code>        ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L72"></a>72 | <code>            Text(&quot;Permitir chamada na tela bloqueada&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L73"></a>73 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L74"></a>74 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L75"></a>75 | <code>    Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L76"></a>76 | <code>        &quot;Economia de bateria: &quot; +</code> | Fornece a expressão &quot;Economia de bateria: &quot; + ao bloco/chamada em construção. |
| <a id="L77"></a>77 | <code>            if (battery) &quot;sem otimização do Android&quot; else &quot;pode atrasar chamadas em repouso&quot;</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L78"></a>78 | <code>    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L79"></a>79 | <code>    OutlinedButton(</code> | Invoca/continua OutlinedButton com os argumentos declarados. Cria controle com contorno e a ação onClick declarada. |
| <a id="L80"></a>80 | <code>        onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L81"></a>81 | <code>            settings.launch(Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS))</code> | Invoca/continua settings.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L82"></a>82 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L83"></a>83 | <code>    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L84"></a>84 | <code>        Text(&quot;Configurar bateria&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L85"></a>85 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L86"></a>86 | <code>    Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L87"></a>87 | <code>        &quot;Em Xiaomi, confira também início automático e bateria Sem restrições nas configurações do app. As opções dependem da versão do sistema.&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L88"></a>88 | <code>        style = MaterialTheme.typography.bodySmall,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L89"></a>89 | <code>    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L90"></a>90 | <code>    Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L91"></a>91 | <code>        &quot;Sem internet, após Forçar parada ou encerrar o agente em Apps ativos, não há chamada imediata. Abra o app e toque Conectar para retomar. Não perturbe e volume de toque continuam valendo.&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L92"></a>92 | <code>        style = MaterialTheme.typography.bodySmall,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L93"></a>93 | <code>    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L94"></a>94 | <code>    Spacer(Modifier.height(4.dp))</code> | Invoca/continua Spacer com os argumentos declarados. |
| <a id="L95"></a>95 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
