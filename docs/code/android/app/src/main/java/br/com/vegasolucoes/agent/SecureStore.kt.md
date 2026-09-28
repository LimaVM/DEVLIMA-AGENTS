# android/app/src/main/java/br/com/vegasolucoes/agent/SecureStore.kt

Cifra sessão/conteúdo com AES-GCM usando chave Android Keystore e escrita atômica em no_backup; dados são vinculados ao applicationId por AAD.

[Arquivo fonte](../../../../../../../../../../../android/app/src/main/java/br/com/vegasolucoes/agent/SecureStore.kt) · 145 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [SessionData](#L18) | Define o tipo SessionData e reúne o estado/contrato descrito para este módulo. |
| [SecureStore](#L30) | Define o tipo SecureStore e reúne o estado/contrato descrito para este módulo. |
| [SecureStore.key](#L38) | Recupera ou gera chave AES no Android Keystore sem exportar seu material para o aplicativo. |
| [SecureStore.encrypt](#L61) | Cifra UTF-8 com IV GCM novo e AAD do applicationId, retornando envelope Base64. |
| [SecureStore.decrypt](#L75) | Valida tamanho e autentica o envelope AES-GCM antes de retornar texto UTF-8. |
| [SecureStore.deviceId](#L89) | Implementa SecureStore.deviceId como parte do fluxo descrito para este arquivo. |
| [SecureStore.save](#L96) | Persiste SecureStore.save, segundo o contrato e as verificações deste módulo. |
| [SecureStore.load](#L119) | Carrega SecureStore.load, segundo o contrato e as verificações deste módulo. |
| [SecureStore.clear](#L141) | Limpa SecureStore.clear, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>package br.com.vegasolucoes.agent</code> | Associa as declarações ao namespace br.com.vegasolucoes.agent. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L3"></a>3 | <code>import android.content.Context</code> | Disponibiliza o símbolo Kotlin/Android android.content.Context neste arquivo. |
| <a id="L4"></a>4 | <code>import android.security.keystore.KeyGenParameterSpec</code> | Disponibiliza o símbolo Kotlin/Android android.security.keystore.KeyGenParameterSpec neste arquivo. |
| <a id="L5"></a>5 | <code>import android.security.keystore.KeyProperties</code> | Disponibiliza o símbolo Kotlin/Android android.security.keystore.KeyProperties neste arquivo. |
| <a id="L6"></a>6 | <code>import android.util.AtomicFile</code> | Disponibiliza o símbolo Kotlin/Android android.util.AtomicFile neste arquivo. |
| <a id="L7"></a>7 | <code>import android.util.Base64</code> | Disponibiliza o símbolo Kotlin/Android android.util.Base64 neste arquivo. |
| <a id="L8"></a>8 | <code>import java.io.File</code> | Disponibiliza o símbolo Kotlin/Android java.io.File neste arquivo. |
| <a id="L9"></a>9 | <code>import java.security.KeyStore</code> | Disponibiliza o símbolo Kotlin/Android java.security.KeyStore neste arquivo. |
| <a id="L10"></a>10 | <code>import java.util.UUID</code> | Disponibiliza o símbolo Kotlin/Android java.util.UUID neste arquivo. |
| <a id="L11"></a>11 | <code>import javax.crypto.Cipher</code> | Disponibiliza o símbolo Kotlin/Android javax.crypto.Cipher neste arquivo. Usa primitiva criptográfica; modo, IV e AAD são configurados nas linhas próximas. |
| <a id="L12"></a>12 | <code>import javax.crypto.KeyGenerator</code> | Disponibiliza o símbolo Kotlin/Android javax.crypto.KeyGenerator neste arquivo. |
| <a id="L13"></a>13 | <code>import javax.crypto.SecretKey</code> | Disponibiliza o símbolo Kotlin/Android javax.crypto.SecretKey neste arquivo. |
| <a id="L14"></a>14 | <code>import javax.crypto.spec.GCMParameterSpec</code> | Disponibiliza o símbolo Kotlin/Android javax.crypto.spec.GCMParameterSpec neste arquivo. |
| <a id="L15"></a>15 | <code>import org.json.JSONObject</code> | Disponibiliza o símbolo Kotlin/Android org.json.JSONObject neste arquivo. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L17"></a>17 | <code>// Documentação: Define o tipo SessionData e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo SessionData e reúne o estado/contrato descrito para este módulo. |
| <a id="L18"></a>18 | <code>data class SessionData(</code> | Define o tipo SessionData e reúne o estado/contrato descrito para este módulo. |
| <a id="L19"></a>19 | <code>    val server: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L20"></a>20 | <code>    val access: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L21"></a>21 | <code>    val refresh: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L22"></a>22 | <code>    val expiresAt: Long,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L23"></a>23 | <code>    val deviceId: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L24"></a>24 | <code>    val username: String,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L25"></a>25 | <code>    val userId: String = &quot;&quot;,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L26"></a>26 | <code>    val timezone: String = &quot;America/Sao_Paulo&quot;,</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L27"></a>27 | <code>)</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L28"></a>28 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L29"></a>29 | <code>// Documentação: Define o tipo SecureStore e reúne o estado/contrato descrito para este módulo.</code> | Comentário de manutenção/documentação: Documentação: Define o tipo SecureStore e reúne o estado/contrato descrito para este módulo. |
| <a id="L30"></a>30 | <code>class SecureStore(private val context: Context) {</code> | Define o tipo SecureStore e reúne o estado/contrato descrito para este módulo. |
| <a id="L31"></a>31 | <code>    private val sessionFile = AtomicFile(File(context.noBackupFilesDir, &quot;session.bin&quot;))</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L32"></a>32 | <code>    private val deviceFile = File(context.noBackupFilesDir, &quot;device-id&quot;)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L33"></a>33 | <code>    private val alias = &quot;devlima-session-v1&quot;</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L35"></a>35 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L36"></a>36 | <code>    // Documentação: Recupera ou gera chave AES no Android Keystore sem exportar seu material para</code> | Comentário de manutenção/documentação: Documentação: Recupera ou gera chave AES no Android Keystore sem exportar seu material para |
| <a id="L37"></a>37 | <code>    // o aplicativo.</code> | Comentário de manutenção/documentação: o aplicativo. |
| <a id="L38"></a>38 | <code>    private fun key(): SecretKey {</code> | Recupera ou gera chave AES no Android Keystore sem exportar seu material para o aplicativo. |
| <a id="L39"></a>39 | <code>        val store = KeyStore.getInstance(&quot;AndroidKeyStore&quot;).apply { load(null) }</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L40"></a>40 | <code>        (store.getKey(alias, null) as? SecretKey)?.let {</code> | Invoca/continua store.getKey com os argumentos declarados. |
| <a id="L41"></a>41 | <code>            return it</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L42"></a>42 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L43"></a>43 | <code>        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, &quot;AndroidKeyStore&quot;)</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L44"></a>44 | <code>            .apply {</code> | Fornece a expressão .apply { ao bloco/chamada em construção. |
| <a id="L45"></a>45 | <code>                init(</code> | Invoca/continua init com os argumentos declarados. |
| <a id="L46"></a>46 | <code>                    KeyGenParameterSpec.Builder(</code> | Invoca/continua KeyGenParameterSpec.Builder com os argumentos declarados. |
| <a id="L47"></a>47 | <code>                            alias,</code> | Fornece a expressão alias, ao bloco/chamada em construção. |
| <a id="L48"></a>48 | <code>                            KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,</code> | Fornece a expressão KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT, ao bloco/chamada em construção. |
| <a id="L49"></a>49 | <code>                        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L50"></a>50 | <code>                        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)</code> | Invoca/continua setBlockModes com os argumentos declarados. |
| <a id="L51"></a>51 | <code>                        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)</code> | Invoca/continua setEncryptionPaddings com os argumentos declarados. |
| <a id="L52"></a>52 | <code>                        .build()</code> | Invoca/continua build com os argumentos declarados. |
| <a id="L53"></a>53 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L54"></a>54 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L55"></a>55 | <code>            .generateKey()</code> | Invoca/continua generateKey com os argumentos declarados. |
| <a id="L56"></a>56 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L57"></a>57 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L58"></a>58 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L59"></a>59 | <code>    // Documentação: Cifra UTF-8 com IV GCM novo e AAD do applicationId, retornando envelope</code> | Comentário de manutenção/documentação: Documentação: Cifra UTF-8 com IV GCM novo e AAD do applicationId, retornando envelope |
| <a id="L60"></a>60 | <code>    // Base64.</code> | Comentário de manutenção/documentação: Base64. |
| <a id="L61"></a>61 | <code>    fun encrypt(text: String): String {</code> | Cifra UTF-8 com IV GCM novo e AAD do applicationId, retornando envelope Base64. |
| <a id="L62"></a>62 | <code>        val cipher =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L63"></a>63 | <code>            Cipher.getInstance(&quot;AES/GCM/NoPadding&quot;).apply {</code> | Invoca/continua Cipher.getInstance com os argumentos declarados. Usa primitiva criptográfica; modo, IV e AAD são configurados nas linhas próximas. |
| <a id="L64"></a>64 | <code>                init(Cipher.ENCRYPT_MODE, key())</code> | Invoca/continua init com os argumentos declarados. Usa primitiva criptográfica; modo, IV e AAD são configurados nas linhas próximas. |
| <a id="L65"></a>65 | <code>                updateAAD(BuildConfig.APPLICATION_ID.toByteArray())</code> | Invoca/continua updateAAD com os argumentos declarados. Vincula autenticação GCM ao applicationId declarado. |
| <a id="L66"></a>66 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L67"></a>67 | <code>        return Base64.encodeToString(</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L68"></a>68 | <code>            cipher.iv + cipher.doFinal(text.toByteArray(Charsets.UTF_8)),</code> | Invoca/continua cipher.doFinal com os argumentos declarados. |
| <a id="L69"></a>69 | <code>            Base64.NO_WRAP,</code> | Fornece a expressão Base64.NO_WRAP, ao bloco/chamada em construção. |
| <a id="L70"></a>70 | <code>        )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L71"></a>71 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L72"></a>72 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L73"></a>73 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L74"></a>74 | <code>    // Documentação: Valida tamanho e autentica o envelope AES-GCM antes de retornar texto UTF-8.</code> | Comentário de manutenção/documentação: Documentação: Valida tamanho e autentica o envelope AES-GCM antes de retornar texto UTF-8. |
| <a id="L75"></a>75 | <code>    fun decrypt(text: String): String {</code> | Valida tamanho e autentica o envelope AES-GCM antes de retornar texto UTF-8. |
| <a id="L76"></a>76 | <code>        val bytes = Base64.decode(text, Base64.NO_WRAP)</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L77"></a>77 | <code>        require(bytes.size &gt; 28)</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L78"></a>78 | <code>        val cipher =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L79"></a>79 | <code>            Cipher.getInstance(&quot;AES/GCM/NoPadding&quot;).apply {</code> | Invoca/continua Cipher.getInstance com os argumentos declarados. Usa primitiva criptográfica; modo, IV e AAD são configurados nas linhas próximas. |
| <a id="L80"></a>80 | <code>                init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, bytes.copyOfRange(0, 12)))</code> | Invoca/continua init com os argumentos declarados. Usa primitiva criptográfica; modo, IV e AAD são configurados nas linhas próximas. |
| <a id="L81"></a>81 | <code>                updateAAD(BuildConfig.APPLICATION_ID.toByteArray())</code> | Invoca/continua updateAAD com os argumentos declarados. Vincula autenticação GCM ao applicationId declarado. |
| <a id="L82"></a>82 | <code>            }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L83"></a>83 | <code>        return cipher.doFinal(bytes.copyOfRange(12, bytes.size)).toString(Charsets.UTF_8)</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L84"></a>84 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L85"></a>85 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L86"></a>86 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L87"></a>87 | <code>    // Documentação: Implementa SecureStore.deviceId como parte do fluxo descrito para este</code> | Comentário de manutenção/documentação: Documentação: Implementa SecureStore.deviceId como parte do fluxo descrito para este |
| <a id="L88"></a>88 | <code>    // arquivo.</code> | Comentário de manutenção/documentação: arquivo. |
| <a id="L89"></a>89 | <code>    fun deviceId(): String {</code> | Implementa SecureStore.deviceId como parte do fluxo descrito para este arquivo. |
| <a id="L90"></a>90 | <code>        if (deviceFile.exists()) return UUID.fromString(deviceFile.readText()).toString()</code> | Escolhe este caminho somente quando a condição indicada é satisfeita. |
| <a id="L91"></a>91 | <code>        return UUID.randomUUID().toString().also { deviceFile.writeText(it) }</code> | Encerra este caminho e devolve o resultado ao chamador/label indicado. |
| <a id="L92"></a>92 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L93"></a>93 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L94"></a>94 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L95"></a>95 | <code>    // Documentação: Persiste SecureStore.save, segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: Documentação: Persiste SecureStore.save, segundo o contrato e as verificações deste módulo. |
| <a id="L96"></a>96 | <code>    fun save(data: SessionData) {</code> | Persiste SecureStore.save, segundo o contrato e as verificações deste módulo. |
| <a id="L97"></a>97 | <code>        val json =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L98"></a>98 | <code>            JSONObject()</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L99"></a>99 | <code>                .put(&quot;server&quot;, data.server)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L100"></a>100 | <code>                .put(&quot;access&quot;, data.access)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L101"></a>101 | <code>                .put(&quot;refresh&quot;, data.refresh)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L102"></a>102 | <code>                .put(&quot;expiresAt&quot;, data.expiresAt)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L103"></a>103 | <code>                .put(&quot;deviceId&quot;, data.deviceId)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L104"></a>104 | <code>                .put(&quot;username&quot;, data.username)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L105"></a>105 | <code>                .put(&quot;userId&quot;, data.userId)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L106"></a>106 | <code>                .put(&quot;timezone&quot;, data.timezone)</code> | Invoca/continua put com os argumentos declarados. Adiciona ou atualiza campo/chave com o valor declarado. |
| <a id="L107"></a>107 | <code>        val stream = sessionFile.startWrite()</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L108"></a>108 | <code>        try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L109"></a>109 | <code>            stream.write(encrypt(json.toString()).toByteArray())</code> | Invoca/continua stream.write com os argumentos declarados. |
| <a id="L110"></a>110 | <code>            sessionFile.finishWrite(stream)</code> | Invoca/continua sessionFile.finishWrite com os argumentos declarados. |
| <a id="L111"></a>111 | <code>        } catch (issue: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L112"></a>112 | <code>            sessionFile.failWrite(stream)</code> | Invoca/continua sessionFile.failWrite com os argumentos declarados. |
| <a id="L113"></a>113 | <code>            throw issue</code> | Exige a condição/invariante indicada ou interrompe o fluxo com erro. |
| <a id="L114"></a>114 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L115"></a>115 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L116"></a>116 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L117"></a>117 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L118"></a>118 | <code>    // Documentação: Carrega SecureStore.load, segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: Documentação: Carrega SecureStore.load, segundo o contrato e as verificações deste módulo. |
| <a id="L119"></a>119 | <code>    fun load(): SessionData? =</code> | Carrega SecureStore.load, segundo o contrato e as verificações deste módulo. |
| <a id="L120"></a>120 | <code>        try {</code> | Fornece a expressão try { ao bloco/chamada em construção. |
| <a id="L121"></a>121 | <code>            val data =</code> | Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado. |
| <a id="L122"></a>122 | <code>                JSONObject(</code> | Invoca/continua JSONObject com os argumentos declarados. Monta/interpreta objeto JSON usado pelo contrato do Core/cache. |
| <a id="L123"></a>123 | <code>                    decrypt(sessionFile.openRead().use { it.readBytes().toString(Charsets.UTF_8) })</code> | Invoca/continua decrypt com os argumentos declarados. Garante fechamento do recurso ao terminar este bloco, incluindo falha. |
| <a id="L124"></a>124 | <code>                )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L125"></a>125 | <code>            SessionData(</code> | Invoca/continua SessionData com os argumentos declarados. |
| <a id="L126"></a>126 | <code>                data.getString(&quot;server&quot;),</code> | Invoca/continua data.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L127"></a>127 | <code>                data.getString(&quot;access&quot;),</code> | Invoca/continua data.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L128"></a>128 | <code>                data.getString(&quot;refresh&quot;),</code> | Invoca/continua data.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L129"></a>129 | <code>                data.getLong(&quot;expiresAt&quot;),</code> | Invoca/continua data.getLong com os argumentos declarados. |
| <a id="L130"></a>130 | <code>                data.getString(&quot;deviceId&quot;),</code> | Invoca/continua data.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L131"></a>131 | <code>                data.getString(&quot;username&quot;),</code> | Invoca/continua data.getString com os argumentos declarados. Lê o campo textual indicado; campo ausente/incompatível pode falhar. |
| <a id="L132"></a>132 | <code>                data.optString(&quot;userId&quot;),</code> | Invoca/continua data.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L133"></a>133 | <code>                data.optString(&quot;timezone&quot;, &quot;America/Sao_Paulo&quot;),</code> | Invoca/continua data.optString com os argumentos declarados. Lê texto opcional, aplicando fallback declarado quando necessário. |
| <a id="L134"></a>134 | <code>            )</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L135"></a>135 | <code>        } catch (_: Exception) {</code> | Invoca/continua catch com os argumentos declarados. |
| <a id="L136"></a>136 | <code>            null</code> | Fornece a expressão null ao bloco/chamada em construção. |
| <a id="L137"></a>137 | <code>        }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L138"></a>138 | <code>∅</code> | Linha em branco para separar declarações/blocos; não executa uma ação. |
| <a id="L139"></a>139 | <code>    @Synchronized</code> | Aplica a anotação @Synchronized à declaração seguinte. |
| <a id="L140"></a>140 | <code>    // Documentação: Limpa SecureStore.clear, segundo o contrato e as verificações deste módulo.</code> | Comentário de manutenção/documentação: Documentação: Limpa SecureStore.clear, segundo o contrato e as verificações deste módulo. |
| <a id="L141"></a>141 | <code>    fun clear() {</code> | Limpa SecureStore.clear, segundo o contrato e as verificações deste módulo. |
| <a id="L142"></a>142 | <code>        sessionFile.delete()</code> | Invoca/continua sessionFile.delete com os argumentos declarados. |
| <a id="L143"></a>143 | <code>        deviceFile.delete()</code> | Invoca/continua deviceFile.delete com os argumentos declarados. |
| <a id="L144"></a>144 | <code>    }</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
| <a id="L145"></a>145 | <code>}</code> | Fecha delimitador de bloco, chamada, coleção ou lista de argumentos iniciada acima. |
