package br.com.vegasolucoes.agent

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.util.UUID
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class StorageTest {
    @Test
    fun credentialsAreEncryptedAndEventsSurviveReopenWithoutDuplicate() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val vault = SecureStore(context)
        val device = vault.deviceId()
        val data =
            SessionData(
                "https://agent.vegasolucoes.com.br",
                "fake-test-access-not-a-real-token",
                "fake-test-refresh-not-a-real-token",
                1234567890L,
                device,
                "test",
            )
        vault.save(data)
        assertEquals(data, vault.load())
        assertFalse(File(context.noBackupFilesDir, "session.bin").readText().contains(data.access))
        val event =
            JSONObject()
                .put("event_id", UUID.randomUUID().toString())
                .put("type", "reminder.triggered")
                .put("payload", JSONObject().put("text", "storage-test-coffee"))
        val store = EventStore(context, vault)
        assertTrue(store.save(event))
        assertFalse(store.save(event))
        store.notified(event.getString("event_id"))
        store.close()
        val reopened = EventStore(context, SecureStore(context))
        assertTrue(
            reopened.recent().any { it.getString("event_id") == event.getString("event_id") }
        )
        assertFalse(reopened.shouldNotify(event.getString("event_id")))
        reopened.readableDatabase
            .rawQuery("SELECT payload FROM events WHERE id=?", arrayOf(event.getString("event_id")))
            .use {
                assertTrue(it.moveToFirst())
                assertFalse(it.getString(0).contains("storage-test-coffee"))
            }
        reopened.clear()
        reopened.close()
        vault.clear()
        assertNotEquals(device, vault.deviceId())
    }
}
