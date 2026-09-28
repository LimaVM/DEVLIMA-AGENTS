package br.com.vegasolucoes.agent

import android.app.Application
import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import org.json.JSONObject

class AgentApplication: Application() { override fun onCreate() { super.onCreate();AgentRuntime.initialize(this) } }

object AgentRuntime {
    lateinit var secure: SecureStore
    lateinit var auth: AuthRepository
    lateinit var events: EventStore
    val connection=MutableStateFlow("Desconectado")
    val received=MutableStateFlow<List<JSONObject>>(emptyList())
    val responses=MutableStateFlow<JSONObject?>(null)
    @Volatile var sender: ((JSONObject)->Boolean)?=null
    @Synchronized fun initialize(context: Context) {
        if(::auth.isInitialized) return
        secure=SecureStore(context);auth=AuthRepository(secure);events=EventStore(context,secure)
        received.value=events.recent()
    }
    fun refreshEvents() { received.value=events.recent() }
}
