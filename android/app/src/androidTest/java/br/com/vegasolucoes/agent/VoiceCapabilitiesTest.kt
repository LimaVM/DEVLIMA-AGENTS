package br.com.vegasolucoes.agent

import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
// Documentação: Define o tipo VoiceCapabilitiesTest e reúne o estado/contrato descrito para este
// módulo.
class VoiceCapabilitiesTest {
    @Test
    // Documentação: Implementa
    // VoiceCapabilitiesTest.reportsAvailableEnginesWithoutAssumingPhysicalAudio como parte do
    // fluxo descrito para este arquivo.
    fun reportsAvailableEnginesWithoutAssumingPhysicalAudio() {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val context = instrumentation.targetContext
        val done = CountDownLatch(1)
        var tts: TextToSpeech? = null
        var result = TextToSpeech.ERROR
        var language = TextToSpeech.LANG_NOT_SUPPORTED
        instrumentation.runOnMainSync {
            tts =
                TextToSpeech(context) { status ->
                    result = status
                    done.countDown()
                }
        }
        assertTrue("TTS engine initialization must resolve", done.await(30, TimeUnit.SECONDS))
        instrumentation.runOnMainSync {
            if (result == TextToSpeech.SUCCESS)
                language = tts!!.setLanguage(Locale.forLanguageTag("pt-BR"))
        }
        val report =
            JSONObject()
                .put(
                    "speech_recognizer_available",
                    SpeechRecognizer.isRecognitionAvailable(context),
                )
                .put("tts_initialized", result == TextToSpeech.SUCCESS)
                .put("tts_pt_br_available", language >= 0)
                .put("physical_audio_tested", false)
        File(context.filesDir, "voice-capabilities.json").writeText(report.toString())
        instrumentation.runOnMainSync { tts?.shutdown() }
    }
}
