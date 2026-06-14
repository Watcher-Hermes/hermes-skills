# Sık Karşılaşılan Hatalar ve Çözümleri

APK modding'de en çok rastlanan hatalar, nedenleri ve çözümleri.

---

## 1. apktool Hataları (Decompile/Rebuild Aşaması)

### `brut.androlib.AndrolibException: brut.common.BrutException`

```
Exception in thread "main" brut.androlib.AndrolibException:
  brut.common.BrutException: could not exec command
```

**Sebep:** Java heap yetersiz veya apktool eski.

**Çözüm:**
```bash
export JAVA_OPTS="-Xmx4g"
java -jar apktool.jar b -o cikti.apk _work/
```

### `Resource ID not found: 0x7f0xxxxx`

```
W: Could not find resource ID 0x7f0xxxxx
```

**Sebep:** `res/values/public.xml`'de referansı olmayan bir resource kullanılıyor. Genelde smali'de const ile sabit bir hex ID kullanılmış.

**Çözüm:**
```bash
# public.xml'de hangi ID'ler var kontrol et
grep "0x7f" _work/res/values/public.xml | head -20

# O ID'nin karşılığını bul
grep "0x7f080689" _work/res/values/public.xml
# Çıktı: <public type="drawable" name="ic_launcher" id="0x7f080689" />
```

Smali'de elle yazdığın ID, public.xml'de tanımlı olmalı.

### `Resource entry X is already defined`

```
ERROR: Resource entry colors is already defined.
```

**Sebep:** `res/values/` altında aynı resource type için birden çok dosyada çakışan tanım.

**Çözüm:** Çakışan tanımı bul ve kaldır:
```bash
grep -r "name=\"colors\"" _work/res/values/
```

### `Could not decode arsc file`

```
Exception: Could not decode arsc file
```

**Sebep:** APK'nın resource tablosu (resources.arsc) apktool'un anlayamadığı bir formatta. Genelde çok yeni/özelleştirilmiş APK'lerde olur.

**Çözüm:**
```bash
# Resource'suz decompile dene (binary manifest korunur)
java -jar apktool.jar d -r -f -o _work/ target.apk
```

Bu yöntemle manifest düzenlenebilir ama res/ altına dokunulamaz.

---

## 2. zipalign Hataları

### `Input file not a valid zip file`

```
zipalign: input file not a valid zip file
```

**Sebep:** APK bozuk veya rebuild sırasında yazma hatası oldu.

**Çözüm:** Yeniden rebuild et. Hala olmuyorsa:
```bash
file _build_unsigned.apk   # "Zip archive" görmelisin
unzip -t _build_unsigned.apk  # test et
```

### `Verification FAILED`

```
Verification FAILED
```

**Sebep:** APK içinde 4-byte hizalanmamış dosya var (genelde .so).

**Çözüm:** `-f` flag'i ile tekrar dene:
```bash
zipalign -f -p 4 _build_unsigned.apk _build_aligned.apk
```

Hala başarısızsa, Python ile ZIP_STORED yöntemini kullan.

---

## 3. İmzalama Hataları

### `ERROR: JAR signer: CERT.RSA entry is not a pre-existing signature`

```
ERROR: JAR signer: CERT.RSA entry is not a pre-existing signature
```

**Sebep:** APK zaten imzalı. apksigner çifte imzalamaya çalışıyor.

**Çözüm:** META-INF klasörünü rebuild'den önce temizle:
```bash
rm -rf _work/META-INF/
# sonra rebuild et
```

### `Failed to sign: Signing is not supported for this file`

```
Failed to sign: Signing is not supported for this file
```

**Sebep:** APK dosyası hizalanmamış veya bozuk.

**Çözüm:** Önce zipalign'i çalıştır, sonra imzala. Sıra: rebuild → zipalign → apksigner.

### `W/ziparchive: Unable to open ...'

```
W/ziparchive: Unable to open '/data/app/.../base.apk': No such file or directory
```

**Sebep:** Çok nadir — Android'in APK'yı `/data/app/` altına kopyalarken bir şey bozulmuş.

**Çözüm:** Cihazı yeniden başlat, tekrar dene.

### Sadece v1 imza görünüyor

```bash
apksigner verify _build_aligned.apk
# Çıktı: "Verified using v1"
```

**Sebep:** jarsigner kullanıldı. jarsigner yalnızca v1 imza şeması üretir.

**Çözüm:** apksigner ile yeniden imzala:
```bash
# Önce META-INF'i temizle
zip -d _build_aligned.apk "META-INF/*"
# Sonra apksigner ile imzala
apksigner sign --ks ... _build_aligned.apk
```

---

## 4. Kurulum Hataları

### `INSTALL_FAILED_UPDATE_INCOMPATIBLE`

```
Failure [INSTALL_FAILED_UPDATE_INCOMPATIBLE]
```

**Sebep:** Telefonda aynı uygulamanın farklı bir imzayla imzalanmış sürümü var. Android aynı package name altında iki farklı imza kabul etmez.

**Çözüm 1:** Eski sürümü kaldır:
```bash
adb uninstall com.package.name
```

**Çözüm 2:** Paket ismini değiştir (binary-level patch) — böylece sistem farklı uygulama sanar.

### `INSTALL_FAILED_NO_MATCHING_ABIS`

```
Failure [INSTALL_FAILED_NO_MATCHING_ABIS]
```

**Sebep:** APK içinde cihazın mimarisine uygun native lib yok. One UI 8 (Samsung) arm64-v8a kullanır.

**Çözüm:** Split APK'dan native lib'leri merge et veya arm64-v8a lib'leri olan bir APK bul.

### `INSTALL_FAILED_INVALID_APK`

```
Failure [INSTALL_FAILED_INVALID_APK]
```

**Sebep:** APK parse edilemiyor. Genelde manifest binary corruption veya imza hatası.

**Sıralı çözüm:**
1. `apksigner verify` ile imzayı kontrol et
2. `zipalign -c 4` ile hizalamayı kontrol et
3. `unzip -t` ile zip bütünlüğünü kontrol et
4. Binary-level patch dene (apktool bypass)

### `INSTALL_FAILED_USER_RESTRICTED`

```
Failure [INSTALL_FAILED_USER_RESTRICTED]
```

**Sebep:** Samsung Auto Blocker veya "Yan uygulamaları yükle" kapalı.

**Çözüm:**
- Ayarlar > Güvenlik > Auto Blocker → Kapat
- Ayarlar > Uygulamalar > Özel erişim > Bilinmeyen uygulamaları yükle → İzin ver
- ADB sideload (adb install) Auto Blocker'ı by-pass eder.

### `INSTALL_FAILED_DUPLICATE_PERMISSION`

```
Failure [INSTALL_FAILED_DUPLICATE_PERMISSION]
```

**Sebep:** Manifest'te aynı permission iki kez tanımlanmış.

**Çözüm:** `grep -c "uses-permission" AndroidManifest.xml` ile say, tekrarları temizle.

---

## 5. Çalışma Anı Hataları (Logcat)

### `ClassNotFoundException`

```
FATAL EXCEPTION: main
java.lang.RuntimeException: Unable to instantiate service ...
  java.lang.ClassNotFoundException: Didn't find class "com.package.KeepAliveService"
```

**Sebep:** Smali dosyası yanlış dizinde veya class reference yanlış.

**Çözüm:**
```bash
# Smali dosyasının yeri ile manifest'teki class adı uyuşuyor mu kontrol et
find _work/smali -name "KeepAliveService.smali"
grep "KeepAliveService" _work/AndroidManifest.xml
```

Smali yolu = paket yolu. `com.example.Foo` → `smali/com/example/Foo.smali`

### `ResourceNotFoundException`

```
FATAL EXCEPTION: main
android.content.res.Resources$NotFoundException:
  Resource ID #0x7f080689
```

**Sebep:** Smali'de sabit yazılmış resource ID, public.xml'de yok.

**Çözüm:**
```bash
# Decompile edilmiş APK'da public.xml'e bak
grep "0x7f080689" _work/res/values/public.xml
# Yoksa, başka bir drawable ID'si kullan
grep "drawable" _work/res/values/public.xml | head -20
```

### `SecurityException: Permission Denial`

```
java.lang.SecurityException: Permission Denial:
  startForeground requires android.permission.FOREGROUND_SERVICE
```

**Sebep:** Manifest'te gerekli izin tanımlanmamış.

**Çözüm:** Manifest'e eksik izinleri ekle:
```xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE"/>
<uses-permission android:name="android.permission.WAKE_LOCK"/>
```

### `UnsatisfiedLinkError`

```
java.lang.UnsatisfiedLinkError: dlopen failed:
  library "libnative.so" not found
```

**Sebep:** Native lib (.so) eksik veya yanlış mimari.

**Çözüm:**
```bash
# Hangi lib'ler var kontrol et
ls -la _work/lib/arm64-v8a/
echo "Cihaz mimarisi:"
adb shell getprop ro.product.cpu.abi
```

### `DeadObjectException`

```
java.lang.DeadObjectException: Transaction failed on small parcel;
  remote process probably died
```

**Sebep:** Servis çöktü ve sistemle bağlantısı koptu. Foreground service notification eksik olabilir.

**Çözüm:** Android 16'da foreground service'ler için notification ZORUNLU. Service'in `onStartCommand`'ında `startForeground()` çağrıldığından emin ol.

---

## 6. Resource ID Çakışması (Kritik)

### Belirti
- Rebuild başarılı
- APK kuruluyor
- Ama uygulama açılır açılmaz çöküyor
- Logcat: `ResourceNotFoundException` veya ANR

### Sebep
Smali'de hardcode edilmiş resource ID'ler (0x7f0xxxxx) her APK sürümünde değişebilir. Aynı ID farklı bir resource'a aitse çökme olur.

### Çözüm
```bash
# 1. Mevcut public.xml'de o ID neye ait?
grep "0x7f080689" _work/res/values/public.xml

# 2. Aynı türden başka bir resource bul
grep "drawable" _work/res/values/public.xml | head -10

# 3. Smali'deki sabit ID'yi güncelle
# Eski: const v1, 0x7f080689
# Yeni: const v1, 0x7f080123  (public.xml'de var olan bir drawable ID'si)
```

**Kural:** Asla resource ID'sini tahmin etme. Her zaman `public.xml`'den oku.

---

## 7. Framework-res Eksik

### Belirti
apktool decompile sırasında uyarı:
```
I: Using Apktool 2.x
I: Loading resource table...
W: Could not load framework-res, using aapt default
```

### Sebep
apktool sistem framework'ünü bulamıyor. Genelde ilk kullanımda olur.

### Çözüm
```bash
# Framework-res'i yükle (cihazdan çek)
java -jar apktool.jar if system/framework/framework-res.apk

# Veya alternatif: framework dosyasını manuel yükle
# Otomatik framework yükleme için cihaz bağlı olmalı
```

Windows'ta framework dosyaları:
```
C:\Users\marko\AppData\Local\apktool\framework\1.apk
```

Bu dosya yoksa apktool yedek modda çalışır ama bazı APK'lerde hata çıkar.

---

## 8. imza Çakışması

### Belirti
```bash
adb install mod.apk
# Failure [INSTALL_FAILED_UPDATE_INCOMPATIBLE]
```

### Sebep
Aynı package name altında farklı bir imzayla imzalanmış sürüm zaten yüklü.
- Play Store sürümü (Google imzalı) ← farklı imza
- Önceki mod sürümü (senin keystore'unla) ← aynı imza olabilir

### Çözüm
```bash
# 1. Önce eski sürümü kaldır
adb uninstall com.package.name

# 2. Eğer sistem uygulamasıysa (kaldırılamaz):
# Paket ismini binary-level değiştir
```

**Sistem uygulamaları** (ör. `com.google.*`) root'suz kaldırılamaz. Mutlaka paket ismi değiştir.

---

## Hata Ayıklama Akış Şeması

```
APK kurulamadı mı?
├── "INSTALL_FAILED_UPDATE_INCOMPATIBLE" → İmza çakışması
│   ├── Eski sürümü kaldır → dene
│   └── Olmazsa → paket ismini değiştir
│
├── "INSTALL_FAILED_INVALID_APK" → APK bozuk
│   ├── apksigner verify → imza hatası mı?
│   ├── zipalign -c 4 → hizalama hatası mı?
│   └── unzip -t → zip bozuk mu?
│
├── "INSTALL_FAILED_NO_MATCHING_ABIS" → Native lib hatası
│   └── Split merge yap veya farklı APK bul
│
├── "Uygulama yüklenmedi" (UI hatası) → Auto Blocker
│   └── ADB ile dene: adb install mod.apk
│
└── Kuruluyor ama açılmıyor → Çalışma anı hatası
    └── adb logcat -d | grep FATAL → oku ve fix'le
```
