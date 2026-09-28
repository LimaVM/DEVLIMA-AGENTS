# vm-manager/systemd/devlima-vm-manager.service

Executa o manager no host com diretório e socket privados, credenciais externas e restrições compatíveis com libvirt/KVM.

[Arquivo fonte](../../../../vm-manager/systemd/devlima-vm-manager.service) · 37 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>[Unit]</code> | Abre seção [Unit] do systemd. |
| <a id="L2"></a>2 | <code>Description=DEVLIMA private VM Manager</code> | Define diretiva systemd Description com o valor declarado. |
| <a id="L3"></a>3 | <code>After=libvirtd.service network-online.target</code> | Define diretiva systemd After com o valor declarado. |
| <a id="L4"></a>4 | <code>Wants=network-online.target</code> | Define diretiva systemd Wants com o valor declarado. |
| <a id="L5"></a>5 | <code>Requires=libvirtd.service</code> | Define diretiva systemd Requires com o valor declarado. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L7"></a>7 | <code>[Service]</code> | Abre seção [Service] do systemd. |
| <a id="L8"></a>8 | <code>Type=simple</code> | Define diretiva systemd Type com o valor declarado. |
| <a id="L9"></a>9 | <code>User=root</code> | Define diretiva systemd User com o valor declarado. Define a identidade que executa o serviço. |
| <a id="L10"></a>10 | <code>Group=10001</code> | Define diretiva systemd Group com o valor declarado. |
| <a id="L11"></a>11 | <code>EnvironmentFile=/etc/devlima-vm-manager.env</code> | Define diretiva systemd EnvironmentFile com o valor declarado. Carrega variáveis externas sem embutir valores na unidade. |
| <a id="L12"></a>12 | <code>WorkingDirectory=/opt/devlima-vm-manager</code> | Define diretiva systemd WorkingDirectory com o valor declarado. Define base para caminhos relativos do serviço. |
| <a id="L13"></a>13 | <code>ExecStart=/opt/devlima-vm-manager/venv/bin/uvicorn vm_manager.app:app_factory --factory --uds /run/devlima-vm-manager/api.sock --workers 1 --no-access-log</code> | Define diretiva systemd ExecStart com o valor declarado. Comando executado pela unidade; argumentos/caminho são explícitos. |
| <a id="L14"></a>14 | <code>Restart=on-failure</code> | Define diretiva systemd Restart com o valor declarado. |
| <a id="L15"></a>15 | <code>RestartSec=5</code> | Define diretiva systemd RestartSec com o valor declarado. |
| <a id="L16"></a>16 | <code>RuntimeDirectory=devlima-vm-manager</code> | Define diretiva systemd RuntimeDirectory com o valor declarado. |
| <a id="L17"></a>17 | <code>RuntimeDirectoryMode=0750</code> | Define diretiva systemd RuntimeDirectoryMode com o valor declarado. |
| <a id="L18"></a>18 | <code>StateDirectory=devlima-vm-manager</code> | Define diretiva systemd StateDirectory com o valor declarado. |
| <a id="L19"></a>19 | <code>StateDirectoryMode=0700</code> | Define diretiva systemd StateDirectoryMode com o valor declarado. |
| <a id="L20"></a>20 | <code>UMask=0007</code> | Define diretiva systemd UMask com o valor declarado. |
| <a id="L21"></a>21 | <code>NoNewPrivileges=true</code> | Define diretiva systemd NoNewPrivileges com o valor declarado. |
| <a id="L22"></a>22 | <code>PrivateTmp=true</code> | Define diretiva systemd PrivateTmp com o valor declarado. Isola diretórios temporários do serviço. |
| <a id="L23"></a>23 | <code>ProtectSystem=strict</code> | Define diretiva systemd ProtectSystem com o valor declarado. Restringe escrita nos diretórios do sistema. |
| <a id="L24"></a>24 | <code>ProtectHome=read-only</code> | Define diretiva systemd ProtectHome com o valor declarado. |
| <a id="L25"></a>25 | <code>ReadWritePaths=/var/lib/libvirt/images/devlima-workers /var/lib/devlima-vm-manager /run/devlima-vm-manager</code> | Define diretiva systemd ReadWritePaths com o valor declarado. Permite escrita nos paths declarados sob as restrições da unidade. |
| <a id="L26"></a>26 | <code>ProtectKernelTunables=true</code> | Define diretiva systemd ProtectKernelTunables com o valor declarado. |
| <a id="L27"></a>27 | <code>ProtectKernelModules=true</code> | Define diretiva systemd ProtectKernelModules com o valor declarado. |
| <a id="L28"></a>28 | <code>ProtectControlGroups=true</code> | Define diretiva systemd ProtectControlGroups com o valor declarado. |
| <a id="L29"></a>29 | <code>RestrictSUIDSGID=true</code> | Define diretiva systemd RestrictSUIDSGID com o valor declarado. |
| <a id="L30"></a>30 | <code>LimitNOFILE=4096</code> | Define diretiva systemd LimitNOFILE com o valor declarado. |
| <a id="L31"></a>31 | <code>MemoryHigh=512M</code> | Define diretiva systemd MemoryHigh com o valor declarado. |
| <a id="L32"></a>32 | <code>MemoryMax=1536M</code> | Define diretiva systemd MemoryMax com o valor declarado. |
| <a id="L33"></a>33 | <code>TasksMax=100</code> | Define diretiva systemd TasksMax com o valor declarado. |
| <a id="L34"></a>34 | <code>TimeoutStopSec=6min</code> | Define diretiva systemd TimeoutStopSec com o valor declarado. |
| <a id="L35"></a>35 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L36"></a>36 | <code>[Install]</code> | Abre seção [Install] do systemd. |
| <a id="L37"></a>37 | <code>WantedBy=multi-user.target</code> | Define diretiva systemd WantedBy com o valor declarado. Define alvo systemd utilizado ao habilitar unidade/timer. |
