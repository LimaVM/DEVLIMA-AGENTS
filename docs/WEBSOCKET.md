# Protocolo de conexão — V1

Conexão `wss://agent.vegasolucoes.com.br/ws`. JWT vai no primeiro frame, nunca na URL. Query strings são recusadas. Autenticação precisa chegar em 10 segundos; cada frame tem `event_id` UUID, `type`, `payload` e timestamp opcional do cliente. Servidor inclui timestamp UTC. `protocol=1` é informado em `connection.ready`.

```json
{"event_id":"019f19dc-a6b7-451f-b83a-8495d023d798","type":"connection.authenticate","payload":{"access_token":"JWT","device_id":"019f19dc-a6b7-451f-b83a-8495d023d799","name":"Android"}}
```

Dispositivo recebe um UUID aleatório persistido no app. JWT emitido para uma sessão de dispositivo só permite conectar esse dispositivo. Um novo socket do mesmo dispositivo substitui a conexão anterior. Usuário inativo, versão de token alterada, sessão revogada, dispositivo revogado ou JWT expirado encerram a conexão.

## Autenticação renovável

`POST /auth/login` aceita device_id além de username/password. Retorna access_token de 30 minutos e refresh_token opaco, rotativo, válido por até 30 dias. Um login do mesmo dispositivo revoga sua família anterior. Login sem device_id continua disponível para ferramentas REST e não emite refresh_token.

`POST /auth/refresh` recebe refresh_token e retorna novos tokens. O banco guarda apenas SHA-256 do refresh token aleatório. Cada token só pode ser usado uma vez; reutilização revoga a família e seus JWTs. O cliente serializa refreshes. Reset de senha e desativação invalidam a renovação. O prazo da família é fixo, exigindo novo login ao fim dos 30 dias. Login e refresh compartilham limitação por IP. `POST /auth/logout` revoga a família atual; logout de JWT sem família invalida os tokens antigos desse usuário.

`GET /devices` lista os dispositivos do proprietário. `POST /devices/{id}/revoke` revoga o dispositivo e suas famílias. Não existe cadastro público de usuários.

## Heartbeat e mensagens

Servidor envia `connection.ping` a cada 20s; cliente responde `connection.pong` com payload vazio. Sem resposta por 60s, socket fecha 4408. O transporte também usa ping/pong WebSocket. O Android renova o JWT por HTTPS e reconecta antes da expiração, usando backoff de 1 a 60s com jitter e sinal de retorno da rede.

Cliente envia `chat.message` com payload de ChatSend: content, client_message_id e conversation_id opcional. O event_id do envelope deve ser igual ao client_message_id. Servidor responde `chat.accepted` e `chat.processed`; a resposta humana vem em `agent.message` pela outbox. Só um chat em execução por socket. A inferência roda fora do event loop; heartbeat e entrega continuam durante o processamento.

O Core grava a resposta e seu evento na mesma transação. Replay usa os IDs persistidos e não faz outra inferência/ação. Perder o socket durante um turno pode deixar o processamento terminar no banco; o resultado fica disponível na reconexão/histórico.

Eventos duráveis: agent.message, reminder.triggered, call.incoming, call.cancelled, task.updated e worker.updated. Cada dispositivo tem seu próprio registro EventDelivery. Eventos não confirmados são reenviados após 15s; o dispositivo envia `event.ack` com payload event_id. ACK é idempotente e só confirma um evento enviado ao próprio dispositivo/proprietário. Cancelar um agendamento impede novas entregas de seus eventos antigos.

Entrega é **pelo menos uma vez**. O Android salva o evento em SQLite antes do ACK, deduplica pelo UUID e usa identificador estável da notificação. Payloads locais e tokens são criptografados com AES-GCM/Android Keystore, sem secrets embutidos no APK. ACK confirma persistência no dispositivo, não que o usuário leu o aviso.

Erros usam envelope `error` com código estável, sem eco do payload/tokens. Frames inválidos são recusados; expiração/revogação fecha 4401. Tipos de chamadas/voz serão estendidos na Fase 8.

## Fase 8 — chamadas internas

Cliente envia call.answer/call.reject com payload incoming_event_id UUID; call.end com call_session_id UUID. A identidade do dispositivo vem da conexão autenticada. Resposta efêmera call.command_result confirma a operação; eventos duráveis call.state (payload session/event_id) e call.dismissed (event_id/status) sincronizam os dispositivos.

voice.transcript recebe call_session_id/client_message_id/content (até 4000 caracteres), com event_id igual a client_message_id. O Core verifica sessão ativa/proprietário/dispositivo, usa conversation_id da chamada e conserva idempotência. Resultado agent.message é persistido na outbox. Há um turno em processamento por socket; device_busy é transitório.

Toque expira em 120 segundos desde emissão; ao reconectar, chamada vencida produz MISSED. Sessão sem turno por 10 minutos ou com duração superior a 30 minutos expira; resolução é idempotente. Eventos de lembrete vencidos continuam seguindo a política do scheduler.
