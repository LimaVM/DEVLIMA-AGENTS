# Fase 5 — workers Linux e API privada do hypervisor

Implementação em 2026-09-28: models/migration `0005_workers`, fila PostgreSQL com leases, runner separado, API JWT por proprietário, ações do agente e contexto dos workers/snapshots. O Core retorna operação solicitada/PENDING; READY vem da verificação real do manager. O backend HTTP continua sem acesso a libvirt, Docker ou chaves privadas.

O VM Manager roda em systemd no host e escuta apenas Unix socket protegido por grupo/token. Provider Linux usa overlays do template verificado, cloud-init individual e guest-agent; Provider Windows permanece reservado com 501. Quotas, reservas do host, metadados XML, UUIDs e paths protegem domínios/storage externos. Filtro de rede próprio bloqueia novas conexões de workers para infraestrutura privada e metadata, preservando a rede default e os filtros existentes. Detalhes em [vm-manager/README.md](../vm-manager/README.md).

## API do Core

- `POST /workers` recebe `request_id` UUID, `name?`, `vcpu?`, `ram_mb?`, `disk_gb?` e responde 202 com command_id/worker_id/status.
- `GET /workers`, `GET /workers/{id}`, `/workers/{id}/commands` e `/workers/{id}/snapshots` consultam somente registros do usuário autenticado.
- `POST /workers/{id}/commands` recebe `request_id`, `kind` e argumentos específicos. Tipos: START, STOP, DESTROY, RESET, SNAPSHOT, RESTORE, EXECUTE. RESTORE exige snapshot_id; EXECUTE exige script e aceita timeout até 300s.
- Repetir request_id com o mesmo payload retorna a operação existente. Alterar payload retorna conflito; IDs de outros proprietários retornam 404. Comandos simultâneos do mesmo worker são recusados.

Pedidos pela conversa usam os mesmos handlers e autorização. Scripts são permitidos exclusivamente no worker, pela ação enumerada `run_worker_job`; não existe shell no host. Resultados de jobs ficam nos registros privados da operação, com saída limitada; auditoria registra apenas metadados.

## Recuperação

A fila faz commit antes de acessar o manager. Após timeout/crash, consulta o request_id antes de tentar enviar algo. Um resultado concluído é recuperado sem nova execução; RUNNING espera; uma operação incerta que não pode ser provada fica FAILED/operation_recovery_required. O usuário pode emitir um novo pedido explícito. O manager não repete scripts após um crash.

Snapshot/restore desligam o worker antes de copiar o disco e religam somente quando ele estava ligado. Snapshots são independentes, verificados por checksum, até cinco por worker. Reset recria overlay e cloud-init, preservando snapshots; destroy remove apenas o diretório/domain registrados. Workers não têm autostart após reboot; o Core reconcilia STOPPED e START revalida recursos.

## Validação

- Backend: 126 testes passaram, incluindo isolamento de usuários, replay, leases e recuperação sem repetir efeitos.
- Manager: 11 testes independentes com provider fake cobrem autenticação, quotas, conflito de payload, recuperação conservadora, snapshots, proteção de paths e domínios estrangeiros.
- Produção migrou para `0005_workers`; backend, scheduler e worker-runner saudáveis. Alembic check não detectou divergências. Acesso ao socket testado de dentro do runner UID/GID 10001.
- Backup anterior: `/srv/devlima-agent/backups/phase4-before-0005.dump`, modo 0600.
- O primeiro smoke real confirmou READY/SSH/guest-agent, job e bloqueio de rede. Snapshot encontrou OOM com limite de 512 MiB do manager. A falha foi reconciliada, sem repetir a operação; apenas o worker de teste foi apagado. A conversão passou a usar uma coroutine e cache direto, com MemoryHigh 512 MiB e MemoryMax 1536 MiB no serviço.

O segundo ciclo real passou: CREATE → READY → EXECUTE → isolamento de rede → SNAPSHOT → alteração do arquivo → RESTORE → conteúdo original → STOP/START → RESET → arquivo ausente → DESTROY. O worker foi removido, o template manteve o SHA-256 original e o manager não reiniciou durante o ciclo; pico de memória observado de aproximadamente 514 MiB. A integração real da fila também passou: o container UID/GID 10001 registrou CREATE no banco de teste, executou pelo Unix socket e registrou DESTROY, sem repetir operações concluídas. Ambos os workers dos smokes foram removidos.

## Preparação Android

Atendendo à preferência do proprietário, desenvolvimento/build/emulador Android ficam na VPS. Java 17, Gradle 8.13, SDK/API 36, build-tools 36.0.0 e imagem x86_64 Google APIs instalados fora do checkout. `scripts/bootstrap_android.py` verifica os arquivos oficiais por checksum. SDK ocupa cerca de 5,6 GiB. Gradle/emulador terão limites de recursos; nenhuma build Android depende do llm-server local.

Próxima etapa: Fase 6, protocolo WebSocket autenticado, confirmações por dispositivo, conexão Android e Foreground Service.
