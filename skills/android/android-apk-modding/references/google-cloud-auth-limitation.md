# Google Apps Cloud Auth Limitation (Package Rename + Custom Signature)

## Problem

Google uygulamaları (`com.google.*`) modlanıp custom keystore ile imzalandığında, Google sunucu tarafı hizmetleri (gRPC, Firebase, Cloud Speech API) çalışmaz. Sunucu, APK imzasını doğrular ve custom imzayı reddeder.

## Gözlenen Hatalar

### Live Transcribe (8.7.880674799)

**Belirti:** APK patchname rename ile başarıyla yüklendi, açıldı, crash yok, mikrofon çalışıyor, ses seviyesi UI'da görünüyor — ama transkripsiyon metne dönüşmüyor.

**Logcat hataları:**
```
TranscriptionResultRece: io.grpc.StatusRuntimeException: INVALID_ARGUMENT:
  Application credential header not valid. Please fix the client to pass a valid application credential header.

RepeatingRecognitionSes: Closing Session #141 due to non-network error.

FA: Failed to retrieve Firebase Instance Id
```

**Akış:**
1. Kullanıcı konuşur → mikrofon ses alır
2. App sesi Google Cloud Speech API'ye (gRPC) gönderir
3. Google sunucusu `application credential header`'ı kontrol eder
4. Custom imza → red → transcription session kapanır
5. Kullanıcı metin görmez, "kapandı" der

### Firebase Services

```
Failed to retrieve Firebase Instance Id
```

Firebase Instance ID alınamaz. Bu, Firebase Cloud Messaging, Firebase Auth ve Firebase Analytics'in çalışmayacağı anlamına gelir.

## Etkilenen Google Hizmetleri

| Hizmet | Etki | Örnek |
|--------|------|-------|
| Cloud Speech-to-Text | ❌ Tamamen çalışmaz | Live Transcribe, Voice Access |
| Firebase Instance ID | ❌ Alınamaz | Bildirimler, analytics |
| Firebase Auth | ❌ Giriş yapılamaz | Google hesabı gereken özellikler |
| Google Sign-In | ❌ Oturum açılamaz | Hesap bağlantısı |
| Firebase Remote Config | ❌ Yapılandırma alınamaz | A/B testleri, feature flag'ler |
| Play Integrity | ❌ Sertifika doğrulaması | Lisans/lisanssızlık kontrolleri |
| ML Kit (cloud) | ❌ Cloud modeller | Online text recognition |

## Neden

Google'ın Android uygulamaları `com.google.android.gms` (Google Play Services) üzerinden sunuculara bağlanır. GPS, bağlanan uygulamanın imza sertifikasını alır ve Google'ın sunucularına iletir. Sunucu, sertifikayı Google'ın imza veritabanıyla karşılaştırır.

- **Orijinal imza** = Google'ın sertifikası → sunucu "bu gerçek Google uygulaması" der → kabul
- **Custom imza** = Bizim keystore → sunucu "bu sahte" der → red

Bu kontroller atlatılamaz çünkü tamamen Google'ın kontrolündeki sunucularda gerçekleşir. APK seviyesinde yapılabilecek hiçbir değişiklik sunucu tarafındaki imza doğrulamasını etkilemez.

## Çalışan Alternatifler (Zorluk Sırasıyla)

| Yöntem | Root? | Açıklama |
|--------|-------|----------|
| **Root + Frida** | Evet | System app'e Frida hook, onPause'u runtime'da boşalt. Orijinal imza korunur. |
| **Root + System分区** | Evet | /system/app altındaki APK'yı değiştir. Orijinal imza? Hayır — şifrelenmiş bölüm. |
| **Root + Xposed/LSPosed** | Evet | Module ile lifecycle metodlarına müdahale. |
| **Magisk Module** | Evet | Systemless modül, sistem bölümüne yazmaz. |

Root'suz çözüm yoktur.

## Frida Non-Root Notları

Android 16 + One UI 8'de root'suz cihazda Frida:

```
# Attach
frida -U -n com.google... → "unable to access process with pid X"
  → Sebep: App debuggable değil, Frida server yetkisi yok

# Spawn
frida -U -f com.google... → "InvocationTargetException"
  → Sebep: System app spawn edilemez, Frida server shell kullanıcısı
```

Sadece **debuggable** uygulamalara (geliştirici tarafından `android:debuggable=true` ile imzalanmış) Frida root'suz bağlanabilir. Sistem uygulamaları `ro.debuggable=0` ile korunur.

## Doğrulama

```bash
# Telefon root'lu mu?
adb shell "su -c id"
# Çıktı: "uid=0(root)" → root var
# Çıktı: "su: inaccessible or not found" → root yok

# Uygulama debuggable mı?
adb shell "dumpsys package com.google... | grep -i debug"
# Çıktı varsa → debuggable
# Çıktı yoksa → non-debuggable

# Sistem debuggable mı?
adb shell "getprop ro.debuggable"
# 1 → evet, 0 → hayır
```
