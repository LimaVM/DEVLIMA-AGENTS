# Fase 4 — tarefas, agendamento e recuperação

Implementada em 2026-09-28. Migration `0004_planning` cria tasks, schedules, scheduled_events, outbox_events e scheduler_heartbeats. Backend e scheduler são processos separados; PostgreSQL continua sendo a fonte da verdade.

## Funcionamento

As APIs autenticadas `/tasks`, `/reminders` e `/scheduled-calls` oferecem criação, consulta, edição de tarefas/lembretes, conclusão de tarefas e cancelamento de agendamentos. Ações da LLM passam pelo parser, autorização e savepoints; uma ação recusada não invalida outra ação válida do mesmo turno. Propostas iguais no mesmo turno são deduplicadas. A resposta humana informa o resultado efetivamente persistido.

Datas precisam conter offset, são normalizadas para UTC e consultadas na timezone do usuário. Novos agendamentos precisam estar no futuro e dentro de 366 dias. Recorrência suporta DAILY/WEEKLY/MONTHLY/YEARLY e campos limitados; regras com frequências subdiárias, campos duplicados ou combinações inválidas são recusadas. O relógio local é preservado em mudanças de horário de verão.

APScheduler acorda o processo a cada cinco segundos; não guarda os eventos de negócio em memória. O scheduler reserva schedules usando `FOR UPDATE SKIP LOCKED` e grava ocorrência/outbox/avanço do próximo horário na mesma transação. UUID determinístico e constraints impedem duplicatas. Um crash antes do commit deixa o evento pendente. Recorrências vencidas durante downtime produzem um único aviso consolidado, com flag late, e avançam para a próxima ocorrência futura.

Cancelamento invalida avisos pendentes. Chamadas produzem `call.incoming` e `call.cancelled`; lembretes produzem `reminder.triggered`; tarefas produzem `task.updated`. A entrega/ACK por dispositivo será conectada na Fase 6; nesta fase os eventos ficam na outbox. Usuários inativos não geram novos disparos.

## Validação

- 120 testes passaram, incluindo os casos anteriores, APIs, isolamento, datas/recorrência, quatro schedulers concorrentes processando vinte agendamentos sem duplicatas e rollback de crash antes do commit.
- Alembic check não encontrou desvio entre migrations e ORM.
- Teste real usando Groq em banco isolado criou uma tarefa e um lembrete de café. Foram duas falhas locais de conexão e duas inferências Groq, com fallback auditado. Replay não chamou a LLM novamente e o scheduler produziu um evento reminder.triggered uma única vez.
- A falha local foi configurada somente no container de integração em uma porta loopback fechada. O llm-server não foi alterado.
- Backup anterior à migration: `/srv/devlima-agent/backups/phase3-before-0004.dump`, modo 0600.

## Comandos

Na VM, a partir de `/srv/devlima-agent`:

```sh
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.planning.scheduler health
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm tests
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test --profile smoke run --rm planning-smoke
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test
```

`planning-smoke` exige banco de teste, fallback habilitado e uma falha local isolada. Recebe a credencial Groq somente para esta integração real autorizada; a suíte pytest mantém credenciais fictícias e rede isolada. O horário futuro é simulado no tick do banco de teste para verificar o aviso sem esperar cinco minutos.

Referências: [APScheduler 3.x](https://apscheduler.readthedocs.io/en/3.x/userguide.html), [recorrência dateutil](https://dateutil.readthedocs.io/en/latest/rrule.html).

Próxima fase: VM Manager e ciclo de vida de workers Linux; Android será compilado/testado na VPS conforme preferência do proprietário.
