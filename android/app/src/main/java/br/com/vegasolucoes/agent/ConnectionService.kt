package br.com.vegasolucoes.agent

import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.net.ConnectivityManager
import android.net.Network
import android.os.Build
import android.os.IBinder
import java.time.Instant
import java.util.UUID
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withTimeoutOrNull
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import org.json.JSONObject

fun outgoing(
    type: String,
    payload: JSONObject = JSONObject(),
    id: String = UUID.randomUUID().toString(),
): JSONObject =
    JSONObject()
        .put("event_id", id)
        .put("timestamp", Instant.now().toString())
        .put("type", type)
        .put("payload", payload)

class ConnectionService : Service() {
    companion object {
        const val STOP = "br.com.vegasolucoes.agent.STOP"
    }

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val wake = Channel<Unit>(Channel.CONFLATED)
    private var activeSocket: WebSocket? = null
    private var started = false
    private lateinit var notifications: AgentNotifications
    private lateinit var connectivity: ConnectivityManager
    private val networkCallback =
        object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                wake.trySend(Unit)
            }
        }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        notifications = AgentNotifications(this)
        connectivity = getSystemService(ConnectivityManager::class.java)
        connectivity.registerDefaultNetworkCallback(networkCallback)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val prefs = getSharedPreferences("connection", MODE_PRIVATE)
        if (intent?.action == STOP) {
            prefs.edit().putBoolean("wanted", false).apply()
            stopSelf()
            return START_NOT_STICKY
        }
        if (
            AgentRuntime.auth.session.value == null ||
                (intent == null && !prefs.getBoolean("wanted", false))
        ) {
            stopSelf()
            return START_NOT_STICKY
        }
        prefs.edit().putBoolean("wanted", true).apply()
        if (Build.VERSION.SDK_INT >= 34)
            startForeground(
                1,
                notifications.foreground("Conectando…"),
                ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE,
            )
        else startForeground(1, notifications.foreground("Conectando…"))
        if (!started) {
            started = true
            scope.launch { connectionLoop() }
        }
        return START_STICKY
    }

    private fun status(value: String) {
        AgentRuntime.connection.value = value
        notifications.status(value)
    }

    private suspend fun connectionLoop() {
        val backoff = Backoff()
        while (scope.isActive) {
            try {
                status("Conectando…")
                val auth = AgentRuntime.auth.access()
                connect(auth, backoff)
            } catch (_: LoginRequired) {
                status("Entre novamente para conectar")
                getSharedPreferences("connection", MODE_PRIVATE)
                    .edit()
                    .putBoolean("wanted", false)
                    .apply()
                stopSelf()
                return
            } catch (issue: CancellationException) {
                throw issue
            } catch (_: Exception) {
                status("Sem conexão; tentando novamente")
            }
            val wait = backoff.nextDelay()
            withTimeoutOrNull(wait) { wake.receive() }
        }
    }

    private suspend fun connect(auth: SessionData, backoff: Backoff) {
        val closed = CompletableDeferred<Unit>()
        val frames = Channel<String>(100)
        var ready = false
        var invalid = false
        val listener =
            object : WebSocketListener() {
                override fun onOpen(ws: WebSocket, response: Response) {
                    ws.send(
                        outgoing(
                                "connection.authenticate",
                                JSONObject()
                                    .put("access_token", auth.access)
                                    .put("device_id", auth.deviceId)
                                    .put("name", Build.MODEL.take(64)),
                            )
                            .toString()
                    )
                }

                override fun onMessage(ws: WebSocket, text: String) {
                    if (text.length > 262144 || frames.trySend(text).isFailure) {
                        ws.close(1009, "Buffer limit")
                        closed.complete(Unit)
                    }
                }

                override fun onClosing(ws: WebSocket, code: Int, reason: String) {
                    if (code == 4401) invalid = true
                    ws.close(code, "")
                    closed.complete(Unit)
                }

                override fun onClosed(ws: WebSocket, code: Int, reason: String) {
                    if (code == 4401) invalid = true
                    closed.complete(Unit)
                }

                override fun onFailure(ws: WebSocket, error: Throwable, response: Response?) {
                    closed.complete(Unit)
                }
            }
        val ws =
            AgentRuntime.auth.http.newWebSocket(
                Request.Builder()
                    .url(auth.server.replaceFirst("https://", "wss://") + "/ws")
                    .build(),
                listener,
            )
        activeSocket = ws
        val processor = scope.launch {
            try {
                for (raw in frames) {
                    if (AgentRuntime.auth.session.value?.deviceId != auth.deviceId) break
                    val event = JSONObject(raw)
                    val id = UUID.fromString(event.getString("event_id")).toString()
                    when (event.getString("type")) {
                        "connection.ready" -> {
                            AgentRuntime.events.reconnect()
                            ready = true
                            backoff.reset()
                            AgentRuntime.sender = { ws.send(it.toString()) }
                            status("Conectado")
                        }
                        "connection.ping" -> ws.send(outgoing("connection.pong").toString())
                        "connection.pong_ack",
                        "event.acknowledged" -> Unit
                        "call.command_result",
                        "chat.accepted",
                        "chat.processed",
                        "error" -> {
                            AgentRuntime.events.response(event)
                            AgentRuntime.voice?.response(event)
                            AgentRuntime.refreshEvents()
                            AgentRuntime.responses.value = event
                        }
                        else -> {
                            AgentRuntime.events.save(event)
                            if (event.getString("type") == "call.state") {
                                val call = event.getJSONObject("payload").getJSONObject("session")
                                if (call.getString("device_id") == auth.deviceId) {
                                    AgentRuntime.call.value = call
                                    if (call.getString("status") != "ACTIVE") {
                                        AgentRuntime.events.cancelVoice(call.getString("id"))
                                        AgentRuntime.voice?.finishLocal()
                                    }
                                }
                            }
                            if (event.getString("type") == "agent.message")
                                AgentRuntime.voice?.reply(event.getJSONObject("payload"))
                            if (AgentRuntime.events.shouldNotify(id)) {
                                notifications.event(event)
                                AgentRuntime.events.notified(id)
                            }
                            AgentRuntime.refreshEvents()
                            ws.send(
                                outgoing("event.ack", JSONObject().put("event_id", id)).toString()
                            )
                        }
                    }
                }
            } catch (_: Exception) {
                ws.close(1003, "Invalid event")
                closed.complete(Unit)
            }
        }
        val queue = scope.launch {
            while (isActive) {
                if (ready)
                    AgentRuntime.events.nextFrame()?.let { frame ->
                        if (ws.send(frame.toString())) {
                            AgentRuntime.events.sent(frame.getString("event_id"))
                            AgentRuntime.refreshEvents()
                        }
                    }
                delay(1000)
            }
        }
        try {
            // Renew authentication through HTTPS before the access JWT expires.
            val untilRefresh =
                (auth.expiresAt - System.currentTimeMillis() - 30000).coerceAtLeast(1000)
            val ended =
                withTimeoutOrNull(untilRefresh) {
                    closed.await()
                    true
                } ?: false
            if (!ended || invalid) AgentRuntime.auth.invalidateAccess()
            if (!ready) status("Conexão não autenticada; tentando novamente")
        } finally {
            AgentRuntime.sender = null
            activeSocket = null
            frames.close()
            processor.cancel()
            queue.cancel()
            ws.close(1000, "Reconnect")
            ws.cancel()
        }
    }

    override fun onDestroy() {
        AgentRuntime.sender = null
        activeSocket?.cancel()
        scope.cancel()
        wake.close()
        runCatching { connectivity.unregisterNetworkCallback(networkCallback) }
        AgentRuntime.connection.value = "Desconectado"
        super.onDestroy()
    }
}
