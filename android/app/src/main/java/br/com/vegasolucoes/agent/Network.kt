package br.com.vegasolucoes.agent

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import org.json.JSONObject
import java.util.concurrent.TimeUnit
import kotlin.random.Random

class ApiFailure(val status: Int,val code: String): Exception(code)
class LoginRequired: Exception("login_required")

fun normalizedServer(value: String): String {
    val url=value.trim().toHttpUrlOrNull() ?: throw IllegalArgumentException("Informe uma URL HTTPS válida")
    require(url.scheme=="https" && url.username.isEmpty() && url.password.isEmpty() && url.query==null && url.fragment==null && url.encodedPath=="/") { "Use HTTPS e apenas o domínio, sem credenciais ou caminho" }
    return url.toString().removeSuffix("/")
}

class Backoff {
    private var attempt=0
    fun reset() { attempt=0 }
    fun nextDelay(): Long { val base=(1000L shl attempt.coerceAtMost(6)).coerceAtMost(60000);attempt=(attempt+1).coerceAtMost(6);return (base*Random.nextDouble(0.8,1.2)).toLong().coerceIn(1000,60000) }
}

class AuthRepository(private val secure: SecureStore) {
    val session=MutableStateFlow(secure.load())
    private val refreshLock=Mutex()
    val http=OkHttpClient.Builder().connectTimeout(10,TimeUnit.SECONDS).readTimeout(130,TimeUnit.SECONDS).writeTimeout(20,TimeUnit.SECONDS).pingInterval(20,TimeUnit.SECONDS).build()
    private fun request(server: String,path: String,data: JSONObject?=null,token: String?=null,method: String=if(data==null)"GET" else "POST"): String {
        val builder=Request.Builder().url(server+path)
        token?.let { builder.header("Authorization","Bearer $it") }
        builder.method(method,data?.toString()?.toRequestBody("application/json; charset=utf-8".toMediaType()))
        http.newCall(builder.build()).execute().use { response ->
            val body=response.body?.string() ?: ""
            if(!response.isSuccessful) throw ApiFailure(response.code,"http_${response.code}")
            return body
        }
    }
    suspend fun login(serverInput: String,username: String,password: String) = withContext(Dispatchers.IO) {
        refreshLock.withLock {
            val server=normalizedServer(serverInput)
            val id=secure.deviceId()
            val answer=JSONObject(request(server,"/auth/login",JSONObject().put("username",username.trim()).put("password",password).put("device_id",id)))
            val data=SessionData(server,answer.getString("access_token"),answer.getString("refresh_token"),System.currentTimeMillis()+answer.getLong("expires_in")*1000,id,username.trim())
            secure.save(data);session.value=data
        }
    }
    suspend fun access(): SessionData = withContext(Dispatchers.IO) {
        refreshLock.withLock {
            val current=session.value ?: throw LoginRequired()
            if(current.expiresAt-System.currentTimeMillis()>60000) return@withLock current
            try {
                val answer=JSONObject(request(current.server,"/auth/refresh",JSONObject().put("refresh_token",current.refresh)))
                val updated=current.copy(access=answer.getString("access_token"),refresh=answer.getString("refresh_token"),expiresAt=System.currentTimeMillis()+answer.getLong("expires_in")*1000)
                secure.save(updated);session.value=updated;updated
            } catch (issue: ApiFailure) {
                if(issue.status==401 || issue.status==403) { secure.clear();session.value=null;throw LoginRequired() }
                throw issue
            }
        }
    }
    suspend fun invalidateAccess() { refreshLock.withLock { session.value?.let { val data=it.copy(expiresAt=0);secure.save(data);session.value=data } } }
    suspend fun api(path: String,method: String="GET",data: JSONObject?=null): String = withContext(Dispatchers.IO) {
        val current=access()
        try { request(current.server,path,data,current.access,method) }
        catch(issue: ApiFailure) {
            if(issue.status!=401) throw issue
            invalidateAccess();val updated=access();request(updated.server,path,data,updated.access,method)
        }
    }
    suspend fun logout() = withContext(Dispatchers.IO) {
        refreshLock.withLock {
            session.value?.let { try { request(it.server,"/auth/logout",JSONObject(),it.access) } catch (_:Exception) { } }
            secure.clear();session.value=null
        }
    }
}
