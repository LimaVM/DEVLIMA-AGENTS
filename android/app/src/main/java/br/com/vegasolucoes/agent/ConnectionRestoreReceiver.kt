package br.com.vegasolucoes.agent

import android.app.ActivityManager
import android.app.ApplicationExitInfo
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.content.ContextCompat

// Documentação: Define o tipo ConnectionRestoreReceiver e reúne o estado/contrato descrito para
// este módulo.
class ConnectionRestoreReceiver : BroadcastReceiver() {
    // Documentação: Restaura somente conexão desejada com sessão válida, sem ignorar parada
    // explícita pelo usuário.
    override fun onReceive(context: Context, intent: Intent) {
        if (
            intent.action !in setOf(Intent.ACTION_BOOT_COMPLETED, Intent.ACTION_MY_PACKAGE_REPLACED)
        )
            return
        val prefs = context.getSharedPreferences("connection", Context.MODE_PRIVATE)
        if (!prefs.getBoolean("wanted", false)) return
        if (Build.VERSION.SDK_INT >= 30) {
            val stopped =
                context
                    .getSystemService(ActivityManager::class.java)
                    .getHistoricalProcessExitReasons(context.packageName, 0, 10)
                    .any {
                        it.reason == ApplicationExitInfo.REASON_USER_REQUESTED &&
                            it.timestamp >= prefs.getLong("enabled_at", 0L)
                    }
            if (stopped) {
                prefs.edit().putBoolean("wanted", false).apply()
                return
            }
        }
        if (AgentRuntime.auth.session.value == null) return
        // Credential storage is available after boot/unlock. Never start the microphone here.
        runCatching {
            ContextCompat.startForegroundService(
                context,
                Intent(context, ConnectionService::class.java),
            )
        }
    }
}
