# APK Keşif ve Ön Belge (Reconnaissance) Referansı

Bu referans, `android-apk-modding` skill'inin **Adım 0 — ÖNBELGE** aşaması için Python ile otomatik analiz metodolojisini belgeler. Elle `grep` yapmak yerine veya onun yanında, aşağıdaki gibi bir Python scripti ile APK'yı baştan aşağı otomatik analiz et.

## Ne Zaman Kullanılır

- APK'yı ilk kez decompile ettiğinde
- "detaylı incele/bu uygulamayı analiz et" talebi geldiğinde
- Yama öncesi neyle uğraştığını anlaman gerektiğinde
- Kullanıcı APK hakkında spesifik soru sormadan önce

## Pipeline: APK'yı Analiz Et

### 1. Split APK Kontrolü ve Merge

Önce APK'nın split olup olmadığını kontrol et:

```python
import zipfile, os
# Split APK: birden fazla .apk dosyası package: ile döner
# base.apk + split_config.arm64_v8a.apk gibi
```

Split varsa merge et (detay: `android-apk-repackaging` skill'indeki split-merge).

### 2. Otomatik Analiz (Python ile)

```python
# Kullanılacak ana değişken
preview = "_preview/"          # apktool d çıktısı
apksigner = "apksigner.bat"    # SDK build-tools altında

def analyze_apk(preview, original_apk_path):
    """
    Aşağıdaki tüm analizleri yapar, dict olarak döndürür.
    """
    result = {}

    # 2a. Version bilgisi
    # apktool.yml'den targetSdk, minSdk, versionCode, versionName, packageName

    # 2b. Manifest izinleri — 20+ izin varsa kategorize et:
    #   KRITIK: RECORD_AUDIO, CAMERA, ACCESS_FINE_LOCATION, READ_CONTACTS,
    #           FOREGROUND_SERVICE_MICROPHONE, SYSTEM_ALERT_WINDOW
    #   NORMAL: INTERNET, ACCESS_NETWORK_STATE, VIBRATE, WAKE_LOCK
    #   DIZI: POST_NOTIFICATIONS, BLUETOOTH_CONNECT, QUERY_ALL_PACKAGES

    # 2c. Component listesi — regex ile manifest'ten çek:
    #   <activity>, <service>, <receiver>, <provider>
    #   Kısa isim göster (paket adından sonrası)

    # 2d. Obfuscation tespiti:
    #   Smali dosyaları a.smali, b.smali, aa.smali ise → R8/ProGuard VAR
    #   Smali dosyaları anlamlı isimlerdeyse (MainActivity.smali) → obfuscation yok
    #   İkinci dex (smali_classes2/) var mı kontrol et

    # 2e. Premium/Lisans taraması:
    premium_kw = ['premium', 'pro', 'license', 'trial', 'entitlement',
                  'purchase', 'subscription', 'isPro', 'isPremium',
                  'upgrade', 'billing', 'playBilling', 'iap']
    # Tüm .smali dosyalarında bu keyword'leri tara
    # Her match için: [keyword] relative_path: eşleşen satır

    # 2f. Native lib analizi:
    # lib/<arch>/ altındaki .so dosyaları
    # Her birinin boyutunu ve toplamını göster
    # Büyük olanların amacını çıkar:
    #   libtensorflowlite_jni.so → ML model çalıştırma
    #   libogg_opus_encoder.so → ses kodlama
    #   libresampler.so → ses yeniden örnekleme

    # 2g. İmza şeması kontrolü (orijinal APK üzerinde):
    # apksigner verify --verbose target.apk
    # v1/v2/v3/v4 şemalarından hangisi aktif

    # 2h. Assets analizi:
    # assets/ altındaki dosyalar
    # .tflite → TensorFlow Lite model
    # .binarypb → protobuf yapılandırma

    # 2i. Firebase/Google API tespiti:
    # Smali'de şu paketleri ara:
    #   com.google.firebase.analytics → telemetri
    #   com.google.firebase.auth → kimlik doğrulama
    #   com.google.firebase.database → Realtime DB
    #   com.google.firebase.storage → dosya depolama
    #   com.google.android.gms.ads → reklam
    #   com.google.firebase.messaging → push bildirim
    #   com.google.android.play.core → Play Billing/Update

    return result
```

### 3. Rapor Formatı (Kullanıcıya Sun)

```
╔════════════════════════════════════════════╗
║  UYGULAMA ADI — DETAYLI ÖN BELGE RAPORU   ║
║  com.package.name                          ║
╚════════════════════════════════════════════╝

[1] TEMEL BİLGİLER
  • Sürüm: 8.7.880674799 (code: 186096)
  • targetSdk: 36 / minSdk: 32
  • APK boyutu: 24 MB

[2] OBFUSCATION
  R8/ProGuard VAR / YOK
  Toplam smali: 9.104 (2 dex)
  Ana paket altındaki sınıflar orijinal/obfuscated

[3] IZINLER (N adet)
  KRITIK: RECORD_AUDIO, FOREGROUND_SERVICE_MICROPHONE
  NORMAL: INTERNET, VIBRATE
  DİĞER: BLUETOOTH_CONNECT, POST_NOTIFICATIONS

[4] YAPI (N Activity + N Service + N Receiver)
  Ana Activity: MainActivity, SettingsActivity
  Kritik Service: ForegroundService, AccessibilityService

[5] FIREBASE/GOOGLE API
  analytics, auth, database, ads → tespit durumu

[6] NATIVE LIBS (N adet — X MB)
  • libtensorflowlite_jni.so  → 7.2 MB (ML)
  • libogg_opus_encoder.so    → 708 KB (ses)

[7] PREMIUM/KONTROL
  Play Billing: var/yok
  Firebase Auth: var/yok
  Sunucu tarafı kontrol: tahmini evet/hayır

YAMA YAPILABİLİRLİK:
  ✅/⚠️/❌ sebeple birlikte
```

## Kritik Tespitler

### Server-Side Yetkilendirme Tespiti

Smali'de şu desenleri ara:
- `isPremium()` / `isPro()` → boolean dönüyorsa → **client-side** → yama yapılabilir
- `fetchPremiumData()` / `getEntitlement()` → HTTP çağrısı → **server-side** → yama çalışmaz
- Google Play Billing sınıfları (`com.android.billingclient`) + Firebase Auth → yüksek ihtimal server-side
- Play Integrity API (`com.google.android.play.integrity`) → kesin server-side

### Firebase Varlığı

Firebase sınıfları `smali_classes2/` içinde de olabilir. Tüm dex'leri kontrol et:
```python
smali_dirs = ['smali', 'smali_classes2', 'smali_classes3', ...]
# hepsini tara
```

## Pratik Örnek: Live Transcribe Keşfi

Google Live Transcribe v8.7 (com.google.audio.hearing.visualization.accessibility.scribe):

| Özellik | Değer |
|---------|-------|
| targetSdk | 36 (Android 16) |
| minSdk | 32 |
| Obfuscation | **VAR** (R8) — 9.104 smali dosyası |
| Split | EVET (base + arm64_v8a) |
| İmza | v3 scheme + SourceStamp |
| Native lib | 7 .so, 8.9 MB (TensorFlow Lite) |
| Firebase | analytics + auth + database + storage |
| Cast | Chromecast desteği var |
| Premium | Play Core + Firebase Auth → muhtemelen sunucu tarafı |
| Ana paket sınıfları | **orijinal isimlerini korumuş** (yama için avantaj) |
