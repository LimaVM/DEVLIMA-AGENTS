package br.com.vegasolucoes.agent
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.json.JSONObject
import java.util.UUID
@RunWith(AndroidJUnit4::class) class QueueTest {
    @Test fun reconnectRetainsIdentityAndReplyMapsNextTurnAtomically() {
        val context=InstrumentationRegistry.getInstrumentation().targetContext;val vault=SecureStore(context);val db=EventStore(context,vault);db.ensureOwner("test-owner-a");val thread=db.newThread();val first=db.enqueue(thread,"primeiro");val second=db.enqueue(thread,"segundo")
        assertEquals(first,db.nextFrame()!!.getString("event_id"));db.sent(first);assertNull(db.nextFrame());db.close()
        val reopened=EventStore(context,vault);reopened.reconnect();assertEquals(first,reopened.nextFrame()!!.getString("event_id"))
        val conversation=UUID.randomUUID().toString();val event=JSONObject().put("event_id",UUID.randomUUID().toString()).put("type","agent.message").put("payload",JSONObject().put("client_message_id",first).put("conversation_id",conversation).put("user_message_id",UUID.randomUUID().toString()).put("assistant_message_id",UUID.randomUUID().toString()).put("reply","resposta"))
        assertTrue(reopened.save(event));assertFalse(reopened.save(event));assertEquals(second,reopened.nextFrame()!!.getString("event_id"));assertEquals(conversation,reopened.nextFrame()!!.getJSONObject("payload").getString("conversation_id"));assertEquals(3,reopened.bubbles(reopened.threads().first()).size)
        reopened.ensureOwner("test-owner-a");assertEquals(1,reopened.threads().size);reopened.ensureOwner("test-owner-b");assertTrue(reopened.threads().isEmpty());assertTrue(reopened.recent().isEmpty());reopened.clear();reopened.close()
    }
}
