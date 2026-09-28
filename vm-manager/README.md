# VM Manager Linux

Serviço root privado no host libvirt, com API apenas em `/run/devlima-vm-manager/api.sock`. O Core registra comandos no PostgreSQL; `worker-runner` acessa esse socket usando token e GID 10001. O backend HTTP não monta socket libvirt, Docker, chave SSH ou o socket do manager. Nenhuma porta TCP é criada pelo manager.

## Instalação na VPS

Pré-requisitos: Ubuntu 24.04, Python 3.12/venv, libvirt/KVM, `python3-libvirt`, qemu-img, cloud-localds, template e chave de workers já existentes. O instalador verifica/retém o token em arquivos 0600, instala um venv com os bindings libvirt do sistema e ativa a unidade systemd.

```sh
cd /srv/devlima-agent
sudo python3 scripts/install_vm_manager.py
sudo systemctl status devlima-vm-manager
```

O código fica em `/opt/devlima-vm-manager`. Registro, operações, snapshots e auditoria ficam em SQLite/WAL sob `/var/lib/devlima-vm-manager` (0700). Imagens ficam em diretórios UUID sob `/var/lib/libvirt/images/devlima-workers`. Chave privada e template permanecem nos paths originais; o template é verificado por SHA-256 e nunca recebe escritas pela aplicação.

## Contrato privado

Bearer obrigatório em todas as rotas. `POST /v1/operations` recebe `request_id`, `worker_id`, `owner` (UUIDs), `kind` e argumentos tipados. Tipos: CREATE, START, STOP, DESTROY, RESET, SNAPSHOT, RESTORE, EXECUTE. CREATE aceita nome lógico e recursos; SNAPSHOT/RESTORE exigem snapshot_id; EXECUTE aceita script (até 8000 caracteres) e timeout (até 300 segundos). Não existe operação de shell no host.

`GET /v1/operations/{id}?owner=UUID` permite recuperar resultado sem repetir a operação. `GET /v1/workers/{id}?owner=UUID` consulta libvirt, DHCP, SSH e guest-agent; `GET /v1/workers?owner=UUID` lista o registro. `GET /health` exige o mesmo token.

O request_id é globalmente único: replay concluído retorna resultado salvo; argumentos diferentes retornam conflito. Após um crash, o manager confirma operações de lifecycle que podem ser provadas pelo estado real. Jobs, reset, snapshot e restore incertos ficam FAILED/operation_recovery_required; o serviço não repete scripts automaticamente. Um novo pedido explícito pode iniciar uma nova operação.

## Proteções e comportamento

- Metadados XML identificam UUID e proprietário, e o disco deve apontar ao diretório registrado. Domínios externos e storage fora desse diretório são recusados.
- Até 2 workers, 4 vCPUs e 8192 MiB somados; reserva de 4096 MiB de memória, 1 CPU do host e 10 GiB de disco. A contagem CPU também considera outros domínios ativos. Recursos e disco são revalidados antes de alocar.
- Rede NAT default preservada. O filtro próprio `devlima-worker-egress` referencia `clean-traffic`, bloqueia novas conexões para redes privadas/Tailscale, metadata e IP público do Core, e permite DNS/DHCP e respostas a conexões existentes. Não altera filtros nem domínios externos. Definição baseada na [documentação libvirt](https://libvirt.org/formatnwfilter.html).
- READY exige cloud-init concluído, SSH com chave e qemu-guest-agent disponível. BOOTING não é tratado como sucesso de prontidão.
- Snapshots são cópias QCOW2 independentes feitas com o worker desligado, identificadas por UUID/checksum, máximo cinco por worker. Worker previamente ligado é religado. Restore verifica checksum antes de substituir o disco.
- Reset recria overlay e seed com novo instance-id, mantendo snapshots. Destroy remove apenas o domínio e diretório gerenciados e marca seus snapshots apagados.
- Stop tenta desligamento limpo por 45s e força parada apenas do worker gerenciado. Não há autostart de workers após reboot; estado STOPPED é reconciliado e START revalida recursos.
- Jobs usam SSH somente para IP DHCP do worker, executam dentro dele por systemd-run com limite de tempo/memória/processos e saída de até 16000 bytes. SSH incerto não dispara repetição automática. O worker é um ambiente descartável com sudo; jobs autorizados podem alterar seu próprio sistema.
- WindowsWorkerProvider tem interface reservada e retorna 501; Windows completo está fora da V1.

## Testes

Testes fake não criam VMs. `scripts/smoke_vm_manager.py`, executado como root na VPS, cria um worker novo e percorre execução, isolamento de rede, snapshot/restore, stop/start, reset e destroy, verificando replay e checksum do template. Não reutiliza nem apaga domínios existentes.

```sh
sudo python3 -u scripts/smoke_vm_manager.py
```
