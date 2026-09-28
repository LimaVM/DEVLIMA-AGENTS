package br.com.vegasolucoes.agent

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioAttributes
import android.media.AudioDeviceInfo
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import androidx.core.content.ContextCompat
import java.util.Locale
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import org.json.JSONObject

// Documentação: Define o tipo VoiceController e reúne o estado/contrato descrito para este
// módulo.
class VoiceController(
    private val context: Context,
    private val call: JSONObject,
    private val onFinished: () -> Unit,
) {
    private val handler = Handler(Looper.getMainLooper())
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    private val audio = context.getSystemService(AudioManager::class.java)
    private var recognizer: SpeechRecognizer? = null
    private var tts: TextToSpeech? = null
    private var ttsReady = false
    private var listening = false
    private var speaking = false
    private var finished = false
    private var awaiting: String? =
        AgentRuntime.events
            .pending()
            .firstOrNull {
                it.callId == call.getString("id") && it.status in setOf("QUEUED", "SENDING")
            }
            ?.id
    private var lastUtterance = ""
    private val attributes =
        AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_VOICE_COMMUNICATION)
            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
            .build()
    private val focus =
        AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT)
            .setAudioAttributes(attributes)
            .setOnAudioFocusChangeListener { value ->
                if (value < 0 && speaking) {
                    pause()
                    AgentRuntime.voiceStatus.value =
                        "Áudio interrompido. Toque em Falar para continuar."
                }
            }
            .build()

    init {
        AgentRuntime.mute.value = false
        audio.mode = AudioManager.MODE_IN_COMMUNICATION
        route(AgentRuntime.speaker.value)
        tts =
            TextToSpeech(context) { result ->
                handler.post {
                    if (finished) return@post
                    ttsReady =
                        result == TextToSpeech.SUCCESS &&
                            (tts?.setLanguage(Locale.forLanguageTag("pt-BR")) ?: -1) >= 0
                    tts?.setAudioAttributes(attributes)
                    AgentRuntime.voiceStatus.value =
                        if (ttsReady) "Pronto. Toque em Falar."
                        else "Voz de saída indisponível. Respostas aparecem no chat."
                }
            }
        tts?.setOnUtteranceProgressListener(
            object : UtteranceProgressListener() {
                // Documentação: Trata o callback de VoiceController.onStart, segundo o contrato e
                // as verificações deste módulo.
                override fun onStart(id: String?) {}

                // Documentação: Trata o callback de VoiceController.onDone, segundo o contrato e
                // as verificações deste módulo.
                override fun onDone(id: String?) {
                    handler.post {
                        if (id == lastUtterance) {
                            speaking = false
                            if (!finished && !AgentRuntime.mute.value) listen()
                        }
                    }
                }

                // Documentação: Trata o callback de VoiceController.onError, segundo o contrato e
                // as verificações deste módulo.
                override fun onError(id: String?) {
                    handler.post {
                        speaking = false
                        AgentRuntime.voiceStatus.value =
                            "Não foi possível reproduzir. Confira o chat."
                    }
                }
            }
        )
        if (SpeechRecognizer.isRecognitionAvailable(context)) {
            recognizer = SpeechRecognizer.createSpeechRecognizer(context)
            recognizer?.setRecognitionListener(
                object : RecognitionListener {
                    // Documentação: Trata o callback de VoiceController.onReadyForSpeech, segundo
                    // o contrato e as verificações deste módulo.
                    override fun onReadyForSpeech(params: Bundle?) {
                        AgentRuntime.voiceStatus.value = "Ouvindo…"
                    }

                    // Documentação: Trata o callback de VoiceController.onBeginningOfSpeech,
                    // segundo o contrato e as verificações deste módulo.
                    override fun onBeginningOfSpeech() {}

                    // Documentação: Trata o callback de VoiceController.onRmsChanged, segundo o
                    // contrato e as verificações deste módulo.
                    override fun onRmsChanged(value: Float) {}

                    // Documentação: Trata o callback de VoiceController.onBufferReceived, segundo
                    // o contrato e as verificações deste módulo.
                    override fun onBufferReceived(buffer: ByteArray?) {}

                    // Documentação: Trata o callback de VoiceController.onEndOfSpeech, segundo o
                    // contrato e as verificações deste módulo.
                    override fun onEndOfSpeech() {
                        AgentRuntime.voiceStatus.value = "Reconhecendo…"
                    }

                    // Documentação: Trata o callback de VoiceController.onError, segundo o
                    // contrato e as verificações deste módulo.
                    override fun onError(error: Int) {
                        Log.w("DevLimaVoice", "speech_recognition_error=$error")
                        listening = false
                        if (!finished && awaiting == null && !speaking && !AgentRuntime.mute.value)
                            AgentRuntime.voiceStatus.value =
                                when (error) {
                                    SpeechRecognizer.ERROR_NO_MATCH,
                                    SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "Não ouvi uma frase. Toque em Falar."
                                    SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Permita o microfone nas configurações do aplicativo."
                                    SpeechRecognizer.ERROR_NETWORK,
                                    SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "O serviço de voz não conseguiu conectar. Confira sua internet e tente novamente."
                                    SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED -> "O serviço de voz escolhido não reconhece português. Confira os idiomas nas configurações de voz do Android."
                                    SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE -> "Baixe português nas configurações de reconhecimento de voz do Android e tente novamente."
                                    SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "O serviço de voz está ocupado. Aguarde e toque em Falar."
                                    else -> "Reconhecimento indisponível. Use texto ou tente novamente."
                                }
                    }

                    // Documentação: Trata o callback de VoiceController.onResults, segundo o
                    // contrato e as verificações deste módulo.
                    override fun onResults(results: Bundle?) {
                        listening = false
                        val text =
                            results
                                ?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                                ?.firstOrNull()
                        if (!text.isNullOrBlank() && !finished && !AgentRuntime.mute.value)
                            sendText(text)
                        else AgentRuntime.voiceStatus.value = "Toque em Falar para continuar."
                    }

                    // Documentação: Trata o callback de VoiceController.onPartialResults, segundo
                    // o contrato e as verificações deste módulo.
                    override fun onPartialResults(results: Bundle?) {}

                    // Documentação: Trata o callback de VoiceController.onEvent, segundo o
                    // contrato e as verificações deste módulo.
                    override fun onEvent(type: Int, params: Bundle?) {}
                }
            )
        }
    }

    // Documentação: Inicia reconhecimento respeitando estado da chamada/mute e libera foco antes
    // da captura.
    fun listen() {
        handler.post {
            if (finished || listening || speaking || awaiting != null || AgentRuntime.mute.value)
                return@post
            if (
                ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) !=
                    PackageManager.PERMISSION_GRANTED || recognizer == null
            ) {
                AgentRuntime.voiceStatus.value = "Microfone/reconhecimento indisponível. Use texto."
                return@post
            }
            // The recognition service manages its own focus. Keeping ours here makes its
            // focus request look like an interruption and cancels the microphone session.
            audio.abandonAudioFocusRequest(focus)
            listening = true
            try {
                recognizer?.startListening(
                    Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                        .putExtra(
                            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM,
                        )
                        .putExtra(RecognizerIntent.EXTRA_LANGUAGE, "pt-BR")
                        .putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
                        .putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
                )
            } catch (_: Exception) {
                listening = false
                AgentRuntime.voiceStatus.value = "Não foi possível abrir o microfone."
            }
        }
    }

    // Documentação: Implementa VoiceController.sendText como parte do fluxo descrito para este
    // arquivo.
    fun sendText(text: String) {
        handler.post {
            if (finished || awaiting != null || text.isBlank()) return@post
            pause()
            awaiting = AgentRuntime.events.enqueueVoice(call, text.take(4000))
            AgentRuntime.refreshEvents()
            AgentRuntime.voiceStatus.value = "Aguardando agente…"
        }
    }

    // Documentação: Encaminha resposta da chamada correspondente ao TTS sem misturar outra
    // conversa.
    fun reply(payload: JSONObject) {
        handler.post {
            if (
                finished ||
                    payload.optString("client_message_id") != awaiting ||
                    payload.optString("conversation_id") != call.getString("conversation_id")
            )
                return@post
            awaiting = null
            val text = payload.getString("reply")
            if (!ttsReady || AgentRuntime.mute.value) {
                AgentRuntime.voiceStatus.value = "Resposta disponível no chat."
                return@post
            }
            if (audio.requestAudioFocus(focus) != AudioManager.AUDIOFOCUS_REQUEST_GRANTED) {
                AgentRuntime.voiceStatus.value = "Resposta disponível no chat; áudio ocupado."
                return@post
            }
            speaking = true
            AgentRuntime.voiceStatus.value = "Agente falando…"
            val chunks = text.chunked(TextToSpeech.getMaxSpeechInputLength() - 1)
            for ((index, chunk) in chunks.withIndex()) {
                val id = "${payload.optString("assistant_message_id")}:$index"
                if (index == chunks.lastIndex) lastUtterance = id
                val result =
                    tts?.speak(
                        chunk,
                        if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD,
                        null,
                        id,
                    )
                if (result == TextToSpeech.ERROR) {
                    speaking = false
                    AgentRuntime.voiceStatus.value = "Resposta disponível no chat."
                    break
                }
            }
        }
    }

    // Documentação: Implementa VoiceController.response como parte do fluxo descrito para este
    // arquivo.
    fun response(event: JSONObject) {
        handler.post {
            val body = event.getJSONObject("payload")
            if (
                event.optString("type") == "error" &&
                    body.optString("client_message_id") == awaiting
            ) {
                val row = AgentRuntime.events.pending().firstOrNull { it.id == awaiting }
                if (row?.status == "FAILED") {
                    awaiting = null
                    AgentRuntime.voiceStatus.value = "Falha no turno. Reenvie pelo chat."
                }
            }
        }
    }

    // Documentação: Interrompe TTS/escuta ativos e libera recursos/foco conforme o estado.
    private fun pause() {
        if (listening) recognizer?.cancel()
        tts?.stop()
        listening = false
        speaking = false
    }

    // Documentação: Alterna VoiceController.toggleMute, segundo o contrato e as verificações
    // deste módulo.
    fun toggleMute() {
        handler.post {
            AgentRuntime.mute.value = !AgentRuntime.mute.value
            if (AgentRuntime.mute.value) {
                pause()
                AgentRuntime.voiceStatus.value = "Microfone silenciado"
            } else AgentRuntime.voiceStatus.value = "Toque em Falar para continuar."
        }
    }

    // Documentação: Alterna VoiceController.toggleSpeaker, segundo o contrato e as verificações
    // deste módulo.
    fun toggleSpeaker() {
        handler.post {
            AgentRuntime.speaker.value = !AgentRuntime.speaker.value
            route(AgentRuntime.speaker.value)
        }
    }

    // Documentação: Implementa VoiceController.route como parte do fluxo descrito para este
    // arquivo.
    private fun route(speaker: Boolean) {
        if (Build.VERSION.SDK_INT >= 31) {
            val type =
                if (speaker) AudioDeviceInfo.TYPE_BUILTIN_SPEAKER
                else AudioDeviceInfo.TYPE_BUILTIN_EARPIECE
            val device = audio.availableCommunicationDevices.firstOrNull { it.type == type }
            if (device != null) audio.setCommunicationDevice(device)
            else AgentRuntime.voiceStatus.value = "Saída escolhida indisponível neste aparelho."
        } else {
            audio.isSpeakerphoneOn = speaker
        }
    }

    // Documentação: Implementa VoiceController.end como parte do fluxo descrito para este
    // arquivo.
    fun end() {
        handler.post {
            if (finished) return@post
            scope.launch {
                try {
                    val result =
                        JSONObject(
                            AgentRuntime.auth.api(
                                "/calls/${call.getString("id")}/end",
                                "POST",
                                JSONObject().put("device_id", call.getString("device_id")),
                            )
                        )
                    AgentRuntime.call.value = result
                    finishLocal()
                } catch (_: Exception) {
                    AgentRuntime.voiceStatus.value =
                        "Não foi possível encerrar no servidor. Tente novamente."
                }
            }
        }
    }

    // Documentação: Implementa VoiceController.finishLocal como parte do fluxo descrito para este
    // arquivo.
    fun finishLocal() {
        handler.post {
            if (finished) return@post
            finished = true
            pause()
            AgentRuntime.events.cancelVoice(call.getString("id"))
            AgentRuntime.refreshEvents()
            onFinished()
        }
    }

    // Documentação: Implementa VoiceController.destroy como parte do fluxo descrito para este
    // arquivo.
    fun destroy() {
        finished = true
        pause()
        recognizer?.destroy()
        tts?.shutdown()
        scope.cancel()
        audio.abandonAudioFocusRequest(focus)
        if (Build.VERSION.SDK_INT >= 31) audio.clearCommunicationDevice()
        audio.mode = AudioManager.MODE_NORMAL
    }
}
