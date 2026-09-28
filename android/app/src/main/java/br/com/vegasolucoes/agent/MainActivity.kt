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
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.launch

val AgentColors=darkColorScheme(primary=Color(0xFF5EEACB),secondary=Color(0xFF87AAFF),background=Color(0xFF0C1420),surface=Color(0xFF142132),onPrimary=Color(0xFF07241C))

class MainActivity: ComponentActivity() {
    override fun onCreate(state: Bundle?) {
        super.onCreate(state);enableEdgeToEdge()
        setContent { MaterialTheme(colorScheme=AgentColors) { Surface(Modifier.fillMaxSize()) { AgentScreen(this) } } }
    }
    fun connect() { ContextCompat.startForegroundService(this,Intent(this,ConnectionService::class.java)) }
    fun disconnect() { stopService(Intent(this,ConnectionService::class.java));getSharedPreferences("connection",MODE_PRIVATE).edit().putBoolean("wanted",false).apply() }
}

@Composable fun AgentScreen(activity: MainActivity) {
    val session by AgentRuntime.auth.session.collectAsStateWithLifecycle()
    val connection by AgentRuntime.connection.collectAsStateWithLifecycle()
    val scope=rememberCoroutineScope()
    var error by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    val permission=rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { activity.connect() }
    fun startConnection() {
        if(Build.VERSION.SDK_INT>=33 && ContextCompat.checkSelfPermission(activity,Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED) permission.launch(Manifest.permission.POST_NOTIFICATIONS)
        else activity.connect()
    }
    Column(Modifier.fillMaxSize().systemBarsPadding().imePadding().verticalScroll(rememberScrollState()).padding(24.dp),verticalArrangement=Arrangement.spacedBy(18.dp)) {
        Spacer(Modifier.height(24.dp))
        Text("DEVLIMA",color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.labelLarge,fontWeight=FontWeight.Bold)
        Text("Seu agente,\nsempre por perto.",style=MaterialTheme.typography.headlineLarge,fontWeight=FontWeight.Bold)
        Text("Converse, organize seus lembretes e receba chamadas do seu agente pessoal.",color=MaterialTheme.colorScheme.onSurfaceVariant)
        if(session==null) {
            var server by remember { mutableStateOf(BuildConfig.DEFAULT_SERVER) }
            var username by remember { mutableStateOf("") }
            var password by remember { mutableStateOf("") }
            OutlinedTextField(server,{server=it},label={Text("Servidor HTTPS")},singleLine=true,modifier=Modifier.fillMaxWidth())
            OutlinedTextField(username,{username=it},label={Text("Usuário")},singleLine=true,modifier=Modifier.fillMaxWidth())
            OutlinedTextField(password,{password=it},label={Text("Senha")},visualTransformation=PasswordVisualTransformation(),singleLine=true,modifier=Modifier.fillMaxWidth())
            Button(onClick={ scope.launch { busy=true;error=null;try { AgentRuntime.auth.login(server,username,password);password="";startConnection() } catch (_:Exception) { error="Não foi possível entrar. Confira servidor, usuário, senha e sua conexão." } finally { busy=false } } },enabled=!busy && username.isNotBlank() && password.isNotBlank(),modifier=Modifier.fillMaxWidth().height(52.dp)) { Text(if(busy)"Entrando…" else "Entrar") }
        } else {
            Card(Modifier.fillMaxWidth()) { Column(Modifier.padding(20.dp),verticalArrangement=Arrangement.spacedBy(10.dp)) {
                Text("Olá, ${session!!.username}",style=MaterialTheme.typography.titleLarge)
                Text(connection,color=MaterialTheme.colorScheme.primary)
                Text("${session!!.server}",style=MaterialTheme.typography.bodySmall)
                Text("Mantenha a conexão ativa para receber lembretes e chamadas. Você pode desconectar a qualquer momento.")
                Row(horizontalArrangement=Arrangement.spacedBy(10.dp)) {
                    Button(onClick={startConnection()}) { Text("Conectar") }
                    OutlinedButton(onClick={activity.disconnect()}) { Text("Desconectar") }
                }
            } }
            Text("Notificações e conexão respeitam as permissões e as restrições de bateria do Android.",style=MaterialTheme.typography.bodySmall,color=MaterialTheme.colorScheme.onSurfaceVariant)
            TextButton(onClick={scope.launch { activity.disconnect();AgentRuntime.auth.logout();AgentRuntime.events.clear();AgentRuntime.refreshEvents() }}) { Text("Sair da conta") }
        }
        error?.let { Text(it,color=MaterialTheme.colorScheme.error) }
    }
}
