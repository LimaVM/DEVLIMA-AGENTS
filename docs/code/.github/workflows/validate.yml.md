# .github/workflows/validate.yml

Define verificações hospedadas de Python/backend/manager/backup; configuração da CI não demonstra que uma execução hospedada tenha passado.

[Arquivo fonte](../../../../.github/workflows/validate.yml) · 35 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>name: Validate backend, manager and recovery</code> | Configura name com Validate backend, manager and recovery. |
| <a id="L2"></a>2 | <code>on:</code> | Configura on com o bloco abaixo. |
| <a id="L3"></a>3 | <code>  push:</code> | Configura push com o bloco abaixo. |
| <a id="L4"></a>4 | <code>    branches: [main]</code> | Configura branches com [main]. Limita branches que acionam o evento da CI. |
| <a id="L5"></a>5 | <code>  pull_request:</code> | Configura pull_request com o bloco abaixo. |
| <a id="L6"></a>6 | <code>  workflow_dispatch:</code> | Configura workflow_dispatch com o bloco abaixo. |
| <a id="L7"></a>7 | <code>permissions:</code> | Configura permissions com o bloco abaixo. Delimita acesso do token da execução GitHub. |
| <a id="L8"></a>8 | <code>  contents: read</code> | Configura contents com read. |
| <a id="L9"></a>9 | <code>jobs:</code> | Configura jobs com o bloco abaixo. |
| <a id="L10"></a>10 | <code>  validate:</code> | Configura validate com o bloco abaixo. |
| <a id="L11"></a>11 | <code>    runs-on: ubuntu-24.04</code> | Configura runs-on com ubuntu-24.04. Seleciona o ambiente do runner de CI. |
| <a id="L12"></a>12 | <code>    timeout-minutes: 20</code> | Configura timeout-minutes com 20. Limita duração do job de CI. |
| <a id="L13"></a>13 | <code>    steps:</code> | Configura steps com o bloco abaixo. |
| <a id="L14"></a>14 | <code>      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6</code> | Configura uses com actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6. Seleciona ação GitHub; o hash fixa sua revisão. |
| <a id="L15"></a>15 | <code>      - name: Check complete code documentation</code> | Configura name com Check complete code documentation. |
| <a id="L16"></a>16 | <code>        run: python3 scripts/document_code.py --check</code> | Configura run com python3 scripts/document_code.py --check. Executa script no runner sob o contexto/ambiente do passo. |
| <a id="L17"></a>17 | <code>      - name: Isolated test configuration</code> | Configura name com Isolated test configuration. |
| <a id="L18"></a>18 | <code>        run: python3 scripts/init_env.py</code> | Configura run com python3 scripts/init_env.py. Executa script no runner sob o contexto/ambiente do passo. |
| <a id="L19"></a>19 | <code>      - name: Build and test isolated PostgreSQL backend</code> | Configura name com Build and test isolated PostgreSQL backend. |
| <a id="L20"></a>20 | <code>        run: &#124;</code> | Configura run com &#124;. Executa script no runner sob o contexto/ambiente do passo. |
| <a id="L21"></a>21 | <code>          docker compose --env-file .env -f infra/docker-compose.yml --profile test build backend tests</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L22"></a>22 | <code>          docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm tests</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L23"></a>23 | <code>          docker compose --env-file .env -f infra/docker-compose.yml --profile test run --rm --no-deps tests ruff check --no-cache .</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L24"></a>24 | <code>      - name: Manager unit tests and authenticated backup tests</code> | Configura name com Manager unit tests and authenticated backup tests. |
| <a id="L25"></a>25 | <code>        run: &#124;</code> | Configura run com &#124;. Executa script no runner sob o contexto/ambiente do passo. |
| <a id="L26"></a>26 | <code>          sudo apt-get update</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L27"></a>27 | <code>          sudo apt-get install -y python3-libvirt python3-cryptography python3-venv</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L28"></a>28 | <code>          python3 -m venv --system-site-packages /tmp/devlima-test-tools</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L29"></a>29 | <code>          /tmp/devlima-test-tools/bin/pip install -r backend/requirements-dev.txt</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L30"></a>30 | <code>          PYTHONPATH=vm-manager /tmp/devlima-test-tools/bin/python -m pytest -q -p no:cacheprovider vm-manager/tests</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L31"></a>31 | <code>          /tmp/devlima-test-tools/bin/python -m unittest discover -s tests -v</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L32"></a>32 | <code>          /tmp/devlima-test-tools/bin/ruff check --no-cache --config backend/pyproject.toml scripts tests vm-manager</code> | Item/fechamento da lista ou objeto de configuração em construção. |
| <a id="L33"></a>33 | <code>      - name: Stop isolated test database</code> | Configura name com Stop isolated test database. |
| <a id="L34"></a>34 | <code>        if: always()</code> | Configura if com always(). Condiciona execução do passo à expressão declarada. |
| <a id="L35"></a>35 | <code>        run: docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test</code> | Configura run com docker compose --env-file .env -f infra/docker-compose.yml --profile test stop postgres-test. Executa script no runner sob o contexto/ambiente do passo. |
