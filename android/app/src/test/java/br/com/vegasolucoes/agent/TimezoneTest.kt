package br.com.vegasolucoes.agent

import java.time.Instant
import org.junit.Assert.*
import org.junit.Test

class TimezoneTest {
    @Test
    fun saoPauloDateUsesAccountTimezoneAndRejectsDstGap() {
        assertEquals(
            Instant.parse("2026-09-28T13:30:00Z"),
            localToInstant("28/09/2026 10:30", "America/Sao_Paulo"),
        )
        assertThrows(IllegalArgumentException::class.java) {
            localToInstant("08/03/2026 02:30", "America/New_York")
        }
        assertThrows(IllegalArgumentException::class.java) {
            localToInstant("01/11/2026 01:30", "America/New_York")
        }
    }
}
