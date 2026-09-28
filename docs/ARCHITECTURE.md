# Arquitetura do DEVLIMA AGENT

## Responsabilidades

Android → HTTPS/WSS → Caddy → Agent Core → PostgreSQL.

O Agent Core valida ações, aplica autorização por usuário, persiste estado e audita operações. A LLM fornece linguagem e ações estruturadas; não é fonte da verdade e não executa shell. PostgreSQL guarda histórico bruto, resumos, memórias, tarefas, agendamentos, eventos e estado dos workers.

O router usa llama.cpp por rede privada, preferencialmente Tailscale. Groq só recebe contexto se `ALLOW_CLOUD_FALLBACK=true` e houver falha técnica permitida. Resposta semanticamente insatisfatória não provoca fallback.

Esse router está implementado na Fase 2: `LLMProvider` → `LlamaCppProvider`/`GroqProvider`, com transporte HTTP compatível e uma única tentativa por provider. Fallback somente por timeout, conexão, 5xx ou erro explícito de modelo indisponível. Erros de autorização/rate limit, JSON inválido e redirects não provocam envio à nuvem. Sem proxy herdado do ambiente e sem seguir redirects.

`llm_requests` registra uma linha por tentativa, correlacionada ao request ID e usuário, com provider/modelo, latência, sucesso/fallback, erro/status e uso de tokens. Não guarda prompts/respostas/chaves; `audit_log` recebe metadados da operação. O recorder faz commit por tentativa; chamadas LLM devem anteceder transações de execução de ações. A persistência de mensagens/contexto será adicionada na Fase 3.

Os endpoints autenticados `/llm/health` e `/llm/chat` permitem validar providers nesta fase. Chat é stateless e não executa ações. O CLI administrativo permite diagnóstico sem criar usuário padrão ou expor JWT.

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

Compose com healthchecks, limites de memória/CPU e restart automático. Migrations executam uma vez antes do backend. A configuração padrão é privada, com Caddy em `127.0.0.1:8443` e `127.0.0.1:8080` para túnel SSH.

Nesta implantação, o domínio fornecido `agent.vegasolucoes.com.br` aponta para o host; Caddy publica 80/443 com certificado público Let’s Encrypt validado externamente. Não foi necessário alterar regras OCI. O modo privado alternativo usa certificado interno, que não é aceito automaticamente pelo Android.

Imagens Python/PostgreSQL/Caddy fixadas por digest e dependências Python por versão exata. Atualizações devem regenerar os pins e executar novamente os testes.

Quotas propostas para a Fase 5 neste host: até 2 workers, 4 vCPUs e 8 GiB RAM somados, reservando pelo menos 4 GiB para host/core/banco. Verificar também RAM disponível, disco e VMs externas ao projeto antes de alocar. O template de 3,5 GiB requer expansão do overlay para 20 GiB, com growpart/resizefs no guest.

## Referências verificadas

- [Docker no Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker e encaminhamento/firewall](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
- [FastAPI em containers](https://fastapi.tiangolo.com/deployment/docker/)
- [HTTPS automático do Caddy](https://caddyserver.com/docs/automatic-https)
