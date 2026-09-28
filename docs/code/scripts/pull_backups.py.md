# scripts/pull_backups.py

Copia backups cifrados por SSH para destino externo local e autentica metadados/checksum sem exportar segredos de conexão.

[Arquivo fonte](../../../scripts/pull_backups.py) · 85 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [main](#L22) | Coordena a entrada de linha de comando deste arquivo: Copia backups cifrados por SSH para destino externo local e autentica metadados/checksum sem exportar segredos de conexão. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>#!/usr/bin/env python3</code> | Comentário: !/usr/bin/env python3 |
| <a id="L2"></a>2 | <code>&quot;&quot;&quot;Pull authenticated, encrypted backups over existing SSH; suitable for macOS launchd.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>import argparse</code> | Importa módulo(s) argparse. |
| <a id="L5"></a>5 | <code>import hashlib</code> | Importa módulo(s) hashlib. |
| <a id="L6"></a>6 | <code>import json</code> | Importa módulo(s) json. |
| <a id="L7"></a>7 | <code>import os</code> | Importa módulo(s) os. |
| <a id="L8"></a>8 | <code>import re</code> | Importa módulo(s) re. |
| <a id="L9"></a>9 | <code>import shlex</code> | Importa módulo(s) shlex. |
| <a id="L10"></a>10 | <code>import subprocess</code> | Importa módulo(s) subprocess. |
| <a id="L11"></a>11 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L12"></a>12 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L13"></a>13 | <code>REMOTE_PROGRAM = (</code> | Define REMOTE_PROGRAM com &quot;import json;from pathlib import Path;root=Path(&#x27;/srv/devlima-agent/backups&#x27;);print(json.dumps([{&#x27;name&#x27;:p.name,&#x27;checksum&#x27;:p.with_suffix(&#x27;.sha256&#x27;).read_text().split()[0]} for p .... |
| <a id="L14"></a>14 | <code>    &quot;import json;from pathlib import Path;root=Path(&#x27;/srv/devlima-agent/backups&#x27;);&quot;</code> | Continua/fecha a instrução da linha 13. Define REMOTE_PROGRAM com &quot;import json;from pathlib import Path;root=Path(&#x27;/srv/devlima-agent/backups&#x27;);print(json.dumps([{&#x27;name&#x27;:p.name,&#x27;checksum&#x27;:p.with_suffix(&#x27;.sha256&#x27;).read_text().split()[0]} for p .... |
| <a id="L15"></a>15 | <code>    &quot;print(json.dumps([{&#x27;name&#x27;:p.name,&#x27;checksum&#x27;:p.with_suffix(&#x27;.sha256&#x27;).read_text().split()[0]} &quot;</code> | Continua/fecha a instrução da linha 13. Define REMOTE_PROGRAM com &quot;import json;from pathlib import Path;root=Path(&#x27;/srv/devlima-agent/backups&#x27;);print(json.dumps([{&#x27;name&#x27;:p.name,&#x27;checksum&#x27;:p.with_suffix(&#x27;.sha256&#x27;).read_text().split()[0]} for p .... |
| <a id="L16"></a>16 | <code>    &quot;for p in sorted(root.glob(&#x27;devlima-*.dlag&#x27;)) if p.with_suffix(&#x27;.sha256&#x27;).exists()]))&quot;</code> | Continua/fecha a instrução da linha 13. Define REMOTE_PROGRAM com &quot;import json;from pathlib import Path;root=Path(&#x27;/srv/devlima-agent/backups&#x27;);print(json.dumps([{&#x27;name&#x27;:p.name,&#x27;checksum&#x27;:p.with_suffix(&#x27;.sha256&#x27;).read_text().split()[0]} for p .... |
| <a id="L17"></a>17 | <code>)</code> | Continua/fecha a instrução da linha 13. Define REMOTE_PROGRAM com &quot;import json;from pathlib import Path;root=Path(&#x27;/srv/devlima-agent/backups&#x27;);print(json.dumps([{&#x27;name&#x27;:p.name,&#x27;checksum&#x27;:p.with_suffix(&#x27;.sha256&#x27;).read_text().split()[0]} for p .... |
| <a id="L18"></a>18 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L19"></a>19 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L20"></a>20 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Copia backups cifrados por</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Copia backups cifrados por |
| <a id="L21"></a>21 | <code># SSH para destino externo local e autentica metadados/checksum sem exportar segredos de conexão.</code> | Comentário: SSH para destino externo local e autentica metadados/checksum sem exportar segredos de conexão. |
| <a id="L22"></a>22 | <code>def main():</code> | Coordena a entrada de linha de comando deste arquivo: Copia backups cifrados por SSH para destino externo local e autentica metadados/checksum sem exportar segredos de conexão. |
| <a id="L23"></a>23 | <code>    parser = argparse.ArgumentParser()</code> | Define parser com argparse.ArgumentParser(). Invoca argparse.ArgumentParser com os argumentos declarados nesta instrução. |
| <a id="L24"></a>24 | <code>    parser.add_argument(&quot;--host&quot;, default=&quot;ubuntu@147.15.33.140&quot;)</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--host&#x27;, default=&#x27;ubuntu@147.15.33.140&#x27; |
| <a id="L25"></a>25 | <code>    parser.add_argument(&quot;--key&quot;, type=Path, required=True)</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--key&#x27;, type=Path, required=True |
| <a id="L26"></a>26 | <code>    parser.add_argument(&quot;--directory&quot;, type=Path, required=True)</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--directory&#x27;, type=Path, required=True |
| <a id="L27"></a>27 | <code>    args = parser.parse_args()</code> | Define args com parser.parse_args(). Invoca parser.parse_args com os argumentos declarados nesta instrução. |
| <a id="L28"></a>28 | <code>    if not re.fullmatch(r&quot;[a-z_][a-z0-9_-]*@[a-zA-Z0-9.-]+&quot;, args.host):</code> | Executa este ramo somente se not re.fullmatch(&#x27;[a-z_][a-z0-9_-]*@[a-zA-Z0-9.-]+&#x27;, args.host); caso contrário, segue o ramo alternativo. |
| <a id="L29"></a>29 | <code>        parser.error(&quot;Use user@hostname without SSH options&quot;)</code> | Invoca parser.error com os argumentos declarados nesta instrução. Argumentos: &#x27;Use user@hostname without SSH options&#x27; |
| <a id="L30"></a>30 | <code>    os.umask(0o077)</code> | Invoca os.umask com os argumentos declarados nesta instrução. Argumentos: 63 |
| <a id="L31"></a>31 | <code>    args.directory.mkdir(mode=0o700, parents=True, exist_ok=True)</code> | Prepara diretório conforme permissões e opções declaradas. Argumentos: mode=448, parents=True, exist_ok=True |
| <a id="L32"></a>32 | <code>    args.directory.chmod(0o700)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 448 |
| <a id="L33"></a>33 | <code>    options = [</code> | Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L34"></a>34 | <code>        &quot;-i&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L35"></a>35 | <code>        str(args.key),</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L36"></a>36 | <code>        &quot;-o&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L37"></a>37 | <code>        &quot;BatchMode=yes&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L38"></a>38 | <code>        &quot;-o&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L39"></a>39 | <code>        &quot;StrictHostKeyChecking=yes&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L40"></a>40 | <code>        &quot;-o&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L41"></a>41 | <code>        &quot;ConnectTimeout=10&quot;,</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L42"></a>42 | <code>    ]</code> | Continua/fecha a instrução da linha 33. Define options com [&#x27;-i&#x27;, str(args.key), &#x27;-o&#x27;, &#x27;BatchMode=yes&#x27;, &#x27;-o&#x27;, &#x27;StrictHostKeyChecking=yes&#x27;, &#x27;-o&#x27;, &#x27;ConnectTimeout=10&#x27;]. |
| <a id="L43"></a>43 | <code>    result = subprocess.check_output(</code> | Define result com subprocess.check_output([&#x27;ssh&#x27;, *options, args.host, &#x27;python3 -c &#x27; + shlex.quote(REMOTE_PROGRAM)], text=True). Invoca subprocess.check_output com os argumentos declarados nesta instrução. Argumentos: [&#x27;ssh&#x27;, *options, args.host, &#x27;python3 -c &#x27; + shlex.quote(REMOTE_PROGRAM)], text=True |
| <a id="L44"></a>44 | <code>        [&quot;ssh&quot;, *options, args.host, &quot;python3 -c &quot; + shlex.quote(REMOTE_PROGRAM)], text=True</code> | Continua/fecha a instrução da linha 43. Define result com subprocess.check_output([&#x27;ssh&#x27;, *options, args.host, &#x27;python3 -c &#x27; + shlex.quote(REMOTE_PROGRAM)], text=True). Invoca subprocess.check_output com os argumentos declarados nesta instrução. Argumentos: [&#x27;ssh&#x27;, *options, args.host, &#x27;python3 -c &#x27; + shlex.quote(REMOTE_PROGRAM)], text=True |
| <a id="L45"></a>45 | <code>    )</code> | Continua/fecha a instrução da linha 43. Define result com subprocess.check_output([&#x27;ssh&#x27;, *options, args.host, &#x27;python3 -c &#x27; + shlex.quote(REMOTE_PROGRAM)], text=True). Invoca subprocess.check_output com os argumentos declarados nesta instrução. Argumentos: [&#x27;ssh&#x27;, *options, args.host, &#x27;python3 -c &#x27; + shlex.quote(REMOTE_PROGRAM)], text=True |
| <a id="L46"></a>46 | <code>    entries = json.loads(result)</code> | Define entries com json.loads(result). Invoca json.loads com os argumentos declarados nesta instrução. Argumentos: result |
| <a id="L47"></a>47 | <code>    downloaded = 0</code> | Define downloaded com 0. |
| <a id="L48"></a>48 | <code>    for entry in entries:</code> | Percorre entries, atribuindo cada elemento a entry. |
| <a id="L49"></a>49 | <code>        name, expected = entry[&quot;name&quot;], entry[&quot;checksum&quot;]</code> | Define (name, expected) com (entry[&#x27;name&#x27;], entry[&#x27;checksum&#x27;]). |
| <a id="L50"></a>50 | <code>        if not re.fullmatch(r&quot;devlima-\d{8}T\d{6}Z\.dlag&quot;, name) or not re.fullmatch(</code> | Executa este ramo somente se not re.fullmatch(&#x27;devlima-\\d{8}T\\d{6}Z\\.dlag&#x27;, name) or not re.fullmatch(&#x27;[a-f0-9]{64}&#x27;, expected); caso contrário, segue o ramo alternativo. |
| <a id="L51"></a>51 | <code>            r&quot;[a-f0-9]{64}&quot;, expected</code> | Continua/fecha a instrução da linha 50. Executa este ramo somente se not re.fullmatch(&#x27;devlima-\\d{8}T\\d{6}Z\\.dlag&#x27;, name) or not re.fullmatch(&#x27;[a-f0-9]{64}&#x27;, expected); caso contrário, segue o ramo alternativo. |
| <a id="L52"></a>52 | <code>        ):</code> | Continua/fecha a instrução da linha 50. Executa este ramo somente se not re.fullmatch(&#x27;devlima-\\d{8}T\\d{6}Z\\.dlag&#x27;, name) or not re.fullmatch(&#x27;[a-f0-9]{64}&#x27;, expected); caso contrário, segue o ramo alternativo. |
| <a id="L53"></a>53 | <code>            raise ValueError(&quot;Unexpected remote backup metadata&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Unexpected remote backup metadata&#x27;). |
| <a id="L54"></a>54 | <code>        target = args.directory / name</code> | Define target com args.directory / name. |
| <a id="L55"></a>55 | <code>        if target.exists():</code> | Executa este ramo somente se target.exists(); caso contrário, segue o ramo alternativo. |
| <a id="L56"></a>56 | <code>            continue</code> | Encerra esta iteração e passa ao próximo elemento do loop. |
| <a id="L57"></a>57 | <code>        temporary = target.with_suffix(&quot;.partial&quot;)</code> | Define temporary com target.with_suffix(&#x27;.partial&#x27;). Invoca target.with_suffix com os argumentos declarados nesta instrução. Argumentos: &#x27;.partial&#x27; |
| <a id="L58"></a>58 | <code>        subprocess.run(</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;scp&#x27;, *options, args.host + &#x27;:/srv/devlima-agent/backups/&#x27; + name, str(temporary)], check=True |
| <a id="L59"></a>59 | <code>            [&quot;scp&quot;, *options, args.host + &quot;:/srv/devlima-agent/backups/&quot; + name, str(temporary)],</code> | Continua/fecha a instrução da linha 58. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;scp&#x27;, *options, args.host + &#x27;:/srv/devlima-agent/backups/&#x27; + name, str(temporary)], check=True |
| <a id="L60"></a>60 | <code>            check=True,</code> | Continua/fecha a instrução da linha 58. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;scp&#x27;, *options, args.host + &#x27;:/srv/devlima-agent/backups/&#x27; + name, str(temporary)], check=True |
| <a id="L61"></a>61 | <code>        )</code> | Continua/fecha a instrução da linha 58. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;scp&#x27;, *options, args.host + &#x27;:/srv/devlima-agent/backups/&#x27; + name, str(temporary)], check=True |
| <a id="L62"></a>62 | <code>        temporary.chmod(0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 384 |
| <a id="L63"></a>63 | <code>        digest = hashlib.sha256()</code> | Define digest com hashlib.sha256(). Calcula digest SHA-256 para identificação/integridade conforme o contexto. |
| <a id="L64"></a>64 | <code>        with temporary.open(&quot;rb&quot;) as source:</code> | Abre contexto(s) temporary.open(&#x27;rb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L65"></a>65 | <code>            while block := source.read(1024 * 1024):</code> | Repete este bloco enquanto (block := source.read(1024 * 1024)) permanecer verdadeiro. |
| <a id="L66"></a>66 | <code>                digest.update(block)</code> | Invoca digest.update com os argumentos declarados nesta instrução. Argumentos: block |
| <a id="L67"></a>67 | <code>        if digest.hexdigest() != expected:</code> | Executa este ramo somente se digest.hexdigest() != expected; caso contrário, segue o ramo alternativo. |
| <a id="L68"></a>68 | <code>            temporary.unlink()</code> | Remove exclusivamente o caminho de arquivo indicado. |
| <a id="L69"></a>69 | <code>            raise ValueError(&quot;Backup checksum mismatch&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Backup checksum mismatch&#x27;). |
| <a id="L70"></a>70 | <code>        temporary.replace(target)</code> | Invoca temporary.replace com os argumentos declarados nesta instrução. Argumentos: target |
| <a id="L71"></a>71 | <code>        target.with_suffix(&quot;.sha256&quot;).write_text(expected + &quot;  &quot; + name + &quot;\n&quot;)</code> | Invoca target.with_suffix(&#x27;.sha256&#x27;).write_text com os argumentos declarados nesta instrução. Argumentos: expected + &#x27;  &#x27; + name + &#x27;\n&#x27; |
| <a id="L72"></a>72 | <code>        downloaded += 1</code> | Atualiza downloaded com 1. |
| <a id="L73"></a>73 | <code>    print(</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L74"></a>74 | <code>        json.dumps(</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L75"></a>75 | <code>            {</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L76"></a>76 | <code>                &quot;copied&quot;: downloaded,</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L77"></a>77 | <code>                &quot;remote_archives&quot;: len(entries),</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L78"></a>78 | <code>                &quot;directory&quot;: str(args.directory),</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L79"></a>79 | <code>            }</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L80"></a>80 | <code>        )</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L81"></a>81 | <code>    )</code> | Continua/fecha a instrução da linha 73. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;copied&#x27;: downloaded, &#x27;remote_archives&#x27;: len(entries), &#x27;directory&#x27;: str(args.directory)}) |
| <a id="L82"></a>82 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L83"></a>83 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L84"></a>84 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L85"></a>85 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
