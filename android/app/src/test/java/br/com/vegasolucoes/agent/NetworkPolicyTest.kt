package br.com.vegasolucoes.agent

import org.junit.Assert.*
import org.junit.Test

class NetworkPolicyTest {
    @Test
    fun backoffIsBoundedAndResettable() {
        val backoff = Backoff()
        repeat(30) { assertTrue(backoff.nextDelay() in 1000..60000) }
        backoff.reset()
        assertTrue(backoff.nextDelay() in 1000..1200)
    }

    @Test
    fun endpointRequiresHttpsWithoutCredentials() {
        assertEquals(
            "https://agent.vegasolucoes.com.br",
            normalizedServer("https://agent.vegasolucoes.com.br/"),
        )
        for (url in
            listOf(
                "http://example.com",
                "https://user:secret@example.com",
                "https://example.com/api",
                "https://example.com/?token=x",
            )) {
            try {
                normalizedServer(url)
                fail(url)
            } catch (_: IllegalArgumentException) {}
        }
    }
}
