# Operação da V1

VPS Ubuntu: `/srv/devlima-agent`. Use sempre `--env-file .env`: o Compose está em `infra/`, e executar sem esse argumento não encontra automaticamente a configuração da raiz. Comandos abaixo partem da raiz do projeto; `sudo` é necessário no host atual para Docker.

## Instalação nova

Pré-requisitos: Docker/Compose e Python 3.12. Domínio com DNS e ingresso 80/443. Configuração criada em modo privado; configure as URLs/modelos e a credencial Groq no `.env` protegido por editor, sem copiar seu conteúdo para logs.

```sh
python3 scripts/init_env.py --domain agent.vegasolucoes.com.br
sudo docker compose --env-file .env -f infra/docker-compose.yml build backend db-admin
sudo docker compose --env-file .env -f infra/docker-compose.yml up -d --wait postgres
python3 scripts/provision_database_roles.py
sudo docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate
python3 scripts/provision_database_roles.py
sudo docker compose --env-file .env -f infra/docker-compose.yml up -d --wait backend scheduler caddy
```

A segunda aplicação dos grants retira escrita da tabela Alembic após a primeira migration. Para workers, primeiro inspecione KVM/libvirt/rede/pool/template e provisione a chave privada no host conforme [VM Manager](../vm-manager/README.md); depois instale o manager e inicie o runner. Não recrie automaticamente redes/pools de um host existente.

## Acesso e usuários

Não há cadastro público nem senha padrão. Nesta implantação, o usuário `devlima` foi criado com senha aleatória entregue em arquivo privado separado. A CLI administrativa não expõe a senha nos argumentos:

```sh
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile ops run --rm db-admin python -m app.cli create-user outro_usuario
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile ops run --rm db-admin python -m app.cli reset-password devlima
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile ops run --rm db-admin python -m app.cli list-users
```

Reset invalida tokens anteriores. Login e refresh compartilham limite de cinco tentativas por IP em quinze minutos, inclusive sucessos. Android usa refresh rotativo com duração máxima da família de 30 dias; ao expirar/revogar, entre novamente. Em Conta, conectar inicia a conexão persistente; desconectar encerra o serviço; sair revoga a sessão e remove os dados locais desse login.

## Saúde e diagnóstico

```sh
curl --fail https://agent.vegasolucoes.com.br/health/ready
sudo docker compose --env-file .env -f infra/docker-compose.yml ps
sudo docker compose --env-file .env -f infra/docker-compose.yml logs --tail 100 backend scheduler worker-runner
sudo docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate alembic current
sudo docker compose --env-file .env -f infra/docker-compose.yml run --rm migrate alembic check
sudo systemctl status devlima-vm-manager devlima-backup.timer
sudo journalctl -u devlima-vm-manager -n 100 --no-pager
```

Logs e arquivos devem permanecer privados. Não executar `docker compose config` sem `--quiet`, listar todos os env vars nem imprimir `.env`. `health/ready` verifica banco/schema; não garante disponibilidade do provider. Para diagnosticar LLM sem token no shell:

```sh
sudo docker compose --env-file .env -f infra/docker-compose.yml exec backend python -m app.llm.cli health
```

O projeto publica somente HTTP/HTTPS. Core 8000, PostgreSQL 5432 e Caddy admin 2019 não têm publicação de porta. Manager usa socket; SDK/emulador/ADB usam loopback. SSH/rpcbind/Tailscale já existentes no host foram preservados. Acesso OCI continua administrado pelo proprietário; não há credencial OCI neste projeto.

## Atualização e rollback

1. Faça backup cifrado e valide restore conforme [RECOVERY.md](RECOVERY.md). Registre o commit atual e preserve a identidade de assinatura Android.
2. Atualize o checkout para o commit aprovado em `main`, preservando `.env` e arquivos privados. Na sessão de desenvolvimento, a VPS recebe um bundle Git do Mac; credencial GitHub não é copiada para o servidor.
3. Construa backend/tests, rode testes isolados, execute `migrate`, reaplique os grants e execute `alembic check`.
4. Recrie backend/scheduler/runner, verifique saúde e HTTPS. Atualize o manager apenas quando não houver operações/VMs dependendo do processo anterior.
5. Compile o Android na VPS e verifique assinatura/checksum antes da distribuição.

Rollback de código é possível se o schema continuar compatível. Não execute downgrade automaticamente sobre dados de produção. Para alteração incompatível, recupere o backup em ambiente novo/isolado, verifique dados e só então planeje a troca. Nunca usar `down -v` no servidor.

## Recuperação de mensagens e chamadas

Outbox/eventos/ACKs são persistidos no PostgreSQL. O app persiste antes de ACK, deduplica por UUID e reenvia mensagens pendentes com o mesmo client_message_id. Resposta concluída é recuperada sem segunda inferência. Uma queda pode exigir reconexão; após force stop, abrir o app e conectar explicitamente.

Chamadas recebidas vencem após dois minutos da emissão; sessão ativa vence por inatividade de dez minutos ou duração máxima de trinta minutos. Após uma interrupção, consulte a sessão e ative áudio com o app visível. Jobs de worker com resultado incerto não são repetidos automaticamente; consulte estado/erro e envie uma nova operação explícita somente após verificar o ambiente.
