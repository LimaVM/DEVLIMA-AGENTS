# scripts/install_vm_manager.py

Instala runtime/serviço do manager e arquivos operacionais após verificar caminhos e recursos, conservando infraestrutura previamente existente.

[Arquivo fonte](../../../scripts/install_vm_manager.py) · 108 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [run](#L15) | Implementa run como parte do fluxo descrito para este arquivo. |
| [main](#L22) | Coordena a entrada de linha de comando deste arquivo: Instala runtime/serviço do manager e arquivos operacionais após verificar caminhos e recursos, conservando infraestrutura previamente existente. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>&quot;&quot;&quot;Install private VM Manager as root on the already inspected Ubuntu host.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>import argparse</code> | Importa módulo(s) argparse. |
| <a id="L4"></a>4 | <code>import grp</code> | Importa módulo(s) grp. |
| <a id="L5"></a>5 | <code>import os</code> | Importa módulo(s) os. |
| <a id="L6"></a>6 | <code>import secrets</code> | Importa módulo(s) secrets. |
| <a id="L7"></a>7 | <code>import shutil</code> | Importa módulo(s) shutil. |
| <a id="L8"></a>8 | <code>import subprocess</code> | Importa módulo(s) subprocess. |
| <a id="L9"></a>9 | <code>import time</code> | Importa módulo(s) time. |
| <a id="L10"></a>10 | <code>import xml.etree.ElementTree as ET</code> | Importa módulo(s) xml.etree.ElementTree. |
| <a id="L11"></a>11 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L12"></a>12 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code># Documentação: Implementa run como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa run como parte do fluxo descrito para este arquivo. |
| <a id="L15"></a>15 | <code>def run(args):</code> | Implementa run como parte do fluxo descrito para este arquivo. |
| <a id="L16"></a>16 | <code>    subprocess.run(args, check=True)</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: args, check=True |
| <a id="L17"></a>17 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L18"></a>18 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L19"></a>19 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Instala runtime/serviço do</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Instala runtime/serviço do |
| <a id="L20"></a>20 | <code># manager e arquivos operacionais após verificar caminhos e recursos, conservando infraestrutura</code> | Comentário: manager e arquivos operacionais após verificar caminhos e recursos, conservando infraestrutura |
| <a id="L21"></a>21 | <code># previamente existente.</code> | Comentário: previamente existente. |
| <a id="L22"></a>22 | <code>def main():</code> | Coordena a entrada de linha de comando deste arquivo: Instala runtime/serviço do manager e arquivos operacionais após verificar caminhos e recursos, conservando infraestrutura previamente existente. |
| <a id="L23"></a>23 | <code>    parser = argparse.ArgumentParser()</code> | Define parser com argparse.ArgumentParser(). Invoca argparse.ArgumentParser com os argumentos declarados nesta instrução. |
| <a id="L24"></a>24 | <code>    parser.add_argument(&quot;--project&quot;, type=Path, default=Path(&quot;/srv/devlima-agent&quot;))</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--project&#x27;, type=Path, default=Path(&#x27;/srv/devlima-agent&#x27;) |
| <a id="L25"></a>25 | <code>    args = parser.parse_args()</code> | Define args com parser.parse_args(). Invoca parser.parse_args com os argumentos declarados nesta instrução. |
| <a id="L26"></a>26 | <code>    if os.geteuid() != 0:</code> | Executa este ramo somente se os.geteuid() != 0; caso contrário, segue o ramo alternativo. |
| <a id="L27"></a>27 | <code>        raise SystemExit(&quot;Run as root on the VM host&quot;)</code> | Interrompe este caminho lançando SystemExit(&#x27;Run as root on the VM host&#x27;). |
| <a id="L28"></a>28 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L29"></a>29 | <code>        grp.getgrgid(10001)</code> | Invoca grp.getgrgid com os argumentos declarados nesta instrução. Argumentos: 10001 |
| <a id="L30"></a>30 | <code>    except KeyError:</code> | Trata exceção KeyError. |
| <a id="L31"></a>31 | <code>        run([&quot;groupadd&quot;, &quot;--system&quot;, &quot;--gid&quot;, &quot;10001&quot;, &quot;devlima-core&quot;])</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;groupadd&#x27;, &#x27;--system&#x27;, &#x27;--gid&#x27;, &#x27;10001&#x27;, &#x27;devlima-core&#x27;] |
| <a id="L32"></a>32 | <code>    project = args.project.resolve(strict=True)</code> | Define project com args.project.resolve(strict=True). Invoca args.project.resolve com os argumentos declarados nesta instrução. Argumentos: strict=True |
| <a id="L33"></a>33 | <code>    source = project / &quot;vm-manager&quot;</code> | Define source com project / &#x27;vm-manager&#x27;. |
| <a id="L34"></a>34 | <code>    destination = Path(&quot;/opt/devlima-vm-manager&quot;)</code> | Define destination com Path(&#x27;/opt/devlima-vm-manager&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/opt/devlima-vm-manager&#x27; |
| <a id="L35"></a>35 | <code>    destination.mkdir(mode=0o755, exist_ok=True)</code> | Prepara diretório conforme permissões e opções declaradas. Argumentos: mode=493, exist_ok=True |
| <a id="L36"></a>36 | <code>    shutil.copytree(source / &quot;vm_manager&quot;, destination / &quot;vm_manager&quot;, dirs_exist_ok=True)</code> | Invoca shutil.copytree com os argumentos declarados nesta instrução. Argumentos: source / &#x27;vm_manager&#x27;, destination / &#x27;vm_manager&#x27;, dirs_exist_ok=True |
| <a id="L37"></a>37 | <code>    shutil.copyfile(source / &quot;requirements.txt&quot;, destination / &quot;requirements.txt&quot;)</code> | Invoca shutil.copyfile com os argumentos declarados nesta instrução. Argumentos: source / &#x27;requirements.txt&#x27;, destination / &#x27;requirements.txt&#x27; |
| <a id="L38"></a>38 | <code>    for directory in (Path(&quot;/var/lib/libvirt/images/devlima-workers&quot;),):</code> | Percorre (Path(&#x27;/var/lib/libvirt/images/devlima-workers&#x27;),), atribuindo cada elemento a directory. |
| <a id="L39"></a>39 | <code>        directory.mkdir(parents=True, exist_ok=True, mode=0o755)</code> | Prepara diretório conforme permissões e opções declaradas. Argumentos: parents=True, exist_ok=True, mode=493 |
| <a id="L40"></a>40 | <code>        directory.chmod(0o755)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 493 |
| <a id="L41"></a>41 | <code>    state = Path(&quot;/var/lib/devlima-vm-manager&quot;)</code> | Define state com Path(&#x27;/var/lib/devlima-vm-manager&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/var/lib/devlima-vm-manager&#x27; |
| <a id="L42"></a>42 | <code>    state.mkdir(mode=0o700, exist_ok=True)</code> | Prepara diretório conforme permissões e opções declaradas. Argumentos: mode=448, exist_ok=True |
| <a id="L43"></a>43 | <code>    state.chmod(0o700)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 448 |
| <a id="L44"></a>44 | <code>    config = Path(&quot;/etc/devlima-vm-manager.env&quot;)</code> | Define config com Path(&#x27;/etc/devlima-vm-manager.env&#x27;). Invoca Path com os argumentos declarados nesta instrução. Argumentos: &#x27;/etc/devlima-vm-manager.env&#x27; |
| <a id="L45"></a>45 | <code>    token = None</code> | Define token com None. |
| <a id="L46"></a>46 | <code>    if config.exists():</code> | Executa este ramo somente se config.exists(); caso contrário, segue o ramo alternativo. |
| <a id="L47"></a>47 | <code>        for line in config.read_text().splitlines():</code> | Percorre config.read_text().splitlines(), atribuindo cada elemento a line. |
| <a id="L48"></a>48 | <code>            if line.startswith(&quot;VM_MANAGER_TOKEN=&quot;):</code> | Executa este ramo somente se line.startswith(&#x27;VM_MANAGER_TOKEN=&#x27;); caso contrário, segue o ramo alternativo. |
| <a id="L49"></a>49 | <code>                token = line.split(&quot;=&quot;, 1)[1]</code> | Define token com line.split(&#x27;=&#x27;, 1)[1]. |
| <a id="L50"></a>50 | <code>    if token is None:</code> | Executa este ramo somente se token is None; caso contrário, segue o ramo alternativo. |
| <a id="L51"></a>51 | <code>        token = secrets.token_urlsafe(48)</code> | Define token com secrets.token_urlsafe(48). Gera material aleatório com secrets para uso operacional externo. Argumentos: 48 |
| <a id="L52"></a>52 | <code>        descriptor = os.open(config, os.O_WRONLY &#124; os.O_CREAT &#124; os.O_EXCL, 0o600)</code> | Define descriptor com os.open(config, os.O_WRONLY &#124; os.O_CREAT &#124; os.O_EXCL, 384). Invoca os.open com os argumentos declarados nesta instrução. Argumentos: config, os.O_WRONLY &#124; os.O_CREAT &#124; os.O_EXCL, 384 |
| <a id="L53"></a>53 | <code>        with os.fdopen(descriptor, &quot;w&quot;) as output:</code> | Abre contexto(s) os.fdopen(descriptor, &#x27;w&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L54"></a>54 | <code>            output.write(&quot;VM_MANAGER_TOKEN=&quot; + token + &quot;\n&quot;)</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: &#x27;VM_MANAGER_TOKEN=&#x27; + token + &#x27;\n&#x27; |
| <a id="L55"></a>55 | <code>    if len(token) &lt; 32 or any(</code> | Executa este ramo somente se len(token) &lt; 32 or any((char not in &#x27;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_&#x27; for char in token)); caso contrário, segue o ramo alternativo. |
| <a id="L56"></a>56 | <code>        char not in &quot;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_&quot;</code> | Continua/fecha a instrução da linha 55. Executa este ramo somente se len(token) &lt; 32 or any((char not in &#x27;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_&#x27; for char in token)); caso contrário, segue o ramo alternativo. |
| <a id="L57"></a>57 | <code>        for char in token</code> | Continua/fecha a instrução da linha 55. Executa este ramo somente se len(token) &lt; 32 or any((char not in &#x27;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_&#x27; for char in token)); caso contrário, segue o ramo alternativo. |
| <a id="L58"></a>58 | <code>    ):</code> | Continua/fecha a instrução da linha 55. Executa este ramo somente se len(token) &lt; 32 or any((char not in &#x27;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_&#x27; for char in token)); caso contrário, segue o ramo alternativo. |
| <a id="L59"></a>59 | <code>        raise SystemExit(&quot;Invalid existing manager token&quot;)</code> | Interrompe este caminho lançando SystemExit(&#x27;Invalid existing manager token&#x27;). |
| <a id="L60"></a>60 | <code>    config.chmod(0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 384 |
| <a id="L61"></a>61 | <code>    env = project / &quot;.env&quot;</code> | Define env com project / &#x27;.env&#x27;. |
| <a id="L62"></a>62 | <code>    content = [</code> | Define content com [line for line in env.read_text().splitlines() if not line.startswith(&#x27;VM_MANAGER_TOKEN=&#x27;)]. |
| <a id="L63"></a>63 | <code>        line for line in env.read_text().splitlines() if not line.startswith(&quot;VM_MANAGER_TOKEN=&quot;)</code> | Continua/fecha a instrução da linha 62. Define content com [line for line in env.read_text().splitlines() if not line.startswith(&#x27;VM_MANAGER_TOKEN=&#x27;)]. |
| <a id="L64"></a>64 | <code>    ]</code> | Continua/fecha a instrução da linha 62. Define content com [line for line in env.read_text().splitlines() if not line.startswith(&#x27;VM_MANAGER_TOKEN=&#x27;)]. |
| <a id="L65"></a>65 | <code>    env.chmod(0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 384 |
| <a id="L66"></a>66 | <code>    env.write_text(&quot;\n&quot;.join(content) + &quot;\nVM_MANAGER_TOKEN=&quot; + token + &quot;\n&quot;)</code> | Invoca env.write_text com os argumentos declarados nesta instrução. Argumentos: &#x27;\n&#x27;.join(content) + &#x27;\nVM_MANAGER_TOKEN=&#x27; + token + &#x27;\n&#x27; |
| <a id="L67"></a>67 | <code>    venv = destination / &quot;venv&quot;</code> | Define venv com destination / &#x27;venv&#x27;. |
| <a id="L68"></a>68 | <code>    if not (venv / &quot;bin/python&quot;).exists():</code> | Executa este ramo somente se not (venv / &#x27;bin/python&#x27;).exists(); caso contrário, segue o ramo alternativo. |
| <a id="L69"></a>69 | <code>        run([&quot;/usr/bin/python3&quot;, &quot;-m&quot;, &quot;venv&quot;, &quot;--system-site-packages&quot;, str(venv)])</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;/usr/bin/python3&#x27;, &#x27;-m&#x27;, &#x27;venv&#x27;, &#x27;--system-site-packages&#x27;, str(venv)] |
| <a id="L70"></a>70 | <code>    run(</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L71"></a>71 | <code>        [</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L72"></a>72 | <code>            str(venv / &quot;bin/pip&quot;),</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L73"></a>73 | <code>            &quot;install&quot;,</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L74"></a>74 | <code>            &quot;--disable-pip-version-check&quot;,</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L75"></a>75 | <code>            &quot;-r&quot;,</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L76"></a>76 | <code>            str(destination / &quot;requirements.txt&quot;),</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L77"></a>77 | <code>        ]</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L78"></a>78 | <code>    )</code> | Continua/fecha a instrução da linha 70. Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [str(venv / &#x27;bin/pip&#x27;), &#x27;install&#x27;, &#x27;--disable-pip-version-check&#x27;, &#x27;-r&#x27;, str(destination / &#x27;requirements.txt&#x27;)] |
| <a id="L79"></a>79 | <code>    shutil.copyfile(</code> | Invoca shutil.copyfile com os argumentos declarados nesta instrução. Argumentos: source / &#x27;systemd/devlima-vm-manager.service&#x27;, &#x27;/etc/systemd/system/devlima-vm-manager.service&#x27; |
| <a id="L80"></a>80 | <code>        source / &quot;systemd/devlima-vm-manager.service&quot;,</code> | Continua/fecha a instrução da linha 79. Invoca shutil.copyfile com os argumentos declarados nesta instrução. Argumentos: source / &#x27;systemd/devlima-vm-manager.service&#x27;, &#x27;/etc/systemd/system/devlima-vm-manager.service&#x27; |
| <a id="L81"></a>81 | <code>        &quot;/etc/systemd/system/devlima-vm-manager.service&quot;,</code> | Continua/fecha a instrução da linha 79. Invoca shutil.copyfile com os argumentos declarados nesta instrução. Argumentos: source / &#x27;systemd/devlima-vm-manager.service&#x27;, &#x27;/etc/systemd/system/devlima-vm-manager.service&#x27; |
| <a id="L82"></a>82 | <code>    )</code> | Continua/fecha a instrução da linha 79. Invoca shutil.copyfile com os argumentos declarados nesta instrução. Argumentos: source / &#x27;systemd/devlima-vm-manager.service&#x27;, &#x27;/etc/systemd/system/devlima-vm-manager.service&#x27; |
| <a id="L83"></a>83 | <code>    filter_xml = ET.parse(source / &quot;systemd/devlima-worker-egress.xml&quot;).getroot()</code> | Define filter_xml com ET.parse(source / &#x27;systemd/devlima-worker-egress.xml&#x27;).getroot(). Invoca ET.parse(source / &#x27;systemd/devlima-worker-egress.xml&#x27;).getroot com os argumentos declarados nesta instrução. |
| <a id="L84"></a>84 | <code>    existing_filter = subprocess.run(</code> | Define existing_filter com subprocess.run([&#x27;virsh&#x27;, &#x27;nwfilter-dumpxml&#x27;, &#x27;devlima-worker-egress&#x27;], capture_output=True, check=False). Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;virsh&#x27;, &#x27;nwfilter-dumpxml&#x27;, &#x27;devlima-worker-egress&#x27;], capture_output=True, check=False |
| <a id="L85"></a>85 | <code>        [&quot;virsh&quot;, &quot;nwfilter-dumpxml&quot;, &quot;devlima-worker-egress&quot;], capture_output=True, check=False</code> | Continua/fecha a instrução da linha 84. Define existing_filter com subprocess.run([&#x27;virsh&#x27;, &#x27;nwfilter-dumpxml&#x27;, &#x27;devlima-worker-egress&#x27;], capture_output=True, check=False). Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;virsh&#x27;, &#x27;nwfilter-dumpxml&#x27;, &#x27;devlima-worker-egress&#x27;], capture_output=True, check=False |
| <a id="L86"></a>86 | <code>    )</code> | Continua/fecha a instrução da linha 84. Define existing_filter com subprocess.run([&#x27;virsh&#x27;, &#x27;nwfilter-dumpxml&#x27;, &#x27;devlima-worker-egress&#x27;], capture_output=True, check=False). Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;virsh&#x27;, &#x27;nwfilter-dumpxml&#x27;, &#x27;devlima-worker-egress&#x27;], capture_output=True, check=False |
| <a id="L87"></a>87 | <code>    if existing_filter.returncode == 0:</code> | Executa este ramo somente se existing_filter.returncode == 0; caso contrário, segue o ramo alternativo. |
| <a id="L88"></a>88 | <code>        ET.SubElement(filter_xml, &quot;uuid&quot;).text = ET.fromstring(existing_filter.stdout).findtext(</code> | Define ET.SubElement(filter_xml, &#x27;uuid&#x27;).text com ET.fromstring(existing_filter.stdout).findtext(&#x27;uuid&#x27;). Invoca ET.fromstring(existing_filter.stdout).findtext com os argumentos declarados nesta instrução. Argumentos: &#x27;uuid&#x27; |
| <a id="L89"></a>89 | <code>            &quot;uuid&quot;</code> | Continua/fecha a instrução da linha 88. Define ET.SubElement(filter_xml, &#x27;uuid&#x27;).text com ET.fromstring(existing_filter.stdout).findtext(&#x27;uuid&#x27;). Invoca ET.fromstring(existing_filter.stdout).findtext com os argumentos declarados nesta instrução. Argumentos: &#x27;uuid&#x27; |
| <a id="L90"></a>90 | <code>        )</code> | Continua/fecha a instrução da linha 88. Define ET.SubElement(filter_xml, &#x27;uuid&#x27;).text com ET.fromstring(existing_filter.stdout).findtext(&#x27;uuid&#x27;). Invoca ET.fromstring(existing_filter.stdout).findtext com os argumentos declarados nesta instrução. Argumentos: &#x27;uuid&#x27; |
| <a id="L91"></a>91 | <code>    filter_file = state / &quot;worker-filter.xml&quot;</code> | Define filter_file com state / &#x27;worker-filter.xml&#x27;. |
| <a id="L92"></a>92 | <code>    filter_file.write_text(ET.tostring(filter_xml, encoding=&quot;unicode&quot;))</code> | Invoca filter_file.write_text com os argumentos declarados nesta instrução. Argumentos: ET.tostring(filter_xml, encoding=&#x27;unicode&#x27;) |
| <a id="L93"></a>93 | <code>    run([&quot;virsh&quot;, &quot;nwfilter-define&quot;, str(filter_file)])</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;virsh&#x27;, &#x27;nwfilter-define&#x27;, str(filter_file)] |
| <a id="L94"></a>94 | <code>    run([&quot;systemctl&quot;, &quot;daemon-reload&quot;])</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;systemctl&#x27;, &#x27;daemon-reload&#x27;] |
| <a id="L95"></a>95 | <code>    run([&quot;systemctl&quot;, &quot;enable&quot;, &quot;devlima-vm-manager.service&quot;])</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;systemctl&#x27;, &#x27;enable&#x27;, &#x27;devlima-vm-manager.service&#x27;] |
| <a id="L96"></a>96 | <code>    run([&quot;systemctl&quot;, &quot;restart&quot;, &quot;devlima-vm-manager.service&quot;])</code> | Invoca run com os argumentos declarados; o receptor determina processo/runner. Argumentos: [&#x27;systemctl&#x27;, &#x27;restart&#x27;, &#x27;devlima-vm-manager.service&#x27;] |
| <a id="L97"></a>97 | <code>    for _ in range(30):</code> | Percorre range(30), atribuindo cada elemento a _. |
| <a id="L98"></a>98 | <code>        if Path(&quot;/run/devlima-vm-manager/api.sock&quot;).exists():</code> | Executa este ramo somente se Path(&#x27;/run/devlima-vm-manager/api.sock&#x27;).exists(); caso contrário, segue o ramo alternativo. |
| <a id="L99"></a>99 | <code>            break</code> | Sai do loop atual; o processamento continua após seu bloco. |
| <a id="L100"></a>100 | <code>        time.sleep(1)</code> | Invoca time.sleep com os argumentos declarados nesta instrução. Argumentos: 1 |
| <a id="L101"></a>101 | <code>    else:</code> | Ramo alternativo quando a condição anterior não é satisfeita. |
| <a id="L102"></a>102 | <code>        raise SystemExit(&quot;Manager socket did not appear; inspect systemd diagnostics&quot;)</code> | Interrompe este caminho lançando SystemExit(&#x27;Manager socket did not appear; inspect systemd diagnostics&#x27;). |
| <a id="L103"></a>103 | <code>    Path(&quot;/run/devlima-vm-manager/api.sock&quot;).chmod(0o660)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 432 |
| <a id="L104"></a>104 | <code>    print(&quot;Private VM Manager installed; token retained in protected env files only.&quot;)</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: &#x27;Private VM Manager installed; token retained in protected env files only.&#x27; |
| <a id="L105"></a>105 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L106"></a>106 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L107"></a>107 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L108"></a>108 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
