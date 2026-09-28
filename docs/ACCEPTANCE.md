# Auditoria de entrega do desenvolvimento V1

Objetivo: fases 4–9, manter LLM local configurada/desligada, usar Groq somente pelo fallback técnico autorizado, testar/implantar/publicar na main e relatar validações dependentes de Android físico.

| Requisito | Evidência inspecionada | Estado |
| --- | --- | --- |
| Tarefas, lembretes, chamadas e scheduler durável | 0004_planning; testes timezone/RRULE/DST, concorrência, crash-before-commit e cancelamento; café 5 min/chamada 2 min realmente entregues no emulador | Implementado e testado |
| Worker Linux: create/status/ready/delete/recreate/reset/snapshot/restore/job | Core WorkerService/runner, manager privado; ciclos reais documentados em PHASE_5/9; Core READY e job confirmados no smoke isolado; template original e nenhuma VM de teste restante | Implementado e testado |
| Quotas, ownership, caminhos e isolamento | Testes manager/Core; filtro de rede real bloqueou metadata/Core; template SHA-256 preservado; runner único consumidor do socket/token | Verificado |
| Android WSS/Foreground Service/reconexão | Kotlin/Compose, Keystore, SQLite cifrado, fila/ACK/heartbeat/backoff; testes backend/instrumentados e reconexão após restart do app/backend | Implementado e testado no emulador |
| Chat/histórico/rotina/memórias | UI e APIs reais; fila idempotente, tarefas editadas/concluídas, lembretes editados/cancelados e cache preservado | Implementado e testado |
| Chamadas, contexto de voz e controles | 0007_calls; concorrência/ownership/expiry/voice replay testados; atendimento/transcrição por texto/resposta/end reais; engines SpeechRecognizer/TTS pt-BR presentes | Implementado; acústica física pendente |
| Hardening PostgreSQL/serviços | Runtime sem superuser/DDL/TRUNCATE, migration separada, administrador fora do Core; testes diretos SQLSTATE 42501 e saúde/schema HTTPS atuais | Verificado |
| Backup externo e recovery | Envelope AES-GCM, timer VPS/LaunchAgent Mac, arquivos externos autenticados, template/identidades conferidos, restore 0007_calls em banco exclusivo e remoção do banco temporário | Verificado; cópia automática depende do Mac ligado |
| Android desenvolvido/build na VPS | assembleRelease/lint/unitários, instrumentados API 36, APK release instalado/aberto, assinatura v2 e checksum conferidos | Verificado |
| Código/documentação na main, artefato acessível | Histórico Git privado, relatórios 0–9/arquitetura/operação/recovery, release privada v1.0.1 com APK/checksum; credencial operacional entregue em arquivo privado | Publicado |
| Secrets fora do Git/APK | .gitignore/contexto Docker; scanner de valores protegidos/histórico e entradas APK sem correspondências; arquivos privados 0600 | Verificado para os segredos conhecidos |
| LLM local desligada/Groq autorizado | Configuração privada conservada; E2E registrou três respostas Groq com fallback_used; política limita falhas que permitem nuvem | Verificado |
| Relatar limites de aparelho físico | Checklist Android e PHASE_9 distinguem engines/emulador de microfone/saída/rede móvel/bateria reais | Documentado; homologação física não declarada |

Os 143 testes backend, 11 manager, cinco backup/configuração e testes Android reportados foram executados. CI GitHub é uma verificação adicional ainda bloqueada em startup_failure antes dos jobs; sucesso hospedado não é inferido dos testes na VPS. Nenhum suporte foi acionado em nome do proprietário.

Desenvolvimento/implantação da V1 e seus artefatos estão entregues. Antes de declarar o aplicativo homologado no telefone do proprietário, executar o checklist físico em [android/README.md](../android/README.md). O relatório técnico detalhado é [PHASE_9.md](PHASE_9.md).
