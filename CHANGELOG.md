# Changelog

## Documentação completa do código — 2026-09-28

Adiciona referência numerada de cada linha de código textual, testes, migrations, build e infraestrutura, com catálogo editorial, manifesto de hashes/contagem e verificação de atualização. Acrescenta comentários a classes/funções Python/Kotlin sem alterar a AST/tokens dos fontes existentes. CI inclui check da referência; execução hospedada continua dependente da disponibilidade do GitHub. Credenciais operacionais conservadas fora do Git, com configuração externa documentada.

## Android 1.0.3 — pré-release, 2026-09-28

Acrescenta CallStyle com toque contínuo limitado ao prazo real de atendimento, tela de chamada sobre bloqueio quando autorizada, desbloqueio antes do atendimento/microfone, atalhos de permissões/bateria e restauração da conexão desejada após boot/atualização. Preserva Desconectar e encerramento explícito pelo usuário; eventos expirados não voltam a tocar.

Compilado/assinado na VPS, quatro unitários e lint sem erros. Instalação USB recusada pelo Xiaomi e testes físicos adiados pelo proprietário; 1.0.2 permanece instalado. Condições de entrega e pendências em [chamadas em background](docs/ANDROID_BACKGROUND_CALLS.md). Backend permanece 1.0.1.

## Android 1.0.2 — 2026-09-28

Corrige a captura física de voz: o foco solicitado pelo serviço de reconhecimento cancelava a própria escuta do aplicativo. O app libera seu foco antes de escutar e trata interrupções durante o TTS. O controlador de voz é observado pela interface, atualizando corretamente Ativar áudio/Falar; erros de reconhecimento possuem orientação específica e diagnóstico sem transcrições nos logs.

Build Android e testes unitários/lint executados na VPS, validação USB em Xiaomi Android 16, chamadas/lembretes reais e reconexão móvel. Backend permanece 1.0.1. Evidências e limites em [validação física](docs/ANDROID_PHYSICAL.md).

## 1.0.1 — 2026-09-28

Corrige o backup automático via systemd: a consulta ao commit confia explicitamente apenas no diretório do projeto, pois root sem SUDO_UID recusava o repositório pertencente a ubuntu. Unidade real executada com sucesso; backup resultante restaurado em banco isolado. LaunchAgent externo no Mac também executado com exit code 0.

Acrescenta prova real de Core READY/job/removal e atualiza documentação de arquitetura/aceitação. Backend e APK usam versão 1.0.1; Android code 101, mesma assinatura e funcionalidades de voz/chat/rotina da 1.0.0.

## 1.0.0 — 2026-09-28

V1 implementada até a fase 9: Core FastAPI/PostgreSQL, autenticação, contexto/memória, tarefas/scheduler/outbox, workers Linux libvirt/KVM e Android Kotlin/Compose com chat, rotina, WSS, chamadas internas, SpeechRecognizer/TTS e alternativa por texto.

Entrega final inclui roles migrations/runtime, backup autenticado e cópia externa, restore isolado verificado, CI de backend/manager/backup, APK release assinado e documentação operacional. E2E temporizado real aprovado no emulador, com Groq enquanto a LLM local estava indisponível.

Homologação de áudio, conectividade móvel e bateria em aparelho físico permanece pendente. Consulte [Fase 9](docs/PHASE_9.md) para evidências e limitações.
