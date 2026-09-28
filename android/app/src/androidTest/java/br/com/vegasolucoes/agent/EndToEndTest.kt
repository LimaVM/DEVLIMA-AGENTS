package br.com.vegasolucoes.agent

import android.Manifest
import android.content.Intent
import android.graphics.Bitmap
import android.os.SystemClock
import androidx.core.content.ContextCompat
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import kotlinx.coroutines.runBlocking
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Assume.assumeTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
// Documentação: Define o tipo EndToEndTest e reúne o estado/contrato descrito para este módulo.
class EndToEndTest {
    @Test(timeout = 720000)
    // Documentação: Implementa EndToEndTest.realCoreCoffeeCallVoiceAndReconnect como parte do
    // fluxo descrito para este arquivo.
    fun realCoreCoffeeCallVoiceAndReconnect() {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val context = instrumentation.targetContext
        val config = File(context.noBackupFilesDir, "e2e-private.json")
        assumeTrue("Private, external E2E configuration must be injected", config.exists())
        val credentials = JSONObject(config.readText())
        require(credentials.getString("username").startsWith("devlima-v1-validation")) {
            "Use only an isolated validation account"
        }
        runBlocking {
            AgentRuntime.auth.login(
                credentials.getString("server"),
                credentials.getString("username"),
                credentials.getString("password"),
            )
        }
        config.delete()
        // Documentação: Implementa EndToEndTest.milestone como parte do fluxo descrito para este
        // arquivo.
        fun milestone(value: String) {
            File(context.filesDir, "e2e-progress.json")
                .writeText(JSONObject().put("stage", value).toString())
        }
        // Documentação: Implementa EndToEndTest.await como parte do fluxo descrito para este
        // arquivo.
        fun await(label: String, timeout: Long = 180000, predicate: () -> Boolean) {
            val end = SystemClock.elapsedRealtime() + timeout
            while (SystemClock.elapsedRealtime() < end) {
                if (predicate()) return
                Thread.sleep(500)
            }
            throw AssertionError("Timeout: $label")
        }
        instrumentation.uiAutomation
            .executeShellCommand(
                "pm grant ${context.packageName} ${Manifest.permission.POST_NOTIFICATIONS}"
            )
            .close()
        instrumentation.uiAutomation
            .executeShellCommand(
                "pm grant ${context.packageName} ${Manifest.permission.RECORD_AUDIO}"
            )
            .close()
        instrumentation.runOnMainSync {
            context.startActivity(
                Intent(context, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            )
        }
        Thread.sleep(1500)
        val thread = AgentRuntime.events.newThread()
        val coffee =
            AgentRuntime.events.enqueue(thread, "Me lembra daqui a 5 minutos de tomar café.")
        assertEquals("QUEUED", AgentRuntime.events.pending().first { it.id == coffee }.status)
        instrumentation.runOnMainSync {
            ContextCompat.startForegroundService(
                context,
                Intent(context, ConnectionService::class.java),
            )
        }
        await("authenticated WSS") { AgentRuntime.connection.value == "Conectado" }
        await("coffee reply") {
            AgentRuntime.events.pending().first { it.id == coffee }.status == "COMPLETED"
        }
        val coffeeReply = AgentRuntime.events.pending().first { it.id == coffee }.result!!
        assertTrue(
            "Reminder action must succeed",
            coffeeReply.getJSONArray("actions").toString().contains("SUCCEEDED"),
        )
        val reminder =
            runBlocking { arrayRows(AgentRuntime.auth.api("/reminders?status=SCHEDULED")) }
                .firstOrNull { it.getString("text").lowercase().contains("café") }
                ?: throw AssertionError("Coffee reminder missing")
        val callMessage =
            AgentRuntime.events.enqueue(
                thread,
                "Me liga daqui a 2 minutos para conversar sobre o café.",
            )
        await("call scheduling reply") {
            AgentRuntime.events.pending().first { it.id == callMessage }.status == "COMPLETED"
        }
        val scheduled =
            runBlocking { arrayRows(AgentRuntime.auth.api("/scheduled-calls?status=SCHEDULED")) }
                .firstOrNull() ?: throw AssertionError("Scheduled call missing")
        milestone("scheduled_ready")
        // App service reconnects with the same device/session and durable queue.
        instrumentation.runOnMainSync {
            context.stopService(Intent(context, ConnectionService::class.java))
        }
        await("disconnected") { AgentRuntime.connection.value == "Desconectado" }
        instrumentation.runOnMainSync {
            ContextCompat.startForegroundService(
                context,
                Intent(context, ConnectionService::class.java),
            )
        }
        await("reconnected") { AgentRuntime.connection.value == "Conectado" }
        await("incoming scheduled call", 240000) {
            AgentRuntime.events.recent().any {
                it.optString("type") == "call.incoming" &&
                    it.getJSONObject("payload").optString("schedule_id") ==
                        scheduled.getString("id")
            }
        }
        val incoming =
            AgentRuntime.events.recent().first {
                it.optString("type") == "call.incoming" &&
                    it.getJSONObject("payload").optString("schedule_id") ==
                        scheduled.getString("id")
            }
        val device = AgentRuntime.auth.session.value!!.deviceId
        val call = runBlocking {
            JSONObject(
                AgentRuntime.auth.api(
                    "/calls/incoming/${incoming.getString("event_id")}/answer",
                    "POST",
                    JSONObject().put("device_id", device),
                )
            )
        }
        AgentRuntime.call.value = call
        instrumentation.runOnMainSync {
            ContextCompat.startForegroundService(context, Intent(context, VoiceService::class.java))
        }
        await("voice foreground service") { AgentRuntime.voice.value != null }
        // Emulator validates transcript/Core/TTS coordination, without claiming physical microphone
        // quality.
        AgentRuntime.voice.value!!.sendText(
            "Olá, quero conversar sobre o café. Responda em uma frase curta."
        )
        await("voice reply", 180000) {
            AgentRuntime.events.pending().any {
                it.callId == call.getString("id") && it.status == "COMPLETED"
            }
        }
        assertTrue(
            AgentRuntime.events
                .pending()
                .first { it.callId == call.getString("id") }
                .result!!
                .getString("conversation_id") == call.getString("conversation_id")
        )
        milestone("voice_turn_complete")
        instrumentation.runOnMainSync {
            AgentRuntime.voice.value?.toggleMute()
            AgentRuntime.voice.value?.toggleSpeaker()
        }
        await("mute state") { AgentRuntime.mute.value }
        AgentRuntime.voice.value!!.end()
        await("ended call") { AgentRuntime.call.value?.optString("status") == "ENDED" }
        await("coffee notification event", 300000) {
            AgentRuntime.events.recent().any {
                it.optString("type") == "reminder.triggered" &&
                    it.getJSONObject("payload").optString("schedule_id") == reminder.getString("id")
            }
        }
        val event =
            AgentRuntime.events.recent().first {
                it.optString("type") == "reminder.triggered" &&
                    it.getJSONObject("payload").optString("schedule_id") == reminder.getString("id")
            }
        assertFalse(AgentRuntime.events.shouldNotify(event.getString("event_id")))
        val history = runBlocking {
            arrayRows(
                AgentRuntime.auth.api(
                    "/chat/conversations/${coffeeReply.getString("conversation_id")}/messages"
                )
            )
        }
        assertEquals(4, history.size)
        val task = runBlocking {
            JSONObject(
                AgentRuntime.auth.api("/tasks", "POST", JSONObject().put("title", "V1 E2E tarefa"))
            )
        }
        runBlocking {
            AgentRuntime.auth.api(
                "/tasks/${task.getString("id")}",
                "PATCH",
                JSONObject().put("title", "V1 E2E tarefa editada"),
            )
            AgentRuntime.auth.api("/tasks/${task.getString("id")}/complete", "POST", JSONObject())
        }
        val future = java.time.Instant.now().plusSeconds(600).toString()
        val cancel = runBlocking {
            JSONObject(
                AgentRuntime.auth.api(
                    "/reminders",
                    "POST",
                    JSONObject().put("text", "V1 cancel test").put("datetime", future),
                )
            )
        }
        runBlocking {
            AgentRuntime.auth.api(
                "/reminders/${cancel.getString("id")}",
                "PATCH",
                JSONObject().put("text", "V1 edited"),
            )
            AgentRuntime.auth.api("/reminders/${cancel.getString("id")}", "DELETE")
        }
        // Capture the actual app after returning to the chat.
        Thread.sleep(1500)
        instrumentation.uiAutomation.takeScreenshot()?.let { bitmap ->
            File(context.filesDir, "e2e-screen.png").outputStream().use {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)
            }
        }
        milestone("passed")
    }
}
