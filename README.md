# DEVLIMA AGENT

Agente pessoal com Core operacional próprio, PostgreSQL como fonte da verdade, inferência llama.cpp privada e fallback Groq configurável. Desenvolvimento por fases conforme TODO.md.

**V1 — backend 1.0.1 / Android 1.0.2, fases 0–9 implementadas:** FastAPI/PostgreSQL, JWT/Argon2id, contexto/memória, tarefas/lembretes/chamadas agendadas, scheduler/outbox, workers Linux e Android com chat, rotina, WSS, chamadas internas e SpeechRecognizer/TTS. Roles de banco separadas, backup cifrado externo e restore verificado. Backend: 143 testes. E2E de café/chamada aprovado no emulador e em Xiaomi Android 16; rede móvel e lembrete com tela bloqueada verificados. Qualidade auditiva e bateria/Doze ainda exigem avaliação complementar.

Servidor: [agent.vegasolucoes.com.br](https://agent.vegasolucoes.com.br/health/ready). [APK assinado e checksum](https://github.com/LimaVM/DEVLIMA-AGENTS/releases/tag/v1.0.2), acesso restrito ao repositório privado. Android 8.0 ou superior. Credenciais são entregues separadamente, sem senha padrão.

## Documentação

- [Estado real e plano inicial](CURRENT_STATE.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Segurança](docs/SECURITY.md)
- [Fases](TODO.md)
- [Roteiro detalhado das próximas fases](docs/ROADMAP.md)
- [Validação da entrega](docs/PHASE_1.md)
- [Router LLM e validação real](docs/PHASE_2.md)
- [Contexto e memória](CONTEXT.md)
- [Validação da Fase 3](docs/PHASE_3.md)
- [Tarefas e scheduler](docs/PHASE_4.md)
- [Workers Linux e recuperação](docs/PHASE_5.md)
- [Conexão Android e sessões](docs/PHASE_6.md)
- [Chat e rotina Android](docs/PHASE_7.md)
- [Chamadas e voz](docs/PHASE_8.md)
- [Validação final V1](docs/PHASE_9.md)
- [Auditoria de aceitação](docs/ACCEPTANCE.md)
- [Operação e atualização](docs/OPERATIONS.md)
- [Backup e recuperação](docs/RECOVERY.md)
- [Changelog](CHANGELOG.md)
- [Protocolo WebSocket](docs/WEBSOCKET.md)
- [Build Android na VPS](android/README.md)
- [Validação em celular físico](docs/ANDROID_PHYSICAL.md)
- [Operação do VM Manager](vm-manager/README.md)

## Repositório e instalação

Repositório privado: [LimaVM/DEVLIMA-AGENTS](https://github.com/LimaVM/DEVLIMA-AGENTS), branch principal `main`. O histórico inclui as entregas por fase. É necessário acesso à conta/repositório para clonar:

```sh
git clone https://github.com/LimaVM/DEVLIMA-AGENTS.git
cd DEVLIMA-AGENTS
```

O clone contém código, migrations, configuração de exemplo, testes e documentação. `.env`, chaves SSH, credenciais, dados PostgreSQL, backups e imagens QCOW2 não são distribuídos; a chave SSH citada nos comandos de operação é provisionada separadamente.

## Executar

Requer Docker Engine/Compose e Python 3 para gerar configuração. Na VM o projeto fica em `/srv/devlima-agent`; use `sudo docker` se o usuário não estiver no grupo Docker.

```sh
python3 scripts/init_env.py
sudo docker compose --env-file .env -f infra/docker-compose.yml build backend db-admin
sudo docker compose --env-file .env -f infra/docker-compose.yml up -d --wait postgres
python3 scripts/provision_database_roles.py
sudo docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate
python3 scripts/provision_database_roles.py
sudo docker compose --env-file .env -f infra/docker-compose.yml up -d --wait backend scheduler caddy
```

Para habilitar workers no host KVM inspecionado, instale o [VM Manager](vm-manager/README.md) e depois execute `docker compose --env-file .env -f infra/docker-compose.yml up -d --wait worker-runner`.

Isso gera secrets sem imprimi-los e sobe acesso privado `https://localhost:8443`. O script recusa sobrescrever `.env`. Para uma implantação nova com domínio/DNS já configurado:

```sh
python3 scripts/init_env.py --domain agent.vegasolucoes.com.br
# Em seguida execute a sequência build → PostgreSQL → roles → migration → grants → serviços acima.
```

O modo domínio publica 80/443 para ACME/HTTPS. Verificar ingresso OCI e DNS; nenhuma credencial OCI é necessária para executar o Compose. `.env`, chaves e dados nunca entram no Git.

## Acesso privado

```sh
ssh -i DEVLIMA-AGENTS.key -L 8443:127.0.0.1:8443 ubuntu@147.15.33.140
```

Obtenha a CA pública do Caddy, sem copiar a chave privada:

```sh
docker compose --env-file .env -f infra/docker-compose.yml cp caddy:/data/caddy/pki/authorities/local/root.crt /tmp/devlima-agent-ca.crt
curl --cacert /tmp/devlima-agent-ca.crt https://localhost:8443/health/ready
```

Em produção com domínio use validação TLS normal:

```sh
curl https://agent.vegasolucoes.com.br/health/ready
```

## Usuários e API

Não há usuário ou senha padrão. Crie seu usuário na VM; a CLI pede a senha sem eco:

```sh
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile ops run --rm db-admin python -m app.cli create-user devlima
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile ops run --rm db-admin python -m app.cli list-users
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile ops run --rm db-admin python -m app.cli reset-password devlima
```

`POST /auth/login` recebe JSON `username` e `password`, retorna JWT com duração de 30 minutos. `GET /auth/me` exige `Authorization: Bearer <token>`. Reset de senha invalida tokens antigos. Cinco tentativas por IP/janela de 15 minutos, inclusive logins bem-sucedidos, limitam tentativas e custo de hashing. Não colocar senhas/tokens em argumentos do shell ou arquivos versionados.

Endpoints públicos: `GET /health/live` e `/health/ready`. Documentação interativa desativada por padrão; para desenvolvimento privado use `ENABLE_API_DOCS=true`. Timestamps UTC e timezone por usuário.

## LLM privada e fallback

O deployment usa `http://100.102.91.22:8080/v1` pelo Tailscale; modelo Gemma 4 12B detectado no servidor. Groq usa `openai/gpt-oss-120b`, selecionado da lista disponível. Credencial somente no `.env` 0600 da VM, nunca no código ou em logs.

`GET /llm/health` e `POST /llm/chat` exigem JWT. O chat recebe `messages` (role/content) e `max_tokens`, e retorna `reply`, provider, modelo, latência, `fallback_used` e request ID. É um endpoint de diagnóstico de providers, sem histórico/contexto persistente; não executa ações da LLM.

Na VM, os diagnósticos administrativos dispensam expor tokens:

```sh
cd /srv/devlima-agent
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.llm.cli health
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.llm.cli smoke
```

O comando smoke envia apenas uma frase de teste. Cada tentativa de inferência é auditada no PostgreSQL sem armazenar prompt/resposta nesses registros. O chat persistente utiliza suas próprias tabelas de mensagens.

Fallback acontece só com timeout, erro de conexão, HTTP 5xx ou código explícito de modelo indisponível. Não ocorre com 401/403/429, 404 genérico, payload inválido ou preferência sobre uma resposta local. Com `ALLOW_CLOUD_FALLBACK=false`, nenhuma chamada ao Groq é feita, inclusive em health checks.

Para desativar fallback, edite a flag no `.env` da VM e recrie o backend com `docker compose --env-file .env -f infra/docker-compose.yml up -d backend`. Não imprimir `.env`, executar Compose `config` sem `--quiet` ou inspecionar todos os env vars do container em logs compartilhados.

## Chat persistente e memórias

Com JWT, `POST /chat/messages` recebe:

```json
{
  "client_message_id": "03fd4bb1-9cd8-42c3-bc20-6f3b29f844b5",
  "content": "Lembre que eu prefiro respostas curtas."
}
```

Omitir `conversation_id` inicia uma conversa. Nas mensagens seguintes, envie o UUID retornado em `conversation_id` e um novo `client_message_id`. Reenvios da mesma mensagem devem reutilizar o UUID para evitar duplicatas. A resposta inclui texto humano `reply`, IDs, provider/fallback, latência, resultados das propostas e estatísticas do contexto.

`GET /chat/conversations` lista conversas; `POST` cria uma conversa vazia com `title`. `GET /chat/conversations/{id}/messages?after_sequence=0&limit=100` consulta o histórico paginado; `/summaries` consulta resumos. `POST /chat/conversations/{id}/archive` arquiva preservando o histórico.

`GET /memories` lista memórias ativas; `POST /memories` recebe `content` e `category` (`fact` ou `preference`) para salvar explicitamente; `DELETE /memories/{id}` desativa. `GET /memories/candidates` lista propostas pendentes. `POST /memories/candidates/{id}/accept` confirma; `/reject` recusa.

Somente pedidos explícitos com proposta literal e confiança suficiente são aceitos automaticamente. Outras propostas esperam confirmação. O sistema executa tarefas/agendamentos e operações validadas de workers; entrega ao Android usa WSS e ACK durável. Limites, recuperação e política completa em [CONTEXT.md](CONTEXT.md).

## Tarefas e agendamento

Com JWT: `POST/GET /tasks`, `PATCH /tasks/{id}`, `POST /tasks/{id}/complete`; `POST/GET /reminders`, `PATCH/DELETE /reminders/{id}`; `POST/GET /scheduled-calls` e `DELETE /scheduled-calls/{id}`. Filtros `date`, `status`, `limit` e `offset` nas listagens. Consulte [Fase 4](docs/PHASE_4.md) para política de recorrência e recuperação.

O serviço Compose `scheduler` consulta eventos duráveis e gera avisos na outbox, entregues por dispositivo via WSS. Pedidos em linguagem natural podem criar/alterar/concluir tarefas e criar/cancelar agendamentos, respeitando propriedade e schemas.

## Testar

Os testes usam um PostgreSQL separado e efêmero; não truncam o banco de produção.

```sh
docker compose --env-file .env -f infra/docker-compose.yml --profile test build tests
docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm tests
docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm --no-deps tests ruff check --no-cache .
docker compose --env-file .env -f infra/docker-compose.yml --profile test --profile smoke run --rm context-smoke
docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test
```

Migrations:

```sh
docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate alembic current
docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate alembic check
```

`context-smoke` usa o banco de teste e a LLM local real com cloud desligado, gerando somente conversas sintéticas. Requer URL/modelo local configurados e pode demorar conforme o hardware do llm-server.

Volume `postgres_data` mantém dados após restart/recreate. Nunca usar `down -v` no servidor. Consulte [RECOVERY.md](docs/RECOVERY.md) para cobertura do backup, restore isolado e recuperação do host.
