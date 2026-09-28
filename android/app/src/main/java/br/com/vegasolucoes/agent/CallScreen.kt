package br.com.vegasolucoes.agent

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import java.time.Instant
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import org.json.JSONObject

@Composable
fun CallOverlay(activity: MainActivity, session: SessionData) {
    val received by AgentRuntime.received.collectAsStateWithLifecycle()
    val call by AgentRuntime.call.collectAsStateWithLifecycle()
    val voice by AgentRuntime.voice.collectAsStateWithLifecycle()
    val status by AgentRuntime.voiceStatus.collectAsStateWithLifecycle()
    val mute by AgentRuntime.mute.collectAsStateWithLifecycle()
    val speaker by AgentRuntime.speaker.collectAsStateWithLifecycle()
    val scope = rememberCoroutineScope()
    var error by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var selected by remember { mutableStateOf<String?>(null) }
    var now by remember { mutableStateOf(Instant.now()) }
    LaunchedEffect(Unit) {
        while (true) {
            now = Instant.now()
            delay(1000)
        }
    }
    val incoming = remember(received, now) { incomingCall(received) }
    fun startVoice() {
        try {
            if (!activity.lifecycle.currentState.isAtLeast(Lifecycle.State.RESUMED)) {
                error = "Volte ao aplicativo para ativar o áudio."
                return
            }
            activity.connect()
            ContextCompat.startForegroundService(
                activity,
                Intent(activity, VoiceService::class.java),
            )
        } catch (_: Exception) {
            error = "Não foi possível ativar o áudio. Continue por texto ou tente novamente."
        }
    }
    fun accept(id: String) {
        scope.launch {
            busy = true
            try {
                val row =
                    JSONObject(
                        AgentRuntime.auth.api(
                            "/calls/incoming/$id/answer",
                            "POST",
                            JSONObject().put("device_id", session.deviceId),
                        )
                    )
                AgentRuntime.call.value = row
                AgentNotifications(activity).cancel(id)
                val event =
                    outgoing("call.state", JSONObject().put("event_id", id).put("session", row))
                AgentRuntime.events.save(event)
                AgentRuntime.refreshEvents()
                startVoice()
                error = null
            } catch (_: Exception) {
                error = "Esta chamada expirou ou não pôde ser atendida. Atualize a conexão."
            } finally {
                busy = false
            }
        }
    }
    val microphone =
        rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) {
            if (selected != null) accept(selected!!) else startVoice()
        }
    val requestedAnswer by AgentRuntime.requestedAnswer.collectAsStateWithLifecycle()
    val lifecycleState by activity.lifecycle.currentStateFlow.collectAsStateWithLifecycle()
    LaunchedEffect(requestedAnswer, incoming, lifecycleState) {
        val requested = requestedAnswer
        if (requested != null && lifecycleState == Lifecycle.State.RESUMED) {
            AgentRuntime.requestedAnswer.value = null
            if (
                incomingCall(received, requested) != null && call?.optString("status") != "ACTIVE"
            ) {
                selected = requested
                if (
                    ContextCompat.checkSelfPermission(activity, Manifest.permission.RECORD_AUDIO) !=
                        PackageManager.PERMISSION_GRANTED
                )
                    microphone.launch(Manifest.permission.RECORD_AUDIO)
                else accept(requested)
            }
        }
    }
    LaunchedEffect(session.deviceId) {
        try {
            val rows = arrayRows(AgentRuntime.auth.api("/calls"))
            AgentRuntime.call.value = rows.firstOrNull {
                it.getString("status") == "ACTIVE" && it.getString("device_id") == session.deviceId
            }
        } catch (_: Exception) {}
    }
    if (call?.optString("status") == "ACTIVE") {
        var duration by remember { mutableLongStateOf(0) }
        var text by remember { mutableStateOf("") }
        LaunchedEffect(call?.optString("id")) {
            while (true) {
                duration =
                    runCatching {
                            java.time.Duration.between(
                                    Instant.parse(call!!.getString("started_at")),
                                    Instant.now(),
                                )
                                .seconds
                                .coerceAtLeast(0)
                        }
                        .getOrDefault(0)
                delay(1000)
            }
        }
        Dialog(
            onDismissRequest = {},
            properties = DialogProperties(usePlatformDefaultWidth = false),
        ) {
            Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                Column(
                    Modifier.fillMaxSize().systemBarsPadding().imePadding().padding(24.dp),
                    verticalArrangement = Arrangement.spacedBy(20.dp),
                ) {
                    Spacer(Modifier.height(24.dp))
                    Text(
                        "DEVLIMA AGENT",
                        color = MaterialTheme.colorScheme.primary,
                        style = MaterialTheme.typography.headlineMedium,
                    )
                    Text("Chamada interna · %02d:%02d".format(duration / 60, duration % 60))
                    Text(call!!.getString("reason"))
                    Text(status)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedButton(onClick = { voice?.toggleMute() }) {
                            Text(if (mute) "Ativar mic" else "Silenciar")
                        }
                        OutlinedButton(onClick = { voice?.toggleSpeaker() }) {
                            Text(if (speaker) "Alto-falante" else "Auricular")
                        }
                    }
                    Button(
                        onClick = {
                            if (voice == null) {
                                selected = null
                                if (
                                    ContextCompat.checkSelfPermission(
                                        activity,
                                        Manifest.permission.RECORD_AUDIO,
                                    ) != PackageManager.PERMISSION_GRANTED
                                )
                                    microphone.launch(Manifest.permission.RECORD_AUDIO)
                                else startVoice()
                            } else voice?.listen()
                        }
                    ) {
                        Text(if (voice == null) "Ativar áudio" else "Falar")
                    }
                    Text(
                        "O reconhecimento de fala pode usar o serviço instalado no Android. Confira suas configurações de voz.",
                        style = MaterialTheme.typography.bodySmall,
                    )
                    OutlinedTextField(
                        text,
                        { if (it.length <= 4000) text = it },
                        label = { Text("Alternativa por texto") },
                        modifier = Modifier.fillMaxWidth(),
                        maxLines = 4,
                    )
                    TextButton(
                        onClick = {
                            if (voice != null) voice?.sendText(text)
                            else {
                                AgentRuntime.events.enqueueVoice(call!!, text)
                                AgentRuntime.refreshEvents()
                                activity.connect()
                            }
                            text = ""
                        },
                        enabled = text.isNotBlank(),
                    ) {
                        Text("Enviar texto")
                    }
                    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
                    Spacer(Modifier.weight(1f))
                    Button(
                        onClick = {
                            if (voice != null) voice?.end()
                            else
                                scope.launch {
                                    try {
                                        AgentRuntime.call.value =
                                            JSONObject(
                                                AgentRuntime.auth.api(
                                                    "/calls/${call!!.getString("id")}/end",
                                                    "POST",
                                                    JSONObject().put("device_id", session.deviceId),
                                                )
                                            )
                                        AgentRuntime.events.cancelVoice(call!!.getString("id"))
                                        AgentRuntime.refreshEvents()
                                    } catch (_: Exception) {
                                        error = "Não foi possível encerrar. Tente novamente."
                                    }
                                }
                        },
                        colors =
                            ButtonDefaults.buttonColors(
                                containerColor = MaterialTheme.colorScheme.error
                            ),
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Text("Encerrar chamada")
                    }
                }
            }
        }
    } else if (incoming != null)
        AlertDialog(
            onDismissRequest = {},
            title = { Text("AGENTE ESTÁ LIGANDO") },
            text = {
                Column {
                    Text(incoming.getJSONObject("payload").optString("text"))
                    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
                }
            },
            confirmButton = {
                TextButton(
                    enabled = !busy,
                    onClick = {
                        selected = incoming.getString("event_id")
                        if (
                            ContextCompat.checkSelfPermission(
                                activity,
                                Manifest.permission.RECORD_AUDIO,
                            ) != PackageManager.PERMISSION_GRANTED
                        )
                            microphone.launch(Manifest.permission.RECORD_AUDIO)
                        else accept(selected!!)
                    },
                ) {
                    Text("Atender")
                }
            },
            dismissButton = {
                TextButton(
                    enabled = !busy,
                    onClick = {
                        scope.launch {
                            busy = true
                            try {
                                val id = incoming.getString("event_id")
                                AgentRuntime.auth.api(
                                    "/calls/incoming/$id/reject",
                                    "POST",
                                    JSONObject().put("device_id", session.deviceId),
                                )
                                AgentRuntime.events.save(
                                    outgoing(
                                        "call.dismissed",
                                        JSONObject().put("event_id", id).put("status", "REJECTED"),
                                    )
                                )
                                AgentRuntime.refreshEvents()
                                AgentNotifications(activity).cancel(id)
                            } catch (_: Exception) {
                                error = "Não foi possível recusar. Tente novamente."
                            } finally {
                                busy = false
                            }
                        }
                    },
                ) {
                    Text("Recusar")
                }
            },
        )
}
