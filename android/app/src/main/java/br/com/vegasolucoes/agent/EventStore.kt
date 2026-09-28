package br.com.vegasolucoes.agent

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.util.UUID
import org.json.JSONArray
import org.json.JSONObject

// Documentação: Define o tipo LocalThread e reúne o estado/contrato descrito para este módulo.
data class LocalThread(val id: String, val serverId: String?, val title: String)

// Documentação: Define o tipo PendingMessage e reúne o estado/contrato descrito para este módulo.
data class PendingMessage(
    val id: String,
    val threadId: String,
    val content: String,
    val status: String,
    val result: JSONObject?,
    val attempts: Int,
    val callId: String? = null,
)

// Documentação: Define o tipo Bubble e reúne o estado/contrato descrito para este módulo.
data class Bubble(
    val text: String,
    val mine: Boolean,
    val state: String = "",
    val retryId: String? = null,
)

// Documentação: Define o tipo EventStore e reúne o estado/contrato descrito para este módulo.
class EventStore(context: Context, private val secure: SecureStore) :
    SQLiteOpenHelper(context, "events.db", null, 3) {
    // Documentação: Trata o callback de EventStore.onCreate, segundo o contrato e as verificações
    // deste módulo.
    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            "CREATE TABLE events(id TEXT PRIMARY KEY,type TEXT NOT NULL,payload TEXT NOT NULL,received_at INTEGER NOT NULL,notified INTEGER NOT NULL DEFAULT 0)"
        )
        createQueue(db)
    }

    // Documentação: Cria EventStore.createQueue, segundo o contrato e as verificações deste
    // módulo.
    private fun createQueue(db: SQLiteDatabase) {
        db.execSQL(
            "CREATE TABLE threads(id TEXT PRIMARY KEY,server_id TEXT UNIQUE,title TEXT NOT NULL,updated INTEGER NOT NULL)"
        )
        db.execSQL(
            "CREATE TABLE pending(id TEXT PRIMARY KEY,thread_id TEXT NOT NULL,content TEXT NOT NULL,status TEXT NOT NULL,result TEXT,attempts INTEGER NOT NULL DEFAULT 0,retry_at INTEGER NOT NULL DEFAULT 0,created INTEGER NOT NULL,call_id TEXT)"
        )
        db.execSQL("CREATE TABLE history(conversation_id TEXT PRIMARY KEY,payload TEXT NOT NULL)")
        db.execSQL("CREATE TABLE metadata(name TEXT PRIMARY KEY,value TEXT NOT NULL)")
    }

    // Documentação: Trata o callback de EventStore.onUpgrade, segundo o contrato e as
    // verificações deste módulo.
    override fun onUpgrade(db: SQLiteDatabase, old: Int, new: Int) {
        if (old < 2) createQueue(db)
        else if (old < 3) db.execSQL("ALTER TABLE pending ADD COLUMN call_id TEXT")
    }

    @Synchronized
    // Documentação: Apaga cache/fila de outro proprietário antes de associar armazenamento ao
    // usuário autenticado.
    fun ensureOwner(owner: String) {
        val db = writableDatabase
        val previous =
            db.rawQuery("SELECT value FROM metadata WHERE name='owner'", null).use {
                if (it.moveToFirst()) secure.decrypt(it.getString(0)) else null
            }
        if (previous != owner) {
            clear()
            db.execSQL(
                "INSERT INTO metadata(name,value) VALUES('owner',?)",
                arrayOf<Any>(secure.encrypt(owner)),
            )
        }
    }

    @Synchronized
    // Documentação: Persiste evento por UUID com deduplicação e atualiza mensagem/thread quando a
    // resposta chega.
    fun save(event: JSONObject): Boolean {
        val id = UUID.fromString(event.getString("event_id")).toString()
        val db = writableDatabase
        db.beginTransaction()
        try {
            val values =
                ContentValues().apply {
                    put("id", id)
                    put("type", event.getString("type"))
                    put("payload", secure.encrypt(event.toString()))
                    put("received_at", System.currentTimeMillis())
                }
            val added =
                db.insertWithOnConflict("events", null, values, SQLiteDatabase.CONFLICT_IGNORE) !=
                    -1L
            if (event.getString("type") == "agent.message") {
                val reply = event.getJSONObject("payload")
                val client = reply.optString("client_message_id")
                val source =
                    db.rawQuery("SELECT thread_id FROM pending WHERE id=?", arrayOf(client)).use {
                        if (it.moveToFirst()) it.getString(0) else null
                    }
                if (source != null) {
                    val duplicate =
                        db.rawQuery(
                                "SELECT id FROM threads WHERE server_id=? AND id!=?",
                                arrayOf(reply.getString("conversation_id"), source),
                            )
                            .use { if (it.moveToFirst()) it.getString(0) else null }
                    if (duplicate != null) {
                        db.execSQL(
                            "UPDATE pending SET thread_id=? WHERE thread_id=?",
                            arrayOf(source, duplicate),
                        )
                        db.delete("threads", "id=?", arrayOf(duplicate))
                    }
                    db.execSQL(
                        "UPDATE threads SET server_id=?,updated=? WHERE id=?",
                        arrayOf<Any>(
                            reply.getString("conversation_id"),
                            System.currentTimeMillis(),
                            source,
                        ),
                    )
                }
                db.execSQL(
                    "UPDATE pending SET status='COMPLETED',result=? WHERE id=?",
                    arrayOf<Any>(secure.encrypt(reply.toString()), client),
                )
            }
            db.setTransactionSuccessful()
            return added
        } finally {
            db.endTransaction()
        }
    }

    @Synchronized
    // Documentação: Implementa EventStore.shouldNotify como parte do fluxo descrito para este
    // arquivo.
    fun shouldNotify(id: String): Boolean =
        readableDatabase.rawQuery("SELECT notified FROM events WHERE id=?", arrayOf(id)).use {
            it.moveToFirst() && it.getInt(0) == 0
        }

    @Synchronized
    // Documentação: Implementa EventStore.notified como parte do fluxo descrito para este
    // arquivo.
    fun notified(id: String) {
        writableDatabase.execSQL("UPDATE events SET notified=1 WHERE id=?", arrayOf<Any>(id))
    }

    @Synchronized
    // Documentação: Implementa EventStore.recent como parte do fluxo descrito para este arquivo.
    fun recent(limit: Int = 100): List<JSONObject> {
        val result = mutableListOf<JSONObject>()
        readableDatabase
            .rawQuery(
                "SELECT payload FROM events ORDER BY received_at DESC LIMIT ?",
                arrayOf(limit.coerceIn(1, 1000).toString()),
            )
            .use { rows ->
                while (rows.moveToNext()) runCatching {
                    result.add(JSONObject(secure.decrypt(rows.getString(0))))
                }
            }
        return result
    }

    @Synchronized
    // Documentação: Implementa EventStore.threads como parte do fluxo descrito para este arquivo.
    fun threads(): List<LocalThread> =
        readableDatabase
            .rawQuery("SELECT id,server_id,title FROM threads ORDER BY updated DESC", null)
            .use { c ->
                buildList {
                    while (c.moveToNext()) add(
                        LocalThread(
                            c.getString(0),
                            if (c.isNull(1)) null else c.getString(1),
                            secure.decrypt(c.getString(2)),
                        )
                    )
                }
            }

    @Synchronized
    // Documentação: Implementa EventStore.newThread como parte do fluxo descrito para este
    // arquivo.
    fun newThread(): String =
        UUID.randomUUID().toString().also {
            writableDatabase.execSQL(
                "INSERT INTO threads VALUES(?,NULL,?,?)",
                arrayOf<Any>(it, secure.encrypt("Nova conversa"), System.currentTimeMillis()),
            )
        }

    @Synchronized
    // Documentação: Importa EventStore.importThreads, segundo o contrato e as verificações deste
    // módulo.
    fun importThreads(rows: JSONArray) {
        val db = writableDatabase
        for (i in 0 until rows.length()) {
            val row = rows.getJSONObject(i)
            val id = row.getString("id")
            db.execSQL(
                "INSERT OR IGNORE INTO threads VALUES(?,?,?,?)",
                arrayOf<Any>(
                    id,
                    id,
                    secure.encrypt(row.getString("title")),
                    System.currentTimeMillis() - i,
                ),
            )
            db.execSQL(
                "UPDATE threads SET title=? WHERE server_id=?",
                arrayOf<Any>(secure.encrypt(row.getString("title")), id),
            )
        }
    }

    @Synchronized
    // Documentação: Enfileira EventStore.enqueue, segundo o contrato e as verificações deste
    // módulo.
    fun enqueue(thread: String, text: String): String {
        require(text.isNotBlank() && text.length <= 4000)
        require(threads().any { it.id == thread })
        val id = UUID.randomUUID().toString()
        writableDatabase.execSQL(
            "INSERT INTO pending(id,thread_id,content,status,created) VALUES(?,?,?,'QUEUED',?)",
            arrayOf<Any>(id, thread, secure.encrypt(text), System.currentTimeMillis()),
        )
        writableDatabase.execSQL(
            "UPDATE threads SET updated=?,title=CASE WHEN server_id IS NULL THEN ? ELSE title END WHERE id=?",
            arrayOf<Any>(System.currentTimeMillis(), secure.encrypt(text.take(60)), thread),
        )
        return id
    }

    @Synchronized
    // Documentação: Implementa EventStore.pending como parte do fluxo descrito para este arquivo.
    fun pending(thread: String? = null): List<PendingMessage> =
        readableDatabase
            .rawQuery(
                "SELECT id,thread_id,content,status,result,attempts,call_id FROM pending" +
                    (if (thread == null) "" else " WHERE thread_id=?") +
                    " ORDER BY created,rowid",
                thread?.let { arrayOf(it) },
            )
            .use { c ->
                buildList {
                    while (c.moveToNext()) add(
                        PendingMessage(
                            c.getString(0),
                            c.getString(1),
                            secure.decrypt(c.getString(2)),
                            c.getString(3),
                            if (c.isNull(4)) null else JSONObject(secure.decrypt(c.getString(4))),
                            c.getInt(5),
                            if (c.isNull(6)) null else c.getString(6),
                        )
                    )
                }
            }

    @Synchronized
    // Documentação: Escolhe o próximo envio durável respeitando ordem global, bloqueio por falha
    // e retry_at.
    fun nextFrame(): JSONObject? {
        // One outstanding turn globally; a failed turn blocks its thread until explicit retry.
        val next =
            pending().firstOrNull { it.status !in setOf("COMPLETED", "CANCELLED") } ?: return null
        if (next.status == "FAILED") return null
        val due =
            readableDatabase
                .rawQuery("SELECT retry_at FROM pending WHERE id=?", arrayOf(next.id))
                .use {
                    it.moveToFirst()
                    it.getLong(0)
                }
        if (due > System.currentTimeMillis()) return null
        val thread = threads().first { it.id == next.threadId }
        if (next.callId != null)
            return outgoing(
                "voice.transcript",
                JSONObject()
                    .put("call_session_id", next.callId)
                    .put("client_message_id", next.id)
                    .put("content", next.content),
                next.id,
            )
        return outgoing(
            "chat.message",
            JSONObject().put("client_message_id", next.id).put("content", next.content).apply {
                thread.serverId?.let { put("conversation_id", it) }
            },
            next.id,
        )
    }

    @Synchronized
    // Documentação: Enfileira EventStore.enqueueVoice, segundo o contrato e as verificações deste
    // módulo.
    fun enqueueVoice(call: JSONObject, text: String): String {
        val conversation = call.getString("conversation_id")
        importThreads(
            JSONArray()
                .put(
                    JSONObject()
                        .put("id", conversation)
                        .put("title", "Chamada: " + call.optString("reason"))
                )
        )
        val thread = threads().first { it.serverId == conversation }
        return enqueue(thread.id, text).also {
            writableDatabase.execSQL(
                "UPDATE pending SET call_id=? WHERE id=?",
                arrayOf(call.getString("id"), it),
            )
        }
    }

    @Synchronized
    // Documentação: Cancela EventStore.cancelVoice, segundo o contrato e as verificações deste
    // módulo.
    fun cancelVoice(callId: String) {
        writableDatabase.execSQL(
            "UPDATE pending SET status='CANCELLED' WHERE call_id=? AND status!='COMPLETED'",
            arrayOf(callId),
        )
    }

    @Synchronized
    // Documentação: Implementa EventStore.sent como parte do fluxo descrito para este arquivo.
    fun sent(id: String) {
        writableDatabase.execSQL(
            "UPDATE pending SET status='SENDING',attempts=attempts+1,retry_at=? WHERE id=? AND status!='COMPLETED'",
            arrayOf<Any>(System.currentTimeMillis() + 180000, id),
        )
    }

    @Synchronized
    // Documentação: Implementa EventStore.response como parte do fluxo descrito para este
    // arquivo.
    fun response(event: JSONObject) {
        val body = event.getJSONObject("payload")
        val id = body.optString("client_message_id")
        if (id.isEmpty()) return
        if (event.getString("type") == "error") {
            val retry =
                body.optString("code") in
                    setOf(
                        "device_busy",
                        "conversation_busy",
                        "processing_lease_expired",
                        "processing_lease_lost",
                        "service_unavailable",
                        "provider_timeout",
                        "provider_connection_failed",
                    )
            val current = pending().firstOrNull { it.id == id } ?: return
            val state = if (retry && current.attempts < 5) "QUEUED" else "FAILED"
            writableDatabase.execSQL(
                "UPDATE pending SET status=?,retry_at=? WHERE id=? AND status!='COMPLETED'",
                arrayOf<Any>(state, System.currentTimeMillis() + 15000, id),
            )
        }
    }

    @Synchronized
    // Documentação: Implementa EventStore.reconnect como parte do fluxo descrito para este
    // arquivo.
    fun reconnect() {
        writableDatabase.execSQL(
            "UPDATE pending SET status='QUEUED',retry_at=0 WHERE status='SENDING'"
        )
    }

    @Synchronized
    // Documentação: Tenta novamente EventStore.retry, segundo o contrato e as verificações deste
    // módulo.
    fun retry(id: String) {
        writableDatabase.execSQL(
            "UPDATE pending SET status='QUEUED',attempts=0,retry_at=0 WHERE id=? AND status='FAILED'",
            arrayOf<Any>(id),
        )
    }

    @Synchronized
    // Documentação: Implementa EventStore.cacheHistory como parte do fluxo descrito para este
    // arquivo.
    fun cacheHistory(id: String, rows: JSONArray) {
        writableDatabase.execSQL(
            "INSERT OR REPLACE INTO history VALUES(?,?)",
            arrayOf<Any>(id, secure.encrypt(rows.toString())),
        )
    }

    @Synchronized
    // Documentação: Implementa EventStore.bubbles como parte do fluxo descrito para este arquivo.
    fun bubbles(thread: LocalThread): List<Bubble> {
        val history =
            thread.serverId?.let { id ->
                readableDatabase
                    .rawQuery("SELECT payload FROM history WHERE conversation_id=?", arrayOf(id))
                    .use {
                        if (it.moveToFirst()) JSONArray(secure.decrypt(it.getString(0)))
                        else JSONArray()
                    }
            } ?: JSONArray()
        val ids = mutableSetOf<String>()
        val result = mutableListOf<Bubble>()
        for (i in 0 until history.length()) {
            val row = history.getJSONObject(i)
            ids.add(row.getString("id"))
            result.add(
                Bubble(
                    row.getString("content"),
                    row.getString("role") == "user",
                    if (row.optString("status") == "FAILED") "Falha no envio" else "",
                )
            )
        }
        for (row in pending(thread.id)) {
            if (row.result == null || row.result.optString("user_message_id") !in ids)
                result.add(
                    Bubble(
                        row.content,
                        true,
                        when (row.status) {
                            "QUEUED" -> "Na fila"
                            "SENDING" -> "Aguardando agente…"
                            "CANCELLED" -> "Chamada encerrada"
                            "FAILED" -> "Falha — toque para tentar novamente"
                            else -> ""
                        },
                        if (row.status == "FAILED") row.id else null,
                    )
                )
            row.result?.let {
                if (it.optString("assistant_message_id") !in ids)
                    result.add(Bubble(it.getString("reply"), false))
            }
        }
        return result
    }

    @Synchronized
    // Documentação: Limpa EventStore.clear, segundo o contrato e as verificações deste módulo.
    fun clear() {
        for (table in
            listOf("events", "pending", "threads", "history", "metadata")) writableDatabase.delete(
            table,
            null,
            null,
        )
    }
}
