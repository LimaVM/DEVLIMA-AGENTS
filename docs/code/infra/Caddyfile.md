# infra/Caddyfile

Publica HTTPS para o domínio configurado, obtém certificado e encaminha HTTP/WSS ao backend mantendo cabeçalhos e limites definidos.

[Arquivo fonte](../../../infra/Caddyfile) · 20 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>{</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L2"></a>2 | <code>    admin off</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L3"></a>3 | <code>}</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L5"></a>5 | <code>{$AGENT_DOMAIN} {</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L6"></a>6 | <code>    request_body {</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L7"></a>7 | <code>        max_size 1MB</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L8"></a>8 | <code>    }</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L9"></a>9 | <code>    header {</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L10"></a>10 | <code>        X-Content-Type-Options nosniff</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L11"></a>11 | <code>        Referrer-Policy no-referrer</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L12"></a>12 | <code>        -Server</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L13"></a>13 | <code>    }</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L14"></a>14 | <code>    reverse_proxy backend:8000 {</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. Encaminha HTTP e upgrades WSS para o backend indicado. |
| <a id="L15"></a>15 | <code>        transport http {</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L16"></a>16 | <code>            dial_timeout 5s</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L17"></a>17 | <code>            response_header_timeout 130s</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L18"></a>18 | <code>        }</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L19"></a>19 | <code>    }</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
| <a id="L20"></a>20 | <code>}</code> | Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend. |
