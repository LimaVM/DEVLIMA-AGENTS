# Roteiro de desenvolvimento

Estado em 2026-09-28: fases 0–5 concluídas. As funcionalidades abaixo são planejadas; os relatórios PHASE_1.md, PHASE_2.md e PHASE_3.md, PHASE_4.md e PHASE_5.md registram o que já foi implementado e validado. A lista de execução está em [TODO.md](../TODO.md).

## Fase 4 — tarefas, lembretes e tempo

Implementar criação, consulta, edição e conclusão de tarefas; lembretes com criação, alteração e cancelamento; chamadas agendadas; e recorrência RRULE. Os pedidos em linguagem natural passam pelo parser e pelo Action Engine, que aplica autorização e persiste o resultado. Datas são interpretadas na timezone do usuário e armazenadas em UTC.

O scheduler será um processo separado. PostgreSQL guardará eventos, estados de execução e uma outbox de entrega; o scheduler acorda e reserva eventos transacionalmente. Identificadores idempotentes e controle de concorrência impedem que dois processos executem intencionalmente o mesmo evento. Definir e testar a política para eventos vencidos durante indisponibilidade.

**Entrega:** backend capaz de registrar e produzir eventos REMINDER/CALL após restart, deploy ou crash. O aplicativo receberá esses eventos nas fases Android; nesta fase não se promete aviso já entregue no celular.

**Validação:** agendar, editar e cancelar eventos, testar recorrência/timezone, reiniciar o scheduler, simular concorrência e verificar recuperação sem execução duplicada.

## Fase 5 — workers Linux descartáveis

Criar VM Manager como serviço systemd privado e autenticado no host. Agent Core usará uma API de operações enumeradas; o serviço controlará libvirt/KVM. Preparar WorkerProvider, LinuxWorkerProvider e a interface futura WindowsWorkerProvider.

Cada worker nascerá de um overlay QCOW2 do template Ubuntu existente, com cloud-init individual, usuário agent, chave pública dos workers, SSH e qemu-guest-agent. O estado READY exige confirmação de IP e disponibilidade do guest-agent/SSH. Configuração inicial planejada: 2 vCPUs, 2048 MiB de RAM e 20 GiB de disco virtual.

Implementar criar, consultar/listar, destruir, resetar, criar snapshot e restaurar snapshot. Reset recria um ambiente limpo; restore retorna a um snapshot identificado. Persistir estados e reconciliá-los com libvirt após falhas. Aplicar quotas e validar recursos disponíveis: planejamento inicial de até dois workers, quatro vCPUs e 8 GiB de RAM somados, reservando recursos para o host/Core/banco.

Proteções obrigatórias: template preservado, IDs e paths validados, identificação explícita de VMs gerenciadas, isolamento dos demais domínios e auditoria. A execução de tarefas será restrita aos ambientes workers. Windows completo e seu template permanecem fora desta V1.

**Entrega:** ciclo de vida de workers Linux acessível pelo Core, com autorização, estados reais e recuperação.

**Validação:** criar/acessar/destruir/recriar um worker e criar/restaurar um snapshot, verificando checksum do template, limites e preservação das VMs externas.

## Fase 6 — conexão Android

Criar aplicativo Kotlin/Jetpack Compose/Material 3 com login e WebSocket Secure autenticado. Definir envelopes de protocolo para mensagens, eventos, ACKs e erros. Heartbeat e reconexão com backoff progressivo acompanharão o estado da conexão.

Integrar a outbox persistente a confirmações por dispositivo e deduplicação de eventos. Uma perda de conexão pode causar reenvio; servidor e cliente devem tolerá-lo. Implementar Foreground Service com notificação persistente de conexão. Documentar limitações de force stop, permissões e restrições de bateria sem tentar contornar as políticas Android. Firebase não será utilizado.

**Entrega:** base do aplicativo autenticada, conectada e capaz de recuperar eventos pendentes.

**Validação:** perda/restabelecimento da rede, alternância Wi-Fi/rede móvel, reinício do app/servidor, expiração de autenticação e confirmações de eventos reenviados.

## Fase 7 — chat, tarefas e lembretes Android

Construir telas de chat/histórico/conversas e estados de envio/processamento/falha. Reenvios utilizarão o client_message_id implementado na Fase 3. Integrar consulta, criação, alteração e conclusão de tarefas e consulta, alteração e cancelamento de lembretes.

Exibir eventos e avisos recebidos, estado da conexão e falhas que exigem ação do usuário. As telas utilizarão APIs e eventos reais do backend.

**Entrega:** aplicativo utilizável para conversar e administrar tarefas/lembretes.

**Validação:** pedir “me lembra daqui a 5 minutos de tomar café”, conferir o agendamento e receber o aviso no aparelho; testar edição, cancelamento, reconexão e histórico persistido.

## Fase 8 — chamada interna e voz

Implementar notificação “AGENTE ESTÁ LIGANDO”, atender/recusar, call_sessions e os estados da sessão. Tela com nome do agente, duração, mute, saída de áudio e encerramento.

A V1 usará SpeechRecognizer para voz → texto, Agent Core/LLM para a resposta e TextToSpeech para texto → voz. Coordenar escuta/reprodução e o contexto da conversa. Será uma chamada dentro do aplicativo; áudio em streaming, WebRTC, Whisper e TTS próprios ficam para evolução futura, mantendo interfaces que permitam trocar a camada de voz.

**Entrega:** atender e conversar por voz com o agente usando chamadas agendadas.

**Validação:** “me liga daqui a 2 minutos”, notificação, atender/recusar/encerrar, conversa com contexto, perda de rede e tratamento das permissões de áudio.

## Fase 9 — segurança, recuperação e conclusão da V1

Separar roles PostgreSQL de migrations/runtime, retirar privilégios administrativos do Core, revisar autenticação, exposição dos serviços, isolamento e auditoria. HTTPS público já está operacional; sua configuração será incluída na revisão final.

Implementar backup externo e testar restore em ambiente separado. Documentar recovery após falhas, atualização e rollback. Compilar o APK e testar em aparelho real.

**Entrega:** V1 completa com procedimentos de operação e recuperação verificados.

**Validação ponta a ponta:** conversa persistente, lembrete de café em cinco minutos, chamada em dois minutos com voz, criar/apagar/recriar worker, snapshot/restore e recuperação após reinícios. Testes em banco separado continuam sendo obrigatórios; não apagar volumes de produção.

## Processo de cada fase

Inspecionar antes de alterar, implementar a fase, investigar/corrigir falhas, executar testes apropriados, implantar e registrar resultados reais. Cada relatório informa alterações, comandos de teste, resultados, problemas conhecidos e a próxima etapa. Secrets, chaves, bancos, imagens de VM e backups ficam fora do Git.
