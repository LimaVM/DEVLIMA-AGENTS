package br.com.vegasolucoes.agent

import android.app.KeyguardManager
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.delay

/** Minimal lock-screen surface. Chat, reason and microphone remain behind unlock. */
class IncomingCallActivity : ComponentActivity() {
    private var answerRequested = false

    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        if (android.os.Build.VERSION.SDK_INT >= 27) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(
                android.view.WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                    android.view.WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON
            )
        }
        answerRequested = intent.action?.startsWith("answer.") == true
        enableEdgeToEdge()
        val id =
            intent.getStringExtra("event_id")
                ?: run {
                    finish()
                    return
                }
        setContent {
            MaterialTheme(colorScheme = AgentColors) {
                val events by AgentRuntime.received.collectAsStateWithLifecycle()
                var tick by remember { mutableIntStateOf(0) }
                LaunchedEffect(id) {
                    while (true) {
                        delay(1000)
                        tick++
                    }
                }
                val incoming = remember(events, tick) { incomingCall(events, id) }
                LaunchedEffect(incoming) { if (incoming == null) finish() }
                Surface(Modifier.fillMaxSize()) {
                    Column(
                        Modifier.fillMaxSize().systemBarsPadding().padding(32.dp),
                        verticalArrangement = Arrangement.spacedBy(24.dp),
                    ) {
                        Spacer(Modifier.weight(1f))
                        Text(
                            "DEVLIMA AGENT",
                            style = MaterialTheme.typography.headlineMedium,
                            color = MaterialTheme.colorScheme.primary,
                        )
                        Text("Agente está ligando", style = MaterialTheme.typography.headlineLarge)
                        Text(
                            "Desbloqueie para conversar. O microfone só será ativado após atender."
                        )
                        Button(
                            onClick = { answer(id) },
                            enabled = incoming != null,
                            modifier = Modifier.fillMaxWidth(),
                        ) {
                            Text("Atender")
                        }
                        OutlinedButton(
                            onClick = {
                                sendBroadcast(
                                    Intent(
                                            this@IncomingCallActivity,
                                            CallRejectReceiver::class.java,
                                        )
                                        .putExtra("event_id", id)
                                )
                            },
                            modifier = Modifier.fillMaxWidth(),
                        ) {
                            Text("Recusar")
                        }
                        Spacer(Modifier.weight(1f))
                    }
                }
            }
        }
    }

    override fun onPostResume() {
        super.onPostResume()
        if (answerRequested) {
            answerRequested = false
            intent.getStringExtra("event_id")?.let { answer(it) }
        }
    }

    private fun answer(id: String) {
        val keyguard = getSystemService(KeyguardManager::class.java)
        fun open() {
            if (incomingCall(AgentRuntime.received.value, id) == null) {
                finish()
                return
            }
            AgentRuntime.requestedAnswer.value = id
            startActivity(
                Intent(this, MainActivity::class.java)
                    .setAction("answer.$id")
                    .addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)
            )
            finish()
        }
        if (!keyguard.isKeyguardLocked) open()
        else if (android.os.Build.VERSION.SDK_INT >= 26)
            keyguard.requestDismissKeyguard(
                this,
                object : KeyguardManager.KeyguardDismissCallback() {
                    override fun onDismissSucceeded() {
                        open()
                    }
                },
            )
    }
}
