# Estado real do host — Fase 0

Inspeção por SSH em **2026-09-28, 05:42 UTC** (02:42 America/Sao_Paulo), antes de instalar serviços do projeto.

## Acesso e sistema

- Host: `147.15.33.140`, hostname `devlima-agents`, usuário `ubuntu` (sudo disponível).
- Ubuntu **24.04.5 LTS**, kernel `6.17.0-1020-oracle`, arquitetura x86_64.
- Python 3.12.3; Git e curl presentes. Docker, Compose, PostgreSQL, Caddy e Tailscale ausentes.
- 6 vCPUs AMD EPYC, 32.088 MiB de RAM total, 31.180 MiB disponíveis na inspeção; sem swap.
- Disco raiz ext4: cerca de 290 GiB, 286 GiB disponíveis.
- Workspace local originalmente continha apenas a chave SSH `DEVLIMA-AGENTS.key`, sem Git ou código. Sua permissão foi corrigida de 0644 para 0600; seu conteúdo não foi registrado.

## Virtualização existente

- `/dev/kvm` presente; `kvm-ok`: **KVM acceleration can be used**.
- libvirtd ativo; libvirt 10.0.0; QEMU 8.2.2.
- `virsh -c qemu:///system list --all`: **nenhuma VM registrada**, inclusive desligada. Não presumir que a VM de teste mencionada no escopo ainda exista.
- Pool `default`: ativo, persistente, autostart, destino `/var/lib/libvirt/images`.
- Rede `default`: ativa, persistente, autostart, NAT, bridge `virbr0`, gateway `192.168.122.1/24`; DHCP `.2` a `.254`.
- IP forwarding já ativo. As regras de NAT e encaminhamento do libvirt existem.
- Permanecem arquivos `cloud-init/linux-worker-01/user-data` e `meta-data`; não foram alterados.

## Template e credenciais dos workers

- Template: `/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2`.
- Formato QCOW2, sem backing file; tamanho virtual 3,5 GiB, arquivo 625.612.288 bytes (~597 MiB).
- SHA-256: `6a81c37564db9b1ee84e141922625e1d7c5b389b99bb3c572e0243607d5bb4d2`.
- Dono `libvirt-qemu:kvm`, modo 0644. Não está protegido por imutabilidade no filesystem; o VM Manager deverá impedir escritas e só trabalhar com overlays. Nenhum chmod/chown foi feito nesse arquivo.
- `/root/.ssh/agent_worker`: root:root, 0600, 411 bytes; chave pública 0644, 101 bytes.
- Fingerprint público ED25519: `SHA256:3blJjDc7Gbyl721p5DSnHlIIjrXRKfW5r/OJnpJtJQo`.
- Conteúdo da chave privada não foi lido nem copiado.

## Rede, firewall e aplicações

- SSH escuta na porta 22. rpcbind escuta TCP/UDP 111; dnsmasq serve a rede do libvirt. Esses serviços existentes não foram alterados.
- UFW ausente. iptables contém regras Oracle `InstanceServices` e libvirt, INPUT com rejeição final e FORWARD com rejeição final.
- Security Lists/NSGs da Oracle não foram inspecionados: não há credenciais/API da OCI nesta sessão. Um socket em escuta não comprova acesso público.
- Não há serviços existentes PostgreSQL, Caddy, Docker ou Tailscale.
- `/srv` vazio; `/opt/unified-monitoring-agent` existente e preservado. Nenhuma configuração de aplicação foi encontrada nos diretórios inspecionados.
- `/etc/docker`, configuração Docker e fontes APT Docker não existiam.
- Endereço privado da interface observado: `10.0.0.218`.

## Plano exato da Fase 1

1. Inicializar Git com exclusão de secrets, chaves, imagens de VM e volumes.
2. Criar backend Python 3.12/FastAPI com configuração validada e módulos separados.
3. Criar PostgreSQL com volume persistente e sem publicação de porta; migrations Alembic para usuários, auditoria e limitação de login.
4. Implementar login JWT, hash Argon2id, consulta do usuário autenticado e CLI administrativa.
5. Containerizar o backend sem privilégios/root, socket Docker, shell remoto ou acesso ao libvirt.
6. Configurar Caddy com TLS privado e publicação somente em loopback. HTTPS público depende de domínio/DNS e regras OCI, a preparar quando informados.
7. Instalar Docker pelo repositório oficial, após salvar a configuração de rede e verificar conflitos. Preservar encaminhamento existente com `ip-forward-no-drop`.
8. Implantar em `/srv/devlima-agent`; gerar secrets aleatórios em `.env` 0600 sem imprimi-los.
9. Validar migrations, autenticação, limitação de login, persistência após reinício, TLS e integridade do template/rede.

Scheduler funcional pertence à Fase 4; router LLM à Fase 2; VM Manager à Fase 5; Android às Fases 6–8. A Fase 1 não simulará essas funcionalidades.

## Resultado posterior da Fase 1

O proprietário informou `agent.vegasolucoes.com.br` durante a implementação; DNS confirmou `147.15.33.140`. O plano de TLS privado foi adaptado para HTTPS público, mantendo o modo privado como default reutilizável. Certificado público emitido e validado externamente, sem alterações manuais no firewall/OCI.

Docker 29.8.1/Compose 5.5.1 instalados como novos pacotes, sem upgrades ou remoções de pacotes existentes. Serviço em `/srv/devlima-agent`, PostgreSQL 17.11 e Caddy 2.11.4; backend Python 3.12 em container não root. Resultados detalhados em [docs/PHASE_1.md](docs/PHASE_1.md).

Template mantém o SHA-256 original. Configuração da rede default, identidade/path/permissões do pool e regras Oracle/libvirt preservados. Os números de espaço disponível/alocado do pool mudaram somente pelo consumo normal de disco da instalação; isso não é alteração do pool. As chaves e arquivos cloud-init existentes permanecem intactos. Nenhuma VM foi criada, apagada ou recriada.

## Nova inspeção da Fase 2

Na sequência, o proprietário informou a credencial Groq e o IP Tailscale do llm-server. Tailscale já estava instalado/ativo/autorizado, com Core `100.108.84.64` e LLM `100.102.91.22`; nada foi reinstalado na VPN.

`http://100.102.91.22:8080/health` respondeu ok; `/v1/models` confirmou Gemma 4 12B Instruct, GGUF UD-Q4_K_XL, contexto servido de 8192 tokens. A credencial foi armazenada somente no `.env` da VM (0600), sem ser reproduzida no relatório. Configuração Groq utiliza `openai/gpt-oss-120b`, presente na lista disponível e validado por inferência.

Fase 2 implantada com migration `0002_llm_requests`, 61 testes passando, inferência local e fallback real validados. Relatório em [docs/PHASE_2.md](docs/PHASE_2.md).

## Resultado da Fase 3

Fase 3 implantada com migration `0003_context`, Agent Core, conversas e histórico persistente, contexto limitado, resumos, memórias/candidatos e parser de ações. Resultado: 97 testes, lint e Alembic check aprovados. Smoke real local confirmou preferência entre conversas, resumo sem apagar histórico e replay sem nova inferência em outro processo.

Backup local anterior à migration em `/srv/devlima-agent/backups/phase2-before-0003.dump`, 0600. As cinco linhas de auditoria e quatro tentativas LLM anteriores permaneceram no banco; não há usuário padrão de produção. Dados do smoke são sintéticos e separados. Não houve alteração no llm-server, libvirt, template ou chaves dos workers.

No Core, requests JSON locais desativam thinking por opções do protocolo llama.cpp, reduzindo a latência observada do chat para cerca de 2,3–4,2 segundos. Configuração de modelos, Tailscale e fallback permanece a da Fase 2. Detalhes em [docs/PHASE_3.md](docs/PHASE_3.md) e [CONTEXT.md](CONTEXT.md). Próxima etapa: Fase 4, tarefas e scheduler.

## Resultado da Fase 4

Migration `0004_planning`, tarefas, lembretes, chamadas agendadas, recorrência e scheduler separados foram implementados. 120 testes e Alembic check aprovados; integração real com Groq criou tarefa/lembrete em banco isolado e gerou aviso idempotente. Backup local anterior à migration em `backups/phase3-before-0004.dump`. Relatório: [docs/PHASE_4.md](docs/PHASE_4.md).

O proprietário autorizou continuar até a Fase 9 sem pausas, com llm-server local desligado e desenvolvimento Android na VPS. JDK 17 foi instalado como pacote novo, sem upgrades/remoções de pacotes existentes. SDK/builds Android serão separados do Core e terão limites de recursos.

## Resultado da Fase 5

Migration `0005_workers`, fila durável, runner e VM Manager systemd privado implantados. Backend 126 testes; manager 11 testes. Ciclo real confirmou jobs, isolamento de rede, snapshot/restore, stop/start, reset limpo e destroy; integração real Core → manager também passou no banco isolado. Template conserva o SHA-256 original, sem domínios externos alterados; todos os workers dos smokes foram removidos. Backup pré-migration em `backups/phase4-before-0005.dump` (0600).

O primeiro snapshot revelou OOM no limite inicial do manager. Conversão foi limitada a uma coroutine/cache direto; unidade usa MemoryHigh 512 MiB e MemoryMax 1536 MiB. Segundo ciclo passou sem reinício, com pico de cerca de 514 MiB. Token do manager fica somente no runner e arquivos protegidos, separado do backend HTTP/scheduler. Relatório em [docs/PHASE_5.md](docs/PHASE_5.md).

Na VPS, JDK 17/Gradle 8.13/SDK 36/build-tools 36.0.0/emulador e imagem Google APIs estão instalados em `/srv/devlima-build-tools` e `/srv/devlima-android-sdk`, fora do Git. Desenvolvimento Android continuará nesse host por preferência do proprietário.

## Resultado da Fase 6

Schema `0006_devices`, backend 0.6.0, refresh rotativo/revogação, WSS autenticado e ACK durável implantados. 136 testes Python passaram; smoke real de socket e WSS público aprovado. Android desenvolvido/compilado na VPS: assembleDebug/lint, 2 testes unitários e 1 instrumentado em emulador API 36 passaram. Sessão e eventos locais criptografados; tela de login e controles de conexão disponíveis. Hardware físico permanece pendente. Relatório em [docs/PHASE_6.md](docs/PHASE_6.md).

## Resultado da Fase 7

Android 0.7.0 compilado na VPS: chat/histórico, fila persistente, rotina (tarefas/lembretes/chamadas agendadas), timezone da conta e confirmação de memórias propostas. 3 testes unitários/2 instrumentados e lint passaram. Banco do Core permanece em 0006_devices; integração real temporizada será verificada na fase final. Relatório em [docs/PHASE_7.md](docs/PHASE_7.md).

## Resultado da Fase 8

Backend 0.8.0/migration 0007_calls, sessões internas, propriedade/dispositivo, expiração e transcrição idempotente implantados. 143 testes e Alembic check passaram. Android 0.8.0 desenvolvido/compilado na VPS, com atender/recusar, tela de chamada e SpeechRecognizer/TTS/alternativa por texto. Lint/3 unitários/3 instrumentados passaram. Validação física e E2E temporizado serão distinguidos no relatório final. [docs/PHASE_8.md](docs/PHASE_8.md).
