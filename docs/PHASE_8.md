# Fase 8 — chamadas internas e voz

Backend 0.8.0/schema 0007_calls implantado. Cada ocorrência pode gerar uma única sessão ao atender, vinculada ao usuário/dispositivo/conversa. Lock da conta e ocorrência impedem atendimento simultâneo. Atender/rejeitar/encerrar são idempotentes; eventos duráveis sincronizam cancelamento e estado entre dispositivos. Toque vence em 120 segundos, inatividade em 10 minutos e duração em 30 minutos. Reconexão marca chamada vencida como perdida.

APIs JWT: GET /calls, POST /calls/incoming/{id}/answer ou reject com device_id; POST /calls/{id}/end; /transcript recebe device_id/client_message_id/content. Sessões rotativas ficam vinculadas ao dispositivo. Protocolo WSS de chamadas/voice.transcript em [WEBSOCKET.md](WEBSOCKET.md). Texto de voz passa pelo mesmo Core/contexto/autorização/idempotência do chat.

Android 0.8.0: notificação AGENTE ESTÁ LIGANDO, Atender abre aplicativo, Recusar usa receiver privado; tela da chamada mostra agente/duração/mute/alto-falante/auricular/encerrar. Permissão de microfone é solicitada no atendimento. Serviço de voz inicia enquanto a Activity está visível e usa o tipo microphone quando autorizado; alternativa por texto é disponível. Recuperar uma sessão ativa exige nova ação para ativar áudio. Sem full-screen intent, Telecom, Firebase ou WebRTC.

SpeechRecognizer é controlado na thread principal; reprodução TTS interrompe escuta e só retoma após a última fala. Falta de engine/permissão/áudio é tratada com texto e ação explícita de tentar novamente. Fila de transcrições conserva UUID e call_session_id após reconexão; encerrar cancela turnos ainda pendentes. Contexto da sessão fica no PostgreSQL. SpeechRecognizer e TTS podem utilizar serviços de rede instalados no Android; a política de fallback Groq do Core não controla esses serviços de voz do aparelho.

Referências oficiais: [SpeechRecognizer](https://developer.android.com/reference/android/speech/SpeechRecognizer), [TTS](https://developer.android.com/reference/android/speech/tts/TextToSpeech), [restrições de foreground/microfone](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start).

## Validação

- 143 testes Python passaram: atendimento concorrente, propriedade/dispositivo, expiração, idempotência, eventos WSS e dois turnos de voz com replay/contexto.
- Lint Python e Alembic check passaram. Backup anterior em backups/phase6-before-0007.dump (0600). Deploy saudável.
- VPS: assembleDebug/lintDebug, 3 testes unitários e 3 instrumentados no emulador API 36 passaram, incluindo identidade/cancelamento da fila de voz.
- Kotlin formatado com ktfmt 0.64 (artefato Maven verificado contra checksum publicado); SDK/builds permanecem na VPS.

Emulador não comprova qualidade do microfone/voz, auricular ou entrega em aparelho bloqueado. Integração autenticada com APK e temporizadores reais entra na Fase 9; teste de hardware físico continua pendente.
