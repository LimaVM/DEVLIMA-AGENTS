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
- [ ] Conversas, mensagens, summaries, memórias e candidatos.
- [ ] Context Builder limitado, UTC/timezone, histórico bruto preservado.
- [ ] JSON Pydantic e Action Engine sem shell arbitrário.

## Fase 4 — tarefas e tempo
- [ ] Tasks, reminders, calls e recorrência RRULE.
- [ ] Scheduler separado, claims transacionais, outbox e idempotência.
- [ ] Reconstrução após crash/reboot e testes de concorrência.

## Fase 5 — workers
- [ ] VM Manager privado via systemd, autenticação e WorkerProvider.
- [ ] Overlays/cloud-init/readiness SSH e guest-agent.
- [ ] Criar/status/destruir/reset/snapshot/restore com quotas.
- [ ] Reconciliação, proteção de paths/template e testes libvirt.
- [ ] WindowsProvider reservado, sem template Windows nesta versão.

## Fase 6 — conexão Android
- [ ] WebSocket autenticado, envelopes, ACK, heartbeat e backoff.
- [ ] Kotlin/Compose/Material 3 e Foreground Service.
- [ ] Documentar limites de bateria/force stop sem contornar Android.

## Fases 7–8 — interface e voz
- [ ] Chat, tarefas e lembretes Android.
- [ ] Notificação de chamada, atender/recusar, call_sessions.
- [ ] SpeechRecognizer, TextToSpeech, mute/speaker/encerrar.

## Fase 9 — conclusão V1
- [x] Domínio/HTTPS público: acesso 80/443 validado externamente; sem alteração de regras OCI.
- [ ] Roles PostgreSQL separadas para migrations/runtime, sem superuser no Core.
- [ ] Backup externo, restore e recovery documentados/testados.
- [ ] Testes ponta a ponta: café 5 min, chamada 2 min, criar/apagar/recriar/restaurar worker.
- [ ] APK compilado e teste em dispositivo real.

Fora do escopo inicial: Firebase, Kubernetes, Redis, RabbitMQ, WebRTC, Whisper server, TTS server, pgvector, automação de browser, email/calendar e multi-agent.
