# Changelog

## 1.0.1 — 2026-09-28

Corrige o backup automático via systemd: a consulta ao commit confia explicitamente apenas no diretório do projeto, pois root sem SUDO_UID recusava o repositório pertencente a ubuntu. Unidade real executada com sucesso; backup resultante restaurado em banco isolado. LaunchAgent externo no Mac também executado com exit code 0.

Acrescenta prova real de Core READY/job/removal e atualiza documentação de arquitetura/aceitação. Backend e APK usam versão 1.0.1; Android code 101, mesma assinatura e funcionalidades de voz/chat/rotina da 1.0.0.

## 1.0.0 — 2026-09-28

V1 implementada até a fase 9: Core FastAPI/PostgreSQL, autenticação, contexto/memória, tarefas/scheduler/outbox, workers Linux libvirt/KVM e Android Kotlin/Compose com chat, rotina, WSS, chamadas internas, SpeechRecognizer/TTS e alternativa por texto.

Entrega final inclui roles migrations/runtime, backup autenticado e cópia externa, restore isolado verificado, CI de backend/manager/backup, APK release assinado e documentação operacional. E2E temporizado real aprovado no emulador, com Groq enquanto a LLM local estava indisponível.

Homologação de áudio, conectividade móvel e bateria em aparelho físico permanece pendente. Consulte [Fase 9](docs/PHASE_9.md) para evidências e limitações.
