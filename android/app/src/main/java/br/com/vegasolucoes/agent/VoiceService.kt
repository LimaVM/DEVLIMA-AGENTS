package br.com.vegasolucoes.agent

import android.Manifest
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.PackageManager
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat

class VoiceService : Service() {
    private var controller: VoiceController? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val call = AgentRuntime.call.value
        if (call == null || call.optString("status") != "ACTIVE") {
            stopSelf()
            return START_NOT_STICKY
        }
        val open =
            PendingIntent.getActivity(
                this,
                42,
                Intent(this, MainActivity::class.java),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )
        val notification =
            NotificationCompat.Builder(this, "connection")
                .setSmallIcon(R.drawable.ic_agent)
                .setContentTitle("Chamada com DevLima Agent")
                .setContentText("Microfone ativo durante a escuta; abra para silenciar ou encerrar")
                .setContentIntent(open)
                .setOngoing(true)
                .build()
        val microphone =
            ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) ==
                PackageManager.PERMISSION_GRANTED
        if (Build.VERSION.SDK_INT >= 34)
            startForeground(
                3,
                notification,
                if (microphone) ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE
                else ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE,
            )
        else startForeground(3, notification)
        if (controller == null) {
            controller = VoiceController(this, call) { stopSelf() }
            AgentRuntime.voice = controller
        }
        return START_NOT_STICKY
    }

    override fun onDestroy() {
        controller?.destroy()
        if (AgentRuntime.voice === controller) AgentRuntime.voice = null
        super.onDestroy()
    }
}
