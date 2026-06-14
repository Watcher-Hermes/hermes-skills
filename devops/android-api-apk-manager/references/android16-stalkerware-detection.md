# Android 16 (May 2026) — FOREGROUND_SERVICE + Mikrofon Stalkerware Detection

## Keşif Kaynağı
Claude Opus 4.8 tarafından analiz edildi (11.06.2026).
Samsung One UI 8 / Android 16 / Mayıs 2026 güvenlik yaması.

## Sorun
Android 16 (Mayıs 2026 güvenlik yaması) ile birlikte Google, FOREGROUND_SERVICE ve RECORD_AUDIO/MIKROFON izinlerini birlikte kullanan uygulamaları **yükleme zamanında stalkerware (takip yazılımı) olarak sınıflandırmaya** başladı. Bu, Play Protect'ten ve Samsung Auto Blocker'dan **bağımsız** bir Android çekirdek katmanıdır.

## Belirtiler
- APK, UI üzerinden (Dosyalar uygulaması / Telegram indirme) yüklenmeye çalışınca engellenir
- Google Play Protect: "Uygulama, cihazınızı korumak için engellendi"
- Samsung Auto Blocker KAPALI olsa bile engellenir
- Play Protect KAPALI olsa bile engellenir
- Hata: "Uygulama yüklenmedi" (başka detay yok)
- ADB ile yükleme ÇALIŞIR (direkt sistem seviyesinde yazar, UI installer'ı bypass eder)

## Etkilenen İzin Kombinasyonu
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE" />
```

## Çözümler (öncelik sırasına göre)

### 1. ADB Sideload (EN GARANTİ)
Direkt sisteme yazar, UI installer katmanını bypass eder:
```bash
"***REMOVED-BASE64***-tools/adb.exe" install "path/to/app-release.apk"
```

### 2. Google Play Store'a Yükleme
Google imzalı + Play Store dağıtımı = güven zinciri. Stalkerware detection'i otomatik geçer.
Maliyet: $25 (bir kereye mahsus geliştirici kaydı) + inceleme süresi.

### 3. targetSdkVersion Düşürme (Riskli)
targetSdkVersion'ı 34'e (Android 14) düşürmek eski kuralları çalıştırabilir ancak:
- Android 16'da düşük targetSdk olan APK'lar da ek uyarılar alabilir
- Geçici çözüm, uzun vadede önerilmez

### 4. Manifest'ten FOREGROUND_SERVICE_MICROPHONE Kaldırma
Android 14+ (API 34) için FOREGROUND_SERVICE_MICROPHONE tipi zorunlu değildir.
Kaldırılırsa uygulama yine çalışır ancak Android 16 yine de RECORD_AUDIO + FOREGROUND_SERVICE kombinasyonunu algılayabilir.

## Önemli Not
Bu detection katmanı Android 16 çekirdeğine gömülüdür. Kök erişimi olmayan bir cihazda kaldırılamaz veya devre dışı bırakılamaz. Tek kalıcı çözüm: ADB ile yükleme veya Play Store dağıtımı.
