package br.com.vegasolucoes.agent

import java.time.Duration
import java.time.Instant
import org.json.JSONObject

// Never ring a delayed outbox replay beyond the server's answer window.
// Documentação: Calcula a janela restante de 120 segundos; valores inválidos, antigos ou muito
// futuros não tornam a chamada atendível.
fun callRemainingMillis(timestamp: String, now: Instant = Instant.now()): Long = runCatching {
    val started = Instant.parse(timestamp)
    if (started.isAfter(now.plusSeconds(5))) 0L
    else Duration.between(now, started.plusSeconds(120)).toMillis().coerceIn(0L, 120000L)
}
    .getOrDefault(0L)

// Documentação: Seleciona chamada ainda não resolvida, opcionalmente por event_id, dentro do
// prazo de atendimento.
fun incomingCall(events: List<JSONObject>, id: String? = null): JSONObject? {
    val resolved =
        events
            .filter { it.optString("type") in setOf("call.dismissed", "call.state") }
            .map { it.getJSONObject("payload").optString("event_id") }
            .toSet()
    return events.firstOrNull {
        it.optString("type") == "call.incoming" &&
            (id == null || it.optString("event_id") == id) &&
            it.optString("event_id") !in resolved &&
            callRemainingMillis(it.optString("timestamp")) > 0
    }
}
