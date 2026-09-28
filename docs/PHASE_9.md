# Fase 9 — hardening, recuperação e entrega V1

Validação em 2026-09-28. Backend e Android **1.0.0**, schema **0007_calls**. Desenvolvimento, build e emulador Android executados na VPS `147.15.33.140`; publicação em `main` no repositório privado.

## Alterações

PostgreSQL possui três identidades separadas. `agent_migrate` é proprietária do schema/tabelas, sem superuser, criação de bancos/roles, replicação ou bypass RLS. `agent_runtime` possui CRUD dos dados e leitura da revisão Alembic, sem DDL/TRUNCATE ou escrita na revisão. O administrador original fica no PostgreSQL e na ferramenta isolada `db-admin`. Backend, scheduler e runner recebem apenas a senha runtime; somente o backend recebe JWT real/Groq, e somente o runner recebe o token/socket do manager.

`scripts/provision_database_roles.py` provisiona e reaplica os grants sem exibir senhas. As configurações geram senhas distintas, privadas e sem sobrescrever `.env`. Uvicorn usa `websockets-sansio`, limite de frame e concorrência. O manager continua privado em Unix socket; backend sem acesso a Docker/libvirt, chaves ou hypervisor.

Backups usam dump PostgreSQL, cópia consistente do SQLite do manager, configurações, chave SSH dos workers e identidade de assinatura Android. O envelope é AES-256-GCM autenticado, processado em blocos, com chave externa de 32 bytes e arquivos 0600. O backup final inclui o template Ubuntu original. Dumps, chaves e conteúdo de backups ficam fora do Git. [Recuperação](RECOVERY.md) descreve cobertura e limites.

Timer da VPS faz backup diário às 03:30 UTC, com atraso aleatório de até cinco minutos e retenção de 14 arquivos. Um LaunchAgent no Mac copia os arquivos cifrados por SSH à 01:00 local. A cópia externa já foi executada; sua continuidade depende de o Mac estar ligado e alcançar a VPS. Não há serviço de storage cloud contratado/configurado.

APK release assinado com RSA 4096, assinatura v2 válida para min SDK 26, package `br.com.vegasolucoes.agent`, versionCode 100. A chave e as senhas permanecem fora do repositório e são incluídas apenas no backup cifrado. APK distribuído como asset da release privada `v1.0.0`.

## Evidências

| Verificação | Resultado observado |
| --- | --- |
| Backend PostgreSQL isolado | 143 testes passaram; Ruff aprovado |
| Manager | 11 testes unitários; ciclo real READY/job/snapshot/restore/stop/start/reset/destroy aprovado |
| Isolamento do worker | HTTP 000 ao tentar metadata OCI com cabeçalho de autenticação, Core público e Core Tailscale; checksum do template intacto |
| Core → runner → manager | Dois ciclos consecutivos de criação/remoção; teste adicional confirmou READY no PostgreSQL, job real com exit_code 0/output esperado e remoção do worker |
| Permissões PostgreSQL runtime | CREATE, ALTER e TRUNCATE rejeitados com SQLSTATE 42501; CRUD permitido; revisão somente leitura |
| Schema/deploy | Alembic sem drift; backend/scheduler/runner/PostgreSQL saudáveis; HTTPS público válido |
| Backup/configuração | Cinco testes host passaram: roundtrip, adulteração/chave incorreta, permissões e geração de secrets |
| Restore | Arquivo autenticado e dump restaurado em banco temporário exclusivo; revisão 0007_calls e contagens conferidas; banco temporário removido |
| Android release | assembleRelease, três testes unitários, lint sem erros, assinatura verificada, instalação e abertura de login no emulador API 36 |
| Android instrumentado básico | Três testes passaram: armazenamento seguro, fila/replay e identidade/cancelamento de transcrição |
| E2E real temporizado | Um teste passou em 310,668 s: café 5 min, chamada 2 min, atendimento, transcrição por texto/resposta, mute/speaker/end, tarefas e edição/cancelamento de lembrete |
| Entrega/contexto real | Três respostas Groq via fallback técnico, seis mensagens persistidas, dez eventos com ACK e uma chamada ENDED |
| Reinício app/servidor | Login/cache preservados após force stop e restart do backend; reabertura e conexão iniciada na interface aprovadas |
| Motores de voz | Emulador informou SpeechRecognizer disponível, TTS inicializado e idioma pt-BR disponível |

O E2E usa conta sintética separada, credencial externa privada e histórico próprio. Ao terminar, essa conta foi desativada, dispositivos/famílias revogados e senha temporária removida. O usuário operacional `devlima` está ativo; login/identidade/logout foram verificados por HTTPS, sem imprimir a senha. O arquivo privado de acesso não entra no Git.

Logs detalhados permanecem privados em `/srv/devlima-build-tools/phase9-e2e.log`, `phase9-worker-smoke.log` e `final-android-build.log`. O workflow versionado configura testes de backend/manager/backup em push/PR e execução manual; builds Android permanecem na VPS.

`/srv/devlima-build-tools/core-ready-smoke.log` registra Core READY/job/removal. O verificador [smoke_core_worker_ready.py](../scripts/smoke_core_worker_ready.py) exige o banco isolado, aguarda prontidão real e remove exclusivamente o worker criado por ele. Na VPS:

```sh
sudo docker compose --env-file .env -f infra/docker-compose.yml --profile test --profile smoke run --rm -T worker-smoke python - < scripts/smoke_core_worker_ready.py
```

**CI GitHub pendente:** o workflow passou na validação `actionlint` 1.7.12, mas o GitHub retornou `startup_failure` antes de criar qualquer job, tanto em push quanto no dispatch manual. A API não disponibilizou logs/check-runs com o motivo. [Execução manual](https://github.com/LimaVM/DEVLIMA-AGENTS/actions/runs/36426645682). Nenhum sucesso de CI hospedada é declarado; os resultados da tabela foram executados na VPS. A mensagem detalhada da interface autenticada do GitHub precisa ser examinada para resolver esse bloqueio.

Actions está habilitado, ações permitidas, workflow ativo no default branch e dispatch aceito pela API. Há [relato público de desenvolvedor com a mesma assinatura BuildFailed/zero jobs](https://github.com/orgs/community/discussions/208832). A correspondência sugere problema de inicialização/registro no serviço GitHub; é uma inferência, sem confirmação do suporte para este repositório. Nenhum ticket/mensagem foi enviado em nome do proprietário.

Capturas reais do emulador: [login da release](images/android-release-login.png) e [aviso de café com conversa sintética](images/android-e2e-coffee.png).

## Artefato

- APK SHA-256: `8061b34766151dfe903e354758b7072b78c875534ab46bce3a05fabf08db5beb`.
- Certificado SHA-256: `b68c5786bdc1088ae635b5611c57beaf9add894269408d5298cf58765bf4348e`.
- Tamanho: 8.545.724 bytes. Android 8.0/API 26 ou superior; target API 36.

## Limites e próxima validação

O llm-server local pode permanecer desligado; falha de conexão/timeout habilita Groq conforme a política já autorizada. A espera da tentativa local continua visível na latência. Com fallback desativado, o serviço não envia contexto à nuvem.

Áudio físico não foi validado: não houve conversa capturada de microfone real nem avaliação de volume/qualidade do alto-falante/auricular. Disponibilidade de engines e controles no emulador não substituem esses testes. Também faltam alternância Wi-Fi/rede móvel e comportamento de bateria/Doze em aparelho real. O checklist está em [android/README.md](../android/README.md).

As fases 0–9 de desenvolvimento, implantação e documentação estão implementadas. A homologação física permanece uma etapa explícita antes de declarar o aplicativo validado no telefone do proprietário.
