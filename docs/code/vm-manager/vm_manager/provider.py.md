# vm-manager/vm_manager/provider.py

Define interface WorkerProvider para lifecycle de VMs e execução permitida, separando o serviço de coordenação da implementação libvirt.

[Arquivo fonte](../../../../vm-manager/vm_manager/provider.py) · 39 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [WorkerProvider](#L5) | Define o tipo WorkerProvider e reúne o estado/contrato descrito para este módulo. |
| [WorkerProvider.close](#L10) | Libera WorkerProvider.close, segundo o contrato e as verificações deste módulo. |
| [WorkerProvider.check_resources](#L13) | Confere WorkerProvider.check_resources, segundo o contrato e as verificações deste módulo. |
| [WorkerProvider.create](#L15) | Cria WorkerProvider.create, segundo o contrato e as verificações deste módulo. |
| [WorkerProvider.status](#L18) | Implementa WorkerProvider.status como parte do fluxo descrito para este arquivo. |
| [WorkerProvider.start](#L21) | Inicia WorkerProvider.start, segundo o contrato e as verificações deste módulo. |
| [WorkerProvider.stop](#L24) | Interrompe WorkerProvider.stop, segundo o contrato e as verificações deste módulo. |
| [WorkerProvider.destroy](#L27) | Implementa WorkerProvider.destroy como parte do fluxo descrito para este arquivo. |
| [WorkerProvider.reset](#L30) | Implementa WorkerProvider.reset como parte do fluxo descrito para este arquivo. |
| [WorkerProvider.snapshot](#L33) | Implementa WorkerProvider.snapshot como parte do fluxo descrito para este arquivo. |
| [WorkerProvider.restore](#L36) | Implementa WorkerProvider.restore como parte do fluxo descrito para este arquivo. |
| [WorkerProvider.execute](#L39) | Implementa WorkerProvider.execute como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from typing import Protocol</code> | Importa Protocol de typing. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code># Documentação: Define o tipo WorkerProvider e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerProvider e reúne o estado/contrato descrito para este módulo. |
| <a id="L5"></a>5 | <code>class WorkerProvider(Protocol):</code> | Define o tipo WorkerProvider e reúne o estado/contrato descrito para este módulo. |
| <a id="L6"></a>6 | <code>    &quot;&quot;&quot;Host-side lifecycle contract. Implementations never accept host shell commands.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>    # Documentação: Libera WorkerProvider.close, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Libera WorkerProvider.close, segundo o contrato e as verificações deste |
| <a id="L9"></a>9 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L10"></a>10 | <code>    def close(self) -&gt; None: ...</code> | Libera WorkerProvider.close, segundo o contrato e as verificações deste módulo. |
| <a id="L11"></a>11 | <code>    # Documentação: Confere WorkerProvider.check_resources, segundo o contrato e as verificações</code> | Comentário: Documentação: Confere WorkerProvider.check_resources, segundo o contrato e as verificações |
| <a id="L12"></a>12 | <code>    # deste módulo.</code> | Comentário: deste módulo. |
| <a id="L13"></a>13 | <code>    def check_resources(self, rows: list[dict], desired: dict) -&gt; None: ...</code> | Confere WorkerProvider.check_resources, segundo o contrato e as verificações deste módulo. |
| <a id="L14"></a>14 | <code>    # Documentação: Cria WorkerProvider.create, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria WorkerProvider.create, segundo o contrato e as verificações deste módulo. |
| <a id="L15"></a>15 | <code>    def create(self, row: dict) -&gt; dict: ...</code> | Cria WorkerProvider.create, segundo o contrato e as verificações deste módulo. |
| <a id="L16"></a>16 | <code>    # Documentação: Implementa WorkerProvider.status como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa WorkerProvider.status como parte do fluxo descrito para este |
| <a id="L17"></a>17 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L18"></a>18 | <code>    def status(self, row: dict) -&gt; dict: ...</code> | Implementa WorkerProvider.status como parte do fluxo descrito para este arquivo. |
| <a id="L19"></a>19 | <code>    # Documentação: Inicia WorkerProvider.start, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Inicia WorkerProvider.start, segundo o contrato e as verificações deste |
| <a id="L20"></a>20 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L21"></a>21 | <code>    def start(self, row: dict) -&gt; dict: ...</code> | Inicia WorkerProvider.start, segundo o contrato e as verificações deste módulo. |
| <a id="L22"></a>22 | <code>    # Documentação: Interrompe WorkerProvider.stop, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Interrompe WorkerProvider.stop, segundo o contrato e as verificações deste |
| <a id="L23"></a>23 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L24"></a>24 | <code>    def stop(self, row: dict) -&gt; bool: ...</code> | Interrompe WorkerProvider.stop, segundo o contrato e as verificações deste módulo. |
| <a id="L25"></a>25 | <code>    # Documentação: Implementa WorkerProvider.destroy como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa WorkerProvider.destroy como parte do fluxo descrito para este |
| <a id="L26"></a>26 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L27"></a>27 | <code>    def destroy(self, row: dict) -&gt; dict: ...</code> | Implementa WorkerProvider.destroy como parte do fluxo descrito para este arquivo. |
| <a id="L28"></a>28 | <code>    # Documentação: Implementa WorkerProvider.reset como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa WorkerProvider.reset como parte do fluxo descrito para este |
| <a id="L29"></a>29 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L30"></a>30 | <code>    def reset(self, row: dict, generation: str) -&gt; dict: ...</code> | Implementa WorkerProvider.reset como parte do fluxo descrito para este arquivo. |
| <a id="L31"></a>31 | <code>    # Documentação: Implementa WorkerProvider.snapshot como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa WorkerProvider.snapshot como parte do fluxo descrito para este |
| <a id="L32"></a>32 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L33"></a>33 | <code>    def snapshot(self, row: dict, identifier: str) -&gt; tuple[dict, dict]: ...</code> | Implementa WorkerProvider.snapshot como parte do fluxo descrito para este arquivo. |
| <a id="L34"></a>34 | <code>    # Documentação: Implementa WorkerProvider.restore como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa WorkerProvider.restore como parte do fluxo descrito para este |
| <a id="L35"></a>35 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L36"></a>36 | <code>    def restore(self, row: dict, snapshot: dict) -&gt; dict: ...</code> | Implementa WorkerProvider.restore como parte do fluxo descrito para este arquivo. |
| <a id="L37"></a>37 | <code>    # Documentação: Implementa WorkerProvider.execute como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa WorkerProvider.execute como parte do fluxo descrito para este |
| <a id="L38"></a>38 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L39"></a>39 | <code>    def execute(self, row: dict, identifier: str, script: str, timeout: int) -&gt; dict: ...</code> | Implementa WorkerProvider.execute como parte do fluxo descrito para este arquivo. |
