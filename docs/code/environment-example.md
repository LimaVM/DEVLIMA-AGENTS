# .env.example

Lista configurações e placeholders para implantação; serve de referência e não contém as credenciais reais do ambiente operacional.

[Arquivo fonte](../../.env.example) · 39 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code># Copie para .env e use scripts/init_env.py para gerar secrets.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L2"></a>2 | <code>COMPOSE_PROJECT_NAME=devlima-agent</code> | Exemplifica a variável COMPOSE_PROJECT_NAME; implantação usa valor externo próprio. |
| <a id="L3"></a>3 | <code>POSTGRES_DB=devlima_agent</code> | Exemplifica a variável POSTGRES_DB; implantação usa valor externo próprio. |
| <a id="L4"></a>4 | <code>POSTGRES_USER=agent</code> | Exemplifica a variável POSTGRES_USER; implantação usa valor externo próprio. |
| <a id="L5"></a>5 | <code>POSTGRES_PASSWORD=</code> | Exemplifica a variável POSTGRES_PASSWORD; implantação usa valor externo próprio. |
| <a id="L6"></a>6 | <code>RUNTIME_POSTGRES_USER=agent_runtime</code> | Exemplifica a variável RUNTIME_POSTGRES_USER; implantação usa valor externo próprio. |
| <a id="L7"></a>7 | <code>RUNTIME_POSTGRES_PASSWORD=</code> | Exemplifica a variável RUNTIME_POSTGRES_PASSWORD; implantação usa valor externo próprio. |
| <a id="L8"></a>8 | <code>MIGRATION_POSTGRES_USER=agent_migrate</code> | Exemplifica a variável MIGRATION_POSTGRES_USER; implantação usa valor externo próprio. |
| <a id="L9"></a>9 | <code>MIGRATION_POSTGRES_PASSWORD=</code> | Exemplifica a variável MIGRATION_POSTGRES_PASSWORD; implantação usa valor externo próprio. |
| <a id="L10"></a>10 | <code>JWT_SECRET=</code> | Exemplifica a variável JWT_SECRET; implantação usa valor externo próprio. |
| <a id="L11"></a>11 | <code>JWT_ISSUER=devlima-agent</code> | Exemplifica a variável JWT_ISSUER; implantação usa valor externo próprio. |
| <a id="L12"></a>12 | <code>JWT_AUDIENCE=devlima-android</code> | Exemplifica a variável JWT_AUDIENCE; implantação usa valor externo próprio. |
| <a id="L13"></a>13 | <code>JWT_TTL_MINUTES=30</code> | Exemplifica a variável JWT_TTL_MINUTES; implantação usa valor externo próprio. |
| <a id="L14"></a>14 | <code>DEFAULT_TIMEZONE=America/Sao_Paulo</code> | Exemplifica a variável DEFAULT_TIMEZONE; implantação usa valor externo próprio. |
| <a id="L15"></a>15 | <code>ENABLE_API_DOCS=false</code> | Exemplifica a variável ENABLE_API_DOCS; implantação usa valor externo próprio. |
| <a id="L16"></a>16 | <code>LOGIN_MAX_ATTEMPTS=5</code> | Exemplifica a variável LOGIN_MAX_ATTEMPTS; implantação usa valor externo próprio. |
| <a id="L17"></a>17 | <code>LOGIN_WINDOW_SECONDS=900</code> | Exemplifica a variável LOGIN_WINDOW_SECONDS; implantação usa valor externo próprio. |
| <a id="L18"></a>18 | <code># Defaults privados. Para HTTPS público, configure domínio/DNS e portas 80/443.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L19"></a>19 | <code>AGENT_DOMAIN=localhost</code> | Exemplifica a variável AGENT_DOMAIN; implantação usa valor externo próprio. |
| <a id="L20"></a>20 | <code>CADDY_CONFIG=Caddyfile.private</code> | Exemplifica a variável CADDY_CONFIG; implantação usa valor externo próprio. |
| <a id="L21"></a>21 | <code>CADDY_BIND=127.0.0.1</code> | Exemplifica a variável CADDY_BIND; implantação usa valor externo próprio. |
| <a id="L22"></a>22 | <code>HTTP_PORT=8080</code> | Exemplifica a variável HTTP_PORT; implantação usa valor externo próprio. |
| <a id="L23"></a>23 | <code>HTTPS_PORT=8443</code> | Exemplifica a variável HTTPS_PORT; implantação usa valor externo próprio. |
| <a id="L24"></a>24 | <code># LLM primária pela rede privada (ex.: http://100.x.x.x:8080/v1).</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L25"></a>25 | <code>LOCAL_LLM_BASE_URL=</code> | Exemplifica a variável LOCAL_LLM_BASE_URL; implantação usa valor externo próprio. |
| <a id="L26"></a>26 | <code>LOCAL_LLM_MODEL=</code> | Exemplifica a variável LOCAL_LLM_MODEL; implantação usa valor externo próprio. |
| <a id="L27"></a>27 | <code>LOCAL_LLM_TIMEOUT=30</code> | Exemplifica a variável LOCAL_LLM_TIMEOUT; implantação usa valor externo próprio. |
| <a id="L28"></a>28 | <code>GROQ_API_KEY=</code> | Exemplifica a variável GROQ_API_KEY; implantação usa valor externo próprio. |
| <a id="L29"></a>29 | <code>GROQ_MODEL=openai/gpt-oss-120b</code> | Exemplifica a variável GROQ_MODEL; implantação usa valor externo próprio. |
| <a id="L30"></a>30 | <code>GROQ_TIMEOUT=30</code> | Exemplifica a variável GROQ_TIMEOUT; implantação usa valor externo próprio. |
| <a id="L31"></a>31 | <code>LLM_HEALTH_TIMEOUT=5</code> | Exemplifica a variável LLM_HEALTH_TIMEOUT; implantação usa valor externo próprio. |
| <a id="L32"></a>32 | <code>ALLOW_CLOUD_FALLBACK=true</code> | Exemplifica a variável ALLOW_CLOUD_FALLBACK; implantação usa valor externo próprio. |
| <a id="L33"></a>33 | <code>CONTEXT_RECENT_MESSAGES=8</code> | Exemplifica a variável CONTEXT_RECENT_MESSAGES; implantação usa valor externo próprio. |
| <a id="L34"></a>34 | <code>CONTEXT_MAX_CHARS=12000</code> | Exemplifica a variável CONTEXT_MAX_CHARS; implantação usa valor externo próprio. |
| <a id="L35"></a>35 | <code>SUMMARY_TRIGGER_MESSAGES=16</code> | Exemplifica a variável SUMMARY_TRIGGER_MESSAGES; implantação usa valor externo próprio. |
| <a id="L36"></a>36 | <code># Token gerado por scripts/install_vm_manager.py na VPS. Não publicar.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L37"></a>37 | <code>VM_MANAGER_TOKEN=</code> | Exemplifica a variável VM_MANAGER_TOKEN; implantação usa valor externo próprio. |
| <a id="L38"></a>38 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L39"></a>39 | <code>SCHEDULER_POLL_SECONDS=5</code> | Exemplifica a variável SCHEDULER_POLL_SECONDS; implantação usa valor externo próprio. |
