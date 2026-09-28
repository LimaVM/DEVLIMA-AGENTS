# Fase 3 — conversas, contexto e memória

Concluída em **2026-09-28**, com implantação em `agent.vegasolucoes.com.br` e inferência real usando o modelo local via Tailscale.

## Entrega

- Migration `0003_context`: `conversations`, `messages`, `conversation_summaries`, `memories`, `memory_candidates` e `agent_actions`, preservando as tabelas anteriores.
- Agent Core com mensagem persistida antes da inferência, resposta transacional, UUID idempotente e lease durável por conversa. Falhas mantêm a mensagem original; reenvios concluídos retornam a resposta salva.
- Context Builder com relógio UTC/local, timezone do usuário, janela recente limitada, resumos incrementais e seleção de memórias próprias. Histórico bruto preservado.
- Memory Manager com candidatos, aceitação automática conservadora, confirmação/rejeição por API, deduplicação e desativação.
- Parser JSON/Pydantic com allowlist de operações e argumentos validados. Ações válidas são registradas `UNSUPPORTED`; execução de tarefas e VMs pertence às fases seguintes.
- APIs autenticadas de chat/conversas/histórico/resumos e memórias/candidatos, com paginação e isolamento por proprietário.
- CLI de teste real em banco separado (`smoke`/`verify`), orçamento configurável e documentação em [CONTEXT.md](../CONTEXT.md).

Backup anterior à migration: `/srv/devlima-agent/backups/phase2-before-0003.dump`, modo 0600. É backup local; backup externo e restore completo continuam previstos na Fase 9.

## Verificação

- **97 testes passaram**, incluindo os 61 anteriores. Casos novos verificam JSON inválido, ações/argumentos não permitidos, UTC, orçamento de contexto, resumo incremental, preservação do histórico, falha opcional do resumo, candidatos, replay, falha/retry, concorrência, lease expirada, arquivamento e isolamento entre usuários.
- Ruff passou. Alembic `check` não encontrou diferenças entre ORM e migrations; a migration foi aplicada primeiro no PostgreSQL de testes e depois no banco persistente.
- Um novo processo/container recuperou oito mensagens, um resumo e uma memória do smoke anterior. Replay retornou a resposta salva com **zero novos requests LLM**.
- Providers local e Groq continuam configurados e saudáveis no container de produção.
- O smoke utilizou quatro turnos reais de chat local, mais o resumo, com **zero tentativas Groq**. O primeiro turno salvou a preferência explícita por respostas curtas; uma nova conversa e uma nova sessão de banco recuperaram essa preferência.
- Latências dos turnos de chat: **4183, 2420, 2375 e 2319 ms**. Contextos entre **2668 e 3289 caracteres**, abaixo do limite. A conversa original reteve todas as mensagens após o resumo.
- HTTPS público `/health/ready` retorna schema `0003_context`. APIs de chat e memória sem JWT retornam 401.
- Os cinco registros de auditoria e quatro registros de inferência anteriores ao deploy foram preservados. Nenhum usuário de produção foi criado automaticamente; os usuários sintéticos ficam exclusivamente no banco de teste.
- PostgreSQL de testes parado ao concluir; template, VMs, pool/rede libvirt e credenciais dos workers não foram alterados.

## Ajuste validado no servidor real

O primeiro smoke encontrou uma resposta de resumo sem conteúdo final e um timeout de chat, mantendo a mensagem `FAILED` e sem fallback cloud. Nos requests JSON do llama.cpp, o provider passou a desativar thinking com `reasoning_effort=none` e `chat_template_kwargs.enable_thinking=false`. O smoke seguinte concluiu todo o fluxo em poucos segundos por turno. As opções não são enviadas ao Groq nem ao diagnóstico sem JSON; um teste verifica essa separação. Não houve mudança no serviço/modelo do llm-server. Referência: [protocolo do llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md).

## Como testar

```sh
curl https://agent.vegasolucoes.com.br/health/ready
```

Na VM:

```sh
cd /srv/devlima-agent
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm tests
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test --profile smoke run --rm context-smoke
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test --profile smoke run --rm context-smoke python -m app.agent.cli verify
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test
```

Execute `verify` depois do smoke, antes de rodar novamente os testes ou parar o banco efêmero. Ele inicia outro processo e verifica persistência/replay sem inferência. O smoke cria dados sintéticos, exige cloud desligado e recusa o banco de produção.

Para usar as APIs reais, crie seu usuário com a CLI administrativa e faça login conforme [README.md](../README.md). Não existe senha padrão.

## Limites e próxima fase

Memórias são selecionadas por palavras/preferências, sem embeddings. O orçamento é de caracteres, sem tokenizer exato. Candidatos inferidos ou reformulados podem ficar pendentes. O filtro de segredos é heurístico e o histórico bruto contém o texto original enviado. A recuperação de turnos abandonados ocorre no próximo request após expirar a lease.

A Fase 4 implementará tasks, reminders, scheduled calls, recorrência, scheduler separado, claims/outbox persistentes e recuperação após reinício. Android e execução de workers continuam nas fases próprias.
