package br.com.vegasolucoes.agent

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.launch

val AgentColors =
    darkColorScheme(
        primary = Color(0xFF5EEACB),
        secondary = Color(0xFF87AAFF),
        background = Color(0xFF0C1420),
        surface = Color(0xFF142132),
        onPrimary = Color(0xFF07241C),
    )

class MainActivity : ComponentActivity() {
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        enableEdgeToEdge()
        setContent {
            MaterialTheme(colorScheme = AgentColors) {
                Surface(Modifier.fillMaxSize()) { AgentScreen(this) }
            }
        }
    }

    fun connect() {
        ContextCompat.startForegroundService(this, Intent(this, ConnectionService::class.java))
    }

    fun disconnect() {
        AgentRuntime.voice.value?.end()
        stopService(Intent(this, ConnectionService::class.java))
        getSharedPreferences("connection", MODE_PRIVATE).edit().putBoolean("wanted", false).apply()
    }
}

@Composable
fun AgentScreen(activity: MainActivity) {
    val session by AgentRuntime.auth.session.collectAsStateWithLifecycle()
    val connection by AgentRuntime.connection.collectAsStateWithLifecycle()
    val scope = rememberCoroutineScope()
    var tab by remember { mutableIntStateOf(0) }
    var denied by remember { mutableStateOf(false) }
    val permission =
        rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            denied = !granted
            activity.connect()
        }
    fun startConnection() {
        if (
            Build.VERSION.SDK_INT >= 33 &&
                ContextCompat.checkSelfPermission(
                    activity,
                    Manifest.permission.POST_NOTIFICATIONS,
                ) != PackageManager.PERMISSION_GRANTED
        )
            permission.launch(Manifest.permission.POST_NOTIFICATIONS)
        else activity.connect()
    }
    if (session == null) {
        LoginScreen { startConnection() }
        return
    }
    CallOverlay(activity, session!!)
    Scaffold(
        modifier = Modifier.systemBarsPadding().imePadding(),
        bottomBar = {
            NavigationBar {
                listOf("Chat", "Rotina", "Conta").forEachIndexed { i, label ->
                    NavigationBarItem(
                        selected = tab == i,
                        onClick = { tab = i },
                        icon = { Text(listOf("●", "✓", "◉")[i]) },
                        label = { Text(label) },
                    )
                }
            }
        },
    ) { padding ->
        Column(Modifier.fillMaxSize().padding(padding)) {
            Row(
                Modifier.fillMaxWidth().padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text(
                    "DEVLIMA AGENT",
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                )
                Text(connection, style = MaterialTheme.typography.labelSmall)
            }
            if (denied)
                Text(
                    "Notificações desativadas. Ative nas configurações para receber avisos.",
                    Modifier.padding(horizontal = 16.dp),
                    color = MaterialTheme.colorScheme.error,
                )
            when (tab) {
                0 -> ChatScreen { startConnection() }
                1 -> RoutineScreen(session!!)
                else ->
                    Column(
                        Modifier.verticalScroll(rememberScrollState()).padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp),
                    ) {
                        Text(
                            "Olá, ${session!!.username}",
                            style = MaterialTheme.typography.headlineSmall,
                        )
                        Text(session!!.server)
                        Text("Horários: ${session!!.timezone}")
                        Text(
                            "Mantenha a conexão ativa para lembretes e chamadas. Force stop e restrições de bateria podem interromper a entrega."
                        )
                        Button(onClick = { startConnection() }) { Text("Conectar") }
                        OutlinedButton(onClick = { activity.disconnect() }) { Text("Desconectar") }
                        TextButton(
                            onClick = {
                                scope.launch {
                                    activity.disconnect()
                                    AgentRuntime.auth.logout()
                                    AgentRuntime.events.clear()
                                    AgentRuntime.refreshEvents()
                                }
                            }
                        ) {
                            Text("Sair da conta")
                        }
                        MemoryScreen()
                    }
            }
        }
    }
}

@Composable
private fun LoginScreen(onLogged: () -> Unit) {
    val scope = rememberCoroutineScope()
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var server by remember { mutableStateOf(BuildConfig.DEFAULT_SERVER) }
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    Column(
        Modifier.fillMaxSize()
            .systemBarsPadding()
            .imePadding()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        Spacer(Modifier.height(24.dp))
        Text("DEVLIMA", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
        Text(
            "Seu agente,\nsempre por perto.",
            style = MaterialTheme.typography.headlineLarge,
            fontWeight = FontWeight.Bold,
        )
        Text("Converse, organize seus lembretes e receba chamadas do seu agente pessoal.")
        OutlinedTextField(
            server,
            { server = it },
            label = { Text("Servidor HTTPS") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Uri),
        )
        OutlinedTextField(
            username,
            { username = it },
            label = { Text("Usuário") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            password,
            { password = it },
            label = { Text("Senha") },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
        )
        Button(
            onClick = {
                scope.launch {
                    busy = true
                    error = null
                    try {
                        AgentRuntime.auth.login(server, username, password)
                        password = ""
                        AgentRuntime.refreshEvents()
                        onLogged()
                    } catch (_: Exception) {
                        error = "Não foi possível entrar. Confira os dados e sua conexão."
                    } finally {
                        busy = false
                    }
                }
            },
            enabled = !busy && username.isNotBlank() && password.isNotBlank(),
            modifier = Modifier.fillMaxWidth().height(52.dp),
        ) {
            Text(if (busy) "Entrando…" else "Entrar")
        }
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    }
}
