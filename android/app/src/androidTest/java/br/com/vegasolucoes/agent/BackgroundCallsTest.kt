package br.com.vegasolucoes.agent

import android.Manifest
import android.app.ActivityManager
import android.app.Notification
import android.app.NotificationManager
import android.content.Intent
import android.os.SystemClock
import androidx.core.content.ContextCompat
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import java.io.File
import java.time.Instant
import kotlinx.coroutines.runBlocking
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Assume.assumeTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
// Documentação: Define o tipo BackgroundCallsTest e reúne o estado/contrato descrito para este
// módulo.
class BackgroundCallsTest {
    private val instrumentation = InstrumentationRegistry.getInstrumentation()
    private val context = instrumentation.targetContext

    // Documentação: Implementa BackgroundCallsTest.await como parte do fluxo descrito para este
    // arquivo.
    private fun await(label: String, condition: () -> Boolean) {
        val deadline = SystemClock.elapsedRealtime() + 45000
        while (SystemClock.elapsedRealtime() < deadline) {
            if (condition()) return
            Thread.sleep(250)
        }
        throw AssertionError("Timeout: $label")
    }

    // Documentação: Implementa BackgroundCallsTest.connect como parte do fluxo descrito para este
    // arquivo.
    private fun connect() {
        val file = File(context.noBackupFilesDir, "e2e-private.json")
        assumeTrue("Isolated, private configuration required", file.exists())
        val credentials = JSONObject(file.readText())
        require(credentials.getString("username").startsWith("devlima-v1-validation"))
        runBlocking {
            AgentRuntime.auth.login(
                credentials.getString("server"),
                credentials.getString("username"),
                credentials.getString("password"),
            )
        }
        file.delete()
        instrumentation.uiAutomation
            .executeShellCommand(
                "pm grant ${context.packageName} ${Manifest.permission.POST_NOTIFICATIONS}"
            )
            .close()
        instrumentation.runOnMainSync {
            context.startActivity(
                Intent(context, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            )
        }
        Thread.sleep(1000)
        instrumentation.runOnMainSync {
            ContextCompat.startForegroundService(
                context,
                Intent(context, ConnectionService::class.java),
            )
        }
        await("connected") { AgentRuntime.connection.value == "Conectado" }
    }

    @Test
    // Documentação: Implementa BackgroundCallsTest.loginAndConnectForExternalIdleProbe como parte
    // do fluxo descrito para este arquivo.
    fun loginAndConnectForExternalIdleProbe() {
        connect()
    }

    @Test
    // Documentação: Implementa BackgroundCallsTest.removedTaskAndLockedScreenReceiveCall como
    // parte do fluxo descrito para este arquivo.
    fun removedTaskAndLockedScreenReceiveCall() {
        connect()
        val schedule = runBlocking {
            JSONObject(
                AgentRuntime.auth.api(
                    "/scheduled-calls",
                    "POST",
                    JSONObject()
                        .put("reason", "Teste de chamada com interface fechada")
                        .put("datetime", Instant.now().plusSeconds(12).toString()),
                )
            )
        }
        instrumentation.runOnMainSync {
            context.getSystemService(ActivityManager::class.java).appTasks.forEach {
                it.finishAndRemoveTask()
            }
        }
        instrumentation.uiAutomation.executeShellCommand("input keyevent 223").close()
        try {
            await("incoming after task removal") {
                AgentRuntime.received.value.any {
                    it.optString("type") == "call.incoming" &&
                        it.getJSONObject("payload").optString("schedule_id") ==
                            schedule.getString("id")
                }
            }
            val event =
                AgentRuntime.received.value.first {
                    it.optString("type") == "call.incoming" &&
                        it.getJSONObject("payload").optString("schedule_id") ==
                            schedule.getString("id")
                }
            val id = event.getString("event_id")
            val manager = context.getSystemService(NotificationManager::class.java)
            await("ringing notification") { manager.activeNotifications.any { it.tag == id } }
            val notification = manager.activeNotifications.first { it.tag == id }.notification
            assertEquals(Notification.CATEGORY_CALL, notification.category)
            assertTrue(notification.flags and Notification.FLAG_INSISTENT != 0)
            assertNotNull(notification.fullScreenIntent)
            assertEquals(
                "android.app.Notification\$CallStyle",
                notification.extras.getString(Notification.EXTRA_TEMPLATE),
            )
            assertNotNull("Persistent connection survives closing its task", AgentRuntime.sender)
            await("incoming UI above lock screen") {
                var visible = false
                instrumentation.runOnMainSync {
                    visible =
                        ActivityLifecycleMonitorRegistry.getInstance()
                            .getActivitiesInStage(Stage.RESUMED)
                            .any { it is IncomingCallActivity }
                }
                visible
            }
            assertNull(
                "Incoming call must not activate microphone before answer",
                AgentRuntime.voice.value,
            )

            context.sendBroadcast(
                Intent(context, CallRejectReceiver::class.java).putExtra("event_id", id)
            )
            await("reject stops ringing") { manager.activeNotifications.none { it.tag == id } }
        } finally {
            instrumentation.uiAutomation.executeShellCommand("input keyevent 224").close()
        }
    }
}
