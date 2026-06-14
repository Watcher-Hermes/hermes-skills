---
name: android-apk-modding
description: APK modding pipeline — tek yön, geri dönüşsüz adımlar. Sistem uygulaması bypass (package rename), split APK merge, smali/dex patching, onPause/onStop boşaltma, manifest düzenleme. Önbelge → Decompile → Yama (karar ağacı) → Rebuild → zipalign → İmzala → Doğrula+logcat.
---

# Android APK Modding Pipeline

## Kural

**Tek yön, geri dönüşsüz.** Her adımda başarı kontrolü var. Sessiz hata bir sonraki adımda patlamaz — adımın kendisinde patlar ve durur.

## Kullanıcı Tercihi

**Önce en basit çözüm.** Karmaşık eklemeler (foreground service, yeni sınıf, hook) yapmadan önce:
1. Mevcut bir metodu boşaltmak yeterli mi? (onPause, onStop)
2. Manifest'te tek satır değişiklik çözüyor mu?
3. Resource/string değişiklik çözüyor mu?
Kullanıcı "sadece ayar değiştir" dediğinde direkt smali'deki ilgili metodu bul ve boşalt. Yeni özellik ekleme, yeni service yazma.

**Kısıtlı ortam (sistem uygulaması, imza koruması):**
Kullanıcı "bilinmeyen kaynaktan kod kullanılmayacak" dediğinde APK modding yapılamaz — sadece ADB komutları çalışır.
Bu durumda SDK izinleri (`appops`) ve Android sistem ayarları (`settings`, `pm`) dışında seçenek yok.

## Gereksinimler

| Araç | Yol |
|------|-----|
| Java 21+ | `java -version` |
| zipalign | `C:\\\\Users\\\\marko\\\\AppData\\\\Local\\\\Android\\\\Sdk\\\\build-tools\\\\37.0.0\\\\zipalign.exe` |
| apksigner | `C:\\\\Users\\\\marko\\\\AppData\\\\Local\\\\Android\\\\Sdk\\\\build-tools\\\\37.0.0\\\\apksigner.bat` |

Pat'ler:
```bash
APKTOOL="java -jar /c/Users/marko/re-hermes/apktool.jar"
ZIPALIGN="***REMOVED-BASE64***-tools/37.0.0/zipalign.exe"
APKSIGNER="***REMOVED-BASE64***-tools/37.0.0/apksigner.bat"
KEYSTORE="***REMOVED-BASE64***.keystore"
KEYALIAS="livetranscriber"
KSPASS="<keystore-sifresi>"
```

---

## Pipeline

### Adım 0a — ADB İLE ÖNCE HAFİF MÜDAHALE DENE (APK Decompile Etmeden)

APK modding'e başlamadan ÖNCE, ADB ile çözülebilecek basit ayarları dene:

**1. Ses kaydı arka plan iznini aç:**
```bash
# Mevcut durumu kontrol et:
adb shell "appops get com.target.package RECORD_AUDIO"

# Eğer "foreground" olarak görünüyorsa, "allow" yap:
adb shell "appops set com.target.package RECORD_AUDIO allow"

# Doğrula:
adb shell "appops get com.target.package RECORD_AUDIO"
# Çıktı: "Uid mode: RECORD_AUDIO: foreground" (bu UID default, değişmez)
#        "RECORD_AUDIO: allow" (ops override, bu satır önemli)
```

Bu, uygulamanın arka planda da ses kaydetmesine izin verir. Özellikle "ekran kilitlenince kayıt dursun" sorununu çözebilir.

**İşe yaramazsa:** Uygulamayı kapatıp aç, tekrar dene. Bazı uygulamalar `foreground`→`allow` değişikliğini runtime'da okumaz, restart gerekir.

**2. Bildirim iznini kontrol et:**
```bash
adb shell "appops get com.target.package POST_NOTIFICATION"
```

**3. Uygulamanın debuggable durumunu değiştir (root'suz çalışmaz):**
```bash
# ÇALIŞMAZ — sadece root ile
adb shell "pm set-debug com.target.package true"
```

**4. Uygulama etkinliğini kontrol et:**
```bash
adb shell "dumpsys package com.target.package | grep enabled"
# enabled=0 = etkin, hidden=true = gizli
```

Eğer bu adım sorunu çözerse, APK modding'e gerek kalmaz. Kullanıcıya rapor ver.

### Adım 0b — ÖNBELGE (Reconnaissance)

APK'yı analiz et, neyle uğraştığını bil. Yamadan önce mutlaka bu adım.

```bash
# 0a — Bilgi çıkar
$APKTOOL d -f -o _preview/ target.apk
```

**KONTROL 0:** Şu soruları cevapla:

| Soru | Nasıl Bakılır |
|------|-------------|
| **targetSdkVersion kaç?** | `grep targetSdk _preview/apktool.yml` |
| **İmza şeması?** | `apksigner verify target.apk` (varsa) |
| **Native lib var mı?** | `ls _preview/lib/` boş mu dolu mu? |
| **Obfuscation var mı?** | `ls _preview/smali/*/` — harf isimleri (a.smali, b.smali) varsa R8/ProGuard var |
| **Split APK mı?** | `grep isSplitRequired _preview/AndroidManifest.xml` |
| **minSdkVersion?** | `grep minSdk _preview/apktool.yml` |
| **Package name?** | `grep package _preview/AndroidManifest.xml` |

```bash
# 0b — Preview dizinini temizle
rm -rf _preview/
```

**GATE 0:** Eğer targetSdk > cihaz SDK'sı → düşürmeyi not et. Native libs varsa split merge gerekebilir. Rapor çıktısı üret, kullanıcıya neyle uğraştığını göster.

**SİSTEM UYGULAMASI KONTROLÜ (Pipeline'ın en kritik kararı):**
```bash
adb shell pm list packages -s | grep com.target.package
# Çıktı varsa = SİSTEM UYGULAMASI
```
Eğer sistem uygulamasıysa:
- `adb uninstall -k --user 0 <pkg>` ile kaldır
- Telefonu yeniden başlat (`adb reboot`)
- `adb install patched.apk` dene
- Hala `INSTALL_FAILED_UPDATE_INCOMPATIBLE` alınıyorsa → **Package rename stratejisine geç** (aşağıdaki bölüm)
- APK'yı telefona manuel kurmak için: push to `/data/local/tmp/`, `adb shell pm install -r -t /data/local/tmp/patch.apk`
- Sdcard'dan kurulum çalışmaz: `pm install` system_server olarak çalışır, sdcard'a erişemez

---

### SİSTEM UYGULAMASI BYPASS: Package Rename Stratejisi

Android 16+ One UI 8'de sistem uygulamalarına yama yapılamaz. Çözüm: **Paket adını değiştir, yeni bir uygulama olarak yükle.**

**ÖNEMLİ UYARI:** apktool'un `renameManifestPackage` özelliği SADECE manifest'teki `package=` attribute'unu değiştirir. **Smali class referanslarını, layout XML'deki custom view isimlerini, permission/provider string'lerini değiştirmez.** Bunların hepsini ayrıca elle yapman gerekir.

#### Full Workflow (Sistem Uygulaması Bypass)

**1) Yeni paket adı seç — AYNI UZUNLUKTA olmalı**
Binary AXML string pool'da offset'ler bozulmasın diye aynı karakter sayısı zorunlu:
```python
orig = "com.google.audio.hearing.visualization.accessibility.scribe"
new  = "com.transcribe.live.service.background.accessibility.extend"
assert len(orig) == len(new), f"Uzunluk farki: {len(orig)} vs {len(new)}"
```

**2) Decompile + apktool.yml ayarı**
```bash
apktool d -f -o _work/ merged_original.apk
# apktool.yml → renameManifestPackage: com.yeni.paket.adi
```

**3) Smali class referanslarını değiştir (EN ÖNEMLİ)**
Sadece manifest rename YETMEZ — DEX içinde `Lcom/eski/paket/Class;` referansları eski kalır:
```bash
# Slaş format (Lcom/eski/paket/Class;)
grep -rl "com/eski/paket/yolu" smali/ smali_classes2/ | \
  xargs sed -i 's|com/eski/paket/yolu|com/yeni/paket/yolu|g'

# Dot format (Class.forName("com.eski.paket.Class"))
grep -rl "com.eski.paket" smali/ smali_classes2/ | \
  xargs sed -i 's/com\.eski\.paket/com.yeni.paket/g'
```
`.class public Lcom/eski/...;` satırı da değişmeli — yoksa `ClassNotFoundException`.

**4) Layout XML'de custom view isimlerini değiştir**
```bash
grep -rl "com.eski.paket" res/ | xargs sed -i 's/com\.eski\.paket/com.yeni.paket/g'
```
Layout inflater tam nitelikli sınıf adıyla yükler (`com.eski.paket.ui.CustomView`).

**5) Permission + Provider string'lerini düzelt**
```bash
sed -i 's/com\.eski\.paket/com.yeni.paket/g' _work/AndroidManifest.xml
```
Düzeltilmezse: `INSTALL_FAILED_DUPLICATE_PERMISSION` veya `INSTALL_FAILED_CONFLICTING_PROVIDER`.

**6) (Opsiyonel) Binary raw/protobuf dosyaları**
AYNI UZUNLUKTA string replacement protobuf'u bozmaz:
```bash
sed -i 's|com/eski/paket|com/yeni/paket|g' res/raw/*
```

**7) Split APK referanslarını manifest'ten temizle**
```xml
<!-- sil: -->
android:requiredSplitTypes="base__abi"
android:splitTypes=""
<meta-data android:name="com.android.vending.splits.required" .../>
<meta-data android:name="com.android.vending.splits" .../>
```

**8) onPause/onStop boşalt (hedef buysa)**
MainActivity'de onPause metodunu bul, invoke-super + return-void dışındaki tüm satırları sil.

**9) İmzala + yükle**
```bash
apksigner sign --ks release.keystore --ks-key-alias alias --ks-pass pass:sifre _build_aligned.apk
adb install _build_aligned.apk
```

**10) LauncherActivity'yi aktifleştir** (rename yapılan uygulamalarda)
Sistem uygulamalarında LauncherActivity alias genelde `android:enabled="false"` olur. Sideload'da bu aktif olmadığı için uygulama menüde görünmez:
```xml
<activity-alias android:enabled="true"  <!-- false → true -->
  android:exported="true"
  android:name="com.yeni.paket.LauncherActivity"
  android:targetActivity="com.yeni.paket.MainActivity">
```
Aktifleştirilmezse `monkey -p com.yeni.paket 1` çıktısı: "No activities found to run, monkey aborted."

**11) logcat ile doğrula**
```bash
adb logcat -c && adb shell am start -n com.yeni.paket/.MainActivity
sleep 8 && adb logcat -d | grep -E "FATAL|CRASH|AndroidRuntime"
```

#### Olası Crash'ler

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `ClassNotFoundException: com.ESKI.paket.Class` | Smali'de class reference değişmemiş | `Class.forName()` string'lerini kontrol et |
| `ClassNotFoundException: com.YENI.paket.Class` | Layout'ta custom view eski kalmış | `res/layout/*.xml` kontrol et |
| `INSTALL_FAILED_DUPLICATE_PERMISSION` | Permission name eski pakette | `<permission android:name>` değiştir |
| `INSTALL_FAILED_CONFLICTING_PROVIDER` | Provider authority eski | `<provider android:authorities>` değiştir |

**ERKEN ÇIKIŞ (ÖNEMLİ):** Smali'de `isPremium()`, `checkLicense()` gibi boolean dönüş yoksa, sadece `fetchPremiumData()` → HTTP POST → null/JSON deseni varsa, bu APK **server-side yetkilendirme** kullanıyordur. Bu durumda yama yapılamaz — `android-apk-hardening` skill'ine yönlendir.

**GOOGLE APPS — Sunucu Taraflı İmza Kontrolü (KRİTİK İSTİSNA):**

Google uygulamalarını (`com.google.*`) modlamak APK seviyesinde çalışsa bile **sunucu tarafında çalışmaz.** Google sunucuları (gRPC, Firebase, Cloud Speech API) uygulama imzasını doğrular. Custom keystore ile imzalanan APK'yı sunucu reddeder.

| Hizmet | Davranış |
|--------|----------|
| **Google Cloud Speech (Live Transcribe)** | Mikrofon açılır, ses alınır, sunucuya giderken imza hatası → "INVALID_ARGUMENT: credential not valid" → transcription session kapanır |
| **Firebase Instance ID** | `Failed to retrieve Firebase Instance Id` — imza eşleşmezse Firebase auth çalışmaz |
| **Firebase Auth / Google Sign-In** | Custom imzalı APK ile Google hesabına bağlanılamaz |

**Kural:** Eğer uygulama cloud tabanlı konuşma tanıma (speech-to-text), canlı altyazı, voice search gibi Google sunucu hizmetlerini kullanıyorsa → **package rename + custom imza ile çalışmaz.**

**İstisnalar:** Offline-only özellikler (önceden indirilmiş dil modelleri, TF Lite ile lokal çalışan modeller) kaynak uygulamada varsa çalışabilir. Ama Live Transcribe'da tüm transkripsiyon sunucu taraflıdır, TF Lite modelleri sadece ses sınıflandırma (sound events) içindir.

**Alternatif stratejiler:**
- Root + sistem bölümüne yama: Orijinal imza korunur, sunucu kabul eder
- Frida hook (root gerekir): APK'ya dokunulmaz, imza bozulmaz. Ancak Android 16+ One UI 8'de non-root cihazlarda Frida system app'lere bağlanamaz (attached failed → spawn failed → root gerekir)
- Root'suz çözüm yok: cloud tabanlı Google uygulamaları modlanamaz

---



### Adım 1 — DECOMPILE

```bash
# Orijinal APK'yı yedekle
cp target.apk target.original.apk

# Decompile
$APKTOOL d -f -o _work/ target.apk
```

**GATE 1:**
```bash
[ -f _work/AndroidManifest.xml ] && echo "MANIFEST_OK" || echo "MANIFEST_FAIL"
[ -d _work/smali ] && echo "SMALI_OK" || echo "SMALI_FAIL"
```

İkisi de OK değilse DUR. apktool sessizce başarısız olmuştur — farklı bir sürüm dene veya APK bozuk.

---

### Adım 2 — YAMA (Karar Ağacı)

Ne tür değişiklik yapılacağını belirle, alt-yordamı seç:

```
Kullanıcının isteği nedir?
├── Manifest değişikliği (izin, servis, debuggable, targetSdk)
│   → ALT-YORDAM: manifest-patch
├── Resource değişikliği (renk, yazı, logo, string)
│   → ALT-YORDAM: resource-patch
└── Smali/davranış değişikliği (yeni özellik, service start, hook)
    → ALT-YORDAM: smali-patch
```

#### ALT-YORDUM: manifest-patch

`_work/AndroidManifest.xml` düz XML — doğrudan düzenle.

Sık yapılanlar:

```xml
<!-- debuggable aç -->
<application android:debuggable="true" ...

<!-- network security config -->
<application android:networkSecurityConfig="@xml/network_security_config" ...

<!-- izin ekle -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE"/>

<!-- split APK referanslarını sil -->
<!-- manifest <manifest> tag'inden şunları kaldır: -->
android:isSplitRequired
android:requiredSplitTypes
android:splitTypes
<!-- meta-data'dan kaldır: -->
splits.required
com.android.vending.splits
```

targetSdk düşürmek için `_work/apktool.yml`:
```yaml
sdkInfo:
  targetSdkVersion: 35   # 36→35
```

**GATE 2M:** `grep "yaptığın değişiklik" _work/AndroidManifest.xml`

#### ALT-YORDUM: resource-patch

- Logo değiştir: `_work/res/drawable/` veya `res/mipmap-*/`
- Renk değiştir: `_work/res/values/colors.xml` — hex value bul ve değiştir
- String değiştir: `_work/res/values/strings.xml`
- Resource ID teyit: `grep "icon\|logo\|splash" _work/res/values/public.xml`

**GATE 2R:** Eski resource artık yok mu? Yeni resource public.xml'de var mı?

#### ALT-YORDUM: smali-patch

**Önce en basit teknik: onPause/onStop Boşaltma**

Kullanıcı "ekran kilitlenince kaydı durdurma" gibi tek bir davranışı kapatmak istediğinde, yeni service/hook ekleme. En hızlı çözüm: Activity'nin onPause() veya onStop() metodundaki kodları silmek.

Adımlar:
1. Activity'de `onPause()` metodunu bul (obfuscated da olsa `invoke-super.*onPause` aranır)
2. Metot içinde transcription/kayıt durduran çağrıları tespit et
3. Metodu sadece `invoke-super` + `return-void` bırak — aradaki tüm kodları sil
4. `.locals` değerini 0'a düşür (eski register sayısından)
5. Aynı kontrolü `onStop()` için de yap — bazı uygulamalar onStop'u kullanır

```smali
.method protected final onPause()V
    .locals 0

    .line 1
    invoke-super {p0}, Lfzv;->onPause()V

    .line 2
    return-void
.end method
```

Bu teknik uygulama minimize edildiğinde/kilitlendiğinde kaydın devam etmesini sağlar. İstenmeyen yan etki: kullanıcı uygulamadan çıkınca da kayıt devam eder.

**İleri teknik — obfuscated APK'lerde yeni sınıf ekleme:**

Obfuscated APK'lerde sınıf isimleri a, b, c olur. Mevcut smali'yi anlamaya çalışma. Sadece ya yeni sınıf ekle (karmaşık) ya da onPause boşalt (basit).

**Yeni smali sınıfı ekleme şablonu (basic KeepAliveService):**

```smali
# _work/smali/com/package/KeepAliveService.smali
.class public Lcom/package/KeepAliveService;
.super Landroid/app/Service;
.source "KeepAliveService.smali"

.method public onStartCommand(Landroid/content/Intent;II)I
    .locals 1
    const/4 v0, 0x1
    return v0
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    const/4 v0, 0x0
    return-object v0
.end method
```

**Foreground Service şablonu (mikrofon + bildirim):**

foregroundServiceType="microphone" olan service'lerde notification channel + startForeground zorunlu:

```smali
.class public Lcom/package/BgRecordService;
.super Landroid/app/Service;
.source "BgRecordService"

.method public onCreate()V
    .locals 5
    invoke-super {p0}, Landroid/app/Service;->onCreate()V
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v1, 0x1a
    if-lt v0, v1, :cond_0
    const-string v0, "bg_channel"
    const-string v1, "Recording"
    const/4 v2, 0x2
    new-instance v3, Landroid/app/NotificationChannel;
    invoke-direct {v3, v0, v1, v2}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V
    const-class v1, Landroid/app/NotificationManager;
    invoke-virtual {p0, v1}, Lcom/package/BgRecordService;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Landroid/app/NotificationManager;
    invoke-virtual {v1, v3}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V
    :cond_0
    return-void
.end method

.method public onStartCommand(Landroid/content/Intent;II)I
    .locals 3
    invoke-virtual {p0}, Lcom/package/BgRecordService;->getApplicationContext()Landroid/content/Context;
    move-result-object v0
    new-instance v1, Landroid/app/Notification$Builder;
    const-string v2, "bg_channel"
    invoke-direct {v1, v0, v2}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;Ljava/lang/String;)V
    const v2, 0x7f080689
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setSmallIcon(I)Landroid/app/Notification$Builder;
    const-string v2, "App Name"
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setContentTitle(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
    const-string v2, "Recording active"
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setContentText(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setOngoing(Z)Landroid/app/Notification$Builder;
    invoke-virtual {v1}, Landroid/app/Notification$Builder;->build()Landroid/app/Notification;
    move-result-object v1
    const/16 v2, 0x3e8
    invoke-virtual {p0, v2, v1}, Lcom/package/BgRecordService;->startForeground(ILandroid/app/Notification;)V
    const/4 v0, 0x1
    return v0
.end method
```

İcon ID: `grep "icon\\|logo" _work/res/values/public.xml` ile bul → `const v2, 0x7f08XXXX`.

Application.onCreate()'a enjeksiyonda `startForegroundService()` kullan (startService değil) — manifest'te foregroundServiceType varsa startService crash üretebilir. Dönüş tipi void olduğu için smali'de `move-result` kullanma.

**OnCreate'e enjeksiyon:**

Application subclass'ının onCreate'ini bul (`.method public final onCreate()V` ara, invoke-super'dan sonra ekle):

```smali
    new-instance v1, Landroid/content/Intent;
    const-class v0, Lcom/package/KeepAliveService;
    invoke-direct {v1, p0, v0}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    invoke-virtual {p0, v1}, Lcom/package/ApplicationClass;->startForegroundService(Landroid/content/Intent;)V
```

**ÖNEMLİ:** `startForegroundService` void döner — smali'de `move-result` kullanma. Manifest'te `foregroundServiceType` tanımlı service'ler için `startService()` yerine `startForegroundService()` zorunludur. Aksi halde `RuntimeException: Context.startForegroundService()` hata alınır.

**.locals kontrolü:** Enjeksiyon yaptığın metodda `.locals X` varsa, kullandığın register sayısını karşıla. X >= kullandığın en yüksek register+1 olmalı. Yoksa local sayısını artır.

**GATE 2S:** Yeni smali dosyası _work/smali/**/ altında mı? `find _work/smali -name "*.smali" | wc -l` arttı mı?

---

### Adım 3 — REBUILD

```bash
$APKTOOL b -o _build_unsigned.apk _work/
```

**GATE 3:**
```bash
[ -f _build_unsigned.apk ] && echo "APK_OLUSTU: $(stat -c%s _build_unsigned.apk) bytes" || (echo "REBUILD_FAILED"; exit 1)
```

Hata varsa apktool log'unu oku:
- `brut.androlib.AndrolibException` → genelde kaynak XML hatası
- `Resource ID 0x7f0xxxxx not found` → eksik resource
- `Unknown resource type` → public.xml bozulmuş

**Hata varsa DUR.** Aynı hatayı 3 kez fix'lemeden dene — başarısızsa farklı strateji (binary-level patch, Bölüm 13).

---

### Adım 4 — ZIPALIGN (Atlanamaz)

```bash
"$ZIPALIGN" -p 4 _build_unsigned.apk _build_aligned.apk
```

**GATE 4:**
```bash
"$ZIPALIGN" -c 4 _build_aligned.apk
# Çıktı "Verification successful" içermeli
```

Başarısızsa: APK bozuk, rebuild'e dön. `-f` flag'i ekle (üzerine yaz):

```bash
"$ZIPALIGN" -f -p 4 _build_unsigned.apk _build_aligned.apk
```

---

### Adım 5 — İMZALA

**UYARI:** jarsigner KULLANMA. jarsigner sadece v1 imza üretir. Android 7+ v2/v3 ister. **apksigner zorunlu.**

```bash
"$APKSIGNER" sign \
  --ks "$KEYSTORE" \
  --ks-key-alias "$KEYALIAS" \
  --ks-pass pass:${KSPASS} \
  --key-pass pass:${KSPASS} \
  _build_aligned.apk
```

**GATE 5:**
```bash
"$APKSIGNER" verify _build_aligned.apk
# Çıktı "Verified using v1, v2, v3 scheme" içermeli
```

Sadece v1 görünüyorsa → jarsigner ile imzalamışsındır, başa dön.
"ERROR: JAR signer" hatası → zipalign atlanmış olabilir, adım 4'e dön.

---

### Adım 6 — DOĞRULA (En Değerli Adım)

Çoğu skill bu adımı atlar ve "tamam" der. Sonra uygulama açılışta çöker. **Bu adım atlanamaz.**

**6a — Cihaza kur:**

**Sistem uygulaması tespiti (Google ön yüklü uygulamaları, Samsung apps):**
```bash
# Sistem uygulaması mı kontrol et:
adb shell pm list packages -s | grep com.target.package
# Çıktı varsa = sistem uygulaması. Kaldırmak için:
adb uninstall -k --user 0 com.target.package
# Ardından telefonu YENİDEN BAŞLAT:
adb reboot && sleep 60 && adb wait-for-device
```

Normal kullanıcı uygulaması için:
```bash
adb install _build_aligned.apk
```

Eğer `INSTALL_FAILED_UPDATE_INCOMPATIBLE` alınırsa:
1. Sistem uygulaması mı kontrol et (`pm list packages -s`)
2. `adb uninstall -k --user 0 <pkg>` dene
3. Telefonu yeniden başlat
4. Tekrar dene
5. Hala hata alınıyorsa → root gerekir. Sistem uygulaması imza koruması kırılamaz.

**GATE 6a:** `adb shell pm list packages | grep com.package.name` ile kontrol et.

**6b — Logcat hazırlık + çalıştır:**
```bash
adb logcat -c                          # log temizle
adb shell monkey -p com.package.name 1  # uygulamayı aç

# 3 saniye bekle, sonra crash kontrolü:
adb logcat -d -b crash | grep -i "com.package.name"
adb logcat -d | grep -i "FATAL\|ANR\|Exception\|deadObject" | grep "com.package.name"
```

**GATE 6b:**
```bash
CRASH_COUNT=$(adb logcat -d | grep -c -i "FATAL\|ANR\|Exception\|deadObject.*com.package.name")
[ "$CRASH_COUNT" = "0" ] && echo "DOGRULAMA_GECTI" || echo "DOGRULAMA_KALDI: $CRASH_COUNT crash"
```

Crush varsa logcat çıktısını oku:
- `ClassNotFoundException` → smali'de class reference yanlış
- `ResourceNotFoundException` → resource ID public.xml'de yok
- `UnsatisfiedLinkError` → native lib hizalanmamış veya eksik
- `SecurityException` → manifest'te eksik izin

**6c — Rapor:**
```
DURUM: GECTI / KALDI
targetSdk: 35
Split: hayır
Native lib: arm64-v8a (3 .so)
Obfuscation: R8 var
APK boyutu: 12.4 MB
İmza: v2+v3
Logcat: 0 crash
```

---

## Troubleshooting — Sessiz Hataların Kök Sebebi

| Hata | Gerçek Sebep | Çözüm |
|------|-------------|-------|
| "Parse error" / "Package invalid" | .so dosyaları DEFLATE ile sıkıştırılmış | ZIP_STORED ile yeniden paketle |
| Installation "incompatible" | isSplitRequired kaldırılmamış | Manifest'ten split referanslarını sil |
| App opens then crashes silently | Resource ID yanlış | public.xml'den ID'yi teyit et |
| "App not installed" / INSTALL_FAILED_UPDATE_INCOMPATIBLE | İmza çakışması (farklı keystore) veya sistem uygulaması | Eski sürümü kaldır (`adb uninstall --user 0`). Sistem uygulamasıysa + reboot dene. Hala olmazsa → root gerekir. Kullanıcıya bildir. |
| INSTALL_FAILED_MISSING_SPLIT | Split APK base'den ayrı yükleniyor | Manifest'ten `requiredSplitTypes` + `splitTypes` taglerini sil. Meta-data'dan `splits.required`, `com.android.vending.splits` kaldır. |
| Google Play Services broken | Orijinal imza gitti — GMSCore reddediyor | Kaçınılmaz. Alternatif API stratejisi |
| apktool b hata vermiyor ama APK yok | Java heap yetersiz | `export JAVA_OPTS="-Xmx4g"` ile tekrar dene |
| `pm install` sdcard'dan "Can't open file" | system_server sdcard'a erişemez | APK'yı `/data/local/tmp/`'e push et, ordan kur: `adb push apk /data/local/tmp/` + `adb shell pm install -r -t /data/local/tmp/apk` |
| `appops set` çalışıyor ama uygulama hala foreground davranıyor | Uygulama runtime'da ops değişikliğini okumaz, restart gerekir | Uygulamayı kapatıp aç: `adb shell am force-stop com.package` + manuel başlat |
| Auto Blocker / Play Protect engelliyor | Samsung Auto Blocker veya Google Play Protect | ADB ile kapat: `adb shell settings put global package_verifier_enable 0 && adb shell settings put global verifier_verify_adb_installs 0 && adb shell settings put global auto_blocker_enabled 0 && adb shell settings put secure auto_blocker_enabled 0`. Veya direkt `adb install` dene (Auto Blocker'ı bypass eder). |
| Sistem uygulamasına yama yapılamıyor (Android 16+, One UI 8) | `INSTALL_FAILED_UPDATE_INCOMPATIBLE` — reboot sonrası bile düzelmez | **Package rename stratejisi dene** (references/package-rename-bypass.md). Root'suz tek çözüm: rename + sideload. |
| `INSTALL_FAILED_DUPLICATE_PERMISSION` | `<permission>` ismi eski pakette kalmış | Manifest'teki permission string'ini yeni paket adına çevir |
| `INSTALL_FAILED_CONFLICTING_PROVIDER` | `<provider android:authorities>` çakışıyor | Provider authority'yi yeni paket adına çevir |
| `ClassNotFoundException` (package rename sonrası) | Smali'de class reference veya layout'ta custom view değişmemiş | Tüm smali + res XML'lerde eski paket adını tara ve değiştir |

## APK Yüklenemeyince — Runtime Alternatifleri

APK rebuild + imzalama işe yaramadığında (sistem uygulaması, Android 16+ koruma):
- Kullanıcıya **dürüstçe söyle:** root'suz sistem uygulaması yüklenemez. Zorlama.
- **Package rename + yeniden imzala** (Bölüm 13) ile farklı paket olarak yükle dene
- Runtime hook (Frida) alternatifini belirt ama kullanıcı istemedikçe uygulama

## Merge APK Rebuild — Resource Compilation Hataları

Split APK'yı merge ettikten sonra apktool rebuild'te `invalid value for type 'X'. Expected a reference` hatası alınırsa:

**Sebep:** Merge script'i values-*/ dizinlerindeki XML'lerde boolean değerleri yanlış tip bağlamında bırakır.

**Toplu düzeltme:** Tüm XML'leri tara, `>true</item>` veya `>false</item>` içeren satırları sil. Bu genelde anims.xml, layouts.xml, xmls.xml, animators.xml, drawables.xml, styles.xml, fonts.xml, interpolators.xml, menus.xml dosyalarında olur.

İkinci hata: `public.xml: no definition for declared symbol` — merge'de public.xml güncellenmemiştir. O zaman merge APK'yı bırak, orijinal split + base APK'yı ayrı imzalayıp `adb install-multiple` dene.

## Binary-level Package Name Değiştirme (apktool bypass)

apktool bazı APK'lerde "Paket geçersiz" hatası üretir. Güvenli alternatif:

Python ile binary AndroidManifest.xml'de UTF-16LE string değiştir:
```python
import zipfile
orig = "com.google.audio.hearing.visualization.accessibility.scribe"
new_pkg = "com.live.transcribe.hermes.twentyfourhours.extended.android"
assert len(orig) == len(new_pkg), "Uzunluklar esit olmali!"
with zipfile.ZipFile("target.apk", "r") as z:
    manifest = z.read("AndroidManifest.xml")
new_manifest = manifest.replace(orig.encode('utf-16-le'), new_pkg.encode('utf-16-le'))
# sonra yeni zip yarat, imzalı APK'yı bu binary manifest ile replace et
```

Kurallar:
- Yeni isim **kesinlikle aynı uzunlukta** olmalı
- Google paket isimlerini (`com.google.*`, `com.android.*`) kullanma — Samsung bloklar
- `manifest.count(orig_utf16)` ile kaç yerde geçtiğini kontrol et

---

## Skill Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `references/obfuscated-lifecycle-methods.md` | Obfuscated APK'lerde onPause/onStop bulma ve boşaltma |
| `references/rootless-patching-methods.md` | Root'suz runtime müdahale yöntemleri karşılaştırması |
| `scripts/patch.sh` | 7 adımlı pipeline scripti — tek komutla önbelge→doğrula |
| `references/smali-syntax.md` | Smali sözdizimi referansı (register, invoke, if/else, şablonlar) |
| `references/foreground-service-smali.md` | Foreground service smali şablonu |
| `references/google-cloud-auth-limitation.md` | Google apps cloud auth limitation — custom imza ile sunucu reddi, Frida non-root notları |
| `references/package-rename-bypass.md` | Sistem uygulaması bypass: package rename + smali/res patching — full workflow, real vaka |
| `references/session-20260613-live-transcribe-package-rename.md` | Live Transcribe package rename oturumu — crash döngüsü (5 hata), LauncherActivity fix, Samsung security bypass, Windows path separator uyarısı |
| `references/live-transcribe-xray-analysis.md` | Live Transcribe X-ray: Lgfq, Lgmw sınıf haritası, onPause/onResume kod akışı |
| `references/live-transcribe-lifecycle-analysis.md` | Live Transcribe lifecycle metod haritası (onPause/onResume/onStop satır satır) |
| `references/live-transcribe-community-research.md` | Dünya çapında topluluk araştırması — kimse modlamamış, neden mod yok, alternatifler |
| `references/observations.md` | Oturum notları (Split APK merge, binary rename, Telegram upload, Samsung uyarıları) |
| `references/session-20260613-live-transcribe-package-rename.md` | Live Transcribe package rename oturumu — crash döngüsü (5 hata), LauncherActivity fix, Samsung security bypass, Windows path separator uyarısı |\n| `references/audio-record-tcp-bridge.md` | SpeechRecognizer alternatifi — sesi PC'ye akit, orada isle (APK modding cozemediginde) |\n\n### patch.sh Kullanımı

```bash
# Ortam hazırlık
export KSPASS='sifreni-gir'

# Full pipeline (önbelge → decompile → rebuild → zipalign → imzala → doğrula)
bash scripts/patch.sh target.apk full

# Manifest yaması: targetSdk düşür + debuggable aç
bash scripts/patch.sh target.apk manifest targetSdk=35 debuggable=true

# Manifest: split APK referanslarını temizle
bash scripts/patch.sh target.apk manifest split-clean

# Resource değişikliği: renk
bash scripts/patch.sh target.apk resource color primary_blue #FF0000

# Smali: yeni service sınıfı ekle
bash scripts/patch.sh target.apk smali KeepAliveService
```
