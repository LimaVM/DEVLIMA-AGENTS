# Configuração externa e credenciais

O repositório contém código e exemplos de configuração; os valores operacionais ficam nos arquivos privados abaixo. O gerador da referência lê somente arquivos versionados e não copia esses arquivos para os guias.

| Componente | Arquivo/local | Conteúdo e uso |
| --- | --- | --- |
| Core/PostgreSQL/Groq | `/srv/devlima-agent/.env` | Segredos JWT, credenciais de banco/roles, API key Groq e token do manager. Docker Compose injeta apenas variáveis necessárias a cada serviço. |
| Exemplo de implantação | `.env.example` | Nomes, valores de exemplo e opções disponíveis. `scripts/init_env.py` cria configuração nova e recusa sobrescrever uma existente. |
| Usuário operacional | `backups/operator-credentials.json` privado | Servidor, usuário e senha entregues ao proprietário. Senha do usuário no PostgreSQL é armazenada como hash Argon2. |
| Android release | `/srv/devlima-build-tools/signing.properties` e `agent-release.jks` | Caminho do keystore, alias e senhas de assinatura. O build na VPS lê esses arquivos externos; conserve o certificado para atualizações do app. |
| Android em execução | Android Keystore e `no_backup/session.bin` | Chave AES não exportada, sessão/token cifrados e identificador do dispositivo. A senha de login não é persistida pelo app. |
| Manager | Configuração/arquivo de token externo, referenciado pelo serviço systemd | Autentica API por Unix socket. Core/runner recebem o valor apropriado, sem acesso arbitrário ao host. |
| SSH da VPS | Chave SSH dedicada no workspace privado | Acessa `ubuntu` no host autorizado; não é distribuída com APK ou clone. |
| SSH dos workers | `/root/.ssh/agent_worker` e `.pub` no host | Identidade dedicada à comunicação com workers descartáveis. Preserve esses arquivos e suas permissões. |
| Backup | `/etc/devlima-backup.key` no host e cópia externa privada | Chave de envelope AES-GCM; arquivos `.dlag` contêm pacote autenticado/cifrado. Restore depende da chave externa correta. |
| E2E Android | `no_backup/e2e-private.json`, somente no package debug | Credencial temporária de conta sintética. O teste remove o arquivo após login; conta/dispositivo devem ser revogados ao terminar. |

Use [OPERATIONS.md](OPERATIONS.md) para provisionamento/atualização e [RECOVERY.md](RECOVERY.md) para recuperação. Permissões de arquivos privados e valores reais não são inferidos pelo guia de código. Repositório privado não altera o formato operacional de entrega desses valores: eles permanecem separados do histórico Git e dos artefatos públicos de código.

## Principais variáveis

| Variável | Finalidade |
| --- | --- |
| `POSTGRES_PASSWORD` | Administração inicial do banco; não é a credencial de runtime do Core. |
| `RUNTIME_POSTGRES_PASSWORD` | Papel restrito utilizado pelo Core/scheduler/runner. |
| `MIGRATION_POSTGRES_PASSWORD` | Papel capaz de aplicar migrations. |
| `JWT_SECRET` | Assinatura JWT; configuração exige comprimento mínimo. |
| `GROQ_API_KEY` | Autenticação do provider de fallback; permanece no backend. |
| `VM_MANAGER_TOKEN` | Autenticação privada de comandos do manager. |
| `LOCAL_LLM_BASE_URL` / `LOCAL_LLM_MODEL` | Endpoint privado/modelo primário; a URL não aceita credenciais embutidas. |
| `ALLOW_CLOUD_FALLBACK` | Permite fallback somente quando a política classifica a falha como elegível. |

Modificar um segredo exige atualizar o arquivo externo e reiniciar/recarregar o componente adequado. Não confunda troca de senha do usuário, revogação de dispositivo/família e mudança do segredo JWT: cada operação tem impacto e fluxo próprios descritos no código e na operação.
