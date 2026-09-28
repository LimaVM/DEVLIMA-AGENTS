# android/app/src/main/java/br/com/vegasolucoes/agent/VoiceService.kt

Hospeda voz como foreground service após atendimento com interface visível; disponibiliza controlador reativo e libera áudio ao encerrar.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/VoiceService.kt) · 70 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [VoiceService](#L15) | Define o tipo VoiceService e reúne o estado/contrato descrito para este módulo. |
| [VoiceService.onBind](#L20) | Trata o callback de VoiceService.onBind, segundo o contrato e as verificações deste módulo. |
| [VoiceService.onStartCommand](#L24) | Trata o callback de VoiceService.onStartCommand, segundo o contrato e as verificações deste módulo. |
| [VoiceService.onDestroy](#L65) | Trata o callback de VoiceService.onDestroy, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.app.PendingIntent</code> | Disponibiliza o símbolo Kotlin/Android android.app.PendingIntent neste arquivo. |
| <a id="L5"></a>5 | <code>import android.app.Service</code> | Disponibiliza o símbolo Kotlin/Android android.app.Service neste arquivo. |
| <a id="L6"></a>6 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L7"></a>7 | <code>import android.content.pm.PackageManager</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.PackageManager neste arquivo. |
| <a id="L8"></a>8 | <code>import android.content.pm.ServiceInfo</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.ServiceInfo neste arquivo. |
| <a id="L9"></a>9 | <code>import android.os.Build</code> | Disponibiliza o símbolo Kotlin/Android android.os.Build neste arquivo. |
| <a id="L10"></a>10 | <code>import android.os.IBinder</code> | Disponibiliza o símbolo Kotlin/Android android.os.IBinder neste arquivo. |
| <a id="L11"></a>11 | <code>import androidx.core.app.NotificationCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.app.NotificationCompat neste arquivo. |
| <a id="L12"></a>12 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L14"></a>14 | <code>// Documentação: Define o tipo VoiceService e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo VoiceService e reúne o estado/contrato descrito para este módulo. |
| <a id="L15"></a>15 | <code>class VoiceService : Service() {</code> | Define o tipo VoiceService e reúne o estado/contrato descrito para este módulo. |
| <a id="L16"></a>16 | <code>    private var controller: VoiceController? = null</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L17"></a>17 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L18"></a>18 | <code>    // Documentação: Trata o callback de VoiceService.onBind, segundo o contrato e as verificações</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceService.onBind, segundo o contrato e as verificações |
| <a id="L19"></a>19 | <code>    // deste módulo.</code> | Comentário de manutenção/documentação: deste módulo. |
| <a id="L20"></a>20 | <code>    override fun onBind(intent: Intent?): IBinder? = null</code> | Trata o callback de VoiceService.onBind, segundo o contrato e as verificações deste módulo. |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L22"></a>22 | <code>    // Documentação: Trata o callback de VoiceService.onStartCommand, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceService.onStartCommand, segundo o contrato e as |
| <a id="L23"></a>23 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L24"></a>24 | <code>    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {</code> | Trata o callback de VoiceService.onStartCommand, segundo o contrato e as verificações deste módulo. |
| <a id="L25"></a>25 | <code>        val call = AgentRuntime.call.value</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L26"></a>26 | <code>        if (call == null &#124;&#124; call.optString(&quot;status&quot;) != &quot;ACTIVE&quot;) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L27"></a>27 | <code>            stopSelf()</code> | Invoca/continua stopSelf com os argumentos declarados. Encerra este serviço conforme seu ciclo de vida Android. |
| <a id="L28"></a>28 | <code>            return START_NOT_STICKY</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L29"></a>29 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L30"></a>30 | <code>        val open =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L31"></a>31 | <code>            PendingIntent.getActivity(</code> | Invoca/continua PendingIntent.getActivity com os argumentos declarados. |
| <a id="L32"></a>32 | <code>                this,</code> | Fornece a expressão this, ao bloco/chamada em construção. |
| <a id="L33"></a>33 | <code>                42,</code> | Fornece a expressão 42, ao bloco/chamada em construção. |
| <a id="L34"></a>34 | <code>                Intent(this, MainActivity::class.java),</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L35"></a>35 | <code>                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,</code> | Fornece a expressão PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT, ao bloco/chamada em construção. |
| <a id="L36"></a>36 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L37"></a>37 | <code>        val notification =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L38"></a>38 | <code>            NotificationCompat.Builder(this, &quot;connection&quot;)</code> | Invoca/continua NotificationCompat.Builder com os argumentos declarados. |
| <a id="L39"></a>39 | <code>                .setSmallIcon(R.drawable.ic_agent)</code> | Invoca/continua setSmallIcon com os argumentos declarados. |
| <a id="L40"></a>40 | <code>                .setContentTitle(&quot;Chamada com DevLima Agent&quot;)</code> | Invoca/continua setContentTitle com os argumentos declarados. |
| <a id="L41"></a>41 | <code>                .setContentText(&quot;Microfone ativo durante a escuta; abra para silenciar ou encerrar&quot;)</code> | Invoca/continua setContentText com os argumentos declarados. |
| <a id="L42"></a>42 | <code>                .setContentIntent(open)</code> | Invoca/continua setContentIntent com os argumentos declarados. Define destino aberto ao acionar o corpo da notificação. |
| <a id="L43"></a>43 | <code>                .setOngoing(true)</code> | Invoca/continua setOngoing com os argumentos declarados. Indica notificação associada a atividade/chamada em andamento. |
| <a id="L44"></a>44 | <code>                .build()</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L45"></a>45 | <code>        val microphone =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L46"></a>46 | <code>            ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) ==</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L47"></a>47 | <code>                PackageManager.PERMISSION_GRANTED</code> | Fornece a expressão PackageManager.PERMISSION_GRANTED ao bloco/chamada em construção. |
| <a id="L48"></a>48 | <code>        if (Build.VERSION.SDK_INT &gt;= 34)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L49"></a>49 | <code>            startForeground(</code> | Invoca/continua startForeground com os argumentos declarados. Publica notificação obrigatória e promove o serviço ao tipo declarado. |
| <a id="L50"></a>50 | <code>                3,</code> | Fornece a expressão 3, ao bloco/chamada em construção. |
| <a id="L51"></a>51 | <code>                notification,</code> | Fornece a expressão notification, ao bloco/chamada em construção. |
| <a id="L52"></a>52 | <code>                if (microphone) ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L53"></a>53 | <code>                else ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE,</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L54"></a>54 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L55"></a>55 | <code>        else startForeground(3, notification)</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. Publica notificação obrigatória e promove o serviço ao tipo declarado. |
| <a id="L56"></a>56 | <code>        if (controller == null) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L57"></a>57 | <code>            controller = VoiceController(this, call) { stopSelf() }</code> | Invoca/continua VoiceController com os argumentos declarados. Encerra este serviço conforme seu ciclo de vida Android. |
| <a id="L58"></a>58 | <code>            AgentRuntime.voice.value = controller</code> | Fornece a expressão AgentRuntime.voice.value = controller ao bloco/chamada em construção. |
| <a id="L59"></a>59 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L60"></a>60 | <code>        return START_NOT_STICKY</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L61"></a>61 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L62"></a>62 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L63"></a>63 | <code>    // Documentação: Trata o callback de VoiceService.onDestroy, segundo o contrato e as</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceService.onDestroy, segundo o contrato e as |
| <a id="L64"></a>64 | <code>    // verificações deste módulo.</code> | Comentário de manutenção/documentação: verificações deste módulo. |
| <a id="L65"></a>65 | <code>    override fun onDestroy() {</code> | Trata o callback de VoiceService.onDestroy, segundo o contrato e as verificações deste módulo. |
| <a id="L66"></a>66 | <code>        controller?.destroy()</code> | Invoca/continua destroy com os argumentos declarados. |
| <a id="L67"></a>67 | <code>        if (AgentRuntime.voice.value === controller) AgentRuntime.voice.value = null</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L68"></a>68 | <code>        super.onDestroy()</code> | Invoca/continua super.onDestroy com os argumentos declarados. |
| <a id="L69"></a>69 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L70"></a>70 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
