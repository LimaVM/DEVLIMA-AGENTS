# android/app/src/main/java/br/com/vegasolucoes/agent/MainActivity.kt

Hospeda login e navegação Chat/Rotina/Conta, controla conexão desejada e solicita notificações com ação do usuário.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/MainActivity.kt) · 239 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [MainActivity](#L39) | Define o tipo MainActivity e reúne o estado/contrato descrito para este módulo. |
| [MainActivity.onCreate](#L42) | Trata o callback de MainActivity.onCreate, segundo o contrato e as verificações deste módulo. |
| [MainActivity.connect](#L54) | Implementa MainActivity.connect como parte do fluxo descrito para este arquivo. |
| [MainActivity.disconnect](#L60) | Implementa MainActivity.disconnect como parte do fluxo descrito para este arquivo. |
| [AgentScreen](#L69) | Implementa AgentScreen como parte do fluxo descrito para este arquivo. |
| [startConnection](#L81) | Inicia startConnection, segundo o contrato e as verificações deste módulo. |
| [LoginScreen](#L168) | Implementa LoginScreen como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L5"></a>5 | <code>import android.content.pm.PackageManager</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.PackageManager neste arquivo. |
| <a id="L6"></a>6 | <code>import android.os.Build</code> | Disponibiliza o símbolo Kotlin/Android android.os.Build neste arquivo. |
| <a id="L7"></a>7 | <code>import android.os.Bundle</code> | Disponibiliza o símbolo Kotlin/Android android.os.Bundle neste arquivo. |
| <a id="L8"></a>8 | <code>import androidx.activity.ComponentActivity</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.ComponentActivity neste arquivo. |
| <a id="L9"></a>9 | <code>import androidx.activity.compose.rememberLauncherForActivityResult</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.compose.rememberLauncherForActivityResult neste arquivo. |
| <a id="L10"></a>10 | <code>import androidx.activity.compose.setContent</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.compose.setContent neste arquivo. |
| <a id="L11"></a>11 | <code>import androidx.activity.enableEdgeToEdge</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.enableEdgeToEdge neste arquivo. |
| <a id="L12"></a>12 | <code>import androidx.activity.result.contract.ActivityResultContracts</code> | Disponibiliza o símbolo Kotlin/Android androidx.activity.result.contract.ActivityResultContracts neste arquivo. |
| <a id="L13"></a>13 | <code>import androidx.compose.foundation.layout.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.layout.* neste arquivo. |
| <a id="L14"></a>14 | <code>import androidx.compose.foundation.rememberScrollState</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.rememberScrollState neste arquivo. |
| <a id="L15"></a>15 | <code>import androidx.compose.foundation.text.KeyboardOptions</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.text.KeyboardOptions neste arquivo. |
| <a id="L16"></a>16 | <code>import androidx.compose.foundation.verticalScroll</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.foundation.verticalScroll neste arquivo. |
| <a id="L17"></a>17 | <code>import androidx.compose.material3.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.material3.* neste arquivo. |
| <a id="L18"></a>18 | <code>import androidx.compose.runtime.*</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.runtime.* neste arquivo. |
| <a id="L19"></a>19 | <code>import androidx.compose.ui.Modifier</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.Modifier neste arquivo. |
| <a id="L20"></a>20 | <code>import androidx.compose.ui.graphics.Color</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.graphics.Color neste arquivo. |
| <a id="L21"></a>21 | <code>import androidx.compose.ui.text.font.FontWeight</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.text.font.FontWeight neste arquivo. |
| <a id="L22"></a>22 | <code>import androidx.compose.ui.text.input.KeyboardType</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.text.input.KeyboardType neste arquivo. |
| <a id="L23"></a>23 | <code>import androidx.compose.ui.text.input.PasswordVisualTransformation</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.text.input.PasswordVisualTransformation neste arquivo. |
| <a id="L24"></a>24 | <code>import androidx.compose.ui.unit.dp</code> | Disponibiliza o símbolo Kotlin/Android androidx.compose.ui.unit.dp neste arquivo. |
| <a id="L25"></a>25 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L26"></a>26 | <code>import androidx.lifecycle.compose.collectAsStateWithLifecycle</code> | Disponibiliza o símbolo Kotlin/Android androidx.lifecycle.compose.collectAsStateWithLifecycle neste arquivo. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L27"></a>27 | <code>import kotlinx.coroutines.launch</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.launch neste arquivo. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L28"></a>28 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L29"></a>29 | <code>val AgentColors =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L30"></a>30 | <code>    darkColorScheme(</code> | Invoca/continua darkColorScheme com os argumentos declarados. |
| <a id="L31"></a>31 | <code>        primary = Color(0xFF5EEACB),</code> | Invoca/continua Color com os argumentos declarados. |
| <a id="L32"></a>32 | <code>        secondary = Color(0xFF87AAFF),</code> | Invoca/continua Color com os argumentos declarados. |
| <a id="L33"></a>33 | <code>        background = Color(0xFF0C1420),</code> | Invoca/continua Color com os argumentos declarados. |
| <a id="L34"></a>34 | <code>        surface = Color(0xFF142132),</code> | Invoca/continua Color com os argumentos declarados. |
| <a id="L35"></a>35 | <code>        onPrimary = Color(0xFF07241C),</code> | Invoca/continua Color com os argumentos declarados. |
| <a id="L36"></a>36 | <code>    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L38"></a>38 | <code>// Documentação: Define o tipo MainActivity e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo MainActivity e reúne o estado/contrato descrito para este módulo. |
| <a id="L39"></a>39 | <code>class MainActivity : ComponentActivity() {</code> | Define o tipo MainActivity e reúne o estado/contrato descrito para este módulo. |
| <a id="L40"></a>40 | <code>    // Documentação: Trata o callback de MainActivity.onCreate, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de MainActivity.onCreate, segundo o contrato e as |
| <a id="L41"></a>41 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L42"></a>42 | <code>    override fun onCreate(state: Bundle?) {</code> | Trata o callback de MainActivity.onCreate, segundo o contrato e as verificações deste módulo. |
| <a id="L43"></a>43 | <code>        super.onCreate(state)</code> | Invoca/continua super.onCreate com os argumentos declarados. |
| <a id="L44"></a>44 | <code>        enableEdgeToEdge()</code> | Invoca/continua enableEdgeToEdge com os argumentos declarados. |
| <a id="L45"></a>45 | <code>        setContent {</code> | Fornece a expressão setContent { ao bloco/chamada em construção. |
| <a id="L46"></a>46 | <code>            MaterialTheme(colorScheme = AgentColors) {</code> | Invoca/continua MaterialTheme com os argumentos declarados. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L47"></a>47 | <code>                Surface(Modifier.fillMaxSize()) { AgentScreen(this) }</code> | Invoca/continua Surface com os argumentos declarados. Define superfície visual usando cor/forma e componentes filhos. |
| <a id="L48"></a>48 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L49"></a>49 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L50"></a>50 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L51"></a>51 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L52"></a>52 | <code>    // Documentação: Implementa MainActivity.connect como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa MainActivity.connect como parte do fluxo descrito para este |
| <a id="L53"></a>53 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L54"></a>54 | <code>    fun connect() {</code> | Implementa MainActivity.connect como parte do fluxo descrito para este arquivo. |
| <a id="L55"></a>55 | <code>        ContextCompat.startForegroundService(this, Intent(this, ConnectionService::class.java))</code> | Invoca/continua ContextCompat.startForegroundService com os argumentos declarados. Solicita início do serviço; as restrições de background do Android continuam valendo. |
| <a id="L56"></a>56 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L57"></a>57 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L58"></a>58 | <code>    // Documentação: Implementa MainActivity.disconnect como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa MainActivity.disconnect como parte do fluxo descrito para este |
| <a id="L59"></a>59 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L60"></a>60 | <code>    fun disconnect() {</code> | Implementa MainActivity.disconnect como parte do fluxo descrito para este arquivo. |
| <a id="L61"></a>61 | <code>        AgentRuntime.voice.value?.end()</code> | Invoca/continua end com os argumentos declarados. |
| <a id="L62"></a>62 | <code>        stopService(Intent(this, ConnectionService::class.java))</code> | Invoca/continua stopService com os argumentos declarados. Solicita encerrar somente o componente de serviço indicado. |
| <a id="L63"></a>63 | <code>        getSharedPreferences(&quot;connection&quot;, MODE_PRIVATE).edit().putBoolean(&quot;wanted&quot;, false).apply()</code> | Invoca/continua getSharedPreferences com os argumentos declarados. Acessa preferências privadas do aplicativo para conservar escolha/estado. Preferência de manter conexão ativa; desconectar deve impedir restauração automática. |
| <a id="L64"></a>64 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L65"></a>65 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L66"></a>66 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L67"></a>67 | <code>@Composable</code> | Aplica a anotação @Composable à declaração seguinte. |
| <a id="L68"></a>68 | <code>// Documentação: Implementa AgentScreen como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa AgentScreen como parte do fluxo descrito para este arquivo. |
| <a id="L69"></a>69 | <code>fun AgentScreen(activity: MainActivity) {</code> | Implementa AgentScreen como parte do fluxo descrito para este arquivo. |
| <a id="L70"></a>70 | <code>    val session by AgentRuntime.auth.session.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L71"></a>71 | <code>    val connection by AgentRuntime.connection.collectAsStateWithLifecycle()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Observa StateFlow de acordo com o lifecycle para atualizar a interface. |
| <a id="L72"></a>72 | <code>    val scope = rememberCoroutineScope()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L73"></a>73 | <code>    var tab by remember { mutableIntStateOf(0) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L74"></a>74 | <code>    var denied by remember { mutableStateOf(false) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L75"></a>75 | <code>    val permission =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L76"></a>76 | <code>        rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted -&gt;</code> | Invoca/continua rememberLauncherForActivityResult com os argumentos declarados. |
| <a id="L77"></a>77 | <code>            denied = !granted</code> | Fornece o valor de denied no contexto desta expressão. |
| <a id="L78"></a>78 | <code>            activity.connect()</code> | Invoca/continua activity.connect com os argumentos declarados. |
| <a id="L79"></a>79 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L80"></a>80 | <code>    // Documentação: Inicia startConnection, segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: Documentação: Inicia startConnection, segundo o contrato e as verificações deste módulo. |
| <a id="L81"></a>81 | <code>    fun startConnection() {</code> | Inicia startConnection, segundo o contrato e as verificações deste módulo. |
| <a id="L82"></a>82 | <code>        if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L83"></a>83 | <code>            Build.VERSION.SDK_INT &gt;= 33 &amp;&amp;</code> | Fornece a expressão Build.VERSION.SDK_INT &gt;= 33 &amp;&amp; ao bloco/chamada em construção. |
| <a id="L84"></a>84 | <code>                ContextCompat.checkSelfPermission(</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L85"></a>85 | <code>                    activity,</code> | Fornece a expressão activity, ao bloco/chamada em construção. |
| <a id="L86"></a>86 | <code>                    Manifest.permission.POST_NOTIFICATIONS,</code> | Fornece a expressão Manifest.permission.POST_NOTIFICATIONS, ao bloco/chamada em construção. |
| <a id="L87"></a>87 | <code>                ) != PackageManager.PERMISSION_GRANTED</code> | Fornece a expressão ) != PackageManager.PERMISSION_GRANTED ao bloco/chamada em construção. |
| <a id="L88"></a>88 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L89"></a>89 | <code>            permission.launch(Manifest.permission.POST_NOTIFICATIONS)</code> | Invoca/continua permission.launch com os argumentos declarados. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L90"></a>90 | <code>        else activity.connect()</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L91"></a>91 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L92"></a>92 | <code>    if (session == null) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L93"></a>93 | <code>        LoginScreen { startConnection() }</code> | Invoca/continua startConnection com os argumentos declarados. |
| <a id="L94"></a>94 | <code>        return</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L95"></a>95 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L96"></a>96 | <code>    CallOverlay(activity, session!!)</code> | Invoca/continua CallOverlay com os argumentos declarados. |
| <a id="L97"></a>97 | <code>    Scaffold(</code> | Invoca/continua Scaffold com os argumentos declarados. Reserva áreas para navegação/conteúdo e entrega padding ao layout. |
| <a id="L98"></a>98 | <code>        modifier = Modifier.systemBarsPadding().imePadding(),</code> | Invoca/continua Modifier.systemBarsPadding com os argumentos declarados. |
| <a id="L99"></a>99 | <code>        bottomBar = {</code> | Fornece o valor de bottomBar no contexto desta expressão. |
| <a id="L100"></a>100 | <code>            NavigationBar {</code> | Fornece a expressão NavigationBar { ao bloco/chamada em construção. |
| <a id="L101"></a>101 | <code>                listOf(&quot;Chat&quot;, &quot;Rotina&quot;, &quot;Conta&quot;).forEachIndexed { i, label -&gt;</code> | Invoca/continua listOf com os argumentos declarados. |
| <a id="L102"></a>102 | <code>                    NavigationBarItem(</code> | Invoca/continua NavigationBarItem com os argumentos declarados. Cria destino de navegação com seleção e callback onClick. |
| <a id="L103"></a>103 | <code>                        selected = tab == i,</code> | Fornece o valor de selected no contexto desta expressão. |
| <a id="L104"></a>104 | <code>                        onClick = { tab = i },</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L105"></a>105 | <code>                        icon = { Text(listOf(&quot;●&quot;, &quot;✓&quot;, &quot;◉&quot;)[i]) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L106"></a>106 | <code>                        label = { Text(label) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L107"></a>107 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L108"></a>108 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L109"></a>109 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L110"></a>110 | <code>        },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L111"></a>111 | <code>    ) { padding -&gt;</code> | Fornece a expressão ) { padding -&gt; ao bloco/chamada em construção. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L112"></a>112 | <code>        Column(Modifier.fillMaxSize().padding(padding)) {</code> | Invoca/continua Column com os argumentos declarados. Organiza componentes filhos verticalmente no layout. |
| <a id="L113"></a>113 | <code>            Row(</code> | Invoca/continua Row com os argumentos declarados. Organiza componentes filhos horizontalmente no layout. |
| <a id="L114"></a>114 | <code>                Modifier.fillMaxWidth().padding(16.dp),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L115"></a>115 | <code>                horizontalArrangement = Arrangement.SpaceBetween,</code> | Fornece o valor de horizontalArrangement no contexto desta expressão. |
| <a id="L116"></a>116 | <code>            ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L117"></a>117 | <code>                Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L118"></a>118 | <code>                    &quot;DEVLIMA AGENT&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L119"></a>119 | <code>                    fontWeight = FontWeight.Bold,</code> | Fornece o valor de fontWeight no contexto desta expressão. |
| <a id="L120"></a>120 | <code>                    color = MaterialTheme.colorScheme.primary,</code> | Fornece o valor de color no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L121"></a>121 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L122"></a>122 | <code>                Text(connection, style = MaterialTheme.typography.labelSmall)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L123"></a>123 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L124"></a>124 | <code>            if (denied)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L125"></a>125 | <code>                Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L126"></a>126 | <code>                    &quot;Notificações desativadas. Ative nas configurações para receber avisos.&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L127"></a>127 | <code>                    Modifier.padding(horizontal = 16.dp),</code> | Invoca/continua Modifier.padding com os argumentos declarados. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L128"></a>128 | <code>                    color = MaterialTheme.colorScheme.error,</code> | Fornece o valor de color no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L129"></a>129 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L130"></a>130 | <code>            when (tab) {</code> | Despacha o valor/condição para os ramos declarados abaixo. |
| <a id="L131"></a>131 | <code>                0 -&gt; ChatScreen { startConnection() }</code> | Invoca/continua startConnection com os argumentos declarados. |
| <a id="L132"></a>132 | <code>                1 -&gt; RoutineScreen(session!!)</code> | Invoca/continua RoutineScreen com os argumentos declarados. |
| <a id="L133"></a>133 | <code>                else -&gt;</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L134"></a>134 | <code>                    Column(</code> | Invoca/continua Column com os argumentos declarados. Organiza componentes filhos verticalmente no layout. |
| <a id="L135"></a>135 | <code>                        Modifier.verticalScroll(rememberScrollState()).padding(20.dp),</code> | Invoca/continua Modifier.verticalScroll com os argumentos declarados. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L136"></a>136 | <code>                        verticalArrangement = Arrangement.spacedBy(16.dp),</code> | Invoca/continua Arrangement.spacedBy com os argumentos declarados. |
| <a id="L137"></a>137 | <code>                    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L138"></a>138 | <code>                        Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L139"></a>139 | <code>                            &quot;Olá, ${session!!.username}&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L140"></a>140 | <code>                            style = MaterialTheme.typography.headlineSmall,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L141"></a>141 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L142"></a>142 | <code>                        Text(session!!.server)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L143"></a>143 | <code>                        Text(&quot;Horários: ${session!!.timezone}&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L144"></a>144 | <code>                        CallDeliverySettings(activity)</code> | Invoca/continua CallDeliverySettings com os argumentos declarados. |
| <a id="L145"></a>145 | <code>                        Button(onClick = { startConnection() }) { Text(&quot;Conectar&quot;) }</code> | Invoca/continua Button com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L146"></a>146 | <code>                        OutlinedButton(onClick = { activity.disconnect() }) { Text(&quot;Desconectar&quot;) }</code> | Invoca/continua OutlinedButton com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L147"></a>147 | <code>                        TextButton(</code> | Invoca/continua TextButton com os argumentos declarados. Cria ação textual com a condição enabled declarada. |
| <a id="L148"></a>148 | <code>                            onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L149"></a>149 | <code>                                scope.launch {</code> | Fornece a expressão scope.launch { ao bloco/chamada em construção. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L150"></a>150 | <code>                                    activity.disconnect()</code> | Invoca/continua activity.disconnect com os argumentos declarados. |
| <a id="L151"></a>151 | <code>                                    AgentRuntime.auth.logout()</code> | Invoca/continua AgentRuntime.auth.logout com os argumentos declarados. |
| <a id="L152"></a>152 | <code>                                    AgentRuntime.events.clear()</code> | Invoca/continua AgentRuntime.events.clear com os argumentos declarados. |
| <a id="L153"></a>153 | <code>                                    AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L154"></a>154 | <code>                                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L155"></a>155 | <code>                            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L156"></a>156 | <code>                        ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L157"></a>157 | <code>                            Text(&quot;Sair da conta&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L158"></a>158 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L159"></a>159 | <code>                        MemoryScreen()</code> | Invoca/continua MemoryScreen com os argumentos declarados. |
| <a id="L160"></a>160 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L161"></a>161 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L162"></a>162 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L163"></a>163 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L164"></a>164 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L165"></a>165 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L166"></a>166 | <code>@Composable</code> | Aplica a anotação @Composable à declaração seguinte. |
| <a id="L167"></a>167 | <code>// Documentação: Implementa LoginScreen como parte do fluxo descrito para este arquivo.</code> | Comentário de manutenção/documentação: Documentação: Implementa LoginScreen como parte do fluxo descrito para este arquivo. |
| <a id="L168"></a>168 | <code>private fun LoginScreen(onLogged: () -&gt; Unit) {</code> | Implementa LoginScreen como parte do fluxo descrito para este arquivo. |
| <a id="L169"></a>169 | <code>    val scope = rememberCoroutineScope()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L170"></a>170 | <code>    var busy by remember { mutableStateOf(false) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L171"></a>171 | <code>    var error by remember { mutableStateOf&lt;String?&gt;(null) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L172"></a>172 | <code>    var server by remember { mutableStateOf(BuildConfig.DEFAULT_SERVER) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L173"></a>173 | <code>    var username by remember { mutableStateOf(&quot;&quot;) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L174"></a>174 | <code>    var password by remember { mutableStateOf(&quot;&quot;) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Conserva valor/estado entre recomposições do trecho Compose. |
| <a id="L175"></a>175 | <code>    Column(</code> | Invoca/continua Column com os argumentos declarados. Organiza componentes filhos verticalmente no layout. |
| <a id="L176"></a>176 | <code>        Modifier.fillMaxSize()</code> | Invoca/continua Modifier.fillMaxSize com os argumentos declarados. Solicita ocupar o tamanho disponível no layout pai. |
| <a id="L177"></a>177 | <code>            .systemBarsPadding()</code> | Invoca/continua systemBarsPadding com os argumentos declarados. |
| <a id="L178"></a>178 | <code>            .imePadding()</code> | Invoca/continua imePadding com os argumentos declarados. |
| <a id="L179"></a>179 | <code>            .verticalScroll(rememberScrollState())</code> | Invoca/continua verticalScroll com os argumentos declarados. |
| <a id="L180"></a>180 | <code>            .padding(24.dp),</code> | Invoca/continua padding com os argumentos declarados. Aplica espaço interno ao componente segundo os valores declarados. |
| <a id="L181"></a>181 | <code>        verticalArrangement = Arrangement.spacedBy(18.dp),</code> | Invoca/continua Arrangement.spacedBy com os argumentos declarados. |
| <a id="L182"></a>182 | <code>    ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L183"></a>183 | <code>        Spacer(Modifier.height(24.dp))</code> | Invoca/continua Spacer com os argumentos declarados. |
| <a id="L184"></a>184 | <code>        Text(&quot;DEVLIMA&quot;, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L185"></a>185 | <code>        Text(</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L186"></a>186 | <code>            &quot;Seu agente,\nsempre por perto.&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L187"></a>187 | <code>            style = MaterialTheme.typography.headlineLarge,</code> | Fornece o valor de style no contexto desta expressão. Disponibiliza cores/tipografia ao conteúdo Compose. |
| <a id="L188"></a>188 | <code>            fontWeight = FontWeight.Bold,</code> | Fornece o valor de fontWeight no contexto desta expressão. |
| <a id="L189"></a>189 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L190"></a>190 | <code>        Text(&quot;Converse, organize seus lembretes e receba chamadas do seu agente pessoal.&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L191"></a>191 | <code>        OutlinedTextField(</code> | Invoca/continua OutlinedTextField com os argumentos declarados. Liga entrada de texto ao valor e callback de alteração. |
| <a id="L192"></a>192 | <code>            server,</code> | Fornece a expressão server, ao bloco/chamada em construção. |
| <a id="L193"></a>193 | <code>            { server = it },</code> | Fornece a expressão { server = it }, ao bloco/chamada em construção. |
| <a id="L194"></a>194 | <code>            label = { Text(&quot;Servidor HTTPS&quot;) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L195"></a>195 | <code>            singleLine = true,</code> | Fornece o valor de singleLine no contexto desta expressão. |
| <a id="L196"></a>196 | <code>            modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L197"></a>197 | <code>            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Uri),</code> | Invoca/continua KeyboardOptions com os argumentos declarados. |
| <a id="L198"></a>198 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L199"></a>199 | <code>        OutlinedTextField(</code> | Invoca/continua OutlinedTextField com os argumentos declarados. Liga entrada de texto ao valor e callback de alteração. |
| <a id="L200"></a>200 | <code>            username,</code> | Fornece a expressão username, ao bloco/chamada em construção. |
| <a id="L201"></a>201 | <code>            { username = it },</code> | Fornece a expressão { username = it }, ao bloco/chamada em construção. |
| <a id="L202"></a>202 | <code>            label = { Text(&quot;Usuário&quot;) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L203"></a>203 | <code>            singleLine = true,</code> | Fornece o valor de singleLine no contexto desta expressão. |
| <a id="L204"></a>204 | <code>            modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L205"></a>205 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L206"></a>206 | <code>        OutlinedTextField(</code> | Invoca/continua OutlinedTextField com os argumentos declarados. Liga entrada de texto ao valor e callback de alteração. |
| <a id="L207"></a>207 | <code>            password,</code> | Fornece a expressão password, ao bloco/chamada em construção. |
| <a id="L208"></a>208 | <code>            { password = it },</code> | Fornece a expressão { password = it }, ao bloco/chamada em construção. |
| <a id="L209"></a>209 | <code>            label = { Text(&quot;Senha&quot;) },</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L210"></a>210 | <code>            visualTransformation = PasswordVisualTransformation(),</code> | Invoca/continua PasswordVisualTransformation com os argumentos declarados. |
| <a id="L211"></a>211 | <code>            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),</code> | Invoca/continua KeyboardOptions com os argumentos declarados. |
| <a id="L212"></a>212 | <code>            singleLine = true,</code> | Fornece o valor de singleLine no contexto desta expressão. |
| <a id="L213"></a>213 | <code>            modifier = Modifier.fillMaxWidth(),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L214"></a>214 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L215"></a>215 | <code>        Button(</code> | Invoca/continua Button com os argumentos declarados. Cria controle que executa onClick quando habilitado e acionado. |
| <a id="L216"></a>216 | <code>            onClick = {</code> | Fornece o valor de onClick no contexto desta expressão. |
| <a id="L217"></a>217 | <code>                scope.launch {</code> | Fornece a expressão scope.launch { ao bloco/chamada em construção. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L218"></a>218 | <code>                    busy = true</code> | Fornece o valor de busy no contexto desta expressão. |
| <a id="L219"></a>219 | <code>                    error = null</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L220"></a>220 | <code>                    try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L221"></a>221 | <code>                        AgentRuntime.auth.login(server, username, password)</code> | Invoca/continua AgentRuntime.auth.login com os argumentos declarados. |
| <a id="L222"></a>222 | <code>                        password = &quot;&quot;</code> | Fornece o valor de password no contexto desta expressão. |
| <a id="L223"></a>223 | <code>                        AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L224"></a>224 | <code>                        onLogged()</code> | Invoca/continua onLogged com os argumentos declarados. |
| <a id="L225"></a>225 | <code>                    } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L226"></a>226 | <code>                        error = &quot;Não foi possível entrar. Confira os dados e sua conexão.&quot;</code> | Fornece o valor de error no contexto desta expressão. |
| <a id="L227"></a>227 | <code>                    } finally {</code> | Fornece a expressão } finally { ao bloco/chamada em construção. |
| <a id="L228"></a>228 | <code>                        busy = false</code> | Fornece o valor de busy no contexto desta expressão. |
| <a id="L229"></a>229 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L230"></a>230 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L231"></a>231 | <code>            },</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L232"></a>232 | <code>            enabled = !busy &amp;&amp; username.isNotBlank() &amp;&amp; password.isNotBlank(),</code> | Invoca/continua username.isNotBlank com os argumentos declarados. |
| <a id="L233"></a>233 | <code>            modifier = Modifier.fillMaxWidth().height(52.dp),</code> | Invoca/continua Modifier.fillMaxWidth com os argumentos declarados. Solicita ocupar a largura disponível no layout pai. |
| <a id="L234"></a>234 | <code>        ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L235"></a>235 | <code>            Text(if (busy) &quot;Entrando…&quot; else &quot;Entrar&quot;)</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L236"></a>236 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L237"></a>237 | <code>        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }</code> | Invoca/continua Text com os argumentos declarados. Renderiza texto/estado com estilo e conteúdo declarados. |
| <a id="L238"></a>238 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L239"></a>239 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
