# Root'suz Android Runtime Müdahale Yöntemleri

Araştırma tarihi: 2026-06-12
Kaynak: Tor + DuckDuckGo, Japon/Kore/Çin/İngilizce siteler

## Yöntem Karşılaştırması

| Yöntem | APK Repackage? | Root? | Method Hook? | Sistem Uyg.? | Durum |
|--------|---------------|-------|-------------|-------------|-------|
| appops set | Hayır | Hayır | Hayır (izin) | Evet | Çalışır |
| Shizuku | Hayır | Hayır | Hayır | Evet (ADB) | Sadece API |
| LSPatch | Evet | Hayır | Evet (Xposed) | Hayır | Repackage gerekli |
| Frida Gadget | Evet | Hayır | Evet | Hayır | Repackage gerekli |
| Frida Server | Hayır | Evet | Evet | Evet | Root gerekli |
| jadx + recompile | Evet | Hayır | Hayır | Hayır | Repackage gerekli |

## Detaylı Yöntemler

### 1. appops — SDK İzin Değiştirme (ÖNCELİKLİ)

ADB ile uygulamanın SDK seviyesindeki izinlerini değiştirir.
APK modding gerektirmez, her telefonda çalışır.

```bash
adb shell "appops set com.package RECORD_AUDIO allow"
adb shell "appops get com.package"
```

**Sınırlama:** Uygulamanın kod davranışını değiştiremez, sadece SDK izinlerini.
onPause'da kaydı durduran kod varsa appops bunu engelleyemez.

**Kaynak:** Android SDK built-in (Android 4.3+)

### 2. Shizuku (Kore kaynaklarından)

ADB veya root aracılığıyla sistem API'lerine doğrudan erişim sağlar.
Play Store'da mevcut. Sistem uygulamalarını yönetebilir ama metod hook'layamaz.

**Kaynak:** https://shizuku.rikka.app/

### 3. LSPatch (Root'suz Xposed)

APK içine dex+.so enjekte eder. Xposed API'sini çalıştırarak herhangi bir metodu hook'layabilir.
Sınırlama: APK yeniden imzalanır -> sistem uygulaması imza korumasına takılır.

**Kaynak:** https://github.com/LSPosed/LSPatch

### 4. Frida Gadget

APK'ya libfrida-gadget.so enjekte ederek runtime hook.
Sınırlama: APK yeniden imzalanır -> sistem uygulaması imza korumasına takılır.

**Kaynak:** https://frida.re/docs/gadget/

## Android 16+ (One UI 8) Değişiklikleri

- adb uninstall --user 0 sonrası bile imza kaydı sistemde kalır
- INSTALL_FAILED_UPDATE_INCOMPATIBLE reboot sonrası da devam eder
- Sistem uygulamalarına yama yapmak root gerektirir
- Auto Blocker üçüncü parti APK kurulumlarını engeller
