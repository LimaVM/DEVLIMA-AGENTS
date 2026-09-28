# Backup e recuperação

## Cobertura

O arquivo `.dlag` contém dump PostgreSQL, manifesto com commit/checksums, `.env`, credencial operacional privada, config/token do manager, cópia consistente de seu SQLite, chave SSH dos workers e keystore/properties de assinatura Android. A opção `--include-template` inclui a imagem base Ubuntu original; ela foi usada na cópia final externa da V1. Backups diários menores referenciam seu checksum e dispensam repetir os ~597 MiB da imagem.

Discos/snapshots dos guests **não são incluídos**. Os workers são descartáveis; preserve resultados necessários fora deles antes de reset/destroy ou falha do host. Metadados de um worker não substituem seu disco. Certificados Caddy podem ser reemitidos via DNS/ACME; código vem do Git; SDK/JDK/emulador são reinstaláveis. A autorização Tailscale do novo host exige acesso à tailnet e não vem no backup.

Criptografia AES-256-GCM autentica o envelope; SHA-256 auxilia conferência de transferência. Chave externa binária: `/etc/devlima-backup.key`, root 0600; sua cópia privada fica em `backups/devlima-backup.key` no Mac. Sem ela, o backup não pode ser recuperado. Preserve também a chave SSH de acesso à VPS em local seguro; ela não faz parte do arquivo.

## Rotina existente

Unidades em `infra/systemd/` instaladas em `/etc/systemd/system`: timer diário 03:30 UTC, aleatoriedade até 300 s, execução perdida recuperada quando o host volta. Arquivos em `/srv/devlima-agent/backups`, modo 0600, retenção de 14 arquivos automáticos. Dumps antigos pré-migration não são removidos por essa retenção.

A unidade foi realmente iniciada via systemctl e terminou com Result=success/ExecMainStatus=0 após a correção 1.0.1. A consulta ao commit usa safe.directory apenas para o projeto atual, sem confiar globalmente em outros repositórios. O LaunchAgent foi iniciado via launchctl e terminou com exit code 0, copiando o backup cifrado para o Mac.

```sh
cd /srv/devlima-agent
sudo python3 scripts/backup.py
sudo python3 scripts/backup.py --include-template
sudo systemctl list-timers devlima-backup.timer
sudo journalctl -u devlima-backup.service -n 30 --no-pager
```

A cópia externa está em `/Users/devlima/Desktop/DEVLIMA-AGENTS/backups/offsite`. O LaunchAgent `com.vegasolucoes.devlima-backup` chama o script à 01:00 local; log privado em `backups/pull-backups.log`. Depende do Mac ligado/rede/SSH. Não há retenção automática da cópia externa, para preservar também o arquivo com template. Execução manual no Mac:

```sh
python3 scripts/pull_backups.py --key DEVLIMA-AGENTS.key --directory backups/offsite
```

O script exige host key já verificada, copia por SSH, confere checksum e só então renomeia o arquivo parcial. Guarde uma cópia do arquivo com template e da chave em armazenamento independente adicional se o Mac deixar de ser o destino permanente.

## Validar restore sem alterar produção

Requer Python 3.12 e `python3-cryptography` na VPS. O verificador autentica o arquivo antes de extrair, recusa paths inseguros, confere hashes e restaura exclusivamente em um banco `restore_validation_<UUID>`; ele o apaga ao terminar. Nunca aponta para o banco operacional.

```sh
sudo python3 scripts/restore_validate.py backups/devlima-AAAAMMDDTHHMMSSZ.dlag
```

Resultado validado: revisão `0007_calls`; duas contas (operacional e validação), seis mensagens sintéticas, três agendamentos e uma sessão de chamada. O usuário de validação foi posteriormente desativado; o backup final guarda esse estado.

Para autenticar/extrair offline no Mac, use o Python do ambiente privado `build/backup-tools` com cryptography instalado:

```sh
build/backup-tools/bin/python scripts/restore_validate.py backups/offsite/devlima-AAAAMMDDTHHMMSSZ.dlag --key backups/devlima-backup.key --extract-to backups/restore-private
```

O diretório deve ser novo e privado. A extração contém secrets em plaintext: mantenha-o 0700, confira somente metadados necessários e remova essa cópia temporária depois do uso. Não abra/sincronize seu conteúdo em serviços públicos.

## Recuperar um host perdido

Procedimento para **host novo e banco vazio**, sem tentar sobrescrever a produção existente:

1. Instale Ubuntu 24.04, Docker/Compose, Python 3.12/cryptography e dependências libvirt/KVM. Clone a versão do Git indicada no manifesto para `/srv/devlima-agent`. Transfira o backup e a chave separadamente, por canal privado.
2. Autentique e extraia com `restore_validate.py --extract-to` em diretório novo. Restaure `config/core.env` como `/srv/devlima-agent/.env` 0600 e a credencial operacional em `backups/` 0600. Não execute `init_env.py`, pois ele criaria identidades diferentes.
3. Construa backend/db-admin e suba **somente PostgreSQL** com volume novo. Provisione roles; restaure o dump no banco vazio com `pg_restore --single-transaction --exit-on-error --no-owner --no-acl`, via stdin de `docker compose exec -T postgres`, usando o administrador definido no `.env`. Não coloque sua senha na linha de comando. Reaplique os grants para transferir a propriedade dos objetos à role de migration; confira `alembic current/check` antes de iniciar os serviços.
4. Reinstale rede/pool libvirt somente após inspecionar o novo host. Restaure a imagem base no path original, confira o SHA-256 registrado e use owner `libvirt-qemu:kvm`, modo 0644. Restaure chave worker root 0600 e pública 0644. O instalador do manager verifica o template.
5. Antes de iniciar o manager, restaure seu env root 0600 e SQLite em `/var/lib/devlima-vm-manager/registry.sqlite3`, diretório root 0700. Sem os discos dos guests, não tente iniciar os workers antigos; revise a reconciliação e crie novos workers descartáveis. Não habilite autostart indiscriminado.
6. Restaure keystore/properties em `/srv/devlima-build-tools` com owner do build e modo 0600. Preserve alias/senha/certificado para que futuros APKs atualizem o app instalado. Reinstale SDK/JDK conforme documentação Android.
7. Inicie manager, backend/scheduler/runner/Caddy; autorize Tailscale e confira DNS/TLS/saúde, usuário, histórico, agendamentos e permissões runtime. Só troque o DNS/ingresso depois da validação do host recuperado. Instale timer e destino externo novamente.

O restore PostgreSQL e a extração autenticada foram realmente executados; reconstrução integral de uma segunda VPS não foi executada nesta sessão. A rotina não promete RPO zero: dump e metadados são consistentes individualmente, mas não constituem uma transação distribuída entre PostgreSQL e libvirt/SQLite.
