package br.com.vegasolucoes.agent

import org.junit.Assert.*
import org.junit.Test

// Documentação: Define o tipo NetworkPolicyTest e reúne o estado/contrato descrito para este
// módulo.
class NetworkPolicyTest {
    @Test
    // Documentação: Implementa NetworkPolicyTest.backoffIsBoundedAndResettable como parte do
    // fluxo descrito para este arquivo.
    fun backoffIsBoundedAndResettable() {
        val backoff = Backoff()
        repeat(30) { assertTrue(backoff.nextDelay() in 1000..60000) }
        backoff.reset()
        assertTrue(backoff.nextDelay() in 1000..1200)
    }

    @Test
    // Documentação: Implementa NetworkPolicyTest.endpointRequiresHttpsWithoutCredentials como
    // parte do fluxo descrito para este arquivo.
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
