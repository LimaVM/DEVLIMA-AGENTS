# vm-manager/vm_manager/config.py

Define configuração de paths, quotas, rede/template e carregamento protegido do token; VMError contém somente código/status públicos.

[Arquivo fonte](../../../../vm-manager/vm_manager/config.py) · 39 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [Settings](#L8) | Define o tipo Settings e reúne o estado/contrato descrito para este módulo. |
| [Settings.secure_token](#L28) | Implementa Settings.secure_token como parte do fluxo descrito para este arquivo. |
| [VMError](#L35) | Define o tipo VMError e reúne o estado/contrato descrito para este módulo. |
| [VMError.__init__](#L37) | Inicializa VMError com as dependências e estado declarados. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>from pydantic import SecretStr, field_validator</code> | Importa SecretStr, field_validator de pydantic. |
| <a id="L4"></a>4 | <code>from pydantic_settings import BaseSettings, SettingsConfigDict</code> | Importa BaseSettings, SettingsConfigDict de pydantic_settings. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code># Documentação: Define o tipo Settings e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Settings e reúne o estado/contrato descrito para este módulo. |
| <a id="L8"></a>8 | <code>class Settings(BaseSettings):</code> | Define o tipo Settings e reúne o estado/contrato descrito para este módulo. |
| <a id="L9"></a>9 | <code>    model_config = SettingsConfigDict(env_prefix=&quot;VM_MANAGER_&quot;, hide_input_in_errors=True)</code> | Define model_config com SettingsConfigDict(env_prefix=&#x27;VM_MANAGER_&#x27;, hide_input_in_errors=True). Invoca SettingsConfigDict com os argumentos declarados nesta instrução. Argumentos: env_prefix=&#x27;VM_MANAGER_&#x27;, hide_input_in_errors=True |
| <a id="L10"></a>10 | <code>    token: SecretStr</code> | Define token com None. |
| <a id="L11"></a>11 | <code>    state_root: Path = Path(&quot;/var/lib/devlima-vm-manager&quot;)</code> | Define state_root com Path(&#x27;/var/lib/devlima-vm-manager&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/var/lib/devlima-vm-manager&#x27; |
| <a id="L12"></a>12 | <code>    worker_root: Path = Path(&quot;/var/lib/libvirt/images/devlima-workers&quot;)</code> | Define worker_root com Path(&#x27;/var/lib/libvirt/images/devlima-workers&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/var/lib/libvirt/images/devlima-workers&#x27; |
| <a id="L13"></a>13 | <code>    template: Path = Path(&quot;/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2&quot;)</code> | Define template com Path(&#x27;/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2&#x27; |
| <a id="L14"></a>14 | <code>    template_sha256: str = &quot;6a81c37564db9b1ee84e141922625e1d7c5b389b99bb3c572e0243607d5bb4d2&quot;</code> | Define template_sha256 com &#x27;6a81c37564db9b1ee84e141922625e1d7c5b389b99bb3c572e0243607d5bb4d2&#x27;. |
| <a id="L15"></a>15 | <code>    ssh_private_key: Path = Path(&quot;/root/.ssh/agent_worker&quot;)</code> | Define ssh_private_key com Path(&#x27;/root/.ssh/agent_worker&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/root/.ssh/agent_worker&#x27; |
| <a id="L16"></a>16 | <code>    ssh_public_key: Path = Path(&quot;/root/.ssh/agent_worker.pub&quot;)</code> | Define ssh_public_key com Path(&#x27;/root/.ssh/agent_worker.pub&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/root/.ssh/agent_worker.pub&#x27; |
| <a id="L17"></a>17 | <code>    max_workers: int = 2</code> | Define max_workers com 2. |
| <a id="L18"></a>18 | <code>    max_total_vcpu: int = 4</code> | Define max_total_vcpu com 4. |
| <a id="L19"></a>19 | <code>    max_total_ram_mb: int = 8192</code> | Define max_total_ram_mb com 8192. |
| <a id="L20"></a>20 | <code>    host_ram_reserve_mb: int = 4096</code> | Define host_ram_reserve_mb com 4096. |
| <a id="L21"></a>21 | <code>    disk_reserve_gb: int = 10</code> | Define disk_reserve_gb com 10. |
| <a id="L22"></a>22 | <code>    network: str = &quot;default&quot;</code> | Define network com &#x27;default&#x27;. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code>    @field_validator(&quot;token&quot;)</code> | Aplica o decorator field_validator(&quot;token&quot;) à definição que segue. |
| <a id="L25"></a>25 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L26"></a>26 | <code>    # Documentação: Implementa Settings.secure_token como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa Settings.secure_token como parte do fluxo descrito para este |
| <a id="L27"></a>27 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L28"></a>28 | <code>    def secure_token(cls, value):</code> | Implementa Settings.secure_token como parte do fluxo descrito para este arquivo. |
| <a id="L29"></a>29 | <code>        if len(value.get_secret_value()) &lt; 32:</code> | Executa este ramo somente se len(value.get_secret_value()) &lt; 32; caso contrário, segue o ramo alternativo. |
| <a id="L30"></a>30 | <code>            raise ValueError(&quot;Manager token must have at least 32 characters&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Manager token must have at least 32 characters&#x27;). |
| <a id="L31"></a>31 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L32"></a>32 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L33"></a>33 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L34"></a>34 | <code># Documentação: Define o tipo VMError e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo VMError e reúne o estado/contrato descrito para este módulo. |
| <a id="L35"></a>35 | <code>class VMError(Exception):</code> | Define o tipo VMError e reúne o estado/contrato descrito para este módulo. |
| <a id="L36"></a>36 | <code>    # Documentação: Inicializa VMError com as dependências e estado declarados.</code> | Comentário: Documentação: Inicializa VMError com as dependências e estado declarados. |
| <a id="L37"></a>37 | <code>    def __init__(self, code, status=409):</code> | Inicializa VMError com as dependências e estado declarados. |
| <a id="L38"></a>38 | <code>        self.code, self.status = code, status</code> | Define (self.code, self.status) com (code, status). |
| <a id="L39"></a>39 | <code>        super().__init__(code)</code> | Invoca super().__init__ com os argumentos declarados nesta instrução. Argumentos: code |
