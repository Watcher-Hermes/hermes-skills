---
name: android-apk-hardening
description: Kendi APK'ını saldırgan gözüyle oku, lisans/premium kırılganlıklarını tespit et, sertleştir. Client-side güvenlik denetimi + savunma stratejisi.
---

# Android APK Hardening — Lisans/Premium Kırılganlık Denetimi

## Tersine Mühendislik ve Sertleştirme

Mevcut `android-apk-modding` skill'i **saldırı** içindi. Bu skill onun aynası: **kendi APK'ını savunmak.** Önce kırılganlıkları bul, sonra kapat.

---

## Pratik Öncelik Sırası (Bu Sırayla Yap)

```
1. KRİTİK — Korunan işlevi sunucuya taşı
   Client'ta "premium musun?" sorma, veriyi sunucudan getir.
   Atlanan if, sunucuda olmayan veriyi var edemez.   ❌

2. KRİTİK — Play Integrity sunucuda doğrula
   Nonce sunucuda üret, token sunucuda Google ile çöz.
   Client'ta if'e bağlanmaz, replay-proof.            ❌

3. UCUZ — R8 + imza self-check + dağıtık kontrol
   İmza kontrolünü "tespit et → sunucuya bildir" yap.
   Client'ta karar verirse ⚠️, bildirime çevirince ❌.  ⚠️→❌

4. PAHALI — NDK/native'e taşı
   Son çare. Geliştirme maliyeti en yüksek.
   Ghidra gerekir, caydırıcılık en yüksek.            ⚠️
```

> **Kısa kural:** Client'taki her şey aşılabilir. Gerçek sınır sunucu.
> Önce 1-2'yi kur, sonra 3'ü ekle, 4'ü en sona bırak.

---

## Faz 1 — APK'yı Saldırgan Gözüyle Oku

Amaç yama yapmak değil, "lisans/premium mantığım ne kadar görünür ve ne kadar tek-noktaya bağlı?" sorusunu yanıtlamak.

### 1a — jadx ile Java seviyesinde analiz

jadx-gui ile APK'yı aç, decompile edilmiş Java kodunu oku. Aradığın şeyler:

```bash
jadx-gui app.apk
```

- `isPremium()`, `checkLicense()`, `isPro()`, `hasSubscription()` gibi metot isimleri
- `if (valid) { unlock() }` deseni — tek satırlık yamaya açık
- `SharedPreferences.getBoolean("premium", false)` — kolay atlatılır
- `BuildConfig.PREMIUM` veya `BuildConfig.DEBUG` — derleme sabiti, en kolayı

**KIRMIZI BAYRAK — Tek nokta:** jadx'te gördüğün tek bir boolean kararı, saldırganın da göreceği ilk şeydir. Tek satırlık `if-eqz → if-nez` smali değişikliğiyle kırılır.

**GATE:** jadx çıktısında lisans/premium kararının yeri tespit edildi mi? Kaç noktada karar veriliyor?

### 1b — apktool ile smali'ye in

```bash
apktool d app.apk -o _audit/
```

Kontrol noktası sayısı:
- Tek metot mu (`isPremium()` → return boolean)?
- Birden çok yere dağılmış mı (her premium özellik ayrı kontrol)?
- SharedPreferences'tan mı okuyor (kolay)?
- Her açılışta sunucudan mı doğruluyor (zor)?
- Root check var mı? Varsa nerede?

```bash
# Smali'de lisans/premium ile ilgili tüm referansları tar
grep -r -i "premium\|license\|pro\|unlock\|subscription\|purchase" _audit/smali/ | grep -v ".line" | head -30
```

**SORULAR:**
```
- Premium kararı client'ta mı?    → KIRILGAN
- Sunucu doğrulaması var mı?      → Token replay'e açık mı?
- SharedPreferences mı?           → Tek satır
- root tespiti var mı?            → Atlanabilir mi?
- Integrity API kullanılıyor mu?  → Verdict client'ta mı doğrulanıyor?
```

### 1c — String ve sabitler

```bash
# Hardcode edilmiş API anahtarları, endpoint'ler, "license_valid" benzeri flag string'leri
strings app.apk | grep -i "api\|key\|secret\|token\|license\|premium\|https://" | head -20
```

Bunlar:
- Saldırgana harita verir (hangi endpoint, hangi parametre)
- Hardcode edilmiş sırların sızması demektir
- `license_valid`, `is_premium` gibi açık string sabitleri gömülüyse, doğrudan hedef gösterir

### 1d — Kırılganlık Haritası Çıktısı

Faz 1'in çıktısı şu cümleleri kurabilmek olmalı:

```
ÖRNEK: "Premium kararım client tarafında, tek boolean (isPremium),
SharedPreferences'ta 'premium_unlocked' anahtarıyla saklanıyor,
sunucu hiç sormuyor. if-eqz → if-nez yamasıyla 30 saniyede kırılır."
```

Bu cümleyi kurabiliyorsan zaafiyet net.

---

## Faz 2 — Sertleştirme

Kırılganlık haritasındaki her maddeyi bir savunmayla eşle.

### İlke 1: Client'a Güvenme (Temel Kural)

Client tarafı kod cihazda çalışır, cihaz kullanıcının elindedir. Her client-side kontrol nihayetinde atlatılabilir.

**DOĞRU:** Premium kararını client'ta verme. Korunan işlevin kendisini sunucuya taşı.
**YANLIŞ:** Client'ta `if (premium) { showFeature() }` — o if satırı yamanır.

```java
// KÖTÜ — client'ta karar
if (isPremium) { showPremiumFeature(); }

// İYİ — premium özellik sunucudan gelir
api.getPremiumData(token).enqueue(response -> {
    // response zaten yetkilendirilmiş, client karar vermez
    showData(response);
});
```

Atlanan bir if bloğu, sunucuda olmayan veriyi var edemez.

### İlke 2: Server-side Doğrulama

Lisans/abonelik durumu sunucuda tutulur. Client her oturumda kısa ömürlü bir token ile kendini doğrular.

```
Akış:
1. Client → Sunucu: "ben premium'um, işte token"
2. Sunucu → Google Play Developer API: "bu token geçerli mi?"
3. Google → Sunucu: "geçerli / değil"
4. Sunucu → Client: premium veri (veya hata)

NOT: Client'tan gelen "satın aldım" iddiasına asla doğrudan güvenme.
```

Google Play Billing için:
```java
// Sunucu tarafında — Play Developer API ile doğrula
// purchases.subscriptions.get(packageName, subscriptionId, token)
// Client'tan gelen purchase token'ı sunucuda doğrula
```

### İlke 3: Play Integrity API — Doğru Entegrasyon

**Kritik nokta:** Integrity verdict'i client'ta değil, **sunucuda** doğrulanmalı.

```
DOĞRU AKIŞ:
1. Sunucu bir nonce üretir → client'a gönderir
2. Client nonce'u Integrity API'sine verir
3. Integrity API imzalı token döndürür
4. Client token'ı sunucuya iletir
5. Sunucu token'ı Google ile çözer ve doğrular
6. Nonce eşleşiyor mu? Cihaz bütünlüğü yerinde mi? → Karar sunucuda

YANLIŞ:
if (integrityOk) { ... }  ← Bu if'i atlatmak yine tek satır
```

Nonce server-side üretildiği ve token server-side çözüldüğü için replay ve client-yamasına dayanıklı.

### İlke 4: Anti-Tamper (Gerçekçi Beklentiyle)

Bunlar caydırıcıdır, mutlak değil. Amaç çıtayı yükseltmek, kırmayı imkansız kılmak DEĞİL.

#### 4a — İmza Doğrulama

Uygulama çalışırken kendi imza sertifikası hash'ini kontrol eder. Yeniden paketlenip başka anahtarla imzalanmışsa fark eder.

```java
private boolean checkSignature(Context ctx) {
    String validHash = "a1:b2:c3:..."; // gerçek hash
    try {
        PackageInfo pkg = ctx.getPackageManager()
            .getPackageInfo(ctx.getPackageName(),
                PackageManager.GET_SIGNATURES);
        String currentHash = hash(pkg.signatures[0].toByteArray());
        return validHash.equals(currentHash);
    } catch (Exception e) {
        return false;
    }
}
```

**UYARI:** Bu kontrolün kendisi de smali'de bir yer olduğundan, tek başına yeterli değil. Sunucuya bildiren bir yapıyla birleştir (imza hash'i sunucuda da doğrulanabilir veya imza başarısızsa sunucuya rapor gönder).

#### 4b — R8/ProGuard Obfuscation

Sınıf/metot adlarını anlamsızlaştırır, jadx çıktısını okumayı ciddi zorlaştırır. Bedava ve etkili ilk savunma.

```gradle
// build.gradle
android {
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

Bir APK'yı R8 ile küçültüp sonra jadx'te açmayı dene — farkı göreceksin.

#### 4c — Kontrol Noktalarını Çoğalt ve Dağıt

Tek `isPremium()` yerine kararı birden çok yere böl. Saldırganın her birini bulup yaması gerekir.

```java
// KÖTÜ — tek nokta
if (licenseManager.isPremium()) { showFeature(); }

// İYİ — dağıtık kontrol
if (licenseManager.isPremium() &&
    integrityCheck.passes() &&
    serverToken.isValid()) {
    showFeature();
}
```

Saldırgan üçünü de bulup yamamalı. Caydırıcılık artar.

#### 4d — Kritik Mantığı NDK/Native'e Taşı

.so içindeki C/C++ kodu apktool ile decompile edilmez, sadece zorlu disassembly ile okunur (Ghidra, IDA).

```cpp
// native-lib.cpp
extern "C" JNIEXPORT jboolean JNICALL
Java_com_app_NativeLicense_check(JNIEnv* env, jobject thiz, jstring input) {
    // Java'da görünmeyen lisans mantığı
    // Derin obfuscation + anti-debug
    return verify(input); // true/false
}
```

**Seviyeler:**
- Java'da kontrol → apktool/jadx ile 5 dk
- Native'de kontrol → Ghidra ile saatler
- Native'de obfuscated + anti-debug → günler

### Tehdit Modelini Netleştir

Şunu kabul et: kararlı bir saldırgan, cihazda çalışan her şeyi eninde sonunda aşabilir (root + Frida dinamik enstrümantasyon + GPT ile analiz).

**Gerçek güvenlik sınırın sunucu.** Anti-tamper'ın işi:
- Saldırıyı imkânsız kılmak değil
- Pahalı ve kırılgan kılıp çoğu kullanıcı için caydırmak

---

## Kırılganlık Haritası → Savunma Eşleme Tablosu (Öncelik Sıralı)

| Öncelik | Kırılganlık | Savunma | Etki |
|---------|-------------|---------|------|
| **1 — KRİTİK** | Premium kararı client'ta boolean | Korunan işlevin verisini sunucuya taşı, client'ta karar verme | ❌ Atlanan if, sunucuda olmayan veriyi var edemez |
| **2 — KRİTİK** | Play Integrity verdict'i client'ta doğrulanıyor | Nonce sunucuda üret, token'ı sunucuda Google ile çöz | ❌ Client'ta if'e bağlı değil, replay-proof |
| **3 — UCUZ** | jadx ile okunabilir kod | R8/ProGuard obfuscation | ⚠️ Caydırıcı, okumayı zorlaştırır |
| **4 — UCUZ** | İmza kontrolü yok | İmza self-check + **sunucuya bildir** (karar verme) | ❌ `if (!imzaOk) { sunucuyaBildir() }` — karar client'ta değil |
| **5 — UCUZ** | Tek noktadan karar | Dağıtık kontrol (3+ nokta) | ⚠️ Çıtayı yükseltir, hepsi bulunana kadar korur |
| **6 — PAHALI** | Java'da lisans mantığı | NDK/native'e taşı (Ghidra gerekir) | ⚠️ En yüksek maliyet, son çare |

### Özet — Tablonun Tek Cümlelik Dersi

> Client'taki her şey aşılabilir. Gerçek güvenlik sınırın sunucu.
> Client tarafı sadece geciktirme katmanıdır.

### Nihai Sonuç — Yama Yapılamaz Tasarım

Server-yetkilendirmeli tasarımda APK yaması ölü yol:
- Cihazda atlanacak karar yok: `isPremium()` boolean'ı yok, `if-eqz` yok
- Korunan veri cihazda değil, sunucuda üretiliyor
- APK yamalanıp imzalansa bile sunucu "yetkili değilsin" der
- Saldırı yüzeyi "herkes yamalayabilir"den "geçerli hesap gerekir"e kayar

Kalan riskler APK zafiyeti değil, standart auth sorunları:
- Hesap paylaşımı → cihaz başına oturum, eşzamanlı oturum limiti
- Hesap ele geçirme → MFA, token binding, şüpheli giriş tespiti

---

## Pipeline: Denetimden Sertleştirmeye

```
Adım 0 — jadx ile Java analizi (isPremium nerede?)
    → Kırılganlık haritası oluştur
Adım 1 — apktool ile smali taraması (kaç nokta?)
    → Kontrol sayısını belirle
Adım 2 — String/sabit taraması (API key, flag, endpoint)
    → Hardcode sırları tespit et
Adım 3 — Kırılganlık → Savunma eşleme
    → Her maddeye bir veya daha çok savunma ata
Adım 4 — Sertleştirme uygulama
    → R8 aç, dağıtık kontrol ekle, sunucu doğrulaması kur
Adım 5 — Test: yamala ve dene
    → apktool ile aynı yöntemleri dene, savunma işe yarıyor mu?
```

---

## Skill Dosyaları

| Dosya | Açıklama |
|-------|----------|
| Bu skill | APK hardening denetimi ve sertleştirme rehberi |
| `scripts/apk-audit.sh` | 6 adımlı salt-okunur audit scripti — tek komutla rapor |
| `references/PremiumRepository.kt` | YANLIŞ + DOĞRU karşılaştırmalı Android kodu |
| `references/server-pattern.md` | Server-side yetkilendirme akışı + kritik noktalar |
| `references/unpatchable-design.md` | Bu tasarımda neden yama yapılamadığı |
| `android-apk-modding` | Karşıt skill — saldırı perspektifi |

### apk-audit.sh Kullanımı

```bash
# Kullanmadan önce: kendi metot/değişken adlarını KEYWORDS satırına ekle
# Script'in başındaki şu satırı düzenle:
#   KEYWORDS="isPremium|checkLicense|verifyPurchase|...|seninMetodun"

# Çalıştır
bash scripts/apk-audit.sh benim-uygulamam.apk

# Çıktı: REPORT.md — APK değiştirilmez, sadece analiz edilir
```

### Kırılganlık Haritası Cümlesi (Raporun Kalbi)

Raporun en altında şu cümle otomatik doldurulur:

```
Premium kararım [client/server] tarafında,
[tek/N] noktada,
[SharedPreferences/sunucu] ile saklanıyor,
obfuscation [var/yok],
native [var/yok].
```

Bu cümlede **"client / tek / SharedPreferences / yok / yok"** çıkarsa sertleştirme şart.

---

## İlgili Araçlar

| Araç | Ne İçin |
|------|---------|
| jadx-gui | Java decompile (ilk analiz) |
| apktool | Smali seviyesinde inceleme |
| strings | Hardcode sabit taraması |
| Frida | Dinamik enstrümantasyon testi (savunmayı doğrulamak için) |
| Ghidra | Native (.so) kod analizi |
