# Desenvolvimento por fases

## Fase 0 — inspeção
- [x] Acesso SSH e versões reais.
- [x] KVM, libvirt, rede, pool, domínios e espaço.
- [x] Template, checksum e metadados das chaves.
- [x] Estado de serviços, firewall e diretórios.
- [x] CURRENT_STATE.md, arquitetura, segurança e plano da Fase 1.

## Fase 1 — fundação
- [x] Git e exclusões de secrets.
- [x] FastAPI/Pydantic/SQLAlchemy e endpoints de saúde.
- [x] PostgreSQL persistente e migrations Alembic.
- [x] JWT/Argon2id, limitação de login, auditoria e CLI.
- [x] Compose/Caddy, default privado e HTTPS público no domínio informado.
- [x] Deploy real, 21 testes, persistência e preservação do template.

## Fase 2 — router LLM
- [x] LLMProvider, llama.cpp e Groq com timeouts.
- [x] Fallback exclusivamente técnico e flag de privacidade.
- [x] URL privada/modelo Gemma local e Groq configurados via environment.
- [x] Auditoria sem secrets, healthchecks, 61 testes e inferências reais local/fallback.

## Fase 3 — contexto e memória
- [x] Conversas, mensagens, summaries, memórias e candidatos.
- [x] Context Builder limitado, UTC/timezone, histórico bruto preservado.
- [x] JSON Pydantic e Action Engine sem shell arbitrário; execução nas fases seguintes.
- [x] Replay idempotente, leases, confirmação de memória e isolamento por usuário.
- [x] Deploy, 97 testes, fluxo local real e persistência em novo processo.

## Fase 4 — tarefas e tempo
- [x] Tasks, reminders, calls e recorrência RRULE.
- [x] Scheduler separado, claims transacionais, outbox e idempotência.
- [x] Recuperação transacional após crash/restart e testes de concorrência.

## Fase 5 — workers
- [x] VM Manager privado via systemd, autenticação e WorkerProvider.
- [x] Overlays/cloud-init/readiness SSH e guest-agent.
- [x] Criar/status/destruir/reset/snapshot/restore com quotas.
- [x] Reconciliação, proteção de paths/template e testes libvirt.
- [x] WindowsProvider reservado, sem template Windows nesta versão.

## Fase 6 — conexão Android
- [x] WebSocket autenticado, envelopes, ACK, heartbeat e backoff.
- [x] Kotlin/Compose/Material 3 e Foreground Service.
- [x] Documentar limites de bateria/force stop sem contornar Android.

## Fases 7–8 — interface e voz
- [x] Chat, tarefas e lembretes Android.
- [x] Notificação de chamada, atender/recusar, call_sessions.
- [x] SpeechRecognizer, TextToSpeech, mute/speaker/encerrar.

## Fase 9 — conclusão V1
- [x] Domínio/HTTPS público: acesso 80/443 validado externamente; sem alteração de regras OCI.
- [x] Roles PostgreSQL separadas para migrations/runtime, sem superuser no Core; DDL/TRUNCATE negados.
- [x] Backup cifrado, cópia externa no Mac, template/identidades preservados e restore isolado verificado.
- [x] Café 5 min e chamada 2 min no emulador, transcrição por texto/resposta, contexto e ACKs reais.
- [x] Criar/apagar/criar novo worker pelo Core; READY/job/snapshot/restore/reset/destroy reais no manager.
- [x] Recuperação após reinício do app/backend e sessão persistida.
- [x] APK Android 1.0.2 release assinado; desenvolvimento/build na VPS e validação USB em Xiaomi Android 16.
- [x] E2E físico de café/chamada, rede móvel, lembrete com tela bloqueada e correção da escuta por foco de áudio.
- [ ] Execução hospedada da CI: GitHub retorna startup_failure sem jobs/logs, embora actionlint e testes na VPS passem.
- [x] Proprietário confirmou resposta de voz audível no celular.
- [x] Android 1.0.3: CallStyle/toque contínuo, tela bloqueada com desbloqueio, configurações de entrega e restauração após boot; build/lint/quatro unitários na VPS.
- [ ] Validar 1.0.3 no Xiaomi: app fora dos recentes, chamada bloqueada/Doze, permissões, reinício e parada explícita; testes adiados pelo proprietário.
- [ ] Completar avaliação auditiva de auricular/alto-falante, bateria/Doze e cenários de permissão negada em aparelho físico; ver ANDROID_PHYSICAL.md.

Fora do escopo inicial: Firebase, Kubernetes, Redis, RabbitMQ, WebRTC, Whisper server, TTS server, pgvector, automação de browser, email/calendar e multi-agent.
