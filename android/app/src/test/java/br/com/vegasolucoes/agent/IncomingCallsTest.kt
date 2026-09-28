package br.com.vegasolucoes.agent

import java.time.Instant
import org.junit.Assert.*
import org.junit.Test

class IncomingCallsTest {
    @Test
    fun replayCannotExtendRingingWindow() {
        val now = Instant.parse("2026-09-28T18:00:00Z")
        assertEquals(1000L, callRemainingMillis("2026-09-28T17:58:01Z", now))
        assertEquals(0L, callRemainingMillis("2026-09-28T17:58:00Z", now))
        assertEquals(0L, callRemainingMillis("2026-09-28T17:00:00Z", now))
        assertEquals(0L, callRemainingMillis("invalid", now))
        assertEquals(0L, callRemainingMillis("2026-09-28T19:00:00Z", now))
        assertEquals(120000L, callRemainingMillis("2026-09-28T18:00:00Z", now))
    }
}
