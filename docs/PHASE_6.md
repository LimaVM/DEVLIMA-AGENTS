# Fase 6 — conexão Android e entrega durável

Backend version 0.6.0/migration `0006_devices`: dispositivos, famílias de sessão com refresh token rotativo, revogação, WebSocket autenticado e ACK por dispositivo. Agent Core grava `agent.message` na mesma transação da resposta. Protocolo em [WEBSOCKET.md](WEBSOCKET.md).

Android desenvolvido e compilado na VPS, conforme preferência do proprietário. App Kotlin 2.3.10, Compose/Material 3, AGP 8.13.2, Gradle 8.13, JDK 17, compile/target SDK 36 e min SDK 26. Compose BOM 2026.02.01 foi fixado por compatibilidade: BOM 2026.09.00 exige API 37/AGP 9.1. O compiler usa o DSL compilerOptions atual. Referências: [AGP](https://developer.android.com/build/releases/agp-8-13-0-release-notes), [Kotlin](https://kotlinlang.org/docs/releases.html), [Compose BOM](https://developer.android.com/develop/ui/compose/bom).

App inclui tela de login/servidor HTTPS, controle de conectar/desconectar/sair, sessão criptografada AES-GCM com Android Keystore, eventos locais criptografados em SQLite, confirmação após persistência, notificação de conexão, canais de lembretes/chamadas, heartbeat, backoff e resposta ao retorno da rede. Senha não é armazenada; não há credencial Groq ou segredo do backend no APK.

Foreground Service declara specialUse para conexão do agente iniciada pelo usuário, com notificação persistente e ação de desconectar. Não há receiver BOOT_COMPLETED, solicitação automática de isenção de bateria, Firebase ou tentativa de contornar force stop. Iniciar e manter o serviço depende das políticas Android; negar notificações limita os avisos. Tipo de serviço conforme [documentação Android](https://developer.android.com/develop/background-work/services/fgs/service-types).

## Validação realizada

- Backend: 136 testes passaram, incluindo rotação/reuso de refresh, logout/revogação, isolamento, ACK/reenvio por dispositivo, autenticação WebSocket e chat/replay sem segunda inferência.
- Lint Python passou; Alembic check sem divergências.
- Smoke Uvicorn/websockets-sansio real passou no banco isolado: autenticação, evento, ACK persistente e reconexão. WSS público validou TLS/upgrade e rejeitou token inválido com 4401.
- Deploy saudável no domínio com schema `0006_devices`; backup anterior em `backups/phase5-before-0006.dump`, 0600.
- Android assembleDebug, 2 testes unitários e lintDebug passaram na VPS. APK debug inicial de aproximadamente 12 MiB. Lint apresenta avisos de versões mais novas; versões foram fixadas para compatibilidade do SDK.

Um teste instrumentado passou no emulador API 36 da VPS: criptografia da sessão/eventos, persistência após reabertura, deduplicação, marca de notificação e regeneração do device ID. APK instalado e tela inicial aberta; nenhum crash AndroidRuntime observado. Aparelho físico e alternância real Wi-Fi/rede móvel continuam reservados à validação final; nenhum teste de hardware foi presumido.

Próxima etapa: Fase 7, chat/histórico, fila de envio e interface de tarefas/lembretes.
