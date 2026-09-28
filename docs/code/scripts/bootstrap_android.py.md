# scripts/bootstrap_android.py

Prepara ferramentas Android na VPS por downloads/extração explícitos; verifica arquivos e limita caminhos extraídos para evitar path traversal.

[Arquivo fonte](../../../scripts/bootstrap_android.py) · 100 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [download](#L18) | Implementa download como parte do fluxo descrito para este arquivo. |
| [extract](#L24) | Implementa extract como parte do fluxo descrito para este arquivo. |
| [main](#L36) | Coordena a entrada de linha de comando deste arquivo: Prepara ferramentas Android na VPS por downloads/extração explícitos; verifica arquivos e limita caminhos extraídos para evitar path traversal. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>&quot;&quot;&quot;Install pinned Android CLI tools on a Linux build host; no project credentials.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>import argparse</code> | Importa módulo(s) argparse. |
| <a id="L4"></a>4 | <code>import hashlib</code> | Importa módulo(s) hashlib. |
| <a id="L5"></a>5 | <code>import shutil</code> | Importa módulo(s) shutil. |
| <a id="L6"></a>6 | <code>import subprocess</code> | Importa módulo(s) subprocess. |
| <a id="L7"></a>7 | <code>import tempfile</code> | Importa módulo(s) tempfile. |
| <a id="L8"></a>8 | <code>import urllib.request</code> | Importa módulo(s) urllib.request. |
| <a id="L9"></a>9 | <code>import zipfile</code> | Importa módulo(s) zipfile. |
| <a id="L10"></a>10 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L11"></a>11 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L12"></a>12 | <code>SDK_ARCHIVE = &quot;commandlinetools-linux-16111833_latest.zip&quot;</code> | Define SDK_ARCHIVE com &#x27;commandlinetools-linux-16111833_latest.zip&#x27;. |
| <a id="L13"></a>13 | <code>SDK_SHA1 = &quot;e025545c62a8e64c7559119566a569fb1dec5f60&quot;</code> | Define SDK_SHA1 com &#x27;e025545c62a8e64c7559119566a569fb1dec5f60&#x27;. |
| <a id="L14"></a>14 | <code>GRADLE_VERSION = &quot;8.13&quot;</code> | Define GRADLE_VERSION com &#x27;8.13&#x27;. |
| <a id="L15"></a>15 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L17"></a>17 | <code># Documentação: Implementa download como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa download como parte do fluxo descrito para este arquivo. |
| <a id="L18"></a>18 | <code>def download(url, path):</code> | Implementa download como parte do fluxo descrito para este arquivo. |
| <a id="L19"></a>19 | <code>    with urllib.request.urlopen(url, timeout=120) as response, path.open(&quot;wb&quot;) as target:</code> | Abre contexto(s) urllib.request.urlopen(url, timeout=120), path.open(&#x27;wb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L20"></a>20 | <code>        shutil.copyfileobj(response, target)</code> | Invoca shutil.copyfileobj com os argumentos declarados nesta instrução. Argumentos: response, target |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code># Documentação: Implementa extract como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa extract como parte do fluxo descrito para este arquivo. |
| <a id="L24"></a>24 | <code>def extract(path, directory):</code> | Implementa extract como parte do fluxo descrito para este arquivo. |
| <a id="L25"></a>25 | <code>    root = directory.resolve()</code> | Define root com directory.resolve(). Invoca directory.resolve com os argumentos declarados nesta instrução. |
| <a id="L26"></a>26 | <code>    with zipfile.ZipFile(path) as archive:</code> | Abre contexto(s) zipfile.ZipFile(path); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L27"></a>27 | <code>        for item in archive.infolist():</code> | Percorre archive.infolist(), atribuindo cada elemento a item. |
| <a id="L28"></a>28 | <code>            if not (root / item.filename).resolve().is_relative_to(root):</code> | Executa este ramo somente se not (root / item.filename).resolve().is_relative_to(root); caso contrário, segue o ramo alternativo. |
| <a id="L29"></a>29 | <code>                raise RuntimeError(&quot;Unsafe archive path&quot;)</code> | Interrompe este caminho lançando RuntimeError(&#x27;Unsafe archive path&#x27;). |
| <a id="L30"></a>30 | <code>        archive.extractall(root)</code> | Invoca archive.extractall com os argumentos declarados nesta instrução. Argumentos: root |
| <a id="L31"></a>31 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L32"></a>32 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L33"></a>33 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Prepara ferramentas Android</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Prepara ferramentas Android |
| <a id="L34"></a>34 | <code># na VPS por downloads/extração explícitos; verifica arquivos e limita caminhos extraídos para</code> | Comentário: na VPS por downloads/extração explícitos; verifica arquivos e limita caminhos extraídos para |
| <a id="L35"></a>35 | <code># evitar path traversal.</code> | Comentário: evitar path traversal. |
| <a id="L36"></a>36 | <code>def main():</code> | Coordena a entrada de linha de comando deste arquivo: Prepara ferramentas Android na VPS por downloads/extração explícitos; verifica arquivos e limita caminhos extraídos para evitar path traversal. |
| <a id="L37"></a>37 | <code>    parser = argparse.ArgumentParser()</code> | Define parser com argparse.ArgumentParser(). Invoca argparse.ArgumentParser com os argumentos declarados nesta instrução. |
| <a id="L38"></a>38 | <code>    parser.add_argument(&quot;--sdk-root&quot;, type=Path, default=Path(&quot;/srv/devlima-android-sdk&quot;))</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--sdk-root&#x27;, type=Path, default=Path(&#x27;/srv/devlima-android-sdk&#x27;) |
| <a id="L39"></a>39 | <code>    parser.add_argument(&quot;--tools-root&quot;, type=Path, default=Path(&quot;/srv/devlima-build-tools&quot;))</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--tools-root&#x27;, type=Path, default=Path(&#x27;/srv/devlima-build-tools&#x27;) |
| <a id="L40"></a>40 | <code>    parser.add_argument(&quot;--emulator&quot;, action=&quot;store_true&quot;)</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--emulator&#x27;, action=&#x27;store_true&#x27; |
| <a id="L41"></a>41 | <code>    args = parser.parse_args()</code> | Define args com parser.parse_args(). Invoca parser.parse_args com os argumentos declarados nesta instrução. |
| <a id="L42"></a>42 | <code>    if not args.sdk_root.is_absolute() or not args.tools_root.is_absolute():</code> | Executa este ramo somente se not args.sdk_root.is_absolute() or not args.tools_root.is_absolute(); caso contrário, segue o ramo alternativo. |
| <a id="L43"></a>43 | <code>        raise SystemExit(&quot;Use absolute installation directories&quot;)</code> | Interrompe este caminho lançando SystemExit(&#x27;Use absolute installation directories&#x27;). |
| <a id="L44"></a>44 | <code>    for directory in (args.sdk_root, args.tools_root):</code> | Percorre (args.sdk_root, args.tools_root), atribuindo cada elemento a directory. |
| <a id="L45"></a>45 | <code>        directory.mkdir(parents=True, exist_ok=True)</code> | Prepara diretório conforme permissões e opções declaradas. Argumentos: parents=True, exist_ok=True |
| <a id="L46"></a>46 | <code>    manager = args.sdk_root / &quot;cmdline-tools/latest/bin/sdkmanager&quot;</code> | Define manager com args.sdk_root / &#x27;cmdline-tools/latest/bin/sdkmanager&#x27;. |
| <a id="L47"></a>47 | <code>    with tempfile.TemporaryDirectory(prefix=&quot;devlima-android-&quot;) as temporary:</code> | Abre contexto(s) tempfile.TemporaryDirectory(prefix=&#x27;devlima-android-&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L48"></a>48 | <code>        staging = Path(temporary)</code> | Define staging com Path(temporary). Invoca Path com os argumentos declarados nesta instrução. Argumentos: temporary |
| <a id="L49"></a>49 | <code>        if not manager.exists():</code> | Executa este ramo somente se not manager.exists(); caso contrário, segue o ramo alternativo. |
| <a id="L50"></a>50 | <code>            archive = staging / &quot;sdk.zip&quot;</code> | Define archive com staging / &#x27;sdk.zip&#x27;. |
| <a id="L51"></a>51 | <code>            download(&quot;https://dl.google.com/android/repository/&quot; + SDK_ARCHIVE, archive)</code> | Invoca download com os argumentos declarados nesta instrução. Argumentos: &#x27;https://dl.google.com/android/repository/&#x27; + SDK_ARCHIVE, archive |
| <a id="L52"></a>52 | <code>            if hashlib.sha1(archive.read_bytes()).hexdigest() != SDK_SHA1:</code> | Executa este ramo somente se hashlib.sha1(archive.read_bytes()).hexdigest() != SDK_SHA1; caso contrário, segue o ramo alternativo. |
| <a id="L53"></a>53 | <code>                raise RuntimeError(&quot;Android archive checksum mismatch&quot;)</code> | Interrompe este caminho lançando RuntimeError(&#x27;Android archive checksum mismatch&#x27;). |
| <a id="L54"></a>54 | <code>            extract(archive, staging)</code> | Invoca extract com os argumentos declarados nesta instrução. Argumentos: archive, staging |
| <a id="L55"></a>55 | <code>            destination = args.sdk_root / &quot;cmdline-tools/latest&quot;</code> | Define destination com args.sdk_root / &#x27;cmdline-tools/latest&#x27;. |
| <a id="L56"></a>56 | <code>            destination.parent.mkdir(parents=True, exist_ok=True)</code> | Prepara diretório conforme permissões e opções declaradas. Argumentos: parents=True, exist_ok=True |
| <a id="L57"></a>57 | <code>            shutil.move(str(staging / &quot;cmdline-tools&quot;), str(destination))</code> | Invoca shutil.move com os argumentos declarados nesta instrução. Argumentos: str(staging / &#x27;cmdline-tools&#x27;), str(destination) |
| <a id="L58"></a>58 | <code>            for executable in (destination / &quot;bin&quot;).iterdir():</code> | Percorre (destination / &#x27;bin&#x27;).iterdir(), atribuindo cada elemento a executable. |
| <a id="L59"></a>59 | <code>                executable.chmod(0o755)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 493 |
| <a id="L60"></a>60 | <code>        gradle = args.tools_root / f&quot;gradle-{GRADLE_VERSION}&quot;</code> | Define gradle com args.tools_root / f&#x27;gradle-{GRADLE_VERSION}&#x27;. |
| <a id="L61"></a>61 | <code>        if not gradle.exists():</code> | Executa este ramo somente se not gradle.exists(); caso contrário, segue o ramo alternativo. |
| <a id="L62"></a>62 | <code>            archive = staging / &quot;gradle.zip&quot;</code> | Define archive com staging / &#x27;gradle.zip&#x27;. |
| <a id="L63"></a>63 | <code>            base = f&quot;https://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip&quot;</code> | Define base com f&#x27;https://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip&#x27;. |
| <a id="L64"></a>64 | <code>            expected = urllib.request.urlopen(base + &quot;.sha256&quot;, timeout=30).read().decode().strip()</code> | Define expected com urllib.request.urlopen(base + &#x27;.sha256&#x27;, timeout=30).read().decode().strip(). Invoca urllib.request.urlopen(base + &#x27;.sha256&#x27;, timeout=30).read().decode().strip com os argumentos declarados nesta instrução. |
| <a id="L65"></a>65 | <code>            download(base, archive)</code> | Invoca download com os argumentos declarados nesta instrução. Argumentos: base, archive |
| <a id="L66"></a>66 | <code>            if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:</code> | Executa este ramo somente se hashlib.sha256(archive.read_bytes()).hexdigest() != expected; caso contrário, segue o ramo alternativo. |
| <a id="L67"></a>67 | <code>                raise RuntimeError(&quot;Gradle archive checksum mismatch&quot;)</code> | Interrompe este caminho lançando RuntimeError(&#x27;Gradle archive checksum mismatch&#x27;). |
| <a id="L68"></a>68 | <code>            extract(archive, args.tools_root)</code> | Invoca extract com os argumentos declarados nesta instrução. Argumentos: archive, args.tools_root |
| <a id="L69"></a>69 | <code>            (gradle / &quot;bin/gradle&quot;).chmod(0o755)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 493 |
| <a id="L70"></a>70 | <code>    packages = [&quot;platform-tools&quot;, &quot;platforms;android-36&quot;, &quot;build-tools;36.0.0&quot;]</code> | Define packages com [&#x27;platform-tools&#x27;, &#x27;platforms;android-36&#x27;, &#x27;build-tools;36.0.0&#x27;]. |
| <a id="L71"></a>71 | <code>    if args.emulator:</code> | Executa este ramo somente se args.emulator; caso contrário, segue o ramo alternativo. |
| <a id="L72"></a>72 | <code>        packages.extend([&quot;emulator&quot;, &quot;system-images;android-36;google_apis;x86_64&quot;])</code> | Invoca packages.extend com os argumentos declarados nesta instrução. Argumentos: [&#x27;emulator&#x27;, &#x27;system-images;android-36;google_apis;x86_64&#x27;] |
| <a id="L73"></a>73 | <code>    log = args.tools_root / &quot;android-sdk-install.log&quot;</code> | Define log com args.tools_root / &#x27;android-sdk-install.log&#x27;. |
| <a id="L74"></a>74 | <code>    with log.open(&quot;wb&quot;) as output:</code> | Abre contexto(s) log.open(&#x27;wb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L75"></a>75 | <code>        subprocess.run(</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L76"></a>76 | <code>            [str(manager), f&quot;--sdk_root={args.sdk_root}&quot;, &quot;--licenses&quot;],</code> | Continua/fecha a instrução da linha 75. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L77"></a>77 | <code>            input=b&quot;y\n&quot; * 100,</code> | Continua/fecha a instrução da linha 75. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L78"></a>78 | <code>            stdout=output,</code> | Continua/fecha a instrução da linha 75. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L79"></a>79 | <code>            stderr=subprocess.STDOUT,</code> | Continua/fecha a instrução da linha 75. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L80"></a>80 | <code>            check=True,</code> | Continua/fecha a instrução da linha 75. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L81"></a>81 | <code>        )</code> | Continua/fecha a instrução da linha 75. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, &#x27;--licenses&#x27;], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L82"></a>82 | <code>        subprocess.run(</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L83"></a>83 | <code>            [str(manager), f&quot;--sdk_root={args.sdk_root}&quot;, *packages],</code> | Continua/fecha a instrução da linha 82. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L84"></a>84 | <code>            input=b&quot;y\n&quot; * 100,</code> | Continua/fecha a instrução da linha 82. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L85"></a>85 | <code>            stdout=output,</code> | Continua/fecha a instrução da linha 82. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L86"></a>86 | <code>            stderr=subprocess.STDOUT,</code> | Continua/fecha a instrução da linha 82. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L87"></a>87 | <code>            check=True,</code> | Continua/fecha a instrução da linha 82. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L88"></a>88 | <code>        )</code> | Continua/fecha a instrução da linha 82. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(manager), f&#x27;--sdk_root={args.sdk_root}&#x27;, *packages], input=b&#x27;y\n&#x27; * 100, stdout=output, stderr=subprocess.STDOUT, check=True |
| <a id="L89"></a>89 | <code>    print(</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L90"></a>90 | <code>        {</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L91"></a>91 | <code>            &quot;sdk_root&quot;: str(args.sdk_root),</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L92"></a>92 | <code>            &quot;gradle&quot;: str(gradle / &quot;bin/gradle&quot;),</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L93"></a>93 | <code>            &quot;packages&quot;: packages,</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L94"></a>94 | <code>            &quot;log&quot;: str(log),</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L95"></a>95 | <code>        }</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L96"></a>96 | <code>    )</code> | Continua/fecha a instrução da linha 89. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;sdk_root&#x27;: str(args.sdk_root), &#x27;gradle&#x27;: str(gradle / &#x27;bin/gradle&#x27;), &#x27;packages&#x27;: packages, &#x27;log&#x27;: str(log)} |
| <a id="L97"></a>97 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L98"></a>98 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L99"></a>99 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L100"></a>100 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
