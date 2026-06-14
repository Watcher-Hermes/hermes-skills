# Package Rename Bypass — Sistem Uygulaması Modding

## Ne Zaman Kullanılır

Sistem uygulaması (Google/Samsung ön yüklü) olduğu için `INSTALL_FAILED_UPDATE_INCOMPATIBLE` alındığında. Android 16+ One UI 8'de root'suz tek çözüm: **aynı uygulamayı farklı paket adıyla sideload olarak yükle.**

## Gerçek Vaka: Live Transcribe (Google Scribe)

| Özellik | Değer |
|---------|-------|
| Paket | `com.google.audio.hearing.visualization.accessibility.scribe` |
| Sürüm | 8.7.880674799 (targetSdk 36) |
| Obfuscation | R8 full (sınıflar a/b/c .smali) |
| Cihaz | Samsung S22 Ultra (SM-S908E), One UI 8, Android 16 |
| Hedef | Ekran kapalıyken transkripsiyon devam etsin (onPause boşaltma) |

## Adım Adım Uygulama

### 1. APK Çekme

```bash
# Split APK paths
adb shell pm path com.google.audio.hearing.visualization.accessibility.scribe
# Çıktı: base.apk + split_config.arm64_v8a.apk
adb pull <path>/base.apk .
adb pull <path>/split_config.arm64_v8a.apk .
```

### 2. Split → Monolithic Merge

Split native lib'ler base'e merge edilir (ZIP_STORED zorunlu):

```python
import zipfile
# split native lib'leri al
with zipfile.ZipFile("split.apk") as z:
    libs = {n: z.read(n) for n in z.namelist() if n.startswith("lib/")}
# base'i oku (META-INF + lib hariç)
with zipfile.ZipFile("base.apk") as z:
    base = {n: (i, z.read(n)) for n, i in [(f, z.getinfo(f)) for f in z.namelist()]
            if not f.startswith("META-INF/") and not f.startswith("lib/")}
# merge yaz
with zipfile.ZipFile("merged.apk", "w", ZIP_DEFLATED) as zout:
    for n, (i, d) in base.items(): zout.writestr(i, d)
    for n, d in libs.items():
        zi = ZipInfo(n); zi.external_attr = 0o644 << 16
        zout.writestr(zi, d, ZIP_STORED)
```

### 3. Decompile

```bash
apktool d -f -o _work/ merged.apk
```

### 4. apktool.yml

```yaml
packageInfo:
  forcedPackageId: 127
  renameManifestPackage: com.yeni.paket.adi  # <-- BURAYI AYARLA
```

### 5. Smali + Resource + Manifest Kitlesel Paket Değiştirme

```python
import os, glob

OLD = "***REMOVED-BASE64***"
NEW = "***REMOVED-BASE64***"
OLD_DOT = OLD.replace("/", ".")
NEW_DOT = NEW.replace("/", ".")

# 1) Smali dosyaları (9104 dosya içinden ~117'si eski paketi içerir)
for root, dirs, files in os.walk("_work/smali"):
    for f in files:
        if not f.endswith(".smali"): continue
        path = os.path.join(root, f)
        with open(path, "rb") as fh:
            data = fh.read()
        if OLD.encode() not in data and OLD_DOT.encode() not in data:
            continue
        text = data.decode("utf-8")
        text = text.replace(f"L{OLD};", f"L{NEW};")     # class ref
        text = text.replace(f"L{OLD}->", f"L{NEW}->")   # method ref
        text = text.replace(OLD_DOT, NEW_DOT)            # string ref
        with open(path, "wb") as fh:
            fh.write(text.encode("utf-8"))

# 2) Manifest dosyası (decoded XML)
with open("_work/AndroidManifest.xml") as f:
    manifest = f.read()
manifest = manifest.replace(OLD_DOT, NEW_DOT)
with open("_work/AndroidManifest.xml", "w") as f:
    f.write(manifest)

# 3) Layout/XML dosyaları (custom view sınıf isimleri)
for f in glob.glob("_work/res/**/*.xml", recursive=True):
    with open(f, "rb") as fh:
        data = fh.read()
    if OLD_DOT.encode() not in data: continue
    text = data.decode("utf-8")
    text = text.replace(OLD_DOT, NEW_DOT)
    with open(f, "wb") as fh:
        fh.write(text.encode("utf-8"))
```

**UYARI:** os.walk Windows'da `\\` kullanır. Eğer Python script'inde path.replace yapıyorsan `/` vs `\\` uyumuna dikkat et. Path string'lerinde `OLD in root` kontrolü Windows'ta her zaman False çünkü `root` `\\` ile `OLD` `/` ile.

### 6. Manifest Temizliği (Split Referansları)

```
<manifest tag'inden kaldır:
  android:requiredSplitTypes="base__abi"
  android:splitTypes=""

meta-data'dan kaldır:
  com.android.vending.splits.required
  com.android.vending.splits
```

### 7. onPause Boşaltma

```python
# MainActivity.smali'de onPause metoduna git
# invoke-super dışındaki tüm satırları sil
# .locals 0 yap
# sadece invoke-super + return-void bırak
```

### 9. (ÖNEMLİ) LauncherActivity Aktifleştir

Sistem uygulamalarında LauncherActivity alias genelde `android:enabled="false"` — sideload'da uygulama menüde görünmez:

```xml
<!-- manifest'te bul: -->
<activity-alias android:enabled="false" ... android:name="com.yeni.paket.LauncherActivity">
<!-- değiştir: -->
<activity-alias android:enabled="true" ...>
```

### 10. Rebuild + İmzala + Yükle

```bash
apktool b -o unsigned.apk _work/
zipalign -f -p 4 unsigned.apk signed.apk
apksigner sign --ks release.keystore --ks-key-alias alias \
  --ks-pass pass:sifre --key-pass pass:sifre signed.apk
adb install signed.apk
```

## Yaşanan Hatalar ve Çözümleri

### HATA 1: INSTALL_FAILED_DUPLICATE_PERMISSION
**Sebep:** `<permission android:name="com.ESKI.paket.PERMISSION_NAME"/>` manifest'te eski paket adıyla kalmış.
**Çözüm:** Manifest'teki tüm `com.ESKI.paket` string'lerini `com.YENI.paket` ile değiştir.

### HATA 2: INSTALL_FAILED_CONFLICTING_PROVIDER
**Sebep:** `<provider android:authorities="com.ESKI.paket.fileprovider"/>` eski provider authority.
**Çözüm:** Provider authority'leri de yeni paket adına çevir.

### HATA 3: ClassNotFoundException — ScribeApplication
**Sebep:** Manifest'te `android:name="com.YENI.paket.ScribeApplication"` yazıyor ama DEX içinde sınıf hala `Lcom/ESKI/paket/ScribeApplication;`.
**Çözüm:** Smali'deki class declaration ve referanslar da değişmeli.

### HATA 4: ClassNotFoundException — MicrophoneListPreference (runtime `Class.forName()`)
**Sebep:** `Class.forName("com.ESKI.paket.ui.settings.MicrophoneListPreference")` çağrısı — runtime string.
**Çözüm:** Tüm smali dosyalarında DOT format (`com.ESKI.paket`) replacement de yap. Slaş format (`Lcom/ESKI/paket/Class;`) yetmez.

### HATA 5: apktool "Renamed manifest package found" — binary rename revert
**Sebep:** Binary-level UTF-16LE rename yapılmış APK'yı apktool tanır ve eski paket adına döndürür.
**Çözüm:** apktool.yml'de `renameManifestPackage` kullan + decoded XML/Smali'de elle değiştir. Binary rename'i apktool'dan ÖNCE değil, apktool SONRASI decoding'de yap.

## Keystore

- **Dosya:** `C:\Users\marko\Desktop\LiveTranscriber\release.keystore`
- **Alias:** `livetranscriber`
- **Şifre:** `hermes123`

## Notlar

- Google paket isimleri (`com.google.*`, `com.android.*`) Samsung One UI 8'de sistem seviyesinde bloklu olabilir.
- Yeni paket adında `google` veya `android` geçmemeli.
- Orijinal uygulama ve renamed uygulama yan yana çalışır (farklı paket, farklı imza).
- `appops set com.yeni.paket RECORD_AUDIO allow` — arka plan ses izni için (onPause yaması ile birlikte kullanılmalı).
- **LauncherActivity fix:** Sistem uygulamalarında launcher alias `android:enabled="false"` olur. Sideload'da görünmez — elle `enabled="true"` yap.
- **Binary protobuf güvenli:** Aynı uzunluktaki string replacement protobuf .pb dosyalarını bozmaz (length-prefixed string, byte sayısı aynı).
- **Windows path separator:** `os.walk` Windows'ta `\\` döndürür, `OLD_SLASH` `/` ile eşleşmez. Directory rename yapma, sadece content replacement yap.
