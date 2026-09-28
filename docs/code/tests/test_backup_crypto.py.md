# tests/test_backup_crypto.py

Verifica roundtrip/autenticação do backup, falha com pacote alterado ou chave incorreta e validação de parâmetros do envelope.

[Arquivo fonte](../../../tests/test_backup_crypto.py) · 88 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [BackupCryptoTests](#L18) | Define o tipo BackupCryptoTests e reúne o estado/contrato descrito para este módulo. |
| [BackupCryptoTests.test_streaming_roundtrip_and_tampering_never_leaves_plaintext](#L22) | Verifica o cenário test_streaming_roundtrip_and_tampering_never_leaves_plaintext; as condições e resultados esperados aparecem nos asserts. |
| [BackupCryptoTests.test_wrong_key_and_header_are_rejected](#L52) | Verifica o cenário test_wrong_key_and_header_are_rejected; as condições e resultados esperados aparecem nos asserts. |
| [BackupCryptoTests.test_public_key_file_permissions_and_length_are_refused](#L74) | Verifica o cenário test_public_key_file_permissions_and_length_are_refused; as condições e resultados esperados aparecem nos asserts. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import importlib.util</code> | Importa módulo(s) importlib.util. |
| <a id="L2"></a>2 | <code>import os</code> | Importa módulo(s) os. |
| <a id="L3"></a>3 | <code>import tempfile</code> | Importa módulo(s) tempfile. |
| <a id="L4"></a>4 | <code>import unittest</code> | Importa módulo(s) unittest. |
| <a id="L5"></a>5 | <code>from pathlib import Path</code> | Importa Path de pathlib. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from cryptography.exceptions import InvalidTag</code> | Importa InvalidTag de cryptography.exceptions. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>spec = importlib.util.spec_from_file_location(</code> | Define spec com importlib.util.spec_from_file_location(&#x27;backup_crypto&#x27;, Path(__file__).resolve().parents[1] / &#x27;scripts/backup_crypto.py&#x27;). Invoca importlib.util.spec_from_file_location com os argumentos declarados nesta instrução. Argumentos: &#x27;backup_crypto&#x27;, Path(__file__).resolve().parents[1] / &#x27;scripts/backup_crypto.py&#x27; |
| <a id="L10"></a>10 | <code>    &quot;backup_crypto&quot;, Path(__file__).resolve().parents[1] / &quot;scripts/backup_crypto.py&quot;</code> | Continua/fecha a instrução da linha 9. Define spec com importlib.util.spec_from_file_location(&#x27;backup_crypto&#x27;, Path(__file__).resolve().parents[1] / &#x27;scripts/backup_crypto.py&#x27;). Invoca importlib.util.spec_from_file_location com os argumentos declarados nesta instrução. Argumentos: &#x27;backup_crypto&#x27;, Path(__file__).resolve().parents[1] / &#x27;scripts/backup_crypto.py&#x27; |
| <a id="L11"></a>11 | <code>)</code> | Continua/fecha a instrução da linha 9. Define spec com importlib.util.spec_from_file_location(&#x27;backup_crypto&#x27;, Path(__file__).resolve().parents[1] / &#x27;scripts/backup_crypto.py&#x27;). Invoca importlib.util.spec_from_file_location com os argumentos declarados nesta instrução. Argumentos: &#x27;backup_crypto&#x27;, Path(__file__).resolve().parents[1] / &#x27;scripts/backup_crypto.py&#x27; |
| <a id="L12"></a>12 | <code>crypto = importlib.util.module_from_spec(spec)</code> | Define crypto com importlib.util.module_from_spec(spec). Invoca importlib.util.module_from_spec com os argumentos declarados nesta instrução. Argumentos: spec |
| <a id="L13"></a>13 | <code>spec.loader.exec_module(crypto)</code> | Invoca spec.loader.exec_module com os argumentos declarados nesta instrução. Argumentos: crypto |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L16"></a>16 | <code># Documentação: Define o tipo BackupCryptoTests e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo BackupCryptoTests e reúne o estado/contrato descrito para este |
| <a id="L17"></a>17 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L18"></a>18 | <code>class BackupCryptoTests(unittest.TestCase):</code> | Define o tipo BackupCryptoTests e reúne o estado/contrato descrito para este módulo. |
| <a id="L19"></a>19 | <code>    # Documentação: Verifica o cenário</code> | Comentário: Documentação: Verifica o cenário |
| <a id="L20"></a>20 | <code>    # test_streaming_roundtrip_and_tampering_never_leaves_plaintext; as condições e resultados</code> | Comentário: test_streaming_roundtrip_and_tampering_never_leaves_plaintext; as condições e resultados |
| <a id="L21"></a>21 | <code>    # esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L22"></a>22 | <code>    def test_streaming_roundtrip_and_tampering_never_leaves_plaintext(self):</code> | Verifica o cenário test_streaming_roundtrip_and_tampering_never_leaves_plaintext; as condições e resultados esperados aparecem nos asserts. |
| <a id="L23"></a>23 | <code>        with tempfile.TemporaryDirectory() as temporary:</code> | Abre contexto(s) tempfile.TemporaryDirectory(); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L24"></a>24 | <code>            root = Path(temporary)</code> | Define root com Path(temporary). Invoca Path com os argumentos declarados nesta instrução. Argumentos: temporary |
| <a id="L25"></a>25 | <code>            key = root / &quot;key&quot;</code> | Define key com root / &#x27;key&#x27;. |
| <a id="L26"></a>26 | <code>            key.write_bytes(os.urandom(32))</code> | Invoca key.write_bytes com os argumentos declarados nesta instrução. Argumentos: os.urandom(32) |
| <a id="L27"></a>27 | <code>            key.chmod(0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 384 |
| <a id="L28"></a>28 | <code>            original = root / &quot;original&quot;</code> | Define original com root / &#x27;original&#x27;. |
| <a id="L29"></a>29 | <code>            original.write_bytes(os.urandom(3 * 1024 * 1024 + 57))</code> | Invoca original.write_bytes com os argumentos declarados nesta instrução. Argumentos: os.urandom(3 * 1024 * 1024 + 57) |
| <a id="L30"></a>30 | <code>            encrypted = root / &quot;encrypted&quot;</code> | Define encrypted com root / &#x27;encrypted&#x27;. |
| <a id="L31"></a>31 | <code>            crypto.encrypt(original, encrypted, key)</code> | Cifra/autentica conteúdo usando o componente de armazenamento indicado. Argumentos: original, encrypted, key |
| <a id="L32"></a>32 | <code>            restored = root / &quot;restored&quot;</code> | Define restored com root / &#x27;restored&#x27;. |
| <a id="L33"></a>33 | <code>            crypto.decrypt(encrypted, restored, key)</code> | Autentica/decifra conteúdo antes de disponibilizá-lo ao restante do fluxo. Argumentos: encrypted, restored, key |
| <a id="L34"></a>34 | <code>            self.assertEqual(crypto.sha256(original), crypto.sha256(restored))</code> | Invoca self.assertEqual com os argumentos declarados nesta instrução. Argumentos: crypto.sha256(original), crypto.sha256(restored) |
| <a id="L35"></a>35 | <code>            self.assertEqual(restored.stat().st_mode &amp; 0o777, 0o600)</code> | Invoca self.assertEqual com os argumentos declarados nesta instrução. Argumentos: restored.stat().st_mode &amp; 511, 384 |
| <a id="L36"></a>36 | <code>            damaged = bytearray(encrypted.read_bytes())</code> | Define damaged com bytearray(encrypted.read_bytes()). Invoca bytearray com os argumentos declarados nesta instrução. Argumentos: encrypted.read_bytes() |
| <a id="L37"></a>37 | <code>            damaged[len(crypto.MAGIC) + 100] ^= 1</code> | Atualiza damaged[len(crypto.MAGIC) + 100] com 1. |
| <a id="L38"></a>38 | <code>            corrupt = root / &quot;corrupt&quot;</code> | Define corrupt com root / &#x27;corrupt&#x27;. |
| <a id="L39"></a>39 | <code>            corrupt.write_bytes(damaged)</code> | Invoca corrupt.write_bytes com os argumentos declarados nesta instrução. Argumentos: damaged |
| <a id="L40"></a>40 | <code>            rejected = root / &quot;rejected&quot;</code> | Define rejected com root / &#x27;rejected&#x27;. |
| <a id="L41"></a>41 | <code>            with self.assertRaises(InvalidTag):</code> | Abre contexto(s) self.assertRaises(InvalidTag); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L42"></a>42 | <code>                crypto.decrypt(corrupt, rejected, key)</code> | Autentica/decifra conteúdo antes de disponibilizá-lo ao restante do fluxo. Argumentos: corrupt, rejected, key |
| <a id="L43"></a>43 | <code>            self.assertFalse(rejected.exists())</code> | Invoca self.assertFalse com os argumentos declarados nesta instrução. Argumentos: rejected.exists() |
| <a id="L44"></a>44 | <code>            existing = root / &quot;existing&quot;</code> | Define existing com root / &#x27;existing&#x27;. |
| <a id="L45"></a>45 | <code>            existing.write_text(&quot;must remain&quot;)</code> | Invoca existing.write_text com os argumentos declarados nesta instrução. Argumentos: &#x27;must remain&#x27; |
| <a id="L46"></a>46 | <code>            with self.assertRaises(FileExistsError):</code> | Abre contexto(s) self.assertRaises(FileExistsError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L47"></a>47 | <code>                crypto.decrypt(encrypted, existing, key)</code> | Autentica/decifra conteúdo antes de disponibilizá-lo ao restante do fluxo. Argumentos: encrypted, existing, key |
| <a id="L48"></a>48 | <code>            self.assertEqual(existing.read_text(), &quot;must remain&quot;)</code> | Invoca self.assertEqual com os argumentos declarados nesta instrução. Argumentos: existing.read_text(), &#x27;must remain&#x27; |
| <a id="L49"></a>49 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L50"></a>50 | <code>    # Documentação: Verifica o cenário test_wrong_key_and_header_are_rejected; as condições e</code> | Comentário: Documentação: Verifica o cenário test_wrong_key_and_header_are_rejected; as condições e |
| <a id="L51"></a>51 | <code>    # resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L52"></a>52 | <code>    def test_wrong_key_and_header_are_rejected(self):</code> | Verifica o cenário test_wrong_key_and_header_are_rejected; as condições e resultados esperados aparecem nos asserts. |
| <a id="L53"></a>53 | <code>        with tempfile.TemporaryDirectory() as temporary:</code> | Abre contexto(s) tempfile.TemporaryDirectory(); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L54"></a>54 | <code>            root = Path(temporary)</code> | Define root com Path(temporary). Invoca Path com os argumentos declarados nesta instrução. Argumentos: temporary |
| <a id="L55"></a>55 | <code>            for name in (&quot;a&quot;, &quot;b&quot;):</code> | Percorre (&#x27;a&#x27;, &#x27;b&#x27;), atribuindo cada elemento a name. |
| <a id="L56"></a>56 | <code>                (root / name).write_bytes(os.urandom(32))</code> | Invoca (root / name).write_bytes com os argumentos declarados nesta instrução. Argumentos: os.urandom(32) |
| <a id="L57"></a>57 | <code>                (root / name).chmod(0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 384 |
| <a id="L58"></a>58 | <code>            source = root / &quot;source&quot;</code> | Define source com root / &#x27;source&#x27;. |
| <a id="L59"></a>59 | <code>            source.write_bytes(b&quot;private information&quot;)</code> | Invoca source.write_bytes com os argumentos declarados nesta instrução. Argumentos: b&#x27;private information&#x27; |
| <a id="L60"></a>60 | <code>            encrypted = root / &quot;encrypted&quot;</code> | Define encrypted com root / &#x27;encrypted&#x27;. |
| <a id="L61"></a>61 | <code>            crypto.encrypt(source, encrypted, root / &quot;a&quot;)</code> | Cifra/autentica conteúdo usando o componente de armazenamento indicado. Argumentos: source, encrypted, root / &#x27;a&#x27; |
| <a id="L62"></a>62 | <code>            with self.assertRaises(InvalidTag):</code> | Abre contexto(s) self.assertRaises(InvalidTag); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L63"></a>63 | <code>                crypto.decrypt(encrypted, root / &quot;bad&quot;, root / &quot;b&quot;)</code> | Autentica/decifra conteúdo antes de disponibilizá-lo ao restante do fluxo. Argumentos: encrypted, root / &#x27;bad&#x27;, root / &#x27;b&#x27; |
| <a id="L64"></a>64 | <code>            self.assertFalse((root / &quot;bad&quot;).exists())</code> | Invoca self.assertFalse com os argumentos declarados nesta instrução. Argumentos: (root / &#x27;bad&#x27;).exists() |
| <a id="L65"></a>65 | <code>            blob = bytearray(encrypted.read_bytes())</code> | Define blob com bytearray(encrypted.read_bytes()). Invoca bytearray com os argumentos declarados nesta instrução. Argumentos: encrypted.read_bytes() |
| <a id="L66"></a>66 | <code>            blob[0] ^= 1</code> | Atualiza blob[0] com 1. |
| <a id="L67"></a>67 | <code>            encrypted.write_bytes(blob)</code> | Invoca encrypted.write_bytes com os argumentos declarados nesta instrução. Argumentos: blob |
| <a id="L68"></a>68 | <code>            with self.assertRaises(ValueError):</code> | Abre contexto(s) self.assertRaises(ValueError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L69"></a>69 | <code>                crypto.decrypt(encrypted, root / &quot;bad&quot;, root / &quot;a&quot;)</code> | Autentica/decifra conteúdo antes de disponibilizá-lo ao restante do fluxo. Argumentos: encrypted, root / &#x27;bad&#x27;, root / &#x27;a&#x27; |
| <a id="L70"></a>70 | <code>            self.assertFalse((root / &quot;bad&quot;).exists())</code> | Invoca self.assertFalse com os argumentos declarados nesta instrução. Argumentos: (root / &#x27;bad&#x27;).exists() |
| <a id="L71"></a>71 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L72"></a>72 | <code>    # Documentação: Verifica o cenário test_public_key_file_permissions_and_length_are_refused; as</code> | Comentário: Documentação: Verifica o cenário test_public_key_file_permissions_and_length_are_refused; as |
| <a id="L73"></a>73 | <code>    # condições e resultados esperados aparecem nos asserts.</code> | Comentário: condições e resultados esperados aparecem nos asserts. |
| <a id="L74"></a>74 | <code>    def test_public_key_file_permissions_and_length_are_refused(self):</code> | Verifica o cenário test_public_key_file_permissions_and_length_are_refused; as condições e resultados esperados aparecem nos asserts. |
| <a id="L75"></a>75 | <code>        with tempfile.TemporaryDirectory() as temporary:</code> | Abre contexto(s) tempfile.TemporaryDirectory(); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L76"></a>76 | <code>            key = Path(temporary) / &quot;key&quot;</code> | Define key com Path(temporary) / &#x27;key&#x27;. |
| <a id="L77"></a>77 | <code>            key.write_bytes(os.urandom(32))</code> | Invoca key.write_bytes com os argumentos declarados nesta instrução. Argumentos: os.urandom(32) |
| <a id="L78"></a>78 | <code>            key.chmod(0o644)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 420 |
| <a id="L79"></a>79 | <code>            with self.assertRaises(ValueError):</code> | Abre contexto(s) self.assertRaises(ValueError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L80"></a>80 | <code>                crypto.secret(key)</code> | Invoca crypto.secret com os argumentos declarados nesta instrução. Argumentos: key |
| <a id="L81"></a>81 | <code>            key.chmod(0o600)</code> | Aplica as permissões de arquivo declaradas no argumento. Argumentos: 384 |
| <a id="L82"></a>82 | <code>            key.write_bytes(b&quot;short&quot;)</code> | Invoca key.write_bytes com os argumentos declarados nesta instrução. Argumentos: b&#x27;short&#x27; |
| <a id="L83"></a>83 | <code>            with self.assertRaises(ValueError):</code> | Abre contexto(s) self.assertRaises(ValueError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L84"></a>84 | <code>                crypto.secret(key)</code> | Invoca crypto.secret com os argumentos declarados nesta instrução. Argumentos: key |
| <a id="L85"></a>85 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L86"></a>86 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L87"></a>87 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L88"></a>88 | <code>    unittest.main()</code> | Invoca unittest.main com os argumentos declarados nesta instrução. |
