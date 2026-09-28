# Segurança

## Limites de confiança

A LLM não acessa credenciais, hypervisor ou shell do host. O backend não monta diretórios do host, chave SSH dos workers, `/dev/kvm`, socket Docker ou socket libvirt. O futuro VM Manager aceitará apenas operações validadas e enumeradas; nunca texto convertido diretamente em comando shell.

JWT assinado com segredo aleatório de pelo menos 32 caracteres, validação de algoritmo, issuer, audience e expiração. Senhas com Argon2id. Redefinição de senha incrementa `token_version`. Sem cadastro público automático; usuários são criados pela CLI, que solicita senha sem eco.

Limitação de login baseada no banco sobre o IP observado: cinco tentativas por janela de quinze minutos. Respostas de erro não distinguem usuário inexistente e senha inválida. Banco não registra senha, token, chave ou conteúdo de `.env`. Buckets expirados são reaproveitados; sua limpeza periódica será adicionada ao scheduler.

Caddy sobrescreve cabeçalhos de encaminhamento recebidos. O backend aceita cabeçalhos de proxy apenas porque sua porta não é publicada e só está acessível na rede de containers controlados; não publicar a porta 8000 diretamente sem revisar essa confiança.

## Secrets e serviços

Secrets residem em `/srv/devlima-agent/.env`, modo 0600, excluído de Git e do contexto Docker. Senhas e JWT são gerados aleatoriamente por script; nenhum usuário com senha padrão é criado.

PostgreSQL fica sem porta publicada. Caddy usa certificados persistentes. Na Fase 1, as portas de Caddy ficam restritas ao loopback e são acessadas por túnel SSH; TLS interno exige confiar explicitamente na CA. Nunca desativar validação TLS no app de produção.

llama.cpp e VM Manager permanecerão privados. Para conexão ao VM Manager preferir rede dedicada/ACL e token próprio, sem reaproveitar JWT de usuário. Tailscale requer autorização do proprietário da tailnet e ainda não foi configurado.

## Host e template

Não remover regras Oracle/libvirt, não executar `iptables -F`, não recriar pools/redes e não tocar VMs externas ao projeto. Antes da instalação Docker, salvar regras para comparação. A configuração `ip-forward-no-drop` preserva a política de encaminhamento; as cadeias Docker adicionadas devem coexistir com as cadeias existentes.

O template existente não é modificado. O VM Manager deverá validar IDs UUID e resolver paths dentro do diretório de workers; rejeitar traversal, symlinks fora do diretório, caminhos fornecidos pelo cliente e operações contra o template. Domínios gerenciados devem carregar metadados de propriedade; uma VM externa nunca é apagada por nome parecido.

Operações destrutivas no host requerem autorização expressa. Workers descartáveis gerenciados podem ser resetados/destruídos mediante autorização do Agent Core, com auditoria.

## Auditoria e recuperação

Registrar login bem-sucedido/falho, criação/reset de usuário e futuramente ações, provider, latência e workers. Não incluir secrets em metadados ou logs HTTP. IDs de requisição correlacionam operações sem registrar corpos completos.

Backup via `pg_dump` comprimido e permissões 0600; testar restauração em banco separado. Persistência do volume não substitui backup externo. Não usar `docker compose down -v` no host. Procedimento completo e testes de recuperação entram na Fase 9.

Pontos existentes identificados: rpcbind escuta em todas as interfaces; alcance público depende do firewall/OCI. O template está em modo 0644 com owner libvirt-qemu. Ambos foram documentados e preservados nesta fase.
