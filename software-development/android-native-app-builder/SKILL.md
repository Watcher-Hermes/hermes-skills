---
name: android-native-app-builder
description: Sıfırdan native Android APK oluşturma — Java + Gradle + SpeechRecognizer. ADB, SDK, Gradle wrapper ile CLI üzerinden tam build.

audience: contributor---

# Android Native App Builder

## Amaç
Masaüstünden Android uygulaması üretip APK'ye build etmek. ADB + Android SDK + Gradle kullanır.

## Ön Koşullar
- Java JDK (17+)
- Android SDK (platform-tools + build-tools + platform)
- Gradle wrapper (indirilir)

## Proje Yapısı
```
<proje_adi>/
├── build.gradle.kts (root — sadece plugin declaration)
├── settings.gradle.kts (repo + include(":app"))
├── gradle.properties (android.useAndroidX=true)
├── local.properties (sdk.dir)
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew + gradlew.bat
└── app/
    ├── build.gradle.kts (android plugin + dependencies)
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/<package>/MainActivity.java
        └── res/
            ├── layout/activity_main.xml
            └── values/
                ├── strings.xml
                └── themes.xml
```

## .gitignore (Zorunlu)

Android projelerinde `.gitignore` kök dizinde olmalı. **`/build` değil, `**/build` kullan** — çünkü `app/build/` alt klasörü de var:

```gitignore
*.iml
.gradle
**/build
/captures
.externalNativeBuild
.cxx
local.properties
release.keystore
nul
.idea/
.DS_Store
*.apk
*.aab
*.keystore
*.jks
```

### Pitfall: `nul` dosyası (Windows)

Windows'ta Gradle bazen `nul` adında 0-byte'lık garip bir dosya oluşturur. Git bunu index'leyemez (`error: short read while indexing nul`). **Çözüm:**

```bash
# Git init'ten ÖNCE nul dosyasını sil
rm -f /c/Users/marko/Desktop/<proje>/nul
# .gitignore'a nul ekle (yukarıdaki template'de zaten var)
```

Eğer `nul` dosyası git add sırasında hataya sebep olursa:
1. `rm -f nul` ile sil
2. `.git` klasörünü silip (`rm -rf .git`) baştan init et
3. `.gitignore`'da `nul` satırı olduğundan emin ol
4. `git add -A` ile tekrar dene

### `.gitignore`'a İlk Eklenmesi Gerekenler (Android Özel)

| Pattern | Neden |
|---------|-------|
| `**/build` | Tüm `build/` alt klasörleri (`app/build/`, `build/`) |
| `release.keystore` | İmza anahtarı — sızdırılırsa başkası APK imzalayabilir |
| `nul` | Windows phantom dosya |
| `.idea/` | Android Studio kişisel ayarları |
| `local.properties` | SDK yolu (kullanıcıya özel) |
| `.gradle` | Gradle cache |

## Önce Mevcut APK'yi Kontrol Et
Kullanıcı "uygulama üretebilir misin" dediğinde hemen build'e atlama. Önce kontrol et:
```bash
ls /c/Users/marko/Desktop/*.apk 2>/dev/null
ls -d /c/Users/marko/Desktop/<proje-adi> 2>/dev/null
```
Eğer APK zaten varsa kullanıcıya **sadece adını ve/veya install komutunu söyle**. Açıklama yapma, emülatör/image indirme önerme. Kullanıcı "gerek var mı" diye sorgular — gereksiz adım atlama.

## Adımlar

### 1. Dizin yapısı
```bash
mkdir -p <proje>/app/src/main/java/com/<pkg>
mkdir -p <proje>/app/src/main/res/layout
mkdir -p <proje>/app/src/main/res/values
mkdir -p <proje>/gradle/wrapper
```

### 2. Gradle wrapper
```bash
# gradle-wrapper.properties yaz
# jar indir
curl -sL "https://github.com/gradle/gradle/raw/v8.11.1/gradle/wrapper/gradle-wrapper.jar" -o gradle/wrapper/gradle-wrapper.jar
# gradlew indir
curl -sL "https://raw.githubusercontent.com/gradle/gradle/v8.11.1/gradlew" -o gradlew
curl -sL "https://raw.githubusercontent.com/gradle/gradle/v8.11.1/gradlew.bat" -o gradlew.bat
chmod +x gradlew gradlew.bat
```

### 3. Build
```bash
export ANDROID_HOME="/c/Users/<user>/AppData/Local/Android/Sdk"
export ANDROID_SDK_ROOT="/c/Users/<user>/AppData/Local/Android/Sdk"
./gradlew assembleDebug --no-daemon
```

### 4. APK konumu
`app/build/outputs/apk/debug/app-debug.apk`

## SpeechRecognizer API için Önemli Noktalar
- **İzin:** `RECORD_AUDIO` manifest'te + çalışma zamanında istenmeli
- **Intent extras:** `EXTRA_PARTIAL_RESULTS=true` (kısmi sonuç), `EXTRA_LANGUAGE_MODEL=FREE_FORM`
- **Sürekli dinleme:** `onResults()` callback'inde `startListening()`'i tekrar çağır
- **Hata yönetimi:** `onError()`'da otomatik yeniden başlatma
- **Pitfall:** SpeechRecognizer servisi destroy edilmezse memory leak; `onDestroy()`'da `speechRecognizer.destroy()` çağır

## Emülatörde UI Otomasyonu (İzin Dialogları)

Emülatörde uygulama test ederken Android izin dialogları (mikrofon, bildirim, depolama) manuel müdahale gerektirir. **uiautomator + ADB ile programatik çözüm:**

### 1. UI Dump Al
```bash
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell uiautomator dump /sdcard/ui.xml
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe pull /sdcard/ui.xml /c/Users/marko/Desktop/
```

### 2. Buton Koordinatlarını Bul (Python/regex)
```python
import re
with open('ui.xml', 'r') as f:
    content = f.read()
for text, bounds in re.findall(r'text="([^"]*)"[^>]*bounds="([^"]*)"', content):
    if text.strip():
        print(f"'{text}' -> {bounds}")
# bounds="[left,top][right,bottom]" → center = ((left+right)/2, (top+bottom)/2)
```

### 3. Tıkla
```bash
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell input tap <center_x> <center_y>
```

### İzin Sırası (LiveTranscriber örneği)
İzin dialogları **sırayla** gelir. Birini yanıtlamadan diğeri görünmez:
1. **RECORD_AUDIO** → "While using the app" (center 720,1590)
2. **POST_NOTIFICATIONS** (Android 13+) → "Allow" (center 720,1695)
   - Foreground Service çalıştırmak için bildirim izni zorunlu

**Pitfall:** BAŞLAT butonuna basınca önce MİKROFON izni gelir, sonra BİLDİRİM izni gelir. İkinci izin gelene kadar `uiautomator dump` ile UI'yi tekrar kontrol et. Arada `sleep 3-5` bırak.

**Kısayol — ADB ile tüm izinleri tek seferde ver (UI tıklamaya gerek kalmaz):**
```bash
adb shell pm grant com.package android.permission.RECORD_AUDIO
adb shell pm grant com.package android.permission.POST_NOTIFICATIONS
# Sonra uygulamayı yeniden başlat:
adb shell am force-stop com.package
adb shell am start -n com.package/.MainActivity
```
Bu yöntemle izin dialogları hiç gösterilmez, doğrudan BAŞLAT'a basabilirsin.

**Pitfall:** Emülatörün sanal mikrofonu olmadığı için BAŞLAT'a basınca SpeechRecognizer hemen hata döner ve duruma yansımaz. Test için "Butonlara basılabiliyor ve durum değişiyor" yeterlidir.

### Ekran Görüntüsü (Emülatör)
```bash
# Python ile (Git Bash path sorununu atlar)
import subprocess
adb = r'C:\\...\\platform-tools\\adb.exe'
subprocess.run([adb, 'exec-out', 'screencap', '-p'], stdout=open('screenshot.png', 'wb'))
```

### OCR ile Ekran Doğrulama
Her ADB işleminden sonra ekran görüntüsü alıp OCR ile uygulama durumunu doğrula:

```python
import pytesseract, cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('emulator_screen.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray, lang='eng+tur')
print(text)  # "Dinleniyor...", "Durduruldu", "Hazır" gibi durum metinlerini göster
```

**Önemli:** Tesseract yolu her sistemde aynı olmayabilir. `which tesseract` veya `C:\Program Files\Tesseract-OCR\tesseract.exe` ile kontrol et. Python'dan kullanırken `pytesseract.tesseract_cmd`'i mutlaka set et.

**OCR ile doğrulanabilen durumlar:**
- Uygulama açıldı mı? → "Canlı Transkript" başlığını ara
- İzin dialog'u mu? → "Allow", "While using the app" metinlerini ara
- Transkripsiyon başladı mı? → "Dinleniyor..." metnini ara
- Transkripsiyon durdu mu? → "Durduruldu" metnini ara

### Logcat Debug
```bash
# Belirli PID'den log al (önce PID'i bul)
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell dumpsys activity services com.package | grep "app=ProcessRecord"
# PID'den log
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell logcat -d --pid=<PID>
```

### Servis Durumu Kontrolü
```bash
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell dumpsys activity services com.package
# Çıktıda "ServiceRecord{...}" varsa servis çalışıyor
```

## Emülatör Test Sınırlamaları

- **Sanal mikrofon yok:** Google APIs sistem imajı (`google_apis;x86_64`) SpeechRecognizer'ı destekler ama varsayılan emülatörde sanal ses girişi yoktur. SpeechRecognizer `ERROR_NO_MATCH` veya `ERROR_SPEECH_TIMEOUT` ile döner, hiçbir callback (onResults/onPartialResults) ateşlenmez.
- **Gerçek test:** Fiziksel telefona yükle (USB hata ayıklama) veya emülatöre host mikrofondan ses yönlendirmesi yap.
- **Google servis kontrolü:** `adb shell pm list packages google` ile doğrula

## Yaygın Hatalar
| Hata | Çözüm |
|------|-------|
| `dependencyResolution` hatası | `dependencyResolutionManagement` olarak düzelt |
| `android.useAndroidX` | `gradle.properties`'e ekle |
| SDK license kabulü | `yes | sdkmanager --licenses` |
| build-tools versiyonu | Gradle otomatik eksik olanı indirir |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | İmza uyuşmazlığı — önce `adb uninstall com.package` yap, sonra tekrar `adb install` |
| `INSTALL_FAILED_ALREADY_EXISTS` | `adb install -r` ile yeniden dene (replace) |

## Testing & Deployment

APK build ettikten sonra test etmek için **CLI build tercih edilir** — Android Studio Gradle sync'i beklemekten daha hızlı ve güvenilirdir.

### A. CLI Build (Tercih Edilen)
```bash
cd <proje_dizini>
export ANDROID_HOME="/c/Users/<user>/AppData/Local/Android/Sdk"
./gradlew assembleDebug --no-daemon
# BUILD SUCCESSFUL in ~10-30sn
```

### B. ADB ile Emülatöre Yükleme

```bash
# 1. Emülatör bağlı mı kontrol et
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe devices

# 2. APK'yı yükle
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe install "C:\Users\marko\Desktop\LiveTranscriber.apk"

# 3. Uygulamayı başlat
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell am start -n com.<package>/.MainActivity

**Pitfall — Git Bash + ADB pull path dönüşümü:** Terminal aracı Git Bash kullanır (`bash`). `adb pull /data/local/tmp/file` gibi bir komut gönderdiğinde Git Bash `/data/local/tmp/file` yolunu `C:/Program Files/Git/data/local/tmp/file` olarak çevirir ve ADB "No such file or directory" hatası alır.
- **Çözüm 1:** Python `execute_code` aracını kullan → `subprocess.run()` ile argümanlar doğrudan geçer, bash araya girmez.
- **Çözüm 2:** `adb.exe shell "cd /data/local/tmp && screencap screen.png"` — shell içinde kal, pull yerine push kullan.
- **Android 16 (API 36) notu:** `screencap` komutu `-p` flag'ini eski sürümler gibi kabul eder ancak sözdizimi `screencap [-ahp] [-d display-id] [FILENAME]` şeklindedir; en kolayı: `screencap /data/local/tmp/screen.png` (çıktı .png uzantısından otomatik tanınır).

# 4. Ekran görüntüsü al
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe exec-out screencap -p > "C:\Users\marko\Desktop\emu_screen.png"
```

### B. Android Studio ile Açma (GUI + Emülatör)

Komut satırından proje yolu vererek Android Studio'yu başlat:

```bash
# Arka planda başlat (hemen döner, Gradle Sync arka planda çalışır)
"C:/Program Files/Android/Android Studio/bin/studio64.exe" "C:\Users\marko\Desktop\<proje_adi>" &

# Bekle — Gradle Sync + emülatör bağlantısı zaman alır (~30-90 sn)
# ADB'den emülatörü görünce APK'yı yükle
```

**Gradle Sync bekleme:**
- `"Importing '...' Gradle Project"` alt status bar'da görünür
- `"Gradle Build Running"` status bar'da görünür
- Sync tamamlanana kadar Run butonu pasiftir (gri)
- Sync bittiğinde emülatör otomatik bağlanır (`localhost:XXXXX device` ADB'de)

**Klavye kısayolu ile çalıştırma (tercih edilen):**
1. Pencereye tıkla/aktif et
2. `Shift+F10` = Run / Çalıştır
3. İzin dialog'larından geç (mikrofon, depolama vb.)

#### Emülatör / AVD:
- Eğer AVD yoksa: `sdkmanager.bat "system-images;android-35;google_apis;x86_64"` (büyük dosya, ~1.5GB, indirme sırasında timeout olabilir → `--no_https` veya arka planda çalıştır)
- Veya Android Studio içinden "Device Manager" ile oluştur
- Mevcut emülatörü CLI'den başlat: `emulator.exe -avd <avd_adi>`
- **Pitfall:** `avdmanager create avd` SDK XML v4 uyarısı + "Package path is not valid" hatası verebilir. Çözüm: sdkmanager ile indirildikten sonra bile `.installer` dosyası kalmışsa sil ve yeniden indir, veya Android Studio'dan AVD oluştur.

#### Emülatör Bağlantısı Kesildi/Kayboldu:
Emülatör process'i kapandıysa (tasklist'te yok, `adb devices` boş):
1. AVD var mı kontrol et: `ls ~/.android/avd/`
2. Yoksa → Android Studio'dan veya `avdmanager` ile yeniden oluştur
3. `emulator.exe -avd <adi>` ile başlat
4. ADB'den görünene kadar bekle
5. Sonra `adb install` ve test devam

### C. Fiziksel Cihaz

```bash
# USB hata ayıklama açık cihazı bağla
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe devices

# APK yükle (aynı komut)
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe install "C:\\Users\\marko\\Desktop\\LiveTranscriber.apk"
```

**Önemli not:** Eğer `adb.exe devices` emülatörü `localhost:XXXXX` olarak göstermişse (TCP/IP üzerinden), `adb install` doğrudan çalışır. Rapor formatı: "APK başarıyla yüklendi → uygulama açıldı → ekran görüntüsü alındı".

### D. Telegram ile APK Gönderme (Fiziksel Cihaza Kurulum İçin)

Kullanıcı APK'yı fiziksel telefonuna kurmak istediğinde doğrudan Telegram Bot API ile gönder:

```python
import re, requests

# .env'den token oku (Python ile, shell quoting sorunlarını atla)
with open(r'C:\Users\marko\AppData\Local\hermes\.env') as f:
    content = f.read()
match = re.search(r'^TELEGRAM_BOT_TOKEN=*** content, re.MULTILINE)
token = match.group(1).strip()
chat_id = "6328823909"  # kullanıcının chat_id'si

# APK'yı doküman olarak gönder
with open(apk_path, 'rb') as f:
    files = {'document': ('UygulamaAdi.apk', f, 'application/vnd.android.package-archive')}
    data = {'chat_id': chat_id, 'caption': 'APK açıklaması'}
    resp = requests.post(f'https://api.telegram.org/bot{token}/sendDocument', files=files, data=data, timeout=30)

print(f"Status: {resp.status_code}")
```

**Önemli:** Chat ID = `TELEGRAM_HOME_CHANNEL` (.env'de). Bu ID genellikle `6328823909` formatındadır. Dosyayı `/c/Users/marko/Desktop/` altına da kopyala ki bilgisayarda da bulunsun.

## Release APK Build (Samsung / One UI / Android 16+)

Samsung One UI 8+ (Android 16+) cihazlarda debug APK'ler **Auto Blocker** tarafından engellenir. Çözüm: release imzalı APK oluştur.

### 1. Keystore Oluştur

```bash
"<java_jdk_yolu>/bin/keytool" -genkey -v \
  -keystore "<proje>/release.keystore" \
  -alias <app_alias> \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass <sifre> -keypass <sifre> \
  -dname "CN=Hermes, OU=Dev, O=Hermes, L=Unknown, ST=Unknown, C=TR"
```

JDK yolunu `which keytool` ile bul. Örn: `C:\Program Files\Microsoft\jdk-21.0.11.10-hotspot\bin\keytool`

### 2. build.gradle.kts'e SigningConfig Ekle

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("../release.keystore")
            storePassword = "<sifre>"
            keyAlias = "<alias>"
            keyPassword = "<sifre>"
        }
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

**Pitfall:** `signingConfigs` bloğu `buildTypes` bloğundan ÖNCE tanımlanmalı.

### 3. Release APK Derle

```bash
cd <proje>
export ANDROID_HOME="/c/Users/<user>/AppData/Local/Android/Sdk"
./gradlew assembleRelease --no-daemon
```

### 4. APK Çıktısı

`app/build/outputs/apk/release/app-release.apk` (~4.7 MB, debug'dan küçük)
Desktop'a: `cp app/build/outputs/apk/release/app-release.apk /c/Users/<user>/Desktop/Uygulama-Release.apk`

### 5. Samsung One UI Özel Ayarları

Kullanıcıya şu adımları ilet (Telegram üzerinden):

1. **Ayarlar > Güvenlik > Auto Blocker > KAPAT** (en önemlisi)
2. **Ayarlar > Biyometri ve güvenlik > Bilinmeyen uygulamalar > Telegram > İzin ver**
3. Alternatif: **Ayarlar > Uygulamalar > Telegram > Özel izinler > Bilinmeyen uygulamaları yükle > İzin ver**

Release APK bu ayarlarla sorunsuz kurulur.

## Debug APK Kurulum Sorun Giderme

Debug APK (debug imzalı) fiziksel telefona yüklenemiyorsa:

### Yaygın Sebepler

| Sorun | Çözüm |
|-------|-------|
| **Bilinmeyen kaynaklar kapalı** | Ayarlar > Güvenlik > Bilinmeyen uygulamalar > AÇIK |
| **Geliştirici seçenekleri kapalı** | Ayarlar > Telefon hakkında > Derleme numarasına 7 kere tıkla → Geliştirici seçenekleri > USB hata ayıklama + USB üzerinden kurulum AÇIK |
| **Telegram'dan bozuk indi** | Telegram bot'tan APK'yı sil, tekrar gönder, yeniden indir |
| **Aynı paket adıyla başka uygulama var** | Eski sürümü kaldır (varsa) |
| **Samsung Auto Blocker (One UI 8+)** | Ayarlar > Güvenlik > Auto Blocker > KAPAT. Debug APK'yi direkt engeller. Release imzalı APK yap veya Auto Blocker'ı kapat. |
| **Android 16 sideload kısıtlaması** | Bilinmeyen kaynaklar iznini Telegram/My Files uygulamasına özel olarak ver. Ayarlar > Uygulamalar > [Uygulama] > Bilinmeyen uygulamaları yükle > İzin ver. |
| **APK bozuk** | `aapt2 dump badging app.apk` ile doğrula — çıktıda `package:` ve `minSdkVersion:` satırları görünmeli |

### Doğrulama

```bash
# APK'nın geçerli olduğunu kontrol et
/path/to/build-tools/35.0.1/aapt2 dump badging "C:\\Users\\marko\\Desktop\\Uygulama.apk" | grep -E "^package:|minSdkVersion:|targetSdkVersion:|native-code:"
```

- `native-code:` satırı yoksa → APK saf Java/Kotlin, tüm mimarilerde çalışır
- `native-code: armeabi-v7a` gibi bir satır varsa → sadece ARM cihazlarda çalışır
- Debug APK'ler Play Store'dan değil, manuel kurulum içindir — bu normaldir

## Referanslar
- `references/livetranscriber-example.md` — LiveTranscriber projesinin tam yapısı ve build detayları (gerçek örnek)
- `references/livetranscriber-save-archive-pattern.md` — Süresiz kayıt + transkriptleri TXT arşive kaydetme deseni
