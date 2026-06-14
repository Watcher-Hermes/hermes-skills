# Live Transcribe Package Rename Oturumu (2026-06-13)

## Hedef

Live Transcribe (Google, sistem uygulaması) — ekran kapalıyken transkripsiyonun devam etmesi. onPause metodunu boşalt.

## Engeller

- **Sistem uygulaması:** Android 16 + One UI 8'de `INSTALL_FAILED_UPDATE_INCOMPATIBLE` — root'suz yama yüklenemez
- **Split APK:** base.apk + split_config.arm64_v8a.apk
- **R8 obfuscation:** Tüm sınıflar tek harf (a.smali, b.smali...)
- **Google cloud auth:** Custom keystore → Google sunucuları reddeder

## Çözülen Hatalar (Crash Cycle)

### Hata 1: `renameManifestPackage` yetersiz kaldı
apktool'un `renameManifestPackage` sadece manifest'te `package=` tag'ını değiştirir. Smali class referansları (`Lcom/google/...;`) ve layout XML'ler (`<com.google...CustomView>`) değişmez.
**Çözüm:** Tüm smali + res XML'lerde grep+sed ile eski→yeni paket adı değiştir.

### Hata 2: Windows path separator (os.walk)
```python
ORIG_SLASH = "com/google/audio/..."  # forward slash
# root = "C:\\...\\smali\\com\\google\\audio\\..."  # Windows backslash
# → ORIG_SLASH in root = FALSE
```
**Çözüm:** Python `os.walk` + string comparison yerine `grep -rl` + `sed` kullan. Grep içerik taraması yapar, path formatından etkilenmez.

### Hata 3: `ClassNotFoundException: com.yeni.paket.ScribeApplication`
Smali'de `.class` declaration ve string referansları değiştirildi ama manifest hala yeni paketi gösteriyordu. Asıl sorun: smali dizin yapısı eski kalmıştı (adım 2'de path separator sorunu).
**Çözüm:** Apktool'un kendi rename mekanizmasına güvenme. Smali + manifest + res XML → hepsinde find-and-replace yap.

### Hata 4: `INSTALL_FAILED_DUPLICATE_PERMISSION`
`<permission android:name="com.ESKI.paket.DYNAMIC_RECEIVER_..." />` hala eski paket adını içeriyordu.
**Çözüm:** AndroidManifest.xml'de `<permission>` ve `<uses-permission>` string'lerini de yeni paket adıyla değiştir.

### Hata 5: `INSTALL_FAILED_CONFLICTING_PROVIDER`
`<provider android:authorities="com.ESKI.paket.fileprovider" />` eski kalmıştı.
**Çözüm:** Tüm `<provider android:authorities>` string'lerini de yeni paket adına çevir.

### Hata 6: LauncherActivity görünmez
`<activity-alias android:enabled="false" ... LauncherActivity>` — sistem uygulamalarında varsayılan olarak kapalı. Sideload'da da kapalı kalır, uygulama ikonu menüde görünmez.
**Çözüm:** `android:enabled="false"` → `android:enabled="true"` yap.

### Hata 7: Google cloud auth (çözülemez)
```
TranscriptionResultRece: INVALID_ARGUMENT: Application credential header not valid
```
Custom imza → Google sunucuları reddeder. Çözümü yok.

## Doğru Workflow

```
1. Split merge (base + native libs, ZIP_STORED)
2. apktool d -f -o _work/ merged.apk
3. apktool.yml → renameManifestPackage: com.yeni.paket
4. sed -i 's|com/eski/yol|com/yeni/yol|g' smali/**/*.smali smali_classes2/**/*.smali
5. sed -i 's|com\.eski\.paket|com.yeni.paket|g' res/**/*.xml
6. sed -i 's|com\.eski\.paket|com.yeni.paket|g' AndroidManifest.xml
7. sed -i 's|android:enabled="false"|android:enabled="true"|' AndroidManifest.xml (LauncherActivity)
8. Split referanslarını temizle (requiredSplitTypes, vending.splits vb.)
9. onPause boşalt (MainActivity.smali)
10. apktool b → zipalign → apksigner
11. adb install
```

## Samsung Güvenlik Devre Dışı (ADB)

```bash
adb shell settings put global package_verifier_enable 0
adb shell settings put global verifier_verify_adb_installs 0
adb shell settings put global auto_blocker_enabled 0
adb shell settings put secure auto_blocker_enabled 0
```
