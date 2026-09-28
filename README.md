# DEVLIMA AGENT

Agente pessoal com Core operacional próprio, PostgreSQL como fonte da verdade, inferência llama.cpp privada e fallback Groq configurável. Desenvolvimento por fases conforme TODO.md.

**Fase 1:** FastAPI, PostgreSQL, migrations, JWT/Argon2id, limitação de login, auditoria, CLI e Caddy. Chat/LLM, tarefas, scheduler, VM Manager e Android ainda não estão implementados.

## Documentação

- [Estado real e plano inicial](CURRENT_STATE.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Segurança](docs/SECURITY.md)
- [Fases](TODO.md)
- [Validação da entrega](docs/PHASE_1.md)

## Executar

Requer Docker Engine/Compose e Python 3 para gerar configuração. Na VM o projeto fica em `/srv/devlima-agent`; use `sudo docker` se o usuário não estiver no grupo Docker.

```sh
python3 scripts/init_env.py
docker compose --env-file .env -f infra/docker-compose.yml up -d --build --wait
```

Isso gera secrets sem imprimi-los e sobe acesso privado `https://localhost:8443`. O script recusa sobrescrever `.env`. Para uma implantação nova com domínio/DNS já configurado:

```sh
python3 scripts/init_env.py --domain agent.vegasolucoes.com.br
docker compose --env-file .env -f infra/docker-compose.yml up -d --build --wait
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
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.cli create-user devlima
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.cli list-users
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.cli reset-password devlima
```

`POST /auth/login` recebe JSON `username` e `password`, retorna JWT com duração de 30 minutos. `GET /auth/me` exige `Authorization: Bearer <token>`. Reset de senha invalida tokens antigos. Cinco tentativas por IP/janela de 15 minutos, inclusive logins bem-sucedidos, limitam tentativas e custo de hashing. Não colocar senhas/tokens em argumentos do shell ou arquivos versionados.

Endpoints públicos: `GET /health/live` e `/health/ready`. Documentação interativa desativada por padrão; para desenvolvimento privado use `ENABLE_API_DOCS=true`. Timestamps UTC e timezone por usuário.

## Testar

Os testes usam um PostgreSQL separado e efêmero; não truncam o banco de produção.

```sh
docker compose --env-file .env -f infra/docker-compose.yml --profile test build tests
docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm tests
docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm --no-deps tests ruff check --no-cache .
docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test
```

Migrations:

```sh
docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate alembic current
docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate alembic check
```

Volume `postgres_data` mantém dados após restart/recreate. Nunca usar `down -v` no servidor. Backup/restore completo, scheduler e recuperação de eventos serão implementados nas fases indicadas.
