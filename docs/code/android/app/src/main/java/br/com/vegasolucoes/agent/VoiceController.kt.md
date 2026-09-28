# android/app/src/main/java/br/com/vegasolucoes/agent/VoiceController.kt

Coordena SpeechRecognizer, TTS, foco de áudio, fila de transcrição e controles. Libera foco antes de escutar e evita registrar o texto reconhecido em logs.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/VoiceController.kt) · 390 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [VoiceController](#L32) | Define o tipo VoiceController e reúne o estado/contrato descrito para este módulo. |
| [VoiceController.onStart](#L92) | Trata o callback de VoiceController.onStart, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onDone](#L96) | Trata o callback de VoiceController.onDone, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onError](#L107) | Trata o callback de VoiceController.onError, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onReadyForSpeech](#L122) | Trata o callback de VoiceController.onReadyForSpeech, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onBeginningOfSpeech](#L128) | Trata o callback de VoiceController.onBeginningOfSpeech, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onRmsChanged](#L132) | Trata o callback de VoiceController.onRmsChanged, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onBufferReceived](#L136) | Trata o callback de VoiceController.onBufferReceived, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onEndOfSpeech](#L140) | Trata o callback de VoiceController.onEndOfSpeech, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onError](#L146) | Trata o callback de VoiceController.onError, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onResults](#L166) | Trata o callback de VoiceController.onResults, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onPartialResults](#L179) | Trata o callback de VoiceController.onPartialResults, segundo o contrato e as verificações deste módulo. |
| [VoiceController.onEvent](#L183) | Trata o callback de VoiceController.onEvent, segundo o contrato e as verificações deste módulo. |
| [VoiceController.listen](#L191) | Inicia reconhecimento respeitando estado da chamada/mute e libera foco antes da captura. |
| [VoiceController.sendText](#L226) | Implementa VoiceController.sendText como parte do fluxo descrito para este arquivo. |
| [VoiceController.reply](#L238) | Encaminha resposta da chamada correspondente ao TTS sem misturar outra conversa. |
| [VoiceController.response](#L280) | Implementa VoiceController.response como parte do fluxo descrito para este arquivo. |
| [VoiceController.pause](#L297) | Interrompe TTS/escuta ativos e libera recursos/foco conforme o estado. |
| [VoiceController.toggleMute](#L306) | Alterna VoiceController.toggleMute, segundo o contrato e as verificações deste módulo. |
| [VoiceController.toggleSpeaker](#L318) | Alterna VoiceController.toggleSpeaker, segundo o contrato e as verificações deste módulo. |
| [VoiceController.route](#L327) | Implementa VoiceController.route como parte do fluxo descrito para este arquivo. |
| [VoiceController.end](#L342) | Implementa VoiceController.end como parte do fluxo descrito para este arquivo. |
| [VoiceController.finishLocal](#L367) | Implementa VoiceController.finishLocal como parte do fluxo descrito para este arquivo. |
| [VoiceController.destroy](#L380) | Implementa VoiceController.destroy como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.Manifest</code> | Disponibiliza o símbolo Kotlin/Android android.Manifest neste arquivo. |
| <a id="L4"></a>4 | <code>import android.content.Context</code> | Disponibiliza o símbolo Kotlin/Android android.content.Context neste arquivo. |
| <a id="L5"></a>5 | <code>import android.content.Intent</code> | Disponibiliza o símbolo Kotlin/Android android.content.Intent neste arquivo. |
| <a id="L6"></a>6 | <code>import android.content.pm.PackageManager</code> | Disponibiliza o símbolo Kotlin/Android android.content.pm.PackageManager neste arquivo. |
| <a id="L7"></a>7 | <code>import android.media.AudioAttributes</code> | Disponibiliza o símbolo Kotlin/Android android.media.AudioAttributes neste arquivo. |
| <a id="L8"></a>8 | <code>import android.media.AudioDeviceInfo</code> | Disponibiliza o símbolo Kotlin/Android android.media.AudioDeviceInfo neste arquivo. |
| <a id="L9"></a>9 | <code>import android.media.AudioFocusRequest</code> | Disponibiliza o símbolo Kotlin/Android android.media.AudioFocusRequest neste arquivo. |
| <a id="L10"></a>10 | <code>import android.media.AudioManager</code> | Disponibiliza o símbolo Kotlin/Android android.media.AudioManager neste arquivo. |
| <a id="L11"></a>11 | <code>import android.os.Build</code> | Disponibiliza o símbolo Kotlin/Android android.os.Build neste arquivo. |
| <a id="L12"></a>12 | <code>import android.os.Bundle</code> | Disponibiliza o símbolo Kotlin/Android android.os.Bundle neste arquivo. |
| <a id="L13"></a>13 | <code>import android.os.Handler</code> | Disponibiliza o símbolo Kotlin/Android android.os.Handler neste arquivo. |
| <a id="L14"></a>14 | <code>import android.os.Looper</code> | Disponibiliza o símbolo Kotlin/Android android.os.Looper neste arquivo. |
| <a id="L15"></a>15 | <code>import android.speech.RecognitionListener</code> | Disponibiliza o símbolo Kotlin/Android android.speech.RecognitionListener neste arquivo. |
| <a id="L16"></a>16 | <code>import android.speech.RecognizerIntent</code> | Disponibiliza o símbolo Kotlin/Android android.speech.RecognizerIntent neste arquivo. |
| <a id="L17"></a>17 | <code>import android.speech.SpeechRecognizer</code> | Disponibiliza o símbolo Kotlin/Android android.speech.SpeechRecognizer neste arquivo. |
| <a id="L18"></a>18 | <code>import android.speech.tts.TextToSpeech</code> | Disponibiliza o símbolo Kotlin/Android android.speech.tts.TextToSpeech neste arquivo. |
| <a id="L19"></a>19 | <code>import android.speech.tts.UtteranceProgressListener</code> | Disponibiliza o símbolo Kotlin/Android android.speech.tts.UtteranceProgressListener neste arquivo. |
| <a id="L20"></a>20 | <code>import android.util.Log</code> | Disponibiliza o símbolo Kotlin/Android android.util.Log neste arquivo. |
| <a id="L21"></a>21 | <code>import androidx.core.content.ContextCompat</code> | Disponibiliza o símbolo Kotlin/Android androidx.core.content.ContextCompat neste arquivo. |
| <a id="L22"></a>22 | <code>import java.util.Locale</code> | Disponibiliza o símbolo Kotlin/Android java.util.Locale neste arquivo. |
| <a id="L23"></a>23 | <code>import kotlinx.coroutines.CoroutineScope</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.CoroutineScope neste arquivo. |
| <a id="L24"></a>24 | <code>import kotlinx.coroutines.Dispatchers</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.Dispatchers neste arquivo. |
| <a id="L25"></a>25 | <code>import kotlinx.coroutines.SupervisorJob</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.SupervisorJob neste arquivo. |
| <a id="L26"></a>26 | <code>import kotlinx.coroutines.cancel</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.cancel neste arquivo. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L27"></a>27 | <code>import kotlinx.coroutines.launch</code> | Disponibiliza o símbolo Kotlin/Android kotlinx.coroutines.launch neste arquivo. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L28"></a>28 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L29"></a>29 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L30"></a>30 | <code>// Documentação: Define o tipo VoiceController e reúne o estado/contrato descrito para este</code> | Comentário de manutenção/documentação: Documentação: Define o tipo VoiceController e reúne o estado/contrato descrito para este |
| <a id="L31"></a>31 | <code>// módulo.</code> | Comentário de manutenção/documentação: módulo. |
| <a id="L32"></a>32 | <code>class VoiceController(</code> | Define o tipo VoiceController e reúne o estado/contrato descrito para este módulo. |
| <a id="L33"></a>33 | <code>    private val context: Context,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L34"></a>34 | <code>    private val call: JSONObject,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L35"></a>35 | <code>    private val onFinished: () -&gt; Unit,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L36"></a>36 | <code>) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L37"></a>37 | <code>    private val handler = Handler(Looper.getMainLooper())</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L38"></a>38 | <code>    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L39"></a>39 | <code>    private val audio = context.getSystemService(AudioManager::class.java)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L40"></a>40 | <code>    private var recognizer: SpeechRecognizer? = null</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L41"></a>41 | <code>    private var tts: TextToSpeech? = null</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L42"></a>42 | <code>    private var ttsReady = false</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L43"></a>43 | <code>    private var listening = false</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L44"></a>44 | <code>    private var speaking = false</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L45"></a>45 | <code>    private var finished = false</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L46"></a>46 | <code>    private var awaiting: String? =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L47"></a>47 | <code>        AgentRuntime.events</code> | Fornece a expressão AgentRuntime.events ao bloco/chamada em construção. |
| <a id="L48"></a>48 | <code>            .pending()</code> | Invoca/continua pending com os argumentos declarados. |
| <a id="L49"></a>49 | <code>            .firstOrNull {</code> | Fornece a expressão .firstOrNull { ao bloco/chamada em construção. |
| <a id="L50"></a>50 | <code>                it.callId == call.getString(&quot;id&quot;) &amp;&amp; it.status in setOf(&quot;QUEUED&quot;, &quot;SENDING&quot;)</code> | Invoca/continua call.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L51"></a>51 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L52"></a>52 | <code>            ?.id</code> | Fornece a expressão ?.id ao bloco/chamada em construção. |
| <a id="L53"></a>53 | <code>    private var lastUtterance = &quot;&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L54"></a>54 | <code>    private val attributes =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L55"></a>55 | <code>        AudioAttributes.Builder()</code> | Invoca/continua AudioAttributes.Builder com os argumentos declarados. |
| <a id="L56"></a>56 | <code>            .setUsage(AudioAttributes.USAGE_VOICE_COMMUNICATION)</code> | Invoca/continua setUsage com os argumentos declarados. |
| <a id="L57"></a>57 | <code>            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)</code> | Invoca/continua setContentType com os argumentos declarados. |
| <a id="L58"></a>58 | <code>            .build()</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L59"></a>59 | <code>    private val focus =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L60"></a>60 | <code>        AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT)</code> | Invoca/continua AudioFocusRequest.Builder com os argumentos declarados. |
| <a id="L61"></a>61 | <code>            .setAudioAttributes(attributes)</code> | Invoca/continua setAudioAttributes com os argumentos declarados. |
| <a id="L62"></a>62 | <code>            .setOnAudioFocusChangeListener { value -&gt;</code> | Fornece a expressão .setOnAudioFocusChangeListener { value -&gt; ao bloco/chamada em construção. |
| <a id="L63"></a>63 | <code>                if (value &lt; 0 &amp;&amp; speaking) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L64"></a>64 | <code>                    pause()</code> | Invoca/continua pause com os argumentos declarados. |
| <a id="L65"></a>65 | <code>                    AgentRuntime.voiceStatus.value =</code> | Fornece a expressão AgentRuntime.voiceStatus.value = ao bloco/chamada em construção. |
| <a id="L66"></a>66 | <code>                        &quot;Áudio interrompido. Toque em Falar para continuar.&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L67"></a>67 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L68"></a>68 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L69"></a>69 | <code>            .build()</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L70"></a>70 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L71"></a>71 | <code>    init {</code> | Fornece a expressão init { ao bloco/chamada em construção. |
| <a id="L72"></a>72 | <code>        AgentRuntime.mute.value = false</code> | Fornece a expressão AgentRuntime.mute.value = false ao bloco/chamada em construção. |
| <a id="L73"></a>73 | <code>        audio.mode = AudioManager.MODE_IN_COMMUNICATION</code> | Fornece a expressão audio.mode = AudioManager.MODE_IN_COMMUNICATION ao bloco/chamada em construção. |
| <a id="L74"></a>74 | <code>        route(AgentRuntime.speaker.value)</code> | Invoca/continua route com os argumentos declarados. |
| <a id="L75"></a>75 | <code>        tts =</code> | Fornece o valor de tts no contexto desta expressão. |
| <a id="L76"></a>76 | <code>            TextToSpeech(context) { result -&gt;</code> | Invoca/continua TextToSpeech com os argumentos declarados. |
| <a id="L77"></a>77 | <code>                handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L78"></a>78 | <code>                    if (finished) return@post</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L79"></a>79 | <code>                    ttsReady =</code> | Fornece o valor de ttsReady no contexto desta expressão. |
| <a id="L80"></a>80 | <code>                        result == TextToSpeech.SUCCESS &amp;&amp;</code> | Fornece o valor de result no contexto desta expressão. |
| <a id="L81"></a>81 | <code>                            (tts?.setLanguage(Locale.forLanguageTag(&quot;pt-BR&quot;)) ?: -1) &gt;= 0</code> | Invoca/continua setLanguage com os argumentos declarados. |
| <a id="L82"></a>82 | <code>                    tts?.setAudioAttributes(attributes)</code> | Invoca/continua setAudioAttributes com os argumentos declarados. |
| <a id="L83"></a>83 | <code>                    AgentRuntime.voiceStatus.value =</code> | Fornece a expressão AgentRuntime.voiceStatus.value = ao bloco/chamada em construção. |
| <a id="L84"></a>84 | <code>                        if (ttsReady) &quot;Pronto. Toque em Falar.&quot;</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L85"></a>85 | <code>                        else &quot;Voz de saída indisponível. Respostas aparecem no chat.&quot;</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L86"></a>86 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L87"></a>87 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L88"></a>88 | <code>        tts?.setOnUtteranceProgressListener(</code> | Invoca/continua setOnUtteranceProgressListener com os argumentos declarados. |
| <a id="L89"></a>89 | <code>            object : UtteranceProgressListener() {</code> | Invoca/continua UtteranceProgressListener com os argumentos declarados. |
| <a id="L90"></a>90 | <code>                // Documentação: Trata o callback de VoiceController.onStart, segundo o contrato e</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onStart, segundo o contrato e |
| <a id="L91"></a>91 | <code>                // as verificações deste módulo.</code> | Comentário de manutenção/documentação: as verificações deste módulo. |
| <a id="L92"></a>92 | <code>                override fun onStart(id: String?) {}</code> | Trata o callback de VoiceController.onStart, segundo o contrato e as verificações deste módulo. |
| <a id="L93"></a>93 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L94"></a>94 | <code>                // Documentação: Trata o callback de VoiceController.onDone, segundo o contrato e</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onDone, segundo o contrato e |
| <a id="L95"></a>95 | <code>                // as verificações deste módulo.</code> | Comentário de manutenção/documentação: as verificações deste módulo. |
| <a id="L96"></a>96 | <code>                override fun onDone(id: String?) {</code> | Trata o callback de VoiceController.onDone, segundo o contrato e as verificações deste módulo. |
| <a id="L97"></a>97 | <code>                    handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L98"></a>98 | <code>                        if (id == lastUtterance) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L99"></a>99 | <code>                            speaking = false</code> | Fornece o valor de speaking no contexto desta expressão. |
| <a id="L100"></a>100 | <code>                            if (!finished &amp;&amp; !AgentRuntime.mute.value) listen()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L101"></a>101 | <code>                        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L102"></a>102 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L103"></a>103 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L104"></a>104 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L105"></a>105 | <code>                // Documentação: Trata o callback de VoiceController.onError, segundo o contrato e</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onError, segundo o contrato e |
| <a id="L106"></a>106 | <code>                // as verificações deste módulo.</code> | Comentário de manutenção/documentação: as verificações deste módulo. |
| <a id="L107"></a>107 | <code>                override fun onError(id: String?) {</code> | Trata o callback de VoiceController.onError, segundo o contrato e as verificações deste módulo. |
| <a id="L108"></a>108 | <code>                    handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L109"></a>109 | <code>                        speaking = false</code> | Fornece o valor de speaking no contexto desta expressão. |
| <a id="L110"></a>110 | <code>                        AgentRuntime.voiceStatus.value =</code> | Fornece a expressão AgentRuntime.voiceStatus.value = ao bloco/chamada em construção. |
| <a id="L111"></a>111 | <code>                            &quot;Não foi possível reproduzir. Confira o chat.&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L112"></a>112 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L113"></a>113 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L114"></a>114 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L115"></a>115 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L116"></a>116 | <code>        if (SpeechRecognizer.isRecognitionAvailable(context)) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L117"></a>117 | <code>            recognizer = SpeechRecognizer.createSpeechRecognizer(context)</code> | Invoca/continua SpeechRecognizer.createSpeechRecognizer com os argumentos declarados. |
| <a id="L118"></a>118 | <code>            recognizer?.setRecognitionListener(</code> | Invoca/continua setRecognitionListener com os argumentos declarados. |
| <a id="L119"></a>119 | <code>                object : RecognitionListener {</code> | Fornece a expressão object : RecognitionListener { ao bloco/chamada em construção. |
| <a id="L120"></a>120 | <code>                    // Documentação: Trata o callback de VoiceController.onReadyForSpeech, segundo</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onReadyForSpeech, segundo |
| <a id="L121"></a>121 | <code>                    // o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: o contrato e as verificações deste módulo. |
| <a id="L122"></a>122 | <code>                    override fun onReadyForSpeech(params: Bundle?) {</code> | Trata o callback de VoiceController.onReadyForSpeech, segundo o contrato e as verificações deste módulo. |
| <a id="L123"></a>123 | <code>                        AgentRuntime.voiceStatus.value = &quot;Ouvindo…&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Ouvindo…&quot; ao bloco/chamada em construção. |
| <a id="L124"></a>124 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L125"></a>125 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L126"></a>126 | <code>                    // Documentação: Trata o callback de VoiceController.onBeginningOfSpeech,</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onBeginningOfSpeech, |
| <a id="L127"></a>127 | <code>                    // segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: segundo o contrato e as verificações deste módulo. |
| <a id="L128"></a>128 | <code>                    override fun onBeginningOfSpeech() {}</code> | Trata o callback de VoiceController.onBeginningOfSpeech, segundo o contrato e as verificações deste módulo. |
| <a id="L129"></a>129 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L130"></a>130 | <code>                    // Documentação: Trata o callback de VoiceController.onRmsChanged, segundo o</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onRmsChanged, segundo o |
| <a id="L131"></a>131 | <code>                    // contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: contrato e as verificações deste módulo. |
| <a id="L132"></a>132 | <code>                    override fun onRmsChanged(value: Float) {}</code> | Trata o callback de VoiceController.onRmsChanged, segundo o contrato e as verificações deste módulo. |
| <a id="L133"></a>133 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L134"></a>134 | <code>                    // Documentação: Trata o callback de VoiceController.onBufferReceived, segundo</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onBufferReceived, segundo |
| <a id="L135"></a>135 | <code>                    // o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: o contrato e as verificações deste módulo. |
| <a id="L136"></a>136 | <code>                    override fun onBufferReceived(buffer: ByteArray?) {}</code> | Trata o callback de VoiceController.onBufferReceived, segundo o contrato e as verificações deste módulo. |
| <a id="L137"></a>137 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L138"></a>138 | <code>                    // Documentação: Trata o callback de VoiceController.onEndOfSpeech, segundo o</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onEndOfSpeech, segundo o |
| <a id="L139"></a>139 | <code>                    // contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: contrato e as verificações deste módulo. |
| <a id="L140"></a>140 | <code>                    override fun onEndOfSpeech() {</code> | Trata o callback de VoiceController.onEndOfSpeech, segundo o contrato e as verificações deste módulo. |
| <a id="L141"></a>141 | <code>                        AgentRuntime.voiceStatus.value = &quot;Reconhecendo…&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Reconhecendo…&quot; ao bloco/chamada em construção. |
| <a id="L142"></a>142 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L143"></a>143 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L144"></a>144 | <code>                    // Documentação: Trata o callback de VoiceController.onError, segundo o</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onError, segundo o |
| <a id="L145"></a>145 | <code>                    // contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: contrato e as verificações deste módulo. |
| <a id="L146"></a>146 | <code>                    override fun onError(error: Int) {</code> | Trata o callback de VoiceController.onError, segundo o contrato e as verificações deste módulo. |
| <a id="L147"></a>147 | <code>                        Log.w(&quot;DevLimaVoice&quot;, &quot;speech_recognition_error=$error&quot;)</code> | Invoca/continua Log.w com os argumentos declarados. |
| <a id="L148"></a>148 | <code>                        listening = false</code> | Fornece o valor de listening no contexto desta expressão. |
| <a id="L149"></a>149 | <code>                        if (!finished &amp;&amp; awaiting == null &amp;&amp; !speaking &amp;&amp; !AgentRuntime.mute.value)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L150"></a>150 | <code>                            AgentRuntime.voiceStatus.value =</code> | Fornece a expressão AgentRuntime.voiceStatus.value = ao bloco/chamada em construção. |
| <a id="L151"></a>151 | <code>                                when (error) {</code> | Despacha o valor/condição para os ramos declarados abaixo. |
| <a id="L152"></a>152 | <code>                                    SpeechRecognizer.ERROR_NO_MATCH,</code> | Fornece a expressão SpeechRecognizer.ERROR_NO_MATCH, ao bloco/chamada em construção. |
| <a id="L153"></a>153 | <code>                                    SpeechRecognizer.ERROR_SPEECH_TIMEOUT -&gt; &quot;Não ouvi uma frase. Toque em Falar.&quot;</code> | Fornece a expressão SpeechRecognizer.ERROR_SPEECH_TIMEOUT -&gt; &quot;Não ouvi uma frase. Toque em Falar.&quot; ao bloco/chamada em construção. |
| <a id="L154"></a>154 | <code>                                    SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -&gt; &quot;Permita o microfone nas configurações do aplicativo.&quot;</code> | Fornece a expressão SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -&gt; &quot;Permita o microfone nas configurações do aplicativo.&quot; ao bloco/chamada em construção. |
| <a id="L155"></a>155 | <code>                                    SpeechRecognizer.ERROR_NETWORK,</code> | Fornece a expressão SpeechRecognizer.ERROR_NETWORK, ao bloco/chamada em construção. |
| <a id="L156"></a>156 | <code>                                    SpeechRecognizer.ERROR_NETWORK_TIMEOUT -&gt; &quot;O serviço de voz não conseguiu conectar. Confira sua internet e tente novamente.&quot;</code> | Fornece a expressão SpeechRecognizer.ERROR_NETWORK_TIMEOUT -&gt; &quot;O serviço de voz não conseguiu conectar. Confira sua internet e tente novamente.&quot; ao bloco/chamada em construção. |
| <a id="L157"></a>157 | <code>                                    SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED -&gt; &quot;O serviço de voz escolhido não reconhece português. Confira os idiomas nas configurações de voz do Android.&quot;</code> | Fornece a expressão SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED -&gt; &quot;O serviço de voz escolhido não reconhece português. Confira os idiomas nas configurações de voz do Android.&quot; ao bloco/chamada em construção. |
| <a id="L158"></a>158 | <code>                                    SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE -&gt; &quot;Baixe português nas configurações de reconhecimento de voz do Android e tente novamente.&quot;</code> | Fornece a expressão SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE -&gt; &quot;Baixe português nas configurações de reconhecimento de voz do Android e tente novamente.&quot; ao bloco/chamada em construção. |
| <a id="L159"></a>159 | <code>                                    SpeechRecognizer.ERROR_RECOGNIZER_BUSY -&gt; &quot;O serviço de voz está ocupado. Aguarde e toque em Falar.&quot;</code> | Fornece a expressão SpeechRecognizer.ERROR_RECOGNIZER_BUSY -&gt; &quot;O serviço de voz está ocupado. Aguarde e toque em Falar.&quot; ao bloco/chamada em construção. |
| <a id="L160"></a>160 | <code>                                    else -&gt; &quot;Reconhecimento indisponível. Use texto ou tente novamente.&quot;</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L161"></a>161 | <code>                                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L162"></a>162 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L163"></a>163 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L164"></a>164 | <code>                    // Documentação: Trata o callback de VoiceController.onResults, segundo o</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onResults, segundo o |
| <a id="L165"></a>165 | <code>                    // contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: contrato e as verificações deste módulo. |
| <a id="L166"></a>166 | <code>                    override fun onResults(results: Bundle?) {</code> | Trata o callback de VoiceController.onResults, segundo o contrato e as verificações deste módulo. |
| <a id="L167"></a>167 | <code>                        listening = false</code> | Fornece o valor de listening no contexto desta expressão. |
| <a id="L168"></a>168 | <code>                        val text =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L169"></a>169 | <code>                            results</code> | Fornece a expressão results ao bloco/chamada em construção. |
| <a id="L170"></a>170 | <code>                                ?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)</code> | Invoca/continua getStringArrayList com os argumentos declarados. |
| <a id="L171"></a>171 | <code>                                ?.firstOrNull()</code> | Invoca/continua firstOrNull com os argumentos declarados. |
| <a id="L172"></a>172 | <code>                        if (!text.isNullOrBlank() &amp;&amp; !finished &amp;&amp; !AgentRuntime.mute.value)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L173"></a>173 | <code>                            sendText(text)</code> | Invoca/continua sendText com os argumentos declarados. Encaminha texto pela fila/contrato da chamada ativa. |
| <a id="L174"></a>174 | <code>                        else AgentRuntime.voiceStatus.value = &quot;Toque em Falar para continuar.&quot;</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L175"></a>175 | <code>                    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L176"></a>176 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L177"></a>177 | <code>                    // Documentação: Trata o callback de VoiceController.onPartialResults, segundo</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onPartialResults, segundo |
| <a id="L178"></a>178 | <code>                    // o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: o contrato e as verificações deste módulo. |
| <a id="L179"></a>179 | <code>                    override fun onPartialResults(results: Bundle?) {}</code> | Trata o callback de VoiceController.onPartialResults, segundo o contrato e as verificações deste módulo. |
| <a id="L180"></a>180 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L181"></a>181 | <code>                    // Documentação: Trata o callback de VoiceController.onEvent, segundo o</code> | Comentário de manutenção/documentação: Documentação: Trata o callback de VoiceController.onEvent, segundo o |
| <a id="L182"></a>182 | <code>                    // contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: contrato e as verificações deste módulo. |
| <a id="L183"></a>183 | <code>                    override fun onEvent(type: Int, params: Bundle?) {}</code> | Trata o callback de VoiceController.onEvent, segundo o contrato e as verificações deste módulo. |
| <a id="L184"></a>184 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L185"></a>185 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L186"></a>186 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L187"></a>187 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L188"></a>188 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L189"></a>189 | <code>    // Documentação: Inicia reconhecimento respeitando estado da chamada/mute e libera foco antes</code> | Comentário de manutenção/documentação: Documentação: Inicia reconhecimento respeitando estado da chamada/mute e libera foco antes |
| <a id="L190"></a>190 | <code>    // da captura.</code> | Comentário de manutenção/documentação: da captura. |
| <a id="L191"></a>191 | <code>    fun listen() {</code> | Inicia reconhecimento respeitando estado da chamada/mute e libera foco antes da captura. |
| <a id="L192"></a>192 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L193"></a>193 | <code>            if (finished &#124;&#124; listening &#124;&#124; speaking &#124;&#124; awaiting != null &#124;&#124; AgentRuntime.mute.value)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L194"></a>194 | <code>                return@post</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L195"></a>195 | <code>            if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L196"></a>196 | <code>                ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) !=</code> | Invoca/continua ContextCompat.checkSelfPermission com os argumentos declarados. Confere autorização; declaração no manifesto não basta. |
| <a id="L197"></a>197 | <code>                    PackageManager.PERMISSION_GRANTED &#124;&#124; recognizer == null</code> | Fornece a expressão PackageManager.PERMISSION_GRANTED &#124;&#124; recognizer == null ao bloco/chamada em construção. |
| <a id="L198"></a>198 | <code>            ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L199"></a>199 | <code>                AgentRuntime.voiceStatus.value = &quot;Microfone/reconhecimento indisponível. Use texto.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Microfone/reconhecimento indisponível. Use texto.&quot; ao bloco/chamada em construção. |
| <a id="L200"></a>200 | <code>                return@post</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L201"></a>201 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L202"></a>202 | <code>            // The recognition service manages its own focus. Keeping ours here makes its</code> | Comentário de manutenção/documentação: The recognition service manages its own focus. Keeping ours here makes its |
| <a id="L203"></a>203 | <code>            // focus request look like an interruption and cancels the microphone session.</code> | Comentário de manutenção/documentação: focus request look like an interruption and cancels the microphone session. |
| <a id="L204"></a>204 | <code>            audio.abandonAudioFocusRequest(focus)</code> | Invoca/continua audio.abandonAudioFocusRequest com os argumentos declarados. Libera foco de áudio do app para não disputar a captura com o reconhecedor. |
| <a id="L205"></a>205 | <code>            listening = true</code> | Fornece o valor de listening no contexto desta expressão. |
| <a id="L206"></a>206 | <code>            try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L207"></a>207 | <code>                recognizer?.startListening(</code> | Invoca/continua startListening com os argumentos declarados. Solicita captura ao serviço SpeechRecognizer; depende de permissão/estado do sistema. |
| <a id="L208"></a>208 | <code>                    Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)</code> | Invoca/continua Intent com os argumentos declarados. |
| <a id="L209"></a>209 | <code>                        .putExtra(</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. |
| <a id="L210"></a>210 | <code>                            RecognizerIntent.EXTRA_LANGUAGE_MODEL,</code> | Fornece a expressão RecognizerIntent.EXTRA_LANGUAGE_MODEL, ao bloco/chamada em construção. |
| <a id="L211"></a>211 | <code>                            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM,</code> | Fornece a expressão RecognizerIntent.LANGUAGE_MODEL_FREE_FORM, ao bloco/chamada em construção. |
| <a id="L212"></a>212 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L213"></a>213 | <code>                        .putExtra(RecognizerIntent.EXTRA_LANGUAGE, &quot;pt-BR&quot;)</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. |
| <a id="L214"></a>214 | <code>                        .putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. |
| <a id="L215"></a>215 | <code>                        .putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)</code> | Invoca/continua putExtra com os argumentos declarados. Acrescenta argumento ao Intent, validado pelo componente destino. |
| <a id="L216"></a>216 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L217"></a>217 | <code>            } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L218"></a>218 | <code>                listening = false</code> | Fornece o valor de listening no contexto desta expressão. |
| <a id="L219"></a>219 | <code>                AgentRuntime.voiceStatus.value = &quot;Não foi possível abrir o microfone.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Não foi possível abrir o microfone.&quot; ao bloco/chamada em construção. |
| <a id="L220"></a>220 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L221"></a>221 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L222"></a>222 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L223"></a>223 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L224"></a>224 | <code>    // Documentação: Implementa VoiceController.sendText como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa VoiceController.sendText como parte do fluxo descrito para este |
| <a id="L225"></a>225 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L226"></a>226 | <code>    fun sendText(text: String) {</code> | Implementa VoiceController.sendText como parte do fluxo descrito para este arquivo. Encaminha texto pela fila/contrato da chamada ativa. |
| <a id="L227"></a>227 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L228"></a>228 | <code>            if (finished &#124;&#124; awaiting != null &#124;&#124; text.isBlank()) return@post</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L229"></a>229 | <code>            pause()</code> | Invoca/continua pause com os argumentos declarados. |
| <a id="L230"></a>230 | <code>            awaiting = AgentRuntime.events.enqueueVoice(call, text.take(4000))</code> | Invoca/continua AgentRuntime.events.enqueueVoice com os argumentos declarados. Grava transcrição na fila durável vinculada à chamada. |
| <a id="L231"></a>231 | <code>            AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L232"></a>232 | <code>            AgentRuntime.voiceStatus.value = &quot;Aguardando agente…&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Aguardando agente…&quot; ao bloco/chamada em construção. |
| <a id="L233"></a>233 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L234"></a>234 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L235"></a>235 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L236"></a>236 | <code>    // Documentação: Encaminha resposta da chamada correspondente ao TTS sem misturar outra</code> | Comentário de manutenção/documentação: Documentação: Encaminha resposta da chamada correspondente ao TTS sem misturar outra |
| <a id="L237"></a>237 | <code>    // conversa.</code> | Comentário de manutenção/documentação: conversa. |
| <a id="L238"></a>238 | <code>    fun reply(payload: JSONObject) {</code> | Encaminha resposta da chamada correspondente ao TTS sem misturar outra conversa. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L239"></a>239 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L240"></a>240 | <code>            if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L241"></a>241 | <code>                finished &#124;&#124;</code> | Fornece a expressão finished &#124;&#124; ao bloco/chamada em construção. |
| <a id="L242"></a>242 | <code>                    payload.optString(&quot;client_message_id&quot;) != awaiting &#124;&#124;</code> | Invoca/continua payload.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L243"></a>243 | <code>                    payload.optString(&quot;conversation_id&quot;) != call.getString(&quot;conversation_id&quot;)</code> | Invoca/continua payload.optString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L244"></a>244 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L245"></a>245 | <code>                return@post</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L246"></a>246 | <code>            awaiting = null</code> | Fornece o valor de awaiting no contexto desta expressão. |
| <a id="L247"></a>247 | <code>            val text = payload.getString(&quot;reply&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L248"></a>248 | <code>            if (!ttsReady &#124;&#124; AgentRuntime.mute.value) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L249"></a>249 | <code>                AgentRuntime.voiceStatus.value = &quot;Resposta disponível no chat.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Resposta disponível no chat.&quot; ao bloco/chamada em construção. |
| <a id="L250"></a>250 | <code>                return@post</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L251"></a>251 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L252"></a>252 | <code>            if (audio.requestAudioFocus(focus) != AudioManager.AUDIOFOCUS_REQUEST_GRANTED) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L253"></a>253 | <code>                AgentRuntime.voiceStatus.value = &quot;Resposta disponível no chat; áudio ocupado.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Resposta disponível no chat; áudio ocupado.&quot; ao bloco/chamada em construção. |
| <a id="L254"></a>254 | <code>                return@post</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L255"></a>255 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L256"></a>256 | <code>            speaking = true</code> | Fornece o valor de speaking no contexto desta expressão. |
| <a id="L257"></a>257 | <code>            AgentRuntime.voiceStatus.value = &quot;Agente falando…&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Agente falando…&quot; ao bloco/chamada em construção. |
| <a id="L258"></a>258 | <code>            val chunks = text.chunked(TextToSpeech.getMaxSpeechInputLength() - 1)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L259"></a>259 | <code>            for ((index, chunk) in chunks.withIndex()) {</code> | Percorre elementos ou repete o bloco enquanto a condição declarada permitir. |
| <a id="L260"></a>260 | <code>                val id = &quot;${payload.optString(&quot;assistant_message_id&quot;)}:$index&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L261"></a>261 | <code>                if (index == chunks.lastIndex) lastUtterance = id</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L262"></a>262 | <code>                val result =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L263"></a>263 | <code>                    tts?.speak(</code> | Invoca/continua speak com os argumentos declarados. |
| <a id="L264"></a>264 | <code>                        chunk,</code> | Fornece a expressão chunk, ao bloco/chamada em construção. |
| <a id="L265"></a>265 | <code>                        if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD,</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L266"></a>266 | <code>                        null,</code> | Fornece a expressão null, ao bloco/chamada em construção. |
| <a id="L267"></a>267 | <code>                        id,</code> | Fornece a expressão id, ao bloco/chamada em construção. |
| <a id="L268"></a>268 | <code>                    )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L269"></a>269 | <code>                if (result == TextToSpeech.ERROR) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L270"></a>270 | <code>                    speaking = false</code> | Fornece o valor de speaking no contexto desta expressão. |
| <a id="L271"></a>271 | <code>                    AgentRuntime.voiceStatus.value = &quot;Resposta disponível no chat.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Resposta disponível no chat.&quot; ao bloco/chamada em construção. |
| <a id="L272"></a>272 | <code>                    break</code> | Fornece a expressão break ao bloco/chamada em construção. |
| <a id="L273"></a>273 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L274"></a>274 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L275"></a>275 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L276"></a>276 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L277"></a>277 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L278"></a>278 | <code>    // Documentação: Implementa VoiceController.response como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa VoiceController.response como parte do fluxo descrito para este |
| <a id="L279"></a>279 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L280"></a>280 | <code>    fun response(event: JSONObject) {</code> | Implementa VoiceController.response como parte do fluxo descrito para este arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L281"></a>281 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L282"></a>282 | <code>            val body = event.getJSONObject(&quot;payload&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L283"></a>283 | <code>            if (</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L284"></a>284 | <code>                event.optString(&quot;type&quot;) == &quot;error&quot; &amp;&amp;</code> | Invoca/continua event.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L285"></a>285 | <code>                    body.optString(&quot;client_message_id&quot;) == awaiting</code> | Invoca/continua body.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L286"></a>286 | <code>            ) {</code> | Fornece a expressão ) { ao bloco/chamada em construção. |
| <a id="L287"></a>287 | <code>                val row = AgentRuntime.events.pending().firstOrNull { it.id == awaiting }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L288"></a>288 | <code>                if (row?.status == &quot;FAILED&quot;) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L289"></a>289 | <code>                    awaiting = null</code> | Fornece o valor de awaiting no contexto desta expressão. |
| <a id="L290"></a>290 | <code>                    AgentRuntime.voiceStatus.value = &quot;Falha no turno. Reenvie pelo chat.&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Falha no turno. Reenvie pelo chat.&quot; ao bloco/chamada em construção. |
| <a id="L291"></a>291 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L292"></a>292 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L293"></a>293 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L294"></a>294 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L295"></a>295 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L296"></a>296 | <code>    // Documentação: Interrompe TTS/escuta ativos e libera recursos/foco conforme o estado.</code> | Comentário de manutenção/documentação: Documentação: Interrompe TTS/escuta ativos e libera recursos/foco conforme o estado. |
| <a id="L297"></a>297 | <code>    private fun pause() {</code> | Interrompe TTS/escuta ativos e libera recursos/foco conforme o estado. |
| <a id="L298"></a>298 | <code>        if (listening) recognizer?.cancel()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L299"></a>299 | <code>        tts?.stop()</code> | Invoca/continua stop com os argumentos declarados. |
| <a id="L300"></a>300 | <code>        listening = false</code> | Fornece o valor de listening no contexto desta expressão. |
| <a id="L301"></a>301 | <code>        speaking = false</code> | Fornece o valor de speaking no contexto desta expressão. |
| <a id="L302"></a>302 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L303"></a>303 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L304"></a>304 | <code>    // Documentação: Alterna VoiceController.toggleMute, segundo o contrato e as verificações</code> | Comentário de manutenção/documentação: Documentação: Alterna VoiceController.toggleMute, segundo o contrato e as verificações |
| <a id="L305"></a>305 | <code>    // deste módulo.</code> | Comentário de manutenção/documentação: deste módulo. |
| <a id="L306"></a>306 | <code>    fun toggleMute() {</code> | Alterna VoiceController.toggleMute, segundo o contrato e as verificações deste módulo. Alterna silêncio e interrupção da voz conforme o controlador. |
| <a id="L307"></a>307 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L308"></a>308 | <code>            AgentRuntime.mute.value = !AgentRuntime.mute.value</code> | Fornece a expressão AgentRuntime.mute.value = !AgentRuntime.mute.value ao bloco/chamada em construção. |
| <a id="L309"></a>309 | <code>            if (AgentRuntime.mute.value) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L310"></a>310 | <code>                pause()</code> | Invoca/continua pause com os argumentos declarados. |
| <a id="L311"></a>311 | <code>                AgentRuntime.voiceStatus.value = &quot;Microfone silenciado&quot;</code> | Fornece a expressão AgentRuntime.voiceStatus.value = &quot;Microfone silenciado&quot; ao bloco/chamada em construção. |
| <a id="L312"></a>312 | <code>            } else AgentRuntime.voiceStatus.value = &quot;Toque em Falar para continuar.&quot;</code> | Fornece a expressão } else AgentRuntime.voiceStatus.value = &quot;Toque em Falar para continuar.&quot; ao bloco/chamada em construção. |
| <a id="L313"></a>313 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L314"></a>314 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L315"></a>315 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L316"></a>316 | <code>    // Documentação: Alterna VoiceController.toggleSpeaker, segundo o contrato e as verificações</code> | Comentário de manutenção/documentação: Documentação: Alterna VoiceController.toggleSpeaker, segundo o contrato e as verificações |
| <a id="L317"></a>317 | <code>    // deste módulo.</code> | Comentário de manutenção/documentação: deste módulo. |
| <a id="L318"></a>318 | <code>    fun toggleSpeaker() {</code> | Alterna VoiceController.toggleSpeaker, segundo o contrato e as verificações deste módulo. Alterna saída solicitada entre alto-falante e auricular. |
| <a id="L319"></a>319 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L320"></a>320 | <code>            AgentRuntime.speaker.value = !AgentRuntime.speaker.value</code> | Fornece a expressão AgentRuntime.speaker.value = !AgentRuntime.speaker.value ao bloco/chamada em construção. |
| <a id="L321"></a>321 | <code>            route(AgentRuntime.speaker.value)</code> | Invoca/continua route com os argumentos declarados. |
| <a id="L322"></a>322 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L323"></a>323 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L324"></a>324 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L325"></a>325 | <code>    // Documentação: Implementa VoiceController.route como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa VoiceController.route como parte do fluxo descrito para este |
| <a id="L326"></a>326 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L327"></a>327 | <code>    private fun route(speaker: Boolean) {</code> | Implementa VoiceController.route como parte do fluxo descrito para este arquivo. |
| <a id="L328"></a>328 | <code>        if (Build.VERSION.SDK_INT &gt;= 31) {</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L329"></a>329 | <code>            val type =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L330"></a>330 | <code>                if (speaker) AudioDeviceInfo.TYPE_BUILTIN_SPEAKER</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L331"></a>331 | <code>                else AudioDeviceInfo.TYPE_BUILTIN_EARPIECE</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L332"></a>332 | <code>            val device = audio.availableCommunicationDevices.firstOrNull { it.type == type }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L333"></a>333 | <code>            if (device != null) audio.setCommunicationDevice(device)</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L334"></a>334 | <code>            else AgentRuntime.voiceStatus.value = &quot;Saída escolhida indisponível neste aparelho.&quot;</code> | Define caminho alternativo, tratamento de erro ou liberação de recursos do bloco anterior. |
| <a id="L335"></a>335 | <code>        } else {</code> | Fornece a expressão } else { ao bloco/chamada em construção. |
| <a id="L336"></a>336 | <code>            audio.isSpeakerphoneOn = speaker</code> | Fornece a expressão audio.isSpeakerphoneOn = speaker ao bloco/chamada em construção. |
| <a id="L337"></a>337 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L338"></a>338 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L339"></a>339 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L340"></a>340 | <code>    // Documentação: Implementa VoiceController.end como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa VoiceController.end como parte do fluxo descrito para este |
| <a id="L341"></a>341 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L342"></a>342 | <code>    fun end() {</code> | Implementa VoiceController.end como parte do fluxo descrito para este arquivo. |
| <a id="L343"></a>343 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L344"></a>344 | <code>            if (finished) return@post</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L345"></a>345 | <code>            scope.launch {</code> | Fornece a expressão scope.launch { ao bloco/chamada em construção. Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo. |
| <a id="L346"></a>346 | <code>                try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L347"></a>347 | <code>                    val result =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L348"></a>348 | <code>                        JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L349"></a>349 | <code>                            AgentRuntime.auth.api(</code> | Invoca/continua AgentRuntime.auth.api com os argumentos declarados. |
| <a id="L350"></a>350 | <code>                                &quot;/calls/${call.getString(&quot;id&quot;)}/end&quot;,</code> | Fornece a expressão &quot;/calls/${call.getString(&quot;id&quot;)}/end&quot;, ao bloco/chamada em construção. |
| <a id="L351"></a>351 | <code>                                &quot;POST&quot;,</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L352"></a>352 | <code>                                JSONObject().put(&quot;device_id&quot;, call.getString(&quot;device_id&quot;)),</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. Identifica o dispositivo autenticado e vincula atendimento ou sessão de refresh. |
| <a id="L353"></a>353 | <code>                            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L354"></a>354 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L355"></a>355 | <code>                    AgentRuntime.call.value = result</code> | Fornece a expressão AgentRuntime.call.value = result ao bloco/chamada em construção. |
| <a id="L356"></a>356 | <code>                    finishLocal()</code> | Invoca/continua finishLocal com os argumentos declarados. |
| <a id="L357"></a>357 | <code>                } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L358"></a>358 | <code>                    AgentRuntime.voiceStatus.value =</code> | Fornece a expressão AgentRuntime.voiceStatus.value = ao bloco/chamada em construção. |
| <a id="L359"></a>359 | <code>                        &quot;Não foi possível encerrar no servidor. Tente novamente.&quot;</code> | Conteúdo literal usado como texto/SQL/argumento; não é uma instrução Kotlin independente. |
| <a id="L360"></a>360 | <code>                }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L361"></a>361 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L362"></a>362 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L363"></a>363 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L364"></a>364 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L365"></a>365 | <code>    // Documentação: Implementa VoiceController.finishLocal como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa VoiceController.finishLocal como parte do fluxo descrito para este |
| <a id="L366"></a>366 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L367"></a>367 | <code>    fun finishLocal() {</code> | Implementa VoiceController.finishLocal como parte do fluxo descrito para este arquivo. |
| <a id="L368"></a>368 | <code>        handler.post {</code> | Fornece a expressão handler.post { ao bloco/chamada em construção. |
| <a id="L369"></a>369 | <code>            if (finished) return@post</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L370"></a>370 | <code>            finished = true</code> | Fornece o valor de finished no contexto desta expressão. |
| <a id="L371"></a>371 | <code>            pause()</code> | Invoca/continua pause com os argumentos declarados. |
| <a id="L372"></a>372 | <code>            AgentRuntime.events.cancelVoice(call.getString(&quot;id&quot;))</code> | Invoca/continua AgentRuntime.events.cancelVoice com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L373"></a>373 | <code>            AgentRuntime.refreshEvents()</code> | Invoca/continua AgentRuntime.refreshEvents com os argumentos declarados. Publica o estado persistido para os observadores da interface. |
| <a id="L374"></a>374 | <code>            onFinished()</code> | Invoca/continua onFinished com os argumentos declarados. |
| <a id="L375"></a>375 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L376"></a>376 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L377"></a>377 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L378"></a>378 | <code>    // Documentação: Implementa VoiceController.destroy como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa VoiceController.destroy como parte do fluxo descrito para este |
| <a id="L379"></a>379 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L380"></a>380 | <code>    fun destroy() {</code> | Implementa VoiceController.destroy como parte do fluxo descrito para este arquivo. |
| <a id="L381"></a>381 | <code>        finished = true</code> | Fornece o valor de finished no contexto desta expressão. |
| <a id="L382"></a>382 | <code>        pause()</code> | Invoca/continua pause com os argumentos declarados. |
| <a id="L383"></a>383 | <code>        recognizer?.destroy()</code> | Invoca/continua destroy com os argumentos declarados. |
| <a id="L384"></a>384 | <code>        tts?.shutdown()</code> | Invoca/continua shutdown com os argumentos declarados. |
| <a id="L385"></a>385 | <code>        scope.cancel()</code> | Invoca/continua scope.cancel com os argumentos declarados. Solicita cancelamento do recurso/notificação identificado. |
| <a id="L386"></a>386 | <code>        audio.abandonAudioFocusRequest(focus)</code> | Invoca/continua audio.abandonAudioFocusRequest com os argumentos declarados. Libera foco de áudio do app para não disputar a captura com o reconhecedor. |
| <a id="L387"></a>387 | <code>        if (Build.VERSION.SDK_INT &gt;= 31) audio.clearCommunicationDevice()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L388"></a>388 | <code>        audio.mode = AudioManager.MODE_NORMAL</code> | Fornece a expressão audio.mode = AudioManager.MODE_NORMAL ao bloco/chamada em construção. |
| <a id="L389"></a>389 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L390"></a>390 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
