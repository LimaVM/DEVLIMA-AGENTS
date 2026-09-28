package br.com.vegasolucoes.agent

import android.Manifest
import android.app.NotificationManager
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.PowerManager
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat

@Composable
// Documentação: Implementa CallDeliverySettings como parte do fluxo descrito para este arquivo.
fun CallDeliverySettings(activity: MainActivity) {
    var revision by remember { mutableIntStateOf(0) }
    val settings =
        rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) {
            revision++
        }
    val manager = activity.getSystemService(NotificationManager::class.java)
    val power = activity.getSystemService(PowerManager::class.java)
    val enabled =
        remember(revision) {
            manager.areNotificationsEnabled() &&
                (Build.VERSION.SDK_INT < 33 ||
                    ContextCompat.checkSelfPermission(
                        activity,
                        Manifest.permission.POST_NOTIFICATIONS,
                    ) == PackageManager.PERMISSION_GRANTED) &&
                (manager.getNotificationChannel(AgentNotifications.CALL_CHANNEL)?.importance
                    ?: 0) >= NotificationManager.IMPORTANCE_HIGH
        }
    val fullscreen =
        remember(revision) { Build.VERSION.SDK_INT < 34 || manager.canUseFullScreenIntent() }
    val battery = remember(revision) { power.isIgnoringBatteryOptimizations(activity.packageName) }
    Text("Receber chamadas com a tela bloqueada", style = MaterialTheme.typography.titleLarge)
    Text(
        "Você pode fechar a tela do app. Mantenha DevLima Agent ativo na notificação para receber chamadas. Ao conectar, ele também tentará reconectar após reiniciar e desbloquear o celular."
    )
    Text("Notificações de chamada: " + if (enabled) "permitidas" else "precisam de configuração")
    OutlinedButton(
        onClick = {
            settings.launch(
                Intent(Settings.ACTION_CHANNEL_NOTIFICATION_SETTINGS)
                    .putExtra(Settings.EXTRA_APP_PACKAGE, activity.packageName)
                    .putExtra(Settings.EXTRA_CHANNEL_ID, AgentNotifications.CALL_CHANNEL)
            )
        }
    ) {
        Text("Configurar toque e notificações")
    }
    if (Build.VERSION.SDK_INT >= 34) {
        Text("Tela de chamada: " + if (fullscreen) "permitida" else "toque para permitir")
        OutlinedButton(
            onClick = {
                settings.launch(
                    Intent(
                        Settings.ACTION_MANAGE_APP_USE_FULL_SCREEN_INTENT,
                        Uri.parse("package:" + activity.packageName),
                    )
                )
            }
        ) {
            Text("Permitir chamada na tela bloqueada")
        }
    }
    Text(
        "Economia de bateria: " +
            if (battery) "sem otimização do Android" else "pode atrasar chamadas em repouso"
    )
    OutlinedButton(
        onClick = {
            settings.launch(Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS))
        }
    ) {
        Text("Configurar bateria")
    }
    Text(
        "Em Xiaomi, confira também início automático e bateria Sem restrições nas configurações do app. As opções dependem da versão do sistema.",
        style = MaterialTheme.typography.bodySmall,
    )
    Text(
        "Sem internet, após Forçar parada ou encerrar o agente em Apps ativos, não há chamada imediata. Abra o app e toque Conectar para retomar. Não perturbe e volume de toque continuam valendo.",
        style = MaterialTheme.typography.bodySmall,
    )
    Spacer(Modifier.height(4.dp))
}
