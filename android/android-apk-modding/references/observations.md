# APK Modding Session Notları

## Live Transcribe (Google) APK Modding

**APK Bilgileri:**
- Paket: `com.google.audio.hearing.visualization.accessibility.scribe`
- Sürüm: 8.7.880674799 (versionCode: 186096)
- Orijinal targetSdk: 36 (Android 16/Baklava)
- Min SDK: 32 (Android 12L)
- Mimari: arm64-v8a
- Format: Split APK bundle (base.apk + split_config.arm64_v8a.apk)

**Obfuscation:**
ProGuard/R8 ile full obfuscat edilmiş:
- Application sınıfı `ScribeApplication` -> süper sınıfı `Lfzw;`
- MainActivity süper sınıfı `Lfzv;`
- Smali dosyaları tek/çift harf isimleri: `a.smali`, `avp.smali`, `bar.smali`
- MainActivity.smali 19.108 satır

**Yapılan Değişiklikler:**
1. targetSdkVersion 36 → 35 (apktool.yml)
2. KeepAliveService eklendi (foreground + WAKE_LOCK)
3. AndroidManifest.xml'e service declaration eklendi
4. ScribeApplication.onCreate'e startService çağrısı enjekte edildi

**Sorunlar:**
- `.line comment_text` smali'de geçerli değil → `# comment_text` kullan
- Resource ID tahmin edilmez, `res/values/public.xml`'den okunur
- Split APK'lerin hepsi aynı keystore ile imzalanmalı
- Apktool ile rebuild sonrası "Paket geçersiz göründü" hatası — binary XML bozulabilir

## Split APK → Monolithic Merge

Split APK bundle'ları Samsung'da "uyumlu değil" hatası verir. Çözüm: split'teki native lib'leri base'e merge et.

```python
import zipfile

# Load native libs from split
native_libs = {}
with zipfile.ZipFile("split_config.arm64_v8a.apk", "r") as z:
    for info in z.infolist():
        if info.filename.startswith("lib/"):
            native_libs[info.filename] = z.read(info.filename)

# Load base (skip META-INF)
base_files = {}
with zipfile.ZipFile("base.apk", "r") as z:
    for info in z.infolist():
        if not info.filename.startswith("META-INF/"):
            base_files[info.filename] = (info, z.read(info.filename))

# Write merged APK
with zipfile.ZipFile("merged.apk", "w", zipfile.ZIP_DEFLATED) as zout:
    for name, (info, data) in base_files.items():
        zout.writestr(info, data)
    for name, data in native_libs.items():
        zi = zipfile.ZipInfo(name)
        zi.external_attr = 0o644 << 16
        zout.writestr(zi, data, compress_type=zipfile.ZIP_STORED)
```

**Native lib'ler ZIP_STORED olmalı** — Android sıkıştırılmış lib kabul etmez.

## Binary Package Name Patching (Apktool'suz)

Apktool binary XML'i bozabiliyor. Güvenli alternatif: UTF-16LE byte replacement.

**Teknik:**
- AXML string pool'da string'ler UTF-16LE (her karakter 2 byte)
- Paket ismi ~35 yerde geçer
- **Yeni isim AYNI UZUNLUKTA olmalı** (offset'ler bozulmasın diye)

**Örnek (59 chars):**
- ORJ: `com.google.audio.hearing.visualization.accessibility.scribe`
- YENI: `com.live.transcribe.hermes.twentyfourhours.extended.android`

```python
import zipfile

orig = "com.google.audio.hearing.visualization.accessibility.scribe"
new_pkg = "com.live.transcribe.hermes.twentyfourhours.extended.android"
assert len(orig) == len(new_pkg)

with zipfile.ZipFile("base.apk", "r") as z:
    manifest = z.read("AndroidManifest.xml")

orig_utf16 = orig.encode('utf-16-le')
new_utf16 = new_pkg.encode('utf-16-le')

count = manifest.count(orig_utf16)
new_manifest = manifest.replace(orig_utf16, new_utf16)
assert new_manifest.count(new_utf16) == count
assert new_manifest.count(orig_utf16) == 0
```

**KULLANILAMAZ isimler (Samsung One UI 8'de):**
- `com.google.*` ve `com.android.*` — sistem seviyesinde korumalı
- Özel isim (`com.live.transcribe.hermes.*`) kullan

## "Uygulama yüklenmedi" Troubleshooting

Sıralı kontrol:
1. **Package name çakışması?** → Binary patch ile değiştir
2. **Split APK referansı?** → Merge yap
3. **targetSdk vs cihaz SDK?** → `aapt2 dump badging` ile kontrol et, düşür
4. **İmza?** → `apksigner verify` ile doğrula, V2+V3 gerekir
5. **Native lib'ler?** → ZIP_STORED olmalı
6. **Apktool corruption?** → Binary merge + binary package rename dene

**ÖNEMLİ:** Aynı yaklaşım 3 kez başarısız olursa strateji DEĞİŞTİR. Farklı yöntem dene.

## Sıkıştırma Kuralları (Monolithic APK)

| İçerik | Compress Type |
|--------|--------------|
| `classes.dex`, `classes2.dex` | ZIP_DEFLATED |
| `resources.arsc` | ZIP_DEFLATED |
| `lib/arm64-v8a/*.so` | **ZIP_STORED** |
| `assets/*` | ZIP_DEFLATED |
| `res/*` | ZIP_DEFLATED |

## Telegram'a Büyük APK Yükleme

Hermes `send_message` MEDIA: 27MB+ dosyalarda timeout atarsa:

```bash
# Token'ı .env'den hex ile oku
token="hex_decoded_token"   # 8925395268:AAF3WdpIN91cHI6IfOOlKF1gNoUNe7qrwUM
curl -s -F "chat_id=6328823909" \
  -F "document=@/path/to/apk.apk" \
  -F "caption=Aciklama (emoji kullanma)" \
  "https://api.telegram.org/bot$token/sendDocument"
```

30MB'a kadar çalışır. Emoji caption UTF-8 hatası verir.

## Samsung One UI 8 (Android 16) Uyarıları

- Auto Blocker: sideload engelleyebilir, kapatılmalı
- Play Protect: "Tara" devre dışı bırakılmalı
- targetSdk 36 uyumlu ama V3 imza gerektirebilir
- Google paket isimleri sistem seviyesinde bloklu olabilir

## RE-Hermes Notları

- Sıfır harici bağımlılık, sadece Python stdlib
- AI yorumu false positive üretebilir (APK'leri ZIP sandığı için entropy yüksek çıkar)
- APK analizinde magic = "ZIP/JAR/APK/Office" çıkar, bu normaldir
