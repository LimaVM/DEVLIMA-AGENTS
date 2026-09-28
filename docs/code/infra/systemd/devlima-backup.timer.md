# infra/systemd/devlima-backup.timer

Agenda a execução do backup no host, incluindo persistência de disparos perdidos e atraso aleatório configurado.

[Arquivo fonte](../../../../infra/systemd/devlima-backup.timer) · 8 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>[Unit]</code> | Abre seção [Unit] do systemd. |
| <a id="L2"></a>2 | <code>Description=Daily encrypted DEVLIMA backup</code> | Define diretiva systemd Description com o valor declarado. |
| <a id="L3"></a>3 | <code>[Timer]</code> | Abre seção [Timer] do systemd. |
| <a id="L4"></a>4 | <code>OnCalendar=*-*-* 03:30:00 UTC</code> | Define diretiva systemd OnCalendar com o valor declarado. Define calendário de disparo do timer. |
| <a id="L5"></a>5 | <code>Persistent=true</code> | Define diretiva systemd Persistent com o valor declarado. Controla recuperação de disparos do timer perdidos durante desligamento. |
| <a id="L6"></a>6 | <code>RandomizedDelaySec=300</code> | Define diretiva systemd RandomizedDelaySec com o valor declarado. Distribui disparos por atraso aleatório. |
| <a id="L7"></a>7 | <code>[Install]</code> | Abre seção [Install] do systemd. |
| <a id="L8"></a>8 | <code>WantedBy=timers.target</code> | Define diretiva systemd WantedBy com o valor declarado. Define alvo systemd utilizado ao habilitar unidade/timer. |
