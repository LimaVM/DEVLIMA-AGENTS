# Chamadas com tela bloqueada — Android 1.0.3

## Comportamento e condições

O usuário pode fechar a interface ou removê-la dos recentes. A conexão WSS é mantida pelo ConnectionService iniciado pelo usuário, com notificação permanente **DevLima Agent ativo** e `stopWithTask=false`. Isso exige um componente em execução no Android. Não existe recebimento imediato de uma chamada remota quando não há serviço/receptor ativo e não se usa push. Firebase permanece fora do projeto.

| Situação | Comportamento esperado / limite |
| --- | --- |
| Tela apagada/bloqueada, interface fechada, serviço conectado | Notificação CallStyle com toque; tela de chamada se a permissão de tela cheia estiver liberada |
| App removido dos recentes | Serviço permanece; implementação pronta, teste no Xiaomi pendente |
| Doze profundo com otimização de bateria | Android pode suspender rede/CPU e atrasar o evento; foreground service sozinho não isenta de Doze |
| Usuário permite exceção de bateria | Android permite rede durante Doze, mas restrições do fabricante e interrupção do processo ainda precisam ser testadas |
| Reinício/atualização do APK | Receiver tenta restaurar conexão previamente ativada, após armazenamento da sessão ficar disponível; não inicia microfone |
| Desconectar/Sair | Conexão deixa de ser desejada; receiver não a reativa |
| Forçar parada / Parar em Apps ativos | Entrega imediata interrompida; reabrir e Conectar. Receiver considera histórico de encerramento pelo usuário |
| Sem internet / sessão revogada | Sem chamada imediata. Backoff/reconexão ou novo login, conforme o motivo |
| Evento recebido depois de 120 segundos | Não toca nem apresenta chamada atendível expirada |

Não se promete entrega em horário exato, duração ilimitada em background ou comportamento idêntico entre fabricantes. O produto não contorna Forçar parada, Não perturbe, volume, permissões ou restrições do sistema.

## Implementação

- Canal `incoming_calls_v2`, importância HIGH, som padrão de toque e vibração; configurações escolhidas pelo usuário são respeitadas. Novo canal permite a configuração de toque adequada, sem tentar alterar canais existentes por código.
- `NotificationCompat.CallStyle`, ações Atender/Recusar e FLAG_INSISTENT. Toque encerra após atendimento, recusa, evento de resolução ou timeout remanescente da janela de 120 segundos.
- `IncomingCallActivity` privada, excluída dos recentes e apta a aparecer sobre bloqueio. Exibe apenas quem liga e controles; nessa tela não há histórico ou motivo da conversa. O microfone fica na interface principal após desbloqueio; a notificação respeita as configurações de privacidade da tela bloqueada.
- Tela cheia usa `USE_FULL_SCREEN_INTENT` e verifica `canUseFullScreenIntent` no Android 14+. Sem autorização, mantém notificação de chamada e respeita a decisão do sistema.
- Atender na notificação/tela bloqueada solicita desbloqueio antes de encaminhar o atendimento. O pedido interno de atendimento não é aceito por extras arbitrários da Activity exportada. Microfone continua exigindo atividade RESUMED e permissão explícita; alternativa de texto preservada.
- `ConnectionRestoreReceiver` responde apenas a BOOT_COMPLETED/MY_PACKAGE_REPLACED, com sessão e preferência de conexão ativa. Não usa armazenamento antes do desbloqueio nem liga microfone em background.
- Conta inclui indicadores e atalhos oficiais para notificações, tela cheia e bateria. Não solicita automaticamente isenção de bateria nem modifica configurações OEM.

## Configuração no telefone

1. Entrar na conta, permitir notificações e tocar **Conectar**.
2. Em **Conta**, abrir **Configurar toque e notificações** e permitir chamadas/alertas, com volume de toque audível.
3. No Android 14+, abrir **Permitir chamada na tela bloqueada** e liberar a opção do sistema, se desejado.
4. Em **Configurar bateria**, permitir que DevLima Agent funcione sem otimização quando chamadas em repouso forem essenciais. No Xiaomi, conferir também início automático e **Sem restrições** nas configurações do app; nomes/localização variam por sistema.
5. Conferir a notificação **DevLima Agent ativo**. Após Forçar parada ou Parar em Apps ativos, reabrir e Conectar.

Essas escolhas ficam sob controle do usuário. Permitir notificações não concede automaticamente tela cheia ou exceção de bateria.

## Validação em 2026-09-28

Build e assinatura foram verificados na VPS: release/debug/AndroidTest, quatro testes unitários sem falhas e lint sem erros. O novo teste unitário cobre evento atrasado, limite de expiração, data inválida e timestamp futuro; replay não renova a janela de toque.

`BackgroundCallsTest` foi compilado para a próxima sessão: conta sintética privada, fechamento dos próprios tasks, tela apagada, chamada real do Core, notificação CallStyle/toque/tela cheia, ausência de início automático de microfone e recusa cancelando a notificação. O teste não demonstra Doze prolongado: instrumentação pode afetar a execução do processo.

Instalações dos packages de teste foram recusadas pelo Xiaomi (`INSTALL_FAILED_USER_RESTRICTED`). O proprietário pediu para testar depois antes de liberar a instalação. Portanto **nenhum teste físico desta versão passou ou foi declarado aprovado**, e o APK 1.0.2 previamente instalado foi preservado. A nova versão é publicada como pré-release para validação.

Próxima sessão: liberar instalação por USB; executar teste de chamada com tela bloqueada e app fora dos recentes; comparar Doze forçado com/sem exceção de bateria, sem instrumentação ativa; restaurar `deviceidle unforce`/`battery reset` e permissões temporárias; testar horas de repouso, atendimento após desbloqueio, timeout/recusa, reinício/desbloqueio e Forçar parada seguido de reabertura. Não reiniciar o telefone ou alterar suas permissões sem coordenar com o proprietário.

## Artefato

Android 1.0.3/code 103, backend 1.0.1/schema 0007_calls. Release assinada. 8.546.040 bytes. SHA-256 `587a7854b8aea0c125c09e0bc11b3b7a9e16385bc888309bcadda6ad05bdfb54`. Certificado SHA-256 `b68c5786bdc1088ae635b5611c57beaf9add894269408d5298cf58765bf4348e`.

## Referências oficiais

- [Doze, rede, exceções de bateria e testes](https://developer.android.com/training/monitoring-device-state/doze-standby)
- [Notificações CallStyle](https://developer.android.com/develop/ui/compose/notifications/call-style)
- [Notificações urgentes e tela cheia](https://developer.android.com/develop/ui/views/notifications/time-sensitive)
- [Parada de foreground services pelo usuário](https://developer.android.com/develop/background-work/services/fgs/handle-user-stopping)
