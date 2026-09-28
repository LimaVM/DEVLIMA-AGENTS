package br.com.vegasolucoes.agent

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioAttributes
import android.media.RingtoneManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.Person
import androidx.core.content.ContextCompat
import org.json.JSONObject

class AgentNotifications(private val context: Context) {
    companion object {
        const val CALL_CHANNEL = "incoming_calls_v2"
    }

    private val manager = context.getSystemService(NotificationManager::class.java)

    init {
        manager.createNotificationChannel(
            NotificationChannel(
                "connection",
                "Conexão do agente",
                NotificationManager.IMPORTANCE_LOW,
            )
        )
        manager.createNotificationChannel(
            NotificationChannel("reminders", "Lembretes", NotificationManager.IMPORTANCE_HIGH)
        )
        manager.createNotificationChannel(
            NotificationChannel(
                    CALL_CHANNEL,
                    "Chamadas internas",
                    NotificationManager.IMPORTANCE_HIGH,
                )
                .apply {
                    description = "Toque de chamadas recebidas do agente"
                    enableVibration(true)
                    setSound(
                        RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE),
                        AudioAttributes.Builder()
                            .setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE)
                            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                            .build(),
                    )
                    lockscreenVisibility = Notification.VISIBILITY_PRIVATE
                }
        )
    }

    fun foreground(text: String): Notification {
        val open =
            PendingIntent.getActivity(
                context,
                0,
                Intent(context, MainActivity::class.java),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )
        val stop =
            PendingIntent.getService(
                context,
                1,
                Intent(context, ConnectionService::class.java).setAction(ConnectionService.STOP),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )
        return NotificationCompat.Builder(context, "connection")
            .setSmallIcon(R.drawable.ic_agent)
            .setContentTitle("DevLima Agent ativo")
            .setContentText(text)
            .setContentIntent(open)
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .addAction(0, "Desconectar", stop)
            .build()
    }

    fun status(text: String) {
        manager.notify(1, foreground(text))
    }

    fun event(event: JSONObject) {
        val type = event.getString("type")
        if (type == "call.dismissed" || type == "call.state") {
            cancel(event.getJSONObject("payload").getString("event_id"))
            return
        }
        if (type != "reminder.triggered" && type != "call.incoming") return
        if (
            Build.VERSION.SDK_INT >= 33 &&
                ContextCompat.checkSelfPermission(
                    context,
                    Manifest.permission.POST_NOTIFICATIONS,
                ) != PackageManager.PERMISSION_GRANTED
        )
            return
        val call = type == "call.incoming"
        val remaining = if (call) callRemainingMillis(event.optString("timestamp")) else 0L
        if (
            call &&
                (remaining == 0L ||
                    incomingCall(AgentRuntime.received.value, event.getString("event_id")) == null)
        )
            return
        val id = event.getString("event_id")
        val payload = event.getJSONObject("payload")
        val open =
            PendingIntent.getActivity(
                context,
                id.hashCode(),
                Intent(
                        context,
                        if (call) IncomingCallActivity::class.java else MainActivity::class.java,
                    )
                    .setAction("event.$id")
                    .putExtra("event_id", id),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )
        val title = if (call) "AGENTE ESTÁ LIGANDO" else "Lembrete do agente"
        val builder =
            NotificationCompat.Builder(context, if (call) CALL_CHANNEL else "reminders")
                .setSmallIcon(R.drawable.ic_agent)
                .setContentTitle(title)
                .setContentText(payload.optString("text", "Abra o agente"))
                .setStyle(NotificationCompat.BigTextStyle().bigText(payload.optString("text")))
                .setContentIntent(open)
                .setAutoCancel(!call)
                .setOnlyAlertOnce(true)
                .setVisibility(NotificationCompat.VISIBILITY_PRIVATE)
                .setCategory(
                    if (call) NotificationCompat.CATEGORY_CALL
                    else NotificationCompat.CATEGORY_REMINDER
                )
        if (call) {
            val answer =
                PendingIntent.getActivity(
                    context,
                    id.hashCode() + 1,
                    Intent(context, IncomingCallActivity::class.java)
                        .setAction("answer.$id")
                        .putExtra("event_id", id),
                    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
                )
            val reject =
                PendingIntent.getBroadcast(
                    context,
                    id.hashCode() + 2,
                    Intent(context, CallRejectReceiver::class.java)
                        .setAction("reject.$id")
                        .putExtra("event_id", id),
                    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
                )
            builder
                .setStyle(
                    NotificationCompat.CallStyle.forIncomingCall(
                        Person.Builder().setName("DevLima Agent").setImportant(true).build(),
                        reject,
                        answer,
                    )
                )
                .setOngoing(true)
                .setTimeoutAfter(remaining)
            if (Build.VERSION.SDK_INT < 34 || manager.canUseFullScreenIntent())
                builder.setFullScreenIntent(open, true)
        }
        val notification = builder.build()
        if (call) notification.flags = notification.flags or Notification.FLAG_INSISTENT
        manager.notify(id, 2, notification)
    }

    fun cancel(id: String) {
        manager.cancel(id, 2)
    }
}
