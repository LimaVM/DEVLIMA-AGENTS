# Arquitetura do DEVLIMA AGENT

## Responsabilidades

Android → HTTPS/WSS → Caddy → Agent Core → PostgreSQL.

O Agent Core valida ações, aplica autorização por usuário, persiste estado e audita operações. A LLM fornece linguagem e ações estruturadas; não é fonte da verdade e não executa shell. PostgreSQL guarda histórico bruto, resumos, memórias, tarefas, agendamentos, eventos e estado dos workers.

O router usará llama.cpp por rede privada, preferencialmente Tailscale. Groq só receberá contexto se `ALLOW_CLOUD_FALLBACK=true` e houver falha técnica permitida. Resposta semanticamente insatisfatória não provoca fallback.

## Processos e isolamento

- **backend:** FastAPI/SQLAlchemy/Pydantic; container não root, sem acesso ao host, libvirt ou socket Docker.
- **postgres:** volume persistente, rede Docker interna, nenhuma porta publicada.
- **scheduler (Fase 4):** processo separado, PostgreSQL como fonte da verdade; APScheduler acorda o processo, mas os eventos duráveis serão reivindicados transacionalmente com lock e identificador idempotente. Não depender de timers em memória.
- **caddy:** TLS, proxy HTTP e WebSocket; dados de certificados persistentes.
- **vm-manager (Fase 5):** serviço systemd no host, API privada autenticada de operações enumeradas. Privilégios limitados ao necessário para libvirt. Core não recebe shell no host.
- **workers:** overlays QCOW2 do template existente, cloud-init individual, rede libvirt default NAT.

Na Fase 1 há somente backend, banco, migration runner e Caddy. Não há scheduler fictício ou VM Manager privilegiado sem implementação.

## Dados e evolução

Migrations explícitas versionam o schema. Nenhum `create_all` no startup de produção. Fase 1 inclui usuários, auditoria e buckets persistentes de limitação de login. As demais tabelas chegam com a respectiva funcionalidade; todas as relações terão escopo por usuário.

Timestamps em UTC com timezone; preferências do usuário armazenam `America/Sao_Paulo` por padrão. Identificadores UUID. JWT de curta duração; `token_version` permite invalidar sessões ao redefinir senha/desativar usuário.

Histórico bruto é preservado; Context Builder compõe janela limitada, resumo, memórias e estado relevante. Candidatos de memória e ações da LLM passam por schemas/validação antes de persistência. pgvector fica reservado para evolução.

Entrega de lembretes/chamadas usará outbox persistente, ACK por dispositivo e deduplicação por `event_id`. Rede não permite prometer entrega exatamente uma vez: servidor e Android devem tolerar reenvios após perda de conexão.

## Deploy e recursos

Compose com healthchecks, limites de memória/CPU e restart automático. Migrations executam uma vez antes do backend. A Fase 1 publica apenas Caddy em `127.0.0.1:8443` e `127.0.0.1:8080` para túnel SSH; não depende de abertura de portas OCI.

HTTPS público será ativado com domínio confirmado, DNS correto e regras de ingresso verificadas. Certificado interno da Fase 1 não é aceito automaticamente pelo Android.

Quotas propostas para a Fase 5 neste host: até 2 workers, 4 vCPUs e 8 GiB RAM somados, reservando pelo menos 4 GiB para host/core/banco. Verificar também RAM disponível, disco e VMs externas ao projeto antes de alocar. O template de 3,5 GiB requer expansão do overlay para 20 GiB, com growpart/resizefs no guest.

## Referências verificadas

- [Docker no Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker e encaminhamento/firewall](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
- [FastAPI em containers](https://fastapi.tiangolo.com/deployment/docker/)
- [HTTPS automático do Caddy](https://caddyserver.com/docs/automatic-https)
