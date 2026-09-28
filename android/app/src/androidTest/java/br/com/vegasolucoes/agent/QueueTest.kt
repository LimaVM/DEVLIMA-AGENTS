package br.com.vegasolucoes.agent

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.util.UUID
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class QueueTest {
    @Test
    fun voiceQueueUsesCallIdentityAndStopsAfterEnd() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val db = EventStore(context, SecureStore(context))
        db.ensureOwner("voice-queue-test")
        val call =
            JSONObject()
                .put("id", UUID.randomUUID().toString())
                .put("conversation_id", UUID.randomUUID().toString())
                .put("reason", "test")
        val message = db.enqueueVoice(call, "Olá por voz")
        val frame = db.nextFrame()!!
        assertEquals("voice.transcript", frame.getString("type"))
        assertEquals(message, frame.getString("event_id"))
        assertEquals(
            call.getString("id"),
            frame.getJSONObject("payload").getString("call_session_id"),
        )
        db.cancelVoice(call.getString("id"))
        assertNull(db.nextFrame())
        db.clear()
        db.close()
    }

    @Test
    fun reconnectRetainsIdentityAndReplyMapsNextTurnAtomically() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val vault = SecureStore(context)
        val db = EventStore(context, vault)
        db.ensureOwner("test-owner-a")
        val thread = db.newThread()
        val first = db.enqueue(thread, "primeiro")
        val second = db.enqueue(thread, "segundo")
        assertEquals(first, db.nextFrame()!!.getString("event_id"))
        db.sent(first)
        assertNull(db.nextFrame())
        db.close()
        val reopened = EventStore(context, vault)
        reopened.reconnect()
        assertEquals(first, reopened.nextFrame()!!.getString("event_id"))
        val conversation = UUID.randomUUID().toString()
        val event =
            JSONObject()
                .put("event_id", UUID.randomUUID().toString())
                .put("type", "agent.message")
                .put(
                    "payload",
                    JSONObject()
                        .put("client_message_id", first)
                        .put("conversation_id", conversation)
                        .put("user_message_id", UUID.randomUUID().toString())
                        .put("assistant_message_id", UUID.randomUUID().toString())
                        .put("reply", "resposta"),
                )
        assertTrue(reopened.save(event))
        assertFalse(reopened.save(event))
        assertEquals(second, reopened.nextFrame()!!.getString("event_id"))
        assertEquals(
            conversation,
            reopened.nextFrame()!!.getJSONObject("payload").getString("conversation_id"),
        )
        assertEquals(3, reopened.bubbles(reopened.threads().first()).size)
        reopened.ensureOwner("test-owner-a")
        assertEquals(1, reopened.threads().size)
        reopened.ensureOwner("test-owner-b")
        assertTrue(reopened.threads().isEmpty())
        assertTrue(reopened.recent().isEmpty())
        reopened.clear()
        reopened.close()
    }
}
