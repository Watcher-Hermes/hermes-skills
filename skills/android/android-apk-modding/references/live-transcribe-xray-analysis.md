# Live Transcribe (Google Scribe) X-Ray Analizi

## APK Bilgileri
- **Paket:** `com.google.audio.hearing.visualization.accessibility.scribe`
- **Sürüm:** 8.7.880674799 (versionCode=186096)
- **Sistem uygulaması:** Evet (Samsung ön yüklü, Google Play'den güncellenmiş)
- **Obfuscation:** R8/ProGuard (tüm sınıf isimleri a/b/c formatında)
- **Split APK:** base + split_config.arm64_v8a
- **targetSdk:** 36, **minSdk:** 32

## Activity Lifecycle Metodları (MainActivity.smali)

Üst sınıf: `Lfzv` (Activity/AppCompatActivity)

### onPause() — transcription duraklatma (KRİTİK)
```
.method protected final onPause()V
    invoke-super onPause
    C:Lgfq;→h()           → Transcription duraklat (pause)
    sget-object Lgmw;->a:Lgmw;
    Lgmw;->c:Z (boolean)   → Ses profili aktif mi kontrolü
    if-nez c → return       → Değilse direkt çık
    as:Lggm;                → Ses listener
    Lgmw;→c()              → Ses ayarlarını temizle
    Lggl;->c(Lggm;)V       → Listener'ı kaldır
```

**onPause boşaltma yaması:** transcription durduran Lgfq.h() ve ses temizleyen Lgmw.c() çağrılarını sil. Sadece invoke-super + return-void kalmalı.

### onResume() — transcription başlatma/kontrol
```
.method public final onResume()
    z:AtomicBoolean → set(false)     → paused bayrağını sıfırla
    aa:Lgbt;→e(RECORD_AUDIO izin)   → Mikrofon iznini kontrol et
    if-ne izin → goto skip           → İzin yoksa transcription başlatma
    l:Lgwc;→b():Lgwa;C()            → Devam/başlat kontrolü
```

### onStop() — cleanup
```
.method public final onStop()
    r:Lgbi;→i(ConcurrentLinkedQueue)→remove(this)   → Queue'dan çıkar
    X()                                              → İç temizlik
    o:ScrollTextFlowLayout ile ilgili işlem
```

### onDestroy() — standart
```
.method protected final onDestroy()
    al:Lgau;→a()              → Cleanup
    isChangingConfigurations() → Kontrol
```

## Önemli Sınıflar

### Lgfq — Transcription Motoru (4771 satır)
Üst sınıf: `Lgdm`
Implement: `Lgfv`

| Alan/Metot | Rolü |
|-----------|------|
| `C:Lgfq` (MainActivity field) | Transcription yöneticisi instance'ı |
| `l:Z` | Aktif mi? (true=transcription çalışıyor) |
| `m:Z` | Duraklatma modu |
| `n:Z` | Duraklatıldı mı? |
| `e:Ljava/lang/Object` | Monitor lock objesi |
| `h()` → pause transcription | `l:Z` kontrol + `q(Z)V` motor durdurma + `H()` temizlik |
| `q(Z)V` | Motoru durdur/başlat |
| `H()` | İç temizlik |

### Lgmw — Ses Profili/Volume Kontrolü (837 satır)
Singleton: `a:Lgmw` (normal), `b:Lgmw` (alternatif)

| Alan/Metot | Rolü |
|-----------|------|
| `c:Z` | Ses profili aktif mi? (constructor'da `Lgef;->d()` ile ayarlanır) |
| `d:I` | Ses modu (2=normal, 3=alternatif) |
| `e:Lgnc` | Ses kaynağı türü |
| `f:SharedPreferences` | Ayarlar |
| `h:F` | Ses seviyesi |
| `k:I` | Alternatif mod |
| `l:Lggm` | Callback/listener |
| `a(Context)` → Başlatma | SharedPrefs + listener bağlama |
| `b()` → Ses regüle | Volume kontrol |
| `c()` → Temizlik | Listener'ı kaldır, ref'leri null yap |

### Lgbi — Activity Yaşam Döngüsü Yöneticisi
| Alan/Metot | Rolü |
|-----------|------|
| `i:ConcurrentLinkedQueue` | Kayıtlı activity'lerin queue'su |
| `f(Lgli)` → Add | Activity'yi queue'ya ekle |
| `remove(Object)` → Remove | Activity'yi queue'dan çıkar (onStop) |

## keyfi

Bu obfuscated APK'de sınıf isimleri R8 ile karıştırılmış:
- `Lgmw` → `smali/gmw.smali`
- `Lgfq` → `smali/gfq.smali`
- `Lgbi` → `smali/gbi.smali`
- `Lggl` → `smali/ggl.smali`
- `Lggm` → `smali/ggm.smali`
- `Lgbt` → `smali/gbt.smali`

Bulma yöntemi: `find . -name "gmw.smali"` veya `grep -rl "\.class.*Lgmw" smali/`

## appops Analizi

```
RECORD_AUDIO: foreground   → Ön plan izni (default)
RECORD_AUDIO: allow        → Arka plan izni (appops set ile değiştirilir)
```

Sadece appops RECORD_AUDIO allow YETMEZ — uygulama kendi kodunda onPause'da transcription'ı durdurur. İkisi birleşmeli: appops izni + onPause yaması.

## Kaynak: LuNiZz / Can Değer

Obsidian vault: `Siber Güvenlik & Yazılım SSS/`
Altın Madeni belgesinde Android & Mobile Security bölümü:
- Android Internals (PDF)
- OWASP Mobile Top 10
- Mobile Systems and Smartphone Security
