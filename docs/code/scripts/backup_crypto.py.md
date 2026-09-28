# scripts/backup_crypto.py

Implementa envelope de backup autenticado em streaming, leitura segura da chave externa, cifragem/decifragem AES-GCM e SHA-256.

[Arquivo fonte](../../../scripts/backup_crypto.py) · 79 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [secret](#L12) | Implementa secret como parte do fluxo descrito para este arquivo. |
| [encrypt](#L23) | Implementa encrypt como parte do fluxo descrito para este arquivo. |
| [decrypt](#L38) | Implementa decrypt como parte do fluxo descrito para este arquivo. |
| [sha256](#L72) | Implementa sha256 como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>&quot;&quot;&quot;Streaming, authenticated AES-256-GCM backup envelope. Keys are external binary files.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>import os</code> | Importa módulo(s) os. |
| <a id="L4"></a>4 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes</code> | Importa Cipher, algorithms, modes de cryptography.hazmat.primitives.ciphers. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>MAGIC = b&quot;DLAGBACKUP1&quot;</code> | Define MAGIC com b&#x27;DLAGBACKUP1&#x27;. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L11"></a>11 | <code># Documentação: Implementa secret como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa secret como parte do fluxo descrito para este arquivo. |
| <a id="L12"></a>12 | <code>def secret(path):</code> | Implementa secret como parte do fluxo descrito para este arquivo. |
| <a id="L13"></a>13 | <code>    path = Path(path)</code> | Define path com Path(path). Invoca Path com os argumentos declarados nesta instrução. Argumentos: path |
| <a id="L14"></a>14 | <code>    if path.stat().st_mode &amp; 0o077:</code> | Executa este ramo somente se path.stat().st_mode &amp; 63; caso contrário, segue o ramo alternativo. |
| <a id="L15"></a>15 | <code>        raise ValueError(&quot;Backup key must have mode 0600&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Backup key must have mode 0600&#x27;). |
| <a id="L16"></a>16 | <code>    key = path.read_bytes()</code> | Define key com path.read_bytes(). Invoca path.read_bytes com os argumentos declarados nesta instrução. |
| <a id="L17"></a>17 | <code>    if len(key) != 32:</code> | Executa este ramo somente se len(key) != 32; caso contrário, segue o ramo alternativo. |
| <a id="L18"></a>18 | <code>        raise ValueError(&quot;Backup key must be exactly 32 bytes&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Backup key must be exactly 32 bytes&#x27;). |
| <a id="L19"></a>19 | <code>    return key</code> | Retorna key ao chamador e encerra este caminho da função. |
| <a id="L20"></a>20 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L22"></a>22 | <code># Documentação: Implementa encrypt como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa encrypt como parte do fluxo descrito para este arquivo. |
| <a id="L23"></a>23 | <code>def encrypt(source, target, key_path):</code> | Implementa encrypt como parte do fluxo descrito para este arquivo. |
| <a id="L24"></a>24 | <code>    nonce = os.urandom(12)</code> | Define nonce com os.urandom(12). Invoca os.urandom com os argumentos declarados nesta instrução. Argumentos: 12 |
| <a id="L25"></a>25 | <code>    encryptor = Cipher(algorithms.AES(secret(key_path)), modes.GCM(nonce)).encryptor()</code> | Define encryptor com Cipher(algorithms.AES(secret(key_path)), modes.GCM(nonce)).encryptor(). Invoca Cipher(algorithms.AES(secret(key_path)), modes.GCM(nonce)).encryptor com os argumentos declarados nesta instrução. |
| <a id="L26"></a>26 | <code>    header = MAGIC + nonce</code> | Define header com MAGIC + nonce. |
| <a id="L27"></a>27 | <code>    encryptor.authenticate_additional_data(header)</code> | Invoca encryptor.authenticate_additional_data com os argumentos declarados nesta instrução. Argumentos: header |
| <a id="L28"></a>28 | <code>    with open(source, &quot;rb&quot;) as input_file, open(target, &quot;xb&quot;) as output:</code> | Abre contexto(s) open(source, &#x27;rb&#x27;), open(target, &#x27;xb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L29"></a>29 | <code>        os.chmod(target, 0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: target, 384 |
| <a id="L30"></a>30 | <code>        output.write(header)</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: header |
| <a id="L31"></a>31 | <code>        while block := input_file.read(1024 * 1024):</code> | Repete este bloco enquanto (block := input_file.read(1024 * 1024)) permanecer verdadeiro. |
| <a id="L32"></a>32 | <code>            output.write(encryptor.update(block))</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: encryptor.update(block) |
| <a id="L33"></a>33 | <code>        output.write(encryptor.finalize())</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: encryptor.finalize() |
| <a id="L34"></a>34 | <code>        output.write(encryptor.tag)</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: encryptor.tag |
| <a id="L35"></a>35 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L36"></a>36 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L37"></a>37 | <code># Documentação: Implementa decrypt como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa decrypt como parte do fluxo descrito para este arquivo. |
| <a id="L38"></a>38 | <code>def decrypt(source, target, key_path):</code> | Implementa decrypt como parte do fluxo descrito para este arquivo. |
| <a id="L39"></a>39 | <code>    with open(source, &quot;rb&quot;) as input_file:</code> | Abre contexto(s) open(source, &#x27;rb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L40"></a>40 | <code>        header = input_file.read(len(MAGIC) + 12)</code> | Define header com input_file.read(len(MAGIC) + 12). Invoca input_file.read com os argumentos declarados nesta instrução. Argumentos: len(MAGIC) + 12 |
| <a id="L41"></a>41 | <code>        if not header.startswith(MAGIC):</code> | Executa este ramo somente se not header.startswith(MAGIC); caso contrário, segue o ramo alternativo. |
| <a id="L42"></a>42 | <code>            raise ValueError(&quot;Invalid backup envelope&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Invalid backup envelope&#x27;). |
| <a id="L43"></a>43 | <code>        input_file.seek(-16, 2)</code> | Invoca input_file.seek com os argumentos declarados nesta instrução. Argumentos: -16, 2 |
| <a id="L44"></a>44 | <code>        tag = input_file.read(16)</code> | Define tag com input_file.read(16). Invoca input_file.read com os argumentos declarados nesta instrução. Argumentos: 16 |
| <a id="L45"></a>45 | <code>        remaining = input_file.tell() - 16 - len(header)</code> | Define remaining com input_file.tell() - 16 - len(header). |
| <a id="L46"></a>46 | <code>        if remaining &lt; 0:</code> | Executa este ramo somente se remaining &lt; 0; caso contrário, segue o ramo alternativo. |
| <a id="L47"></a>47 | <code>            raise ValueError(&quot;Truncated backup&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Truncated backup&#x27;). |
| <a id="L48"></a>48 | <code>        input_file.seek(len(header))</code> | Invoca input_file.seek com os argumentos declarados nesta instrução. Argumentos: len(header) |
| <a id="L49"></a>49 | <code>        decryptor = Cipher(</code> | Define decryptor com Cipher(algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC):], tag)).decryptor(). Invoca Cipher(algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC):], tag)).decryptor com os argumentos declarados nesta instrução. |
| <a id="L50"></a>50 | <code>            algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC) :], tag)</code> | Continua/fecha a instrução da linha 49. Define decryptor com Cipher(algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC):], tag)).decryptor(). Invoca Cipher(algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC):], tag)).decryptor com os argumentos declarados nesta instrução. |
| <a id="L51"></a>51 | <code>        ).decryptor()</code> | Continua/fecha a instrução da linha 49. Define decryptor com Cipher(algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC):], tag)).decryptor(). Invoca Cipher(algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC):], tag)).decryptor com os argumentos declarados nesta instrução. |
| <a id="L52"></a>52 | <code>        decryptor.authenticate_additional_data(header)</code> | Invoca decryptor.authenticate_additional_data com os argumentos declarados nesta instrução. Argumentos: header |
| <a id="L53"></a>53 | <code>        created = False</code> | Define created com False. |
| <a id="L54"></a>54 | <code>        try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L55"></a>55 | <code>            with open(target, &quot;xb&quot;) as output:</code> | Abre contexto(s) open(target, &#x27;xb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L56"></a>56 | <code>                created = True</code> | Define created com True. |
| <a id="L57"></a>57 | <code>                os.chmod(target, 0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: target, 384 |
| <a id="L58"></a>58 | <code>                while remaining:</code> | Repete este bloco enquanto remaining permanecer verdadeiro. |
| <a id="L59"></a>59 | <code>                    block = input_file.read(min(1024 * 1024, remaining))</code> | Define block com input_file.read(min(1024 * 1024, remaining)). Invoca input_file.read com os argumentos declarados nesta instrução. Argumentos: min(1024 * 1024, remaining) |
| <a id="L60"></a>60 | <code>                    if not block:</code> | Executa este ramo somente se not block; caso contrário, segue o ramo alternativo. |
| <a id="L61"></a>61 | <code>                        raise ValueError(&quot;Truncated backup&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Truncated backup&#x27;). |
| <a id="L62"></a>62 | <code>                    remaining -= len(block)</code> | Atualiza remaining com len(block). Invoca len com os argumentos declarados nesta instrução. Argumentos: block |
| <a id="L63"></a>63 | <code>                    output.write(decryptor.update(block))</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: decryptor.update(block) |
| <a id="L64"></a>64 | <code>                output.write(decryptor.finalize())</code> | Invoca output.write com os argumentos declarados nesta instrução. Argumentos: decryptor.finalize() |
| <a id="L65"></a>65 | <code>        except Exception:</code> | Trata exceção Exception. |
| <a id="L66"></a>66 | <code>            if created:</code> | Executa este ramo somente se created; caso contrário, segue o ramo alternativo. |
| <a id="L67"></a>67 | <code>                Path(target).unlink(missing_ok=True)</code> | Remove exclusivamente o caminho de arquivo indicado. Argumentos: missing_ok=True |
| <a id="L68"></a>68 | <code>            raise</code> | Interrompe este caminho lançando None. |
| <a id="L69"></a>69 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L70"></a>70 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L71"></a>71 | <code># Documentação: Implementa sha256 como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa sha256 como parte do fluxo descrito para este arquivo. |
| <a id="L72"></a>72 | <code>def sha256(path):</code> | Implementa sha256 como parte do fluxo descrito para este arquivo. |
| <a id="L73"></a>73 | <code>    import hashlib</code> | Importa módulo(s) hashlib. |
| <a id="L74"></a>74 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L75"></a>75 | <code>    digest = hashlib.sha256()</code> | Define digest com hashlib.sha256(). Calcula digest SHA-256 para identificação/integridade conforme o contexto. |
| <a id="L76"></a>76 | <code>    with open(path, &quot;rb&quot;) as source:</code> | Abre contexto(s) open(path, &#x27;rb&#x27;); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L77"></a>77 | <code>        while block := source.read(1024 * 1024):</code> | Repete este bloco enquanto (block := source.read(1024 * 1024)) permanecer verdadeiro. |
| <a id="L78"></a>78 | <code>            digest.update(block)</code> | Invoca digest.update com os argumentos declarados nesta instrução. Argumentos: block |
| <a id="L79"></a>79 | <code>    return digest.hexdigest()</code> | Retorna digest.hexdigest() ao chamador e encerra este caminho da função. |
