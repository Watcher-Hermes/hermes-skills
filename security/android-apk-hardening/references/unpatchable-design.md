# Neden Bu Tasarımda Yama Yapılamaz?

## Kısa Cevap

Cihazda atlanacak bir karar noktası yok.

## Uzun Cevap

### Yanlış Tasarım (Yamalanabilir)

```kotlin
fun isPremium(): Boolean {
    val v = Prefs.getBoolean("premium", false)
    return v
}
fun showFeature() {
    if (isPremium()) { renderPremiumUi() }
}
```

**Saldırgan:** `isPremium` smali'sinde `const/4 v0, 0x0` → `const/4 v0, 0x1`. 30 saniye.

### Doğru Tasarım (Yamalanamaz)

```kotlin
suspend fun fetchPremiumData(): JSONObject? {
    val nonce = requestNonce() ?: return null
    val integrityToken = requestIntegrityToken(nonce) ?: return null
    // sunucuya gönder, sunucu karar verir
    val resp = http.post("$baseUrl/premium/data", body)
    if (!resp.isSuccessful) return null
    return JSONObject(resp.body)
}
```

**Saldırgan:** Metodu "null dönme" diye yamalar ama:
- requestNonce() sabit döndürse → sunucuda nonce geçersiz → 403
- Sahte integrity token → sunucuda Google çözemez → 403
- Metodu JSON döndürmeye zorlasa → sunucuda o verinin karşılığı yok → anlamsız

### Peki Ya...

| Soru | Cevap |
|------|-------|
| Ya tüm istekleri sahte proxy'e yönlendirirse? | SSL pinning + nonce eşleştirme var |
| Ya Integrity API'sini hook'larsa? | Token sunucuda çözülür, sahte token çözülmez |
| Ya gerçek premium hesap kullanırsa? | O zaman APK zafiyeti değil, auth meselesi |

### Sınır

APK yaması ölü yol. Kalan riskler APK zafiyeti değil, standart auth sorunları: hesap paylaşımı (cihaz başına oturum), hesap ele geçirme (MFA).
