# Segurança

## Limites de confiança

A LLM não acessa credenciais, hypervisor ou shell do host. O backend não monta diretórios do host, chave SSH dos workers, `/dev/kvm`, socket Docker ou socket libvirt. O VM Manager aceita operações validadas/enumeradas e jobs confinados aos guests; nenhum texto de usuário é convertido diretamente em comando shell do host.

JWT assinado com segredo aleatório de pelo menos 32 caracteres, validação de algoritmo, issuer, audience e expiração. Senhas com Argon2id. Redefinição de senha incrementa `token_version`. Sem cadastro público automático; usuários são criados pela CLI, que solicita senha sem eco.

Limitação de login/refresh baseada no banco sobre o IP observado: cinco tentativas por janela de quinze minutos. Respostas de erro não distinguem usuário inexistente e senha inválida. Auditoria não registra senha, token, chave ou conteúdo de `.env`. Buckets expirados são reaproveitados.

Caddy sobrescreve cabeçalhos de encaminhamento recebidos. O backend aceita cabeçalhos de proxy apenas porque sua porta não é publicada e só está acessível na rede de containers controlados; não publicar a porta 8000 diretamente sem revisar essa confiança.

## Secrets e serviços

Secrets residem em `/srv/devlima-agent/.env`, modo 0600, excluído de Git e do contexto Docker. Senhas e JWT são gerados aleatoriamente por script; nenhum usuário com senha padrão é criado.

PostgreSQL fica sem porta publicada. Caddy usa certificados persistentes. Defaults privados restringem portas ao loopback para túnel SSH; TLS interno exige confiar explicitamente na CA. Nesta implantação, o domínio informado usa certificado público Let’s Encrypt e somente 80/443 são publicados pelo projeto. As portas 5432, 8000 e 2019 não aceitaram conexão externa na validação. Nunca desativar validação TLS no app de produção.

A V1 final usa `agent_runtime` no backend/scheduler/runner: CRUD, sem superuser/DDL/TRUNCATE/criação de bancos/roles/bypass RLS e sem escrita na revisão Alembic. `agent_migrate` é proprietária do schema/tabelas e recebe segredo distinto. Administrador fica no PostgreSQL e na ferramenta isolada `db-admin`; não chega ao Core HTTP. Provisionamento reaplicável em `scripts/provision_database_roles.py` e verificação real em `scripts/check_database_privileges.py`.

llama.cpp permanece na Tailscale. VM Manager usa Unix socket com token próprio, restrito a root/GID 10001 e acessível apenas pelo runner. Scheduler/runner não recebem a credencial Groq nem o JWT real; backend HTTP não recebe token/socket do manager. Tailscale requer autorização do proprietário da tailnet.

Atualização Fase 2: Tailscale foi encontrado ativo e autorizado pelo proprietário, IP do Core `100.108.84.64`, LLM `100.102.91.22`. A configuração existente da VPN foi preservada. O backend confirmou comunicação pela rede privada; não foi publicada porta da LLM.

URL da LLM primária é configuração administrativa validada: IP privado/loopback, CGNAT Tailscale ou hostname `.ts.net`, sem credenciais/query/fragment. A URL do Groq é fixa em HTTPS. O client ignora proxies do ambiente e recusa redirects. `ALLOW_CLOUD_FALLBACK=false` impede qualquer requisição cloud; com flag true, apenas falhas técnicas enumeradas permitem enviar contexto.

Testes usam credential fictícia e rede de banco isolada, sem herdar a chave real Groq. Telemetria grava apenas metadados de inferência; mensagens/respostas do usuário não são copiadas para logs. Erros retornam códigos estáveis e nunca o corpo bruto do upstream. Endpoints LLM exigem autenticação e limitam quantidade/tamanho de mensagens e tokens.

## Host e template

Na Fase 3, conversas, mensagens, resumos, memórias e candidatos exigem JWT e são consultados por proprietário. Ações propostas passam por allowlist e schemas; não executam shell ou operações nesta fase. UUID idempotente, lease e verificação de propriedade do turno impedem repetição da gravação e finalização por uma execução antiga.

Histórico bruto contém o que o usuário enviou, inclusive conteúdo sensível que ele possa digitar; resumos também podem carregar fatos desse histórico. O filtro de candidatos recusa formatos conhecidos de segredos e não é um mecanismo universal de DLP. Desativar memória não remove mensagens/resumos anteriores. A proteção do banco e backups e a flag de fallback são, portanto, relevantes para todo o contexto. O smoke real da Fase 3 usa somente dados sintéticos no banco separado, sem chave Groq e com cloud desligado.

Não remover regras Oracle/libvirt, não executar `iptables -F`, não recriar pools/redes e não tocar VMs externas ao projeto. Antes da instalação Docker, salvar regras para comparação. A configuração `ip-forward-no-drop` preserva a política de encaminhamento; as cadeias Docker adicionadas devem coexistir com as cadeias existentes.

O template existente não é modificado. O VM Manager valida IDs UUID e paths dentro do diretório de workers, rejeita traversal/symlinks externos/paths do cliente/operações contra o template. Domínios gerenciados carregam metadados de propriedade; VMs externas são recusadas. Quotas e recursos livres são revalidados. Filtro libvirt bloqueia saída nova para redes privadas, Tailscale, metadata e Core; jobs executam dentro do guest com limites. Detalhes em [VM Manager](../vm-manager/README.md).

Operações destrutivas no host requerem autorização expressa. Workers descartáveis gerenciados podem ser resetados/destruídos mediante autorização do Agent Core, com auditoria.

## Auditoria e recuperação

Auditoria registra login/criação/reset de usuário, ações/provider/latência e workers. Não inclui secrets em metadados ou logs HTTP. IDs de requisição correlacionam operações sem registrar corpos completos.

Backup via `pg_dump` e cópia consistente do manager, envelope AES-256-GCM e chave externa 0600. Cópia cifrada externa no Mac e restore em banco exclusivo temporário foram verificados. Backup contém secrets e assinatura Android; guest disks/snapshots são excluídos. A cópia externa automática depende do Mac ligado. [Cobertura e recuperação](RECOVERY.md). Não usar `docker compose down -v` no host.

Android guarda tokens/eventos com AES-GCM/Keystore e diretórios privados sem backup automático. WSS autentica no primeiro frame, sem token na URL; refresh rotativo, revogação e ACK por dispositivo. Chamadas e transcrições exigem proprietário/dispositivo e UUID idempotente. Reconhecimento/TTS usam engines do aparelho, que podem depender da rede; nenhum contrato de reconhecimento totalmente offline é prometido. Homologação física ainda pendente.

Pontos existentes identificados: rpcbind escuta em todas as interfaces; alcance público depende do firewall/OCI. O template está em modo 0644 com owner libvirt-qemu. Ambos foram documentados e preservados nesta fase.
