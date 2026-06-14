# LiveTranscriber — Referans Proje

## Proje Bilgisi
- **Paket:** `com.livetranscriber`
- **Activity:** `MainActivity`
- **minSdk:** 26 (Android 8.0)
- **targetSdk:** 36 (Android 16)
- **AGP:** 8.7.3
- **Gradle:** 8.11.1
- **UI Dili:** Türkçe
- **API:** SpeechRecognizer (Google built-in, harici API anahtarı yok)

## Proje Yapısı
```
LiveTranscriber/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── local.properties
├── gradle/wrapper/gradle-wrapper.jar
├── gradle/wrapper/gradle-wrapper.properties
├── gradlew / gradlew.bat
└── app/
    ├── build.gradle.kts
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/livetranscriber/MainActivity.java
        └── res/
            ├── layout/activity_main.xml
            └── values/
                ├── strings.xml
                └── themes.xml
```

## MainActivity Özellikleri
- Continuous listening (SpeechRecognizer with `startListening()` in `onResults()` callback)
- Partial results (EXTRA_PARTIAL_RESULTS=true)
- 4 buton: Başlat, Durdur, Temizle, Kopyala
- Runtime permission (RECORD_AUDIO request)
- Turkish UI strings

## Build Komutları
```bash
cd /c/Users/marko/Desktop/LiveTranscriber
export ANDROID_HOME="***REMOVED-BASE64***"
export ANDROID_SDK_ROOT="***REMOVED-BASE64***"
./gradlew assembleDebug --no-daemon
```

## APK Çıktısı
- Debug: `app/build/outputs/apk/debug/app-debug.apk` (~5.5 MB)
- Release: `app/build/outputs/apk/release/app-release.apk` (~4.7 MB)
- Desktop kopyası: `C:\Users\marko\Desktop\LiveTranscriber.apk` (debug) veya `LiveTranscriber-Release.apk`

## Release Build (Samsung One UI 8+ için)
Debug APK Samsung One UI 8'de Auto Blocker tarafından engellenir. Release build gerekli:

```bash
# Keystore oluştur
keytool -genkey -v -keystore release.keystore -alias livetranscriber \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass hermes123 -keypass hermes123 \
  -dname "CN=Hermes, OU=Dev, O=Hermes, L=Unknown, ST=Unknown, C=TR"

# build.gradle.kts'e signingConfigs ekle (bkz. SKILL.md)
# Release build
./gradlew assembleRelease --no-daemon
```

Sonra Telegram'a gönder:
```python
with open('app-release.apk', 'rb') as f:
    requests.post(f'https://api.telegram.org/bot{token}/sendDocument',
        files={'document': ('LiveTranscriber-Release.apk', f, 'application/vnd.android.package-archive')},
        data={'chat_id': '6328823909', 'caption': '🔑 RELEASE imzali APK'})
```

## Obsidian Kaydı
- `C:\Users\marko\OneDrive\Belgeler\Obsidian Vault\Android Uygulamalar\LiveTranscriber.md`

---

## Foreground Service Sürümü (v2)

### Amaç
Activity kapalıyken/arka plandayken transkripsiyona devam etmek.

### Eklenen/Yenilenen Dosyalar
| Dosya | Değişiklik |
|-------|-----------|
| `TranscriptionService.java` | YENİ — Foreground Service + SpeechRecognizer |
| `AndroidManifest.xml` | `foregroundServiceType="microphone"`, `FOREGROUND_SERVICE_MICROPHONE`, `POST_NOTIFICATIONS` |
| `app/build.gradle.kts` | `localbroadcastmanager:1.1.0` bağımlılığı |
| `MainActivity.java` | BroadcastReceiver, Service başlatma/durdurma, ek izin kontrolleri |

### TranscriptionService.java Özeti
- **onStartCommand():** `ACTION_START` → SpeechRecognizer başlat, `ACTION_STOP` → durdur
- **Notification:** Kanal "transcription_channel", intent "OPEN_ACTIVITY" (PendingIntent)
- **Broadcast:** `LocalBroadcastManager` ile Activity'ye status, error, partial, result mesajları
- **SpeechRecognizer Intent:** `EXTRA_PARTIAL_RESULTS=true`, `LANGUAGE_MODEL_FREE_FORM`
- **Sürekli döngü:** `onResults()`'te `startListening()`'i tekrar çağır
- **Hata yönetimi:** `onError()`'da hata koduna göre:
  - `ERROR_NO_MATCH` / `ERROR_SPEECH_TIMEOUT` → sessizce yeniden başlat
  - `ERROR_NETWORK` / `ERROR_SERVER` → kullanıcıya göster + yeniden dene
  - `ERROR_AUDIO` / `ERROR_RECOGNIZER_BUSY` → kullanıcıya göster
- **Gürültü filtresi:** `EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS=2000`, düşük güven skoru filtrele
- **Temizlik:** `onDestroy()` → `speechRecognizer.destroy()`, `notificationManager.cancel()`

### İzinler
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

### Test Sırası (Emülatör)
```bash
# 1. APK yükle
adb install -r app-debug.apk
# 2. Uygulamayı başlat
adb shell am start -n com.livetranscriber/.MainActivity
# 3. İzin dialog'larını geç
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml .
adb shell input tap 720 1590   # "While using the app" (mikrofon)
adb shell input tap 720 1695   # "Allow" (bildirim)
# 4. Servisi doğrula
adb shell dumpsys activity services com.livetranscriber | grep "ServiceRecord"
# 5. Ekran görüntüsü
adb exec-out screencap -p > screen.png
```

### Bilinen Sorun: Emülatörde Mikrofon Yok
- Android emülatöründe varsayılan sanal mikrofon yok
- SpeechRecognizer `ERROR_NO_MATCH` / `ERROR_SPEECH_TIMEOUT` döner
- **Çözüm:** Fiziksel telefona yükle veya emülatöre host ses yönlendirmesi yap

### Samsung One UI 8 / Android 16 Sorunu
- Debug APK Auto Blocker tarafından engellenir ("yüklenemiyor" hatası)
- Kullanıcı ayarları değiştirse bile izin vermez
- **Çözüm:** Release imzalı APK oluştur + kullanıcıya Auto Blocker'ı kapatmasını söyle

### VAD (Voice Activity Detection)
Google SpeechRecognizer'ın dahili VAD'ı ortam seslerini filtreler. Ek gürültü filtresi:
- `MediaRecorder` + RMS hesaplama
- `AudioRecord` + amplitude threshold
- WebRTC VAD (libwebrtc) entegrasyonu

## Emülatörde İzin Dialog Koordinatları (Pixel 10, 1440x3120)
| Dialog | Buton | Merkez |
|--------|-------|--------|
| Mikrofon izni | "While using the app" | 720, 1590 |
| Bildirim izni | "Allow" | 720, 1695 |
| Mikrofon izni | "Only this time" | 720, 1800 |
| Mikrofon izni | "Don't allow" | 720, 2010 |
| Bildirim izni | "Don't allow" | 720, 1905 |
