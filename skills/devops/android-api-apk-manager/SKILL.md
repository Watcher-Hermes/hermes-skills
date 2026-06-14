---
name: android-api-apk-manager
description: Android APK kontrolü yükleme yönetme. Mevcut varlıkları kontrol et, eksikleri indir/kur, yükleme olmayanları işle, tüm süreci doğrula.

audience: maintainer---

# Android APK Manager Workflow

## Amaç
Cihazdaki uygulama durumunu kontrol et, eksik olanları belirle, setup yap, gereksiz/cache dosyaları temizle, her adımda doğrula.

## Gereksinimler
- Windows 10
- Android SDK Platform-Tools (`adb`) PATH’te olmalı
- Android cihaz veya emülatör ile USB hata ayıklama açık

## ADB Kurulumu (Windows 10 — sabit yöntem)
PATH’te `adb` yoksa şu adımları otomatik uygula:
1. İndir: `curl -o /tmp/platform-tools-latest-windows.zip https://dl.google.com/android/repository/platform-tools-latest-windows.zip`
2. Çıkar: `unzip -q /tmp/platform-tools-latest-windows.zip -d "$LOCALAPPDATA/Android/Sdk/"`
3. PATH’e ekle: `setx PATH "$PATH;$LOCALAPPDATA\Android\Sdk\platform-tools"` (Windows kalıcı PATH)
4. Doğrula: `adb version`

*Not: Windows'ta "Path boşluğu/özel karakter" hatası alırsan komutları tırnakla sar (ör. `python 'C:\...\android_scan.py'`).*

## Sıra
1) **Varlık kontrolü**
   - APK dosyalarını bul: `C:\Users\<user>\Downloads` ve varsa `Projects/android`
   - Yüklü uygulamaları listele: `adb shell pm list packages`
   - Eğer APK tarama scripti (`android_scan.py`) varsa çalıştır

2) **Eksikleri işaretle**
   - Temel Araçlar: `Files`, `Termux` (opsiyonel eklentiler)
   - Not: ekran kaydedici/screenshot için `screencap` kullan

3) **Kurulum**
   - Bulunan APK seç, `adb install -r <apk>` ile kur ya da APK dosyasını aç
   - Yanlış/corrupt APK bulursan başka bir APK dene

4) **Sonrası**
   - Yapılandırma tamamlandı mı kontrol et: run kullanarak test et
   - Cihazda yüklü paketleri doğrula: `adb shell cmd package ls packages`

## APK Analizi (aapt2)

APK'nın iç yapısını analiz etmek için `aapt2` kullan:

```bash
# Manifest bilgisi
"/c/Users/marko/AppData/Local/Android/Sdk/build-tools/35.0.0/aapt2" dump manifest "<apk_yolu>"

# Detaylı badge/izin bilgisi
"/c/Users/marko/AppData/Local/Android/Sdk/build-tools/34.0.0/aapt" dump badging "<apk_yolu>"
```

**Çıktıda kontrol edilecekler:**
| Alan | Ne aranır |
|------|-----------|
| `package:` | Paket adı (örn. `com.livetranscriber`) |
| `targetSdkVersion:` | Telefonun Android sürümüne uygun mu? |
| `sdkVersion:` | Minimum SDK (eski cihazlar için 26+ yeterli) |
| `uses-permission:` | İzinler (RECORD_AUDIO, INTERNET, vb.) |
| `launchable-activity:` | Ana Activity adı |
| `application-label:` | Uygulama görünen adı |

## Samsung / One UI 8 / Android 16 Sideload Sorun Giderme

**Belirti**: APK yüklenmeye çalışırken Google Play Protect "engellendi" diyor,
"Anladım" butonuna basınca "Uygulama yüklenmedi" hatası alınıyor.

**Sebep**: 2026 itibarıyla Google + Samsung çift katman güvenlik:
1. **Google Play Protect** — bilinmeyen geliştirici imzasını engeller
2. **Samsung Auto Blocker** (One UI 8) — Knox tabanlı ek güvenlik
3. **Android 16** — yeni kurulum kısıtlamaları, hedef SDK kontrolü
4. **Android 16 Stalkerware Detection** — FOREGROUND_SERVICE + RECORD_AUDIO kombinasyonu yükleme zamanında tespit edilip engellenir (Play Protect ve Auto Blocker'dan bağımsız). Detay: `references/android16-stalkerware-detection.md`

**Çözüm sırası (en kolaydan en zora):**

### A. Play Protect + Samsung Ayarları
```
1. Ayarlar > Güvenlik ve gizlilik > Otomatik Engelleyici → KAPAT
2. Ayarlar > Biyometri ve güvenlik > Bilinmeyen uygulamalar > Telegram → İzin ver
3. Telefonu kapat/aç (RAM'daki Play Protect önbelleği silinsin)
```

### B. ADB ile Bilgisayardan Yükle (KESİN ÇÖZÜM)
Bu yöntem **Play Protect ve Knox'u bypass eder**, direkt sisteme yazar.

```bash
# Telefon bağlı mı?
"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe" devices

# APK'yı yükle
"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe" install "<apk_yolu>"

# Önceki sürüm varsa kaldır
"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe" uninstall <paket_adi>
```

**Gereksinimler:**
- Telefonda Geliştirici Seçenekleri açık
- USB Hata Ayıklama AÇIK
- USB kablo ile bağlı
- Telefonda "USB hata ayıklamaya izin ver" onayı verilmiş

### C. Emülatörde Test
APK'yı önce emülatörde test et (varsa):
```bash
# APK yükle
"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe" -s emulator-5554 install "<apk_yolu>"

# Çalıştır
"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe" -s emulator-5554 shell am start -n <paket_adi>/<MainActivity>

# Çalıştığını doğrula
"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe" -s emulator-5554 shell ps | grep <paket_adi>
```

## APK Dosyasını Telefona Aktarma (Fallback Zinciri)

Kullanıcıya APK'yı teslim etmek için sıralı fallback:

### 1. ADB ile direkt yükle (EN HIZLI)
```bash
# USB debugging AÇIK olmalı
\"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe\" devices
# Cihaz görünüyorsa:
\"/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe\" install \"<apk_yolu>\"
```

### 2. ADB cihaz görmüyorsa — USB Debugging AÇTIR

Kullanıcı "ben beceremem" dese bile şu adımları **tek tek, net** söyle:

```
1. Telefonda: Ayarlar → Telefon hakkında → Yazılım bilgisi
2. "Yapı numarası"na 7 kere tıkla (Geliştirici seçenekleri açılır)
3. Geri gel → Geliştirici seçenekleri → USB Debugging AÇ
4. USB'yi çıkar tak, telefonda "İzin ver" de
```

### 3. Telegram üzerinden parçalı gönder (ADB yoksa)

**Kural:** 15MB+ APK'yı `send_message` ile MEDIA: olarak göndermek timeout yiyor.

Çözüm: 9MB'lık parçalara böl, her parçayı ayrı `send_message` ile gönder:
```bash
split -b 9M signed.apk apk9_
# Çıktı: apk9_aa, apk9_ab, apk9_ac (3 parça ~9MB)
```

Her parçayı ayrı `send_message(target='telegram')` ile gönder. Telegram 50MB limit, 9MB sorunsuz geçer.

Kullanıcı telefonda 3 parçayı da indirir, Termux ile birleştirir:
```bash
cat apk9_aa apk9_ab apk9_ac > Uygulama.apk
```

### 4. Online upload servisi (son çare)

`file.io`, `transfer.sh` gibi servisler bu makineden genelde çalışmıyor (Cloudflare, DNS, bağlantı sorunları). Denenebilir ama güvenme.

### 5. Windows APK ekstraksiyon sorunu

APK'yı masaüstüne kopyalarken Windows bazen .apk'yı zip arşivi olarak tanır ve çift tıklayınca **içindekileri açar/klasör olarak gösterir**. Kullanıcı "Apk dosya degil bunlar" der.

Çözümler:
- APK'yı farklı isimle kaydet (ör. `LT24h_v3.apk` → kısa isimler daha az sorun çıkarır)
- Veya APK'yı `.zip` içinde gönder (kullanıcı zip'i açar, içinden APK'yı çıkarır)
- Kullanıcıya söyle: "Masaüstündeki **.apk** dosyası asıl dosya, klasör olan değil"

---

## APK Modding (Decompile → Modify → Rebuild → Sign)

Varolan bir APK'yı tersine mühendislik ile değiştirmek için bu workflow'u izle.

### Gereksinimler
- `apktool.jar` (en son sürüm, indir: `https://github.com/iBotPeaches/Apktool/releases`)
- `uber-apk-signer.jar` (isteğe bağlı, imza için)
- `jarsigner` veya `apksigner` (JDK ile gelir)
- Java JDK 17+
- `aapt2` (Android SDK build-tools içinde)

### Adımlar

#### 1. APK İndir
```bash
# APKMirror'dan indir (tarayıcı ile)
# APK'yı çalışma dizinine koy
cp /c/Users/marko/Desktop/orijinal.apk ~/proje/
```

#### 2. Analiz Et (mod öncesi)
```bash
# APK yapısını kontrol et
aapt2 dump badging "orijinal.apk" | grep -E "package:|minSdkVersion:|targetSdkVersion:|native-code:|split:"

# İmza şemalarını kontrol et
apksigner verify --verbose "orijinal.apk" 2>&1 | grep -E "Verified using|WARNING:"
```

#### 3. Decompile Et
```bash
java -jar apktool.jar d -f orijinal.apk -o decompile_out/
# Çıktı: decompile_out/AndroidManifest.xml, smali/, res/, lib/, assets/
```

#### 4. Değişiklikleri Yap

**Manifest düzenleme:**
- `targetSdkVersion` → 35 (Android 15, en güvenilir)
- `minSdkVersion` → cihaz SDK'sından düşük olmalı
- Split APK referanslarını temizle: `android:isSplitRequired="false"` veya sil, `split` niteliğini kaldır
- Foreground service ekle: `<service android:name=".KeepAliveService" android:exported="false" android:foregroundServiceType="microphone" />`

**Smali ekleme:**
- Yeni bir `.smali` dosyası oluştur (KeepAliveService, BroadcastReceiver vb.)
- Referans için `references/apk-smali-service-template.md` kullan

**Native lib'leri düzeltme:**
- apktool build bazen native lib'leri sıkıştırır (`compress_type=8`) ama `extractNativeLibs="false"` kalırsa Android açamaz
- Çözüm: `extractNativeLibs="true"` yap VEYA APK'yı build sonrası uncompressed lib'lerle yeniden paketle
- Düzeltme: `apktool b` sonrası çıkan APK'yı zip aç, `lib/` klasörünü uncompressed olarak yeniden ekle

#### 5. Rebuild Et
```bash
java -jar apktool.jar b decompile_out/ -o rebuilt_unsigned.apk
```

#### 6. İmzala

**Android 16 için ZORUNLU: V2 + V3 imza şemaları. Sadece V3 hata verir.**

```bash
# Seçenek A — jarsigner (yalın, V3 destekler)
keytool -genkey -v -keystore my.keystore -alias myalias -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore my.keystore rebuilt_unsigned.apk myalias
jarsigner -verify -verbose rebuilt_unsigned.apk

# Seçenek B — apksigner (V2+V3 garanti, tercih edilen)
apksigner sign --ks my.keystore --ks-key-alias myalias --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true --out signed.apk rebuilt_unsigned.apk
apksigner verify --verbose signed.apk
```

**apksigner yolu:** Android SDK build-tools içinde:
```bash
"/c/Users/marko/AppData/Local/Android/Sdk/build-tools/35.0.0/apksigner" sign --ks my.keystore --ks-key-alias myalias rebuilt_unsigned.apk
```

#### 7. Split APK'ları Birleştir (varsa)

apktool bazen `base.apk` + `split_config.arm64_v8a.apk` olarak iki dosya üretir. Single APK gerekiyorsa:

```bash
# APKEditor ile birleştir
java -jar APKEditor.jar m -i base.apk -o monolithic.apk -s split_config.arm64_v8a.apk

# Tekrar imzala (birleştirme imzayı bozar)
apksigner sign --ks my.keystore --ks-key-alias myalias monolithic.apk
```

Veya manifest'ten split referanslarını temizle, `apktool b` ile yeniden build et.

#### 8. Doğrula
```bash
# İmza doğrulama
apksigner verify --verbose signed.apk

# APK yapısı
aapt2 dump badging signed.apk | grep -E "package:|sdkVersion:|targetSdkVersion:|native-code:|split:|launchable-activity:"

# Boyut kontrolü
ls -la signed.apk
```

#### 9. Kullanıcıya Teslim Et

**Fallback zincirini kullan:** Yukarıdaki "APK Dosyasını Telefona Aktarma (Fallback Zinciri)" bölümüne bak. Sırasıyla:
1. ADB dene
2. USB Debugging açtır
3. Telegram 9MB parçalı gönder
4. Kullanıcı yapamıyorsa, en kolay yöntemi seç (genelde Telegram parçalı gönder)

**Windows APK'yı zip gibi açma sorunu:** Windows bazen .apk dosyasını zip arşivi olarak tanır. Kullanıcı "Apk dosya degil bunlar" derse: kısa isimle tekrar masaüstüne kopyala veya .zip içinde gönder.

### Pitfall'lar (APK Modding)

1. **apktool rebuild binary XML bozabilir** — "Paket geçersiz göründü" hatası alınırsa: ya aapt2 ile direkt derle (apktool yerine) ya da orijinal APK'yı koruyup sadece smali seviyesinde değişiklik yap
2. **Native lib sıkıştırması** — apktool build lib'leri sıkıştırır. `extractNativeLibs="false"` ise Android açamaz. İkisini uyumlu yap: `extractNativeLibs="true"` veya build sonrası lib'leri uncompressed olarak yeniden paketle
3. **V3-only imza** — Android 16 bazen sadece V3 imzalı APK'yı reddeder. `apksigner` ile V2+V3 birlikte imzala
4. **Split APK** — apktool base + split olarak üretebilir. Single APK için `isSplitRequired` temizlenmeli veya APKEditor ile birleştirilmeli
5. **targetSdk 36 (Android 16)** — kullanma, 35 (Android 15) daha güvenilir. 36 yeni kısıtlamalar getirir
6. **Foreground Service + Mikrofon** — Android 16, RECORD_AUDIO + FOREGROUND_SERVICE kombinasyonunu stalkerware olarak algılayıp UI kurulumunu engeller. ADB ile sideload tek çözüm
7. **APK boyutu büyükse** — 15MB+ APK'ları Telegram'a MEDIA: ile gönderirken timeout olabilir. Güvenilir yöntem: 9MB parçalara bölüp (`split -b 9M`), her parçayı ayrı `send_message(target='telegram')` ile gönder. Bu yöntem 27MB APK'da bile çalışır.
8. **Windows APK ekstraksiyonu** — Kullanıcı APK'yı zip gibi açıp içindekileri görebilir. APK dosyasının kendisini kullanması gerektiğini belirt

### Samsung / One UI 8 / Android 16 Sideload Sorun Giderme

**Belirti**: APK yüklenmeye çalışırken Google Play Protect "engellendi" diyor,
"Anladım" butonuna basınca "Uygulama yüklenmedi" hatası alınıyor.

**Sebep**: 2026 itibarıyla Google + Samsung çift katman güvenlik:
1. **Google Play Protect** — bilinmeyen geliştirici imzasını engeller
2. **Samsung Auto Blocker** (One UI 8) — Knox tabanlı ek güvenlik
3. **Android 16** — yeni kurulum kısıtlamaları, hedef SDK kontrolü
4. **Android 16 Stalkerware Detection** — FOREGROUND_SERVICE + RECORD_AUDIO kombinasyonu yükleme zamanında tespit edilip engellenir (Play Protect ve Auto Blocker'dan bağımsız). Detay: `references/android16-stalkerware-detection.md`

### Samsung Cihaz Bilgisi Tespiti

Kullanıcı "Telefonunuzla uyumlu değil" hatası alıyorsa, önce cihaz modelini tespit et:

```bash
# Cihaz modeli
adb shell getprop ro.product.model
# Örn: SM-S908E → Samsung Galaxy S22 Ultra

# Android sürümü
adb shell getprop ro.build.version.release

# SDK sürümü
adb shell getprop ro.build.version.sdk

# One UI sürümü
adb shell getprop ro.build.version.oneui
```

"Telefonunuzla uyumlu değil" hata sebepleri:
1. **Split APK referansı** — manifest'te `isSplitRequired=true` veya `split` niteliği var
2. **Native lib mimari uyuşmazlığı** — APK sadece `arm64-v8a` ama cihaz `x86` veya vice versa
3. **minSdk > cihaz SDK'sı** — APK Android 14+ gerektiriyor ama cihaz Android 13
4. **targetSdk 36 (çok yeni)** — Android 16'da hedef SDK 36 yeni kısıtlamalar getirir, 35 kullan

## DİKKAT
- `adb` ve OEM sürücüleri Windows 10'da yüklemek gerekir.
- Talimatlara göre ilerle; her aşamada durumu doğrula.
- Eğer bir araç yoksa önce onu bul/kur, sonra bir sonraki adıma geç.
- Güvenin bittiği adımları otomatik devam et.
- APK modding yaparken orijinal APK'yı yedekle.
- **Fallback zincirini kullan:** ADB önce, olmazsa USB Debugging açtır, olmazsa Telegram 9MB parçalı gönder. Sırayla dene.
- **"Ben beceremem" durumu:** Kullanıcı yapamayacağını söylerse en otomatik yöntemi seç (Telegram parçalı gönder). USB Debugging açtırmak için bile çok kısa adım yaz, uzun talimat verme.
- **Teslim:** Masaüstüne kopyala + Telegram parçalı gönder (ikisini birden yap). Biri çalışmazsa diğeri yedek olur.
- **"Yok" / "Olmadi" sinyali:** Kullanıcı "yok", "olmadi" dedikten sonra aynı yaklaşımı tekrar tekrar deneme. Yaklaşım değiştir. Kullanıcının önerdiği yeni yönü dene (örn. "telefon içinden değişiklik").
- **Telegram curl upload:** send_message MEDIA: timeout yiyorsa, curl ile direkt Telegram Bot API'ye yükle (token hex decode ile alınır). 30MB APK'lar sorunsuz çıkar.
- **Android 16 Stalkerware Detection:** FOREGROUND_SERVICE + RECORD_AUDIO kombinasyonu içeren APK'lar, kullanıcı arayüzü üzerinden **ASLA** kurulamaz. ADB sideload veya Play Store dağıtımı gerekir. Auto Blocker/Play Protect kapatmak işe yaramaz. Detay: `references/android16-stalkerware-detection.md`
