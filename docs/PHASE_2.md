# Fase 2 — router LLM

Concluída em **2026-09-28**, com deploy na VM e inferência real nos dois providers.

## Criado e alterado

- Interface `LLMProvider` com chat/health_check; providers llama.cpp e Groq; router local → cloud somente em falha técnica enumerada.
- Timeouts por provider, validação de URL privada e nenhum proxy/redirect herdado. Respostas e erros validados sem expor corpos de erro ou credenciais.
- Migration Alembic `0002_llm_requests`, com auditoria por tentativa, latência, provider, modelo, erro, request ID, timestamps UTC, uso de tokens e flag fallback.
- `GET /llm/health` e `POST /llm/chat` autenticados, com limites de entrada. Chat de diagnóstico sem histórico/contexto/actions; a Fase 3 construirá o chat persistente.
- CLI administrativo `python -m app.llm.cli health|smoke`.
- Compose e configuração do backend atualizados; credencial Groq armazenada apenas no `.env` 0600 da VM, excluída do Git/contexto Docker. Credenciais reais não são fornecidas aos containers de testes.
- Backup PostgreSQL anterior à migration em `/srv/devlima-agent/backups/phase1-before-0002.dump`, 0600. É backup local; backup externo/recovery completo permanece na Fase 9.

## Configuração real

- Tailscale Core: `100.108.84.64`; LLM: `100.102.91.22`.
- Base URL: `http://100.102.91.22:8080/v1`.
- Modelo local detectado: `gemma-4-12b-it-UD-Q4_K_XL.gguf`, ID completo retornado por `/v1/models` mantido no `.env`.
- Modelo fallback Groq: `openai/gpt-oss-120b`, confirmado na lista disponível e por inferência. Nenhuma ferramenta cloud/search/code-execution é habilitada no request.
- Timeouts padrão de inferência: 30 s; health: 5 s; fallback habilitado na configuração real.

## Política de fallback

Permitido: timeout, conexão recusada/quebrada, HTTP 5xx, código explícito de modelo não encontrado/disponível/carregado.

Não permitido: configuração ausente, 401/403, 429, 404 genérico, requests inválidos, redirects, resposta JSON inválida/vazia, recusa ou resposta local que possa desagradar. Com `ALLOW_CLOUD_FALLBACK=false`, o Groq não recebe requisições, nem health checks.

## Resultados

- **61 testes passaram**: 21 de fundação e 40 novos casos de providers, fallback, privacidade, health, validação, auditoria, correlação e API autenticada. Ruff passou.
- Alembic `check`: nenhum desvio entre ORM e migrations.
- Health real: local e Groq configurados/saudáveis a partir do container do Core.
- Inferência local: `llama_cpp`, fallback false, resposta “conexão confirmada.”, cerca de **2709 ms**.
- Fallback real: a URL local foi substituída por uma porta loopback fechada somente em um container temporário de diagnóstico; `groq` respondeu “conexão confirmada”, fallback true, cerca de **428 ms**. O servidor llama.cpp não foi interrompido nem alterado.
- Flag false: diagnóstico com falha local retornou `connection_error`, sem tentativa cloud registrada. Testes também verificam zero chamadas ao transporte cloud nessa configuração.
- Requests do fallback compartilham request ID; cada tentativa tem timestamp/latência/código de erro. Os registros de auditoria anteriores à migration foram preservados.
- HTTPS público `/health/ready` retorna schema `0002_llm_requests`; `/llm/health` sem JWT retorna 401.
- PostgreSQL de testes foi parado ao concluir. Não houve alterações no template, workers ou configuração do libvirt.

## Como testar

```sh
curl https://agent.vegasolucoes.com.br/health/ready
```

Na VM:

```sh
cd /srv/devlima-agent
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.llm.cli health
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.llm.cli smoke
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm tests
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test
```

`smoke` faz inferência de uma frase de teste, com auditoria. Não imprimir `.env` ou variáveis completas dos containers. Os modelos/flag/timeout são alterados por configuração administrativa; o cliente da API não pode forçar provider Groq.

## Próxima fase

Fase 3: conversations/messages, histórico bruto preservado, Context Builder limitado, summaries, memories/candidates e protocolo JSON de ações. O endpoint atual não promete memória entre chamadas. Tarefas/scheduler, workers e Android permanecem nas fases posteriores.

Referências de protocolo: [llama.cpp server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md), [compatibilidade Groq](https://console.groq.com/docs/openai), [modelos Groq](https://console.groq.com/docs/models).
