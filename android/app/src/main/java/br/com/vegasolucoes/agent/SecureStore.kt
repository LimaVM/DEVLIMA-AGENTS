package br.com.vegasolucoes.agent

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.AtomicFile
import android.util.Base64
import org.json.JSONObject
import java.io.File
import java.security.KeyStore
import java.util.UUID
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

data class SessionData(val server: String, val access: String, val refresh: String, val expiresAt: Long, val deviceId: String, val username: String)

class SecureStore(private val context: Context) {
    private val sessionFile = AtomicFile(File(context.noBackupFilesDir, "session.bin"))
    private val deviceFile = File(context.noBackupFilesDir, "device-id")
    private val alias = "devlima-session-v1"
    @Synchronized private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(alias, null) as? SecretKey)?.let { return it }
        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore").apply {
            init(KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).build())
        }.generateKey()
    }
    @Synchronized fun encrypt(text: String): String {
        val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply { init(Cipher.ENCRYPT_MODE, key()); updateAAD(BuildConfig.APPLICATION_ID.toByteArray()) }
        return Base64.encodeToString(cipher.iv + cipher.doFinal(text.toByteArray(Charsets.UTF_8)), Base64.NO_WRAP)
    }
    @Synchronized fun decrypt(text: String): String {
        val bytes = Base64.decode(text, Base64.NO_WRAP)
        require(bytes.size > 28)
        val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply { init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, bytes.copyOfRange(0,12))); updateAAD(BuildConfig.APPLICATION_ID.toByteArray()) }
        return cipher.doFinal(bytes.copyOfRange(12,bytes.size)).toString(Charsets.UTF_8)
    }
    @Synchronized fun deviceId(): String {
        if (deviceFile.exists()) return UUID.fromString(deviceFile.readText()).toString()
        return UUID.randomUUID().toString().also { deviceFile.writeText(it) }
    }
    @Synchronized fun save(data: SessionData) {
        val json = JSONObject().put("server",data.server).put("access",data.access).put("refresh",data.refresh).put("expiresAt",data.expiresAt).put("deviceId",data.deviceId).put("username",data.username)
        val stream = sessionFile.startWrite()
        try { stream.write(encrypt(json.toString()).toByteArray()); sessionFile.finishWrite(stream) }
        catch (issue: Exception) { sessionFile.failWrite(stream); throw issue }
    }
    @Synchronized fun load(): SessionData? = try {
        val data = JSONObject(decrypt(sessionFile.openRead().use { it.readBytes().toString(Charsets.UTF_8) }))
        SessionData(data.getString("server"),data.getString("access"),data.getString("refresh"),data.getLong("expiresAt"),data.getString("deviceId"),data.getString("username"))
    } catch (_: Exception) { null }
    @Synchronized fun clear() { sessionFile.delete(); deviceFile.delete() }
}
