# Validação Android em aparelho físico — 2026-09-28

Celular Xiaomi, modelo informado pelo Android `2511FPC34G`, Android 16/API 36, conectado por USB ao Mac. Desenvolvimento, compilação, testes unitários e lint continuaram na VPS. ADB no Mac instalou os APKs e executou a instrumentação no celular.

Os testes usam `br.com.vegasolucoes.agent.debug` e uma conta sintética isolada. Credenciais, serial do aparelho, logs privados e conversas de teste não são versionados. A instalação de produção tem package separado.

## Resultados

| Verificação | Evidência |
| --- | --- |
| Armazenamento, fila/replay e capacidades de voz | Quatro testes instrumentados passaram; SpeechRecognizer disponível, TTS inicializado e pt-BR disponível |
| E2E inicial | Passou em 311,762 s: lembrete café 5 min, chamada 2 min, resposta por transcrição de texto, tarefas, reconexão e ACKs reais |
| Escuta interativa | Depois da correção de foco, interface permaneceu em Ouvindo; uma chamada recebeu três falas e três respostas na mesma conversa, com referências a café |
| Controles | Silenciar/Ativar mic refletiram o estado; Auricular/Alto-falante alternaram; dumpsys confirmou rota earpiece; encerramento confirmado no Core |
| Wi-Fi → dados móveis → Wi-Fi | Wi-Fi desativado temporariamente, transporte CELLULAR presente e lembrete de prova recebido/ACK; estado Wi-Fi original restaurado |
| Tela bloqueada | Comando sleep após agendamento; evento recebido, notificação com o mesmo event_id presente e ACK verificado antes do comando wake |
| Fila offline física | Wi-Fi e dados móveis suspensos brevemente; mensagem visível como Na fila; após restaurar rede, exatamente uma mensagem e uma resposta persistidas, sem duplicação |
| Build da correção | Android 1.0.2/code 102; assembleRelease/Debug/AndroidTest, três unitários e lint sem erros na VPS; assinatura v2 e certificado preservados |
| Regressão final 1.0.2 no aparelho | Quatro instrumentados passaram em 2,643 s e E2E completo passou em 314,167 s, após instalar code 102 |
| Instalação de produção e limpeza | Release assinada 1.0.2/code 102 instalada e aberta no celular; APKs debug/test removidos; conta sintética desativada, senha substituída e duas famílias/dispositivos revogados |

A confirmação auditiva do proprietário sobre volume/qualidade e continuidade semântica do contexto foi solicitada e permanece pendente. As frases usadas na conversa interativa não corresponderam integralmente ao roteiro sugerido; os três turnos na mesma conversation_id e referências a café não constituem uma aprovação automática desse roteiro. Não se declara homologação completa de bateria/Doze, permissões negadas ou desempenho em outros fabricantes.

## Problemas encontrados e correções

Na build anterior, o app solicitava foco antes de iniciar SpeechRecognizer. O serviço Google de reconhecimento solicitava seu próprio foco; o app recebia LOSS_TRANSIENT (-2), cancelava a escuta e recebia ERROR_CLIENT (5). Logs do serviço confirmaram CANCELLED. No emulador, a transcrição injetada por texto não exercitava essa captura física.

VoiceController agora libera seu foco antes de escutar e trata interrupção de foco durante reprodução TTS. Cancelamento do reconhecedor ocorre somente quando uma escuta está ativa. Erros de idioma, permissão, rede e serviço ocupado têm orientação específica; logs registram somente o código de erro, sem a frase reconhecida.

O controlador do serviço tornou-se um StateFlow observado pela tela de chamada. Assim, Ativar áudio muda para Falar quando o serviço inicia; antes, a leitura de um campo não observável deixava o rótulo desatualizado.

## Artefato

Android 1.0.2/code 102, backend permanece 1.0.1/schema 0007_calls. APK 8.545.724 bytes, SHA-256 `c0847aeb38c9463cdfb2fac3a240e995e44a022f552f04f15fc651d049cba4eb`. Certificado SHA-256 `b68c5786bdc1088ae635b5611c57beaf9add894269408d5298cf58765bf4348e`.

## Limites

O teste de tela bloqueada foi breve e não representa horas em Doze ou restrições agressivas de bateria Xiaomi. Reconhecimento pode utilizar o serviço de voz instalado no Android; a política Groq controla o Core, não esse serviço do sistema. Force stop exige reabertura/conexão explícita. A conta de teste foi encerrada; use sua credencial operacional separada para entrar na instalação de produção.
