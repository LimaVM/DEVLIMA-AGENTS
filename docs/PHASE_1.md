# Fase 1 — validação

Concluída em **2026-09-28**, validada no host real e por conexão externa ao domínio.

## Entrega

FastAPI com endpoints live/ready, configuração validada, SQLAlchemy 2, migrations Alembic, tabelas users/audit_log/login_throttles, login JWT, Argon2id, CLI administrativa e limitação persistente/atômica de tentativas. PostgreSQL persistente, Caddy e containers sem acesso do Core ao host.

## Implantação

- Diretório: `/srv/devlima-agent`; fonte local no workspace DEVLIMA-AGENTS.
- Docker 29.8.1; Compose 5.5.1; PostgreSQL 17.11; Caddy 2.11.4.
- Python 3.12, FastAPI 0.141.1, SQLAlchemy 2.0.54, Pydantic 2.13.5, Alembic 1.20.0.
- Backend e PostgreSQL saudáveis; Caddy ativo; migration runner termina com exit 0, comportamento esperado.
- Domínio informado: **https://agent.vegasolucoes.com.br**. Certificado Let’s Encrypt, expiração observada `2026-12-27 04:57:02 UTC`, renovação automática pelo Caddy.
- Banco sem porta publicada; backend sem porta publicada, filesystem read-only, usuário 10001, sem mounts do host e `Privileged=false`.
- `.env` somente no host, 0600, com secrets aleatórios. Nenhum usuário de produção criado automaticamente.
- Arquivos existentes de KVM/libvirt/template/chaves não foram alterados. Backups de inspeção em `/srv/devlima-agent/host-inspection` (não versionados).

## Testes e resultados

1. **21 testes passaram** em PostgreSQL separado/efêmero, sem tocar dados de produção: saúde/schema, UUID de request, docs privadas, erro DB sem secrets, políticas de secrets/senha/timezone, Argon2id, login/auditoria, erros indistinguíveis, autorização, validação sem eco de secrets, assinatura/audience/expiração JWT, revogação de tokens, usuário inativo, rate limit persistente, janela expirada, concorrência de 10 tentativas e CLI create/list/reset.
2. **Ruff passou**. Dependências e imagens fixadas após instalação real. A versão atual do Starlette requer `httpx2` para TestClient; a dependência foi ajustada e a suíte executada novamente com warnings tratados como erro.
3. **Alembic current/check:** `0001_identity (head)`; nenhum desvio entre ORM e migrations.
4. **Persistência:** um marcador de auditoria foi salvo, backend/PostgreSQL reiniciados e o container PostgreSQL recriado mantendo o volume; o marcador permaneceu. Não houve reboot do host.
5. **HTTP externo:** 308 para HTTPS. **HTTPS externo:** `/health/ready` retorna 200 e `{"status":"ready","database":"ok","schema":"0001_identity"}` com certificado verificado. `/auth/me` sem token retorna 401.
6. Portas 5432/8000/2019 sem conexão TCP externa. Só 80/443 são publicados pelo projeto.
7. Template SHA-256 igual ao registrado na Fase 0; XML da rede default idêntico, configuração do pool preservada e todas as regras Oracle/libvirt originais ainda presentes. Chaves dos workers com modos/tamanhos/donos originais.

PostgreSQL de testes foi parado após validação. Não há worker em execução ou alterações em VMs existentes.

## Como testar e criar acesso

```sh
curl https://agent.vegasolucoes.com.br/health/ready
```

Na VM, defina seu usuário/senha sem registrar credenciais em argumentos:

```sh
cd /srv/devlima-agent
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.cli create-user devlima
```

Os comandos completos de testes, migrations e reset de senha estão no [README](../README.md).

## Pendências intencionais

Não há usuário de produção padrão. O proprietário deverá criar sua senha via CLI. Chat/LLM, memória, tarefas, lembretes, scheduler, workers e Android chegam nas fases seguintes.

Fase 2 requer URL/modelo do llama.cpp pela rede privada e, para ativar fallback, chave/modelo Groq em `.env`. Nenhuma credencial deve ser enviada ao Git.

Backup externo/restauração, separação de roles DB e hardening completo ficam na Fase 9. A disponibilidade após restart/recreate dos containers foi testada; recuperação após reboot físico não foi testada para preservar o host durante esta entrega.
