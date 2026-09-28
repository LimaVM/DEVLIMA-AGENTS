# infra/systemd/devlima-backup.service

Executa backup autenticado como serviço oneshot com diretórios e restrições explícitos; não instala um servidor adicional.

[Arquivo fonte](../../../../infra/systemd/devlima-backup.service) · 13 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>[Unit]</code> | Abre seção [Unit] do systemd. |
| <a id="L2"></a>2 | <code>Description=Authenticated encrypted DEVLIMA backup</code> | Define diretiva systemd Description com o valor declarado. |
| <a id="L3"></a>3 | <code>After=docker.service</code> | Define diretiva systemd After com o valor declarado. |
| <a id="L4"></a>4 | <code>Requires=docker.service</code> | Define diretiva systemd Requires com o valor declarado. |
| <a id="L5"></a>5 | <code>[Service]</code> | Abre seção [Service] do systemd. |
| <a id="L6"></a>6 | <code>Type=oneshot</code> | Define diretiva systemd Type com o valor declarado. Termina após o comando, sem manter processo servidor. |
| <a id="L7"></a>7 | <code>User=root</code> | Define diretiva systemd User com o valor declarado. Define a identidade que executa o serviço. |
| <a id="L8"></a>8 | <code>WorkingDirectory=/srv/devlima-agent</code> | Define diretiva systemd WorkingDirectory com o valor declarado. Define base para caminhos relativos do serviço. |
| <a id="L9"></a>9 | <code>ExecStart=/usr/bin/python3 /srv/devlima-agent/scripts/backup.py</code> | Define diretiva systemd ExecStart com o valor declarado. Comando executado pela unidade; argumentos/caminho são explícitos. |
| <a id="L10"></a>10 | <code>UMask=0077</code> | Define diretiva systemd UMask com o valor declarado. |
| <a id="L11"></a>11 | <code>Nice=10</code> | Define diretiva systemd Nice com o valor declarado. |
| <a id="L12"></a>12 | <code>MemoryMax=768M</code> | Define diretiva systemd MemoryMax com o valor declarado. |
| <a id="L13"></a>13 | <code>CPUQuota=50%</code> | Define diretiva systemd CPUQuota com o valor declarado. |
