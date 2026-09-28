package br.com.vegasolucoes.agent

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import org.json.JSONObject
import java.util.UUID

class EventStore(context: Context, private val secure: SecureStore): SQLiteOpenHelper(context,"events.db",null,1) {
    override fun onCreate(db: SQLiteDatabase) { db.execSQL("CREATE TABLE events(id TEXT PRIMARY KEY,type TEXT NOT NULL,payload TEXT NOT NULL,received_at INTEGER NOT NULL,notified INTEGER NOT NULL DEFAULT 0)") }
    override fun onUpgrade(db: SQLiteDatabase,old: Int,new: Int) { error("Unsupported database upgrade") }
    @Synchronized fun save(event: JSONObject): Boolean {
        val id=UUID.fromString(event.getString("event_id")).toString()
        val values=ContentValues().apply { put("id",id);put("type",event.getString("type"));put("payload",secure.encrypt(event.toString()));put("received_at",System.currentTimeMillis()) }
        return writableDatabase.insertWithOnConflict("events",null,values,SQLiteDatabase.CONFLICT_IGNORE) != -1L
    }
    @Synchronized fun shouldNotify(id: String): Boolean = readableDatabase.rawQuery("SELECT notified FROM events WHERE id=?",arrayOf(id)).use { it.moveToFirst() && it.getInt(0)==0 }
    @Synchronized fun notified(id: String) { writableDatabase.execSQL("UPDATE events SET notified=1 WHERE id=?",arrayOf(id)) }
    @Synchronized fun recent(limit: Int=100): List<JSONObject> {
        val result=mutableListOf<JSONObject>()
        readableDatabase.rawQuery("SELECT payload FROM events ORDER BY received_at DESC LIMIT ?",arrayOf(limit.coerceIn(1,1000).toString())).use { rows ->
            while(rows.moveToNext()) { try { result.add(JSONObject(secure.decrypt(rows.getString(0)))) } catch (_:Exception) { } }
        }
        return result
    }
    @Synchronized fun clear() { writableDatabase.delete("events",null,null) }
}
