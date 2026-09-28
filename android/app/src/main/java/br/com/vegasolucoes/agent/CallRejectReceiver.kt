package br.com.vegasolucoes.agent

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject

// Documentação: Define o tipo CallRejectReceiver e reúne o estado/contrato descrito para este
// módulo.
class CallRejectReceiver : BroadcastReceiver() {
    // Documentação: Trata o callback de CallRejectReceiver.onReceive, segundo o contrato e as
    // verificações deste módulo.
    override fun onReceive(context: Context, intent: Intent) {
        val id = intent.getStringExtra("event_id") ?: return
        val session = AgentRuntime.auth.session.value ?: return
        val pending = goAsync()
        CoroutineScope(Dispatchers.IO).launch {
            try {
                AgentRuntime.auth.api(
                    "/calls/incoming/$id/reject",
                    "POST",
                    JSONObject().put("device_id", session.deviceId),
                )
                val event =
                    outgoing(
                        "call.dismissed",
                        JSONObject().put("event_id", id).put("status", "REJECTED"),
                    )
                AgentRuntime.events.save(event)
                AgentRuntime.refreshEvents()
                AgentNotifications(context).cancel(id)
            } catch (_: Exception) {
                AgentRuntime.voiceStatus.value = "Abra o aplicativo para recusar novamente."
            } finally {
                pending.finish()
            }
        }
    }
}
