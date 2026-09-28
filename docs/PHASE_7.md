# Fase 7 — chat e rotina Android

Implementação e compilação realizadas na VPS. App 0.7.0: Chat/Rotina/Conta, lista de conversas, histórico paginado (janela de até 2000 mensagens por atualização), estados de envio e reenvio manual. SQLite criptografa conteúdo de filas, histórico e títulos; identifica a conta pelo servidor e UUID real retornado em /auth/me e limpa dados ao trocar de proprietário. Sair elimina dados locais e revoga a sessão.

Fila persiste UUID antes do envio WSS, serializa turnos e conserva identidade após desconexão/restart. A primeira resposta associa a conversa local ao UUID do Core; resposta/evento e conclusão local são gravados na mesma transação antes do ACK. Reenvio recupera resposta idempotente do Core. Falhas transitórias têm tentativas limitadas; falha definitiva espera ação explícita e bloqueia a fila para preservar ordem. A fila não promete executar envios enquanto o serviço estiver parado.

Rotina usa APIs reais: tarefas (criar/editar/concluir), lembretes (criar/editar/cancelar) e chamadas agendadas (criar/cancelar). Filtros Hoje/Pendentes e atualização explícita; listas mostram até 100 itens. Horário digitado em dd/mm/aaaa hh:mm usa a timezone da conta, normaliza UTC e rejeita gaps/ambiguidades DST. Recorrência inicial diária/semanal é limitada a 30 ocorrências. Consultar/aceitar/recusar memórias propostas está na Conta. Eventos recebidos alimentam as notificações.

## Validação na VPS

- assembleDebug, lintDebug e 3 testes unitários passaram.
- 2 testes instrumentados passaram no emulador API 36: criptografia/persistência e fila com reconexão, deduplicação, associação de conversa e isolamento após troca de conta.
- Corrigido erro de inferência Kotlin 2.3 em arrays SQL com tipos mistos mediante argumento explícito Any.
- Backend permanece no schema 0006_devices; nenhuma migração nova é necessária nesta fase.

Fluxo de café/call com temporização real e integração autenticada Android/produção será executado na Fase 9. Alternância física de redes e teste de microfone/alto-falante dependem do aparelho.
