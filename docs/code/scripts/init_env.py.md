# scripts/init_env.py

Gera .env novo com segredos aleatórios e permissões privadas, sem sobrescrever configuração existente nem imprimir valores secretos.

[Arquivo fonte](../../../scripts/init_env.py) · 45 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [main](#L14) | Coordena a entrada de linha de comando deste arquivo: Gera .env novo com segredos aleatórios e permissões privadas, sem sobrescrever configuração existente nem imprimir valores secretos. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>#!/usr/bin/env python3</code> | Comentário: !/usr/bin/env python3 |
| <a id="L2"></a>2 | <code>&quot;&quot;&quot;Generate secrets without stdout disclosure or overwriting an existing .env.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>import argparse</code> | Importa módulo(s) argparse. |
| <a id="L5"></a>5 | <code>import os</code> | Importa módulo(s) os. |
| <a id="L6"></a>6 | <code>import re</code> | Importa módulo(s) re. |
| <a id="L7"></a>7 | <code>import secrets</code> | Importa módulo(s) secrets. |
| <a id="L8"></a>8 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L11"></a>11 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Gera .env novo com segredos</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Gera .env novo com segredos |
| <a id="L12"></a>12 | <code># aleatórios e permissões privadas, sem sobrescrever configuração existente nem imprimir valores</code> | Comentário: aleatórios e permissões privadas, sem sobrescrever configuração existente nem imprimir valores |
| <a id="L13"></a>13 | <code># secretos.</code> | Comentário: secretos. |
| <a id="L14"></a>14 | <code>def main() -&gt; None:</code> | Coordena a entrada de linha de comando deste arquivo: Gera .env novo com segredos aleatórios e permissões privadas, sem sobrescrever configuração existente nem imprimir valores secretos. |
| <a id="L15"></a>15 | <code>    parser = argparse.ArgumentParser()</code> | Define parser com argparse.ArgumentParser(). Invoca argparse.ArgumentParser com os argumentos declarados nesta instrução. |
| <a id="L16"></a>16 | <code>    parser.add_argument(&quot;--domain&quot;, help=&quot;Public hostname already pointing to this host&quot;)</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--domain&#x27;, help=&#x27;Public hostname already pointing to this host&#x27; |
| <a id="L17"></a>17 | <code>    args = parser.parse_args()</code> | Define args com parser.parse_args(). Invoca parser.parse_args com os argumentos declarados nesta instrução. |
| <a id="L18"></a>18 | <code>    root = Path(__file__).resolve().parents[1]</code> | Define root com Path(__file__).resolve().parents[1]. |
| <a id="L19"></a>19 | <code>    values = (root / &quot;.env.example&quot;).read_text()</code> | Define values com (root / &#x27;.env.example&#x27;).read_text(). Invoca (root / &#x27;.env.example&#x27;).read_text com os argumentos declarados nesta instrução. |
| <a id="L20"></a>20 | <code>    for key in (&quot;POSTGRES_PASSWORD&quot;, &quot;RUNTIME_POSTGRES_PASSWORD&quot;, &quot;MIGRATION_POSTGRES_PASSWORD&quot;):</code> | Percorre (&#x27;POSTGRES_PASSWORD&#x27;, &#x27;RUNTIME_POSTGRES_PASSWORD&#x27;, &#x27;MIGRATION_POSTGRES_PASSWORD&#x27;), atribuindo cada elemento a key. |
| <a id="L21"></a>21 | <code>        values = values.replace(&quot;\n&quot; + key + &quot;=\n&quot;, &quot;\n&quot; + key + &quot;=&quot; + secrets.token_hex(32) + &quot;\n&quot;)</code> | Define values com values.replace(&#x27;\n&#x27; + key + &#x27;=\n&#x27;, &#x27;\n&#x27; + key + &#x27;=&#x27; + secrets.token_hex(32) + &#x27;\n&#x27;). Invoca values.replace com os argumentos declarados nesta instrução. Argumentos: &#x27;\n&#x27; + key + &#x27;=\n&#x27;, &#x27;\n&#x27; + key + &#x27;=&#x27; + secrets.token_hex(32) + &#x27;\n&#x27; |
| <a id="L22"></a>22 | <code>    values = values.replace(&quot;JWT_SECRET=\n&quot;, f&quot;JWT_SECRET={secrets.token_hex(48)}\n&quot;)</code> | Define values com values.replace(&#x27;JWT_SECRET=\n&#x27;, f&#x27;JWT_SECRET={secrets.token_hex(48)}\n&#x27;). Invoca values.replace com os argumentos declarados nesta instrução. Argumentos: &#x27;JWT_SECRET=\n&#x27;, f&#x27;JWT_SECRET={secrets.token_hex(48)}\n&#x27; |
| <a id="L23"></a>23 | <code>    values = values.replace(&quot;VM_MANAGER_TOKEN=\n&quot;, f&quot;VM_MANAGER_TOKEN={secrets.token_hex(32)}\n&quot;)</code> | Define values com values.replace(&#x27;VM_MANAGER_TOKEN=\n&#x27;, f&#x27;VM_MANAGER_TOKEN={secrets.token_hex(32)}\n&#x27;). Invoca values.replace com os argumentos declarados nesta instrução. Argumentos: &#x27;VM_MANAGER_TOKEN=\n&#x27;, f&#x27;VM_MANAGER_TOKEN={secrets.token_hex(32)}\n&#x27; |
| <a id="L24"></a>24 | <code>    if args.domain:</code> | Executa este ramo somente se args.domain; caso contrário, segue o ramo alternativo. |
| <a id="L25"></a>25 | <code>        if not re.fullmatch(r&quot;[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?&quot;, args.domain):</code> | Executa este ramo somente se not re.fullmatch(&#x27;[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?&#x27;, args.domain); caso contrário, segue o ramo alternativo. |
| <a id="L26"></a>26 | <code>            parser.error(&quot;Domínio inválido&quot;)</code> | Invoca parser.error com os argumentos declarados nesta instrução. Argumentos: &#x27;Domínio inválido&#x27; |
| <a id="L27"></a>27 | <code>        for previous, updated in {</code> | Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L28"></a>28 | <code>            &quot;AGENT_DOMAIN=localhost&quot;: f&quot;AGENT_DOMAIN={args.domain}&quot;,</code> | Continua/fecha a instrução da linha 27. Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L29"></a>29 | <code>            &quot;CADDY_CONFIG=Caddyfile.private&quot;: &quot;CADDY_CONFIG=Caddyfile&quot;,</code> | Continua/fecha a instrução da linha 27. Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L30"></a>30 | <code>            &quot;CADDY_BIND=127.0.0.1&quot;: &quot;CADDY_BIND=0.0.0.0&quot;,</code> | Continua/fecha a instrução da linha 27. Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L31"></a>31 | <code>            &quot;HTTP_PORT=8080&quot;: &quot;HTTP_PORT=80&quot;,</code> | Continua/fecha a instrução da linha 27. Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L32"></a>32 | <code>            &quot;HTTPS_PORT=8443&quot;: &quot;HTTPS_PORT=443&quot;,</code> | Continua/fecha a instrução da linha 27. Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L33"></a>33 | <code>        }.items():</code> | Continua/fecha a instrução da linha 27. Percorre {&#x27;AGENT_DOMAIN=localhost&#x27;: f&#x27;AGENT_DOMAIN={args.domain}&#x27;, &#x27;CADDY_CONFIG=Caddyfile.private&#x27;: &#x27;CADDY_CONFIG=Caddyfile&#x27;, &#x27;CADDY_BIND=127.0.0.1&#x27;: &#x27;CADDY_BIND=0.0.0.0&#x27;, &#x27;HTTP_PORT=80..., atribuindo cada elemento a (previous, updated). |
| <a id="L34"></a>34 | <code>            values = values.replace(previous, updated)</code> | Define values com values.replace(previous, updated). Invoca values.replace com os argumentos declarados nesta instrução. Argumentos: previous, updated |
| <a id="L35"></a>35 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L36"></a>36 | <code>        descriptor = os.open(root / &quot;.env&quot;, os.O_WRONLY &#124; os.O_CREAT &#124; os.O_EXCL, 0o600)</code> | Define descriptor com os.open(root / &#x27;.env&#x27;, os.O_WRONLY &#124; os.O_CREAT &#124; os.O_EXCL, 384). Invoca os.open com os argumentos declarados nesta instrução. Argumentos: root / &#x27;.env&#x27;, os.O_WRONLY &#124; os.O_CREAT &#124; os.O_EXCL, 384 |
| <a id="L37"></a>37 | <code>    except FileExistsError:</code> | Trata exceção FileExistsError. |
| <a id="L38"></a>38 | <code>        parser.exit(1, &quot;.env já existe; não foi alterado.\n&quot;)</code> | Invoca parser.exit com os argumentos declarados nesta instrução. Argumentos: 1, &#x27;.env já existe; não foi alterado.\n&#x27; |
| <a id="L39"></a>39 | <code>    with os.fdopen(descriptor, &quot;w&quot;) as output:</code> | Abre contexto(s) os.fdopen(descriptor, &#x27;w&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L40"></a>40 | <code>        output.write(values)</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: values |
| <a id="L41"></a>41 | <code>    print(&quot;.env criado com secrets aleatórios e permissão 0600; valores não exibidos.&quot;)</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: &#x27;.env criado com secrets aleatórios e permissão 0600; valores não exibidos.&#x27; |
| <a id="L42"></a>42 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L43"></a>43 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L44"></a>44 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L45"></a>45 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
