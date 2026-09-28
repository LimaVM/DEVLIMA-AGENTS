package br.com.vegasolucoes.agent

import android.app.Application
import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import org.json.JSONObject

// Documentação: Define o tipo AgentApplication e reúne o estado/contrato descrito para este
// módulo.
class AgentApplication : Application() {
    // Documentação: Trata o callback de AgentApplication.onCreate, segundo o contrato e as
    // verificações deste módulo.
    override fun onCreate() {
        super.onCreate()
        AgentRuntime.initialize(this)
    }
}

// Documentação: Define o tipo AgentRuntime e reúne o estado/contrato descrito para este módulo.
object AgentRuntime {
    lateinit var secure: SecureStore
    lateinit var auth: AuthRepository
    lateinit var events: EventStore
    val connection = MutableStateFlow("Desconectado")
    val received = MutableStateFlow<List<JSONObject>>(emptyList())
    val requestedAnswer = MutableStateFlow<String?>(null)
    val call = MutableStateFlow<JSONObject?>(null)
    val voiceStatus = MutableStateFlow("Pronto para conversar")
    val mute = MutableStateFlow(false)
    val speaker = MutableStateFlow(true)
    val voice = MutableStateFlow<VoiceController?>(null)
    val revision = MutableStateFlow(0L)
    val responses = MutableStateFlow<JSONObject?>(null)
    @Volatile var sender: ((JSONObject) -> Boolean)? = null

    @Synchronized
    // Documentação: Implementa AgentRuntime.initialize como parte do fluxo descrito para este
    // arquivo.
    fun initialize(context: Context) {
        if (::auth.isInitialized) return
        secure = SecureStore(context)
        events = EventStore(context, secure)
        auth = AuthRepository(secure, events)
        received.value = events.recent()
    }

    // Documentação: Atualiza AgentRuntime.refreshEvents, segundo o contrato e as verificações
    // deste módulo.
    fun refreshEvents() {
        received.value = events.recent()
        revision.value++
    }
}
