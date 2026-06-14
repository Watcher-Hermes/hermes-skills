# Samsung Galaxy S22 Ultra — One UI 8 / Android 16 Sideload Fix

## Cihaz
- Model: Samsung Galaxy S22 Ultra (S908E)
- One UI: 8.0
- Android: 16
- Güvenlik yaması: 5 Mayıs 2026

## APK
- Adı: Canlı Transkript (LiveTranscriber-Release.apk)
- Paket: com.livetranscriber
- Version: 1.0 (versionCode=1)
- compileSdkVersion: 35 (Android 15)
- targetSdkVersion: 35
- minSdkVersion: 26 (Android 8.0)
- İzinler: RECORD_AUDIO, INTERNET, FOREGROUND_SERVICE, FOREGROUND_SERVICE_MICROPHONE, POST_NOTIFICATIONS
- MainActivity: com.livetranscriber.MainActivity
- İmza: RELEASE

## Sorun
APK yüklenemiyor:
1. Google Play Protect "Uygulama, cihazınızı korumak için engellendi" diyor
2. "Anladım" butonuna basınca "Uygulama yüklenmedi" hatası geliyor
3. Auto Blocker kapatıldı, telefon yeniden başlatıldı — yine olmuyor

## Sebep (3 katmanlı blok)
1. **Google Play Protect** — bilinmeyen geliştirici (ilk kez görülen imza)
2. **Samsung Knox / Auto Blocker** — One UI 8.0 ek güvenlik katmanı
3. **Android 16 Stalkerware Detection** — FOREGROUND_SERVICE + RECORD_AUDIO kombinasyonu yükleme zamanında tespit edilip engellenir, Play Protect ve Auto Blocker'dan bağımsız bir Android çekirdek katmanıdır. Detay: `references/android16-stalkerware-detection.md`

## Çözüm: ADB ile yükleme (tek çalışan yol)

```bash
# Telefonu USB ile bağla, USB Hata Ayıklama açık olmalı
"***REMOVED-BASE64***-tools/adb.exe" devices

# APK'yı yükle
"***REMOVED-BASE64***-tools/adb.exe" install "C:\Users\marko\Desktop\LiveTranscriber-Release.apk"
```

ADB direkt sisteme yazar, Play Protect ve Knox'u bypass eder.

## Emülatör Testi
APK Android 15 emülatörde (API 35) sorunsuz çalıştı.
Android 16 uyumluluk sorunu tespit edilmedi.

## Güncelleme (12 Haziran 2026) — Live Transcribe Modding Denemeleri

Live Transcribe (Google, paket: `com.google.audio.hearing.visualization.accessibility.scribe`) modding:

| Denenen Yöntem | Sonuç |
|----------------|--------|
| apktool decompile → modify → rebuild → sign | "Paket geçersiz" (binary XML corruption) |
| Python binary merge (base + native libs) | "Uygulama yüklenmedi" |
| Python merge + splits0.xml temizliği | "Uygulama yüklenmedi" |
| Binary-level package rename (hex patch) | "Uygulama yüklenmedi" |
| Pure unmodified merge (base + libs only) | "Uygulama yüklenmedi" |

**Ana bulgu:** Üçüncü taraf imzalı herhangi bir APK (Google dışı imza), RECORD_AUDIO + FOREGROUND_SERVICE içeriyorsa, Samsung One UI 8 / Android 16'da UI üzerinden **kesinlikle kurulamaz**. Kullanıcı Auto Blocker'ı kapattı, Play Protect'i kapattı, orijinal uygulamayı kaldırdı — hepsi boşuna. Android 16 çekirdek katmanındaki stalkerware detection bypass edilemez.

**Çalışan yollar:**
1. **ADB sideload** (`adb install`) — direkt sistem seviyesinde yazar
2. **Play Store dağıtımı** — Google imza zinciri
3. **Telefonda MT Manager ile mod** — orijinal uygulama kurulu, telefonda düzenlenir (kullanıcı önerisi)
