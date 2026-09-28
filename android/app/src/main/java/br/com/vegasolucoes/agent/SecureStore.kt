package br.com.vegasolucoes.agent

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.AtomicFile
import android.util.Base64
import java.io.File
import java.security.KeyStore
import java.util.UUID
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec
import org.json.JSONObject

// Documentação: Define o tipo SessionData e reúne o estado/contrato descrito para este módulo.
data class SessionData(
    val server: String,
    val access: String,
    val refresh: String,
    val expiresAt: Long,
    val deviceId: String,
    val username: String,
    val userId: String = "",
    val timezone: String = "America/Sao_Paulo",
)

// Documentação: Define o tipo SecureStore e reúne o estado/contrato descrito para este módulo.
class SecureStore(private val context: Context) {
    private val sessionFile = AtomicFile(File(context.noBackupFilesDir, "session.bin"))
    private val deviceFile = File(context.noBackupFilesDir, "device-id")
    private val alias = "devlima-session-v1"

    @Synchronized
    // Documentação: Recupera ou gera chave AES no Android Keystore sem exportar seu material para
    // o aplicativo.
    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(alias, null) as? SecretKey)?.let {
            return it
        }
        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
            .apply {
                init(
                    KeyGenParameterSpec.Builder(
                            alias,
                            KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
                        )
                        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                        .build()
                )
            }
            .generateKey()
    }

    @Synchronized
    // Documentação: Cifra UTF-8 com IV GCM novo e AAD do applicationId, retornando envelope
    // Base64.
    fun encrypt(text: String): String {
        val cipher =
            Cipher.getInstance("AES/GCM/NoPadding").apply {
                init(Cipher.ENCRYPT_MODE, key())
                updateAAD(BuildConfig.APPLICATION_ID.toByteArray())
            }
        return Base64.encodeToString(
            cipher.iv + cipher.doFinal(text.toByteArray(Charsets.UTF_8)),
            Base64.NO_WRAP,
        )
    }

    @Synchronized
    // Documentação: Valida tamanho e autentica o envelope AES-GCM antes de retornar texto UTF-8.
    fun decrypt(text: String): String {
        val bytes = Base64.decode(text, Base64.NO_WRAP)
        require(bytes.size > 28)
        val cipher =
            Cipher.getInstance("AES/GCM/NoPadding").apply {
                init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, bytes.copyOfRange(0, 12)))
                updateAAD(BuildConfig.APPLICATION_ID.toByteArray())
            }
        return cipher.doFinal(bytes.copyOfRange(12, bytes.size)).toString(Charsets.UTF_8)
    }

    @Synchronized
    // Documentação: Implementa SecureStore.deviceId como parte do fluxo descrito para este
    // arquivo.
    fun deviceId(): String {
        if (deviceFile.exists()) return UUID.fromString(deviceFile.readText()).toString()
        return UUID.randomUUID().toString().also { deviceFile.writeText(it) }
    }

    @Synchronized
    // Documentação: Persiste SecureStore.save, segundo o contrato e as verificações deste módulo.
    fun save(data: SessionData) {
        val json =
            JSONObject()
                .put("server", data.server)
                .put("access", data.access)
                .put("refresh", data.refresh)
                .put("expiresAt", data.expiresAt)
                .put("deviceId", data.deviceId)
                .put("username", data.username)
                .put("userId", data.userId)
                .put("timezone", data.timezone)
        val stream = sessionFile.startWrite()
        try {
            stream.write(encrypt(json.toString()).toByteArray())
            sessionFile.finishWrite(stream)
        } catch (issue: Exception) {
            sessionFile.failWrite(stream)
            throw issue
        }
    }

    @Synchronized
    // Documentação: Carrega SecureStore.load, segundo o contrato e as verificações deste módulo.
    fun load(): SessionData? =
        try {
            val data =
                JSONObject(
                    decrypt(sessionFile.openRead().use { it.readBytes().toString(Charsets.UTF_8) })
                )
            SessionData(
                data.getString("server"),
                data.getString("access"),
                data.getString("refresh"),
                data.getLong("expiresAt"),
                data.getString("deviceId"),
                data.getString("username"),
                data.optString("userId"),
                data.optString("timezone", "America/Sao_Paulo"),
            )
        } catch (_: Exception) {
            null
        }

    @Synchronized
    // Documentação: Limpa SecureStore.clear, segundo o contrato e as verificações deste módulo.
    fun clear() {
        sessionFile.delete()
        deviceFile.delete()
    }
}
