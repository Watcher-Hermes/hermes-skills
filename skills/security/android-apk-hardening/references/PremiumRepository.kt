// ***REMOVED-BASE64***
// PremiumRepository.kt — Android client referansı
//
// Kilit fikir: client KARAR VERMEZ, İSTER. "Premium miyim?" diye kendine
// sormaz; sunucudan korunan veriyi ister.
// ***REMOVED-BASE64***

import com.google.android.play.core.integrity.IntegrityManagerFactory
import com.google.android.play.core.integrity.IntegrityTokenRequest
import kotlinx.coroutines.tasks.await
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

// ---------------------------------------------------------------------------
// ❌ YANLIŞ — kararı client veriyor. Tek satır smali yamasıyla kırılır.
// ---------------------------------------------------------------------------
object BadGate {
    fun isPremium(): Boolean {
        val v = Prefs.getBoolean("is_premium", false)
        return v
    }
    fun showFeature() {
        if (isPremium()) {
            renderPremiumUi()
        }
    }
}

// ---------------------------------------------------------------------------
// ✅ DOĞRU — client sadece ister; karar ve veri sunucuda.
// ---------------------------------------------------------------------------
class PremiumRepository(
    private val http: OkHttpClient,
    private val baseUrl: String,
    private val sessionToken: String,
    private val context: android.content.Context,
) {
    private val json = "application/json".toMediaType()

    suspend fun fetchPremiumData(): JSONObject? {
        val nonce = requestNonce() ?: return null
        val integrityToken = requestIntegrityToken(nonce) ?: return null

        val body = JSONObject()
            .put("integrityToken", integrityToken)
            .put("nonce", nonce)
            .toString().toRequestBody(json)

        val req = Request.Builder()
            .url("$baseUrl/premium/data")
            .header("Authorization", "Bearer $sessionToken")
            .post(body).build()

        http.newCall(req).execute().use { resp ->
            if (!resp.isSuccessful) return null
            return JSONObject(resp.body?.string() ?: return null)
        }
    }

    private suspend fun requestNonce(): String? {
        val req = Request.Builder()
            .url("$baseUrl/integrity/nonce")
            .header("Authorization", "Bearer $sessionToken")
            .post(ByteArray(0).toRequestBody()).build()
        http.newCall(req).execute().use { resp ->
            if (!resp.isSuccessful) return null
            val text = resp.body?.string() ?: return null
            return JSONObject(text).optString("nonce").ifEmpty { null }
        }
    }

    private suspend fun requestIntegrityToken(nonce: String): String? {
        return try {
            val manager = IntegrityManagerFactory.create(context)
            val response = manager.requestIntegrityToken(
                IntegrityTokenRequest.builder().setNonce(nonce).build()
            ).await()
            response.token()
        } catch (_: Exception) { null }
    }
}

private object Prefs { fun getBoolean(k: String, d: Boolean) = d }
private fun renderPremiumUi(vararg a: Any?) {}
