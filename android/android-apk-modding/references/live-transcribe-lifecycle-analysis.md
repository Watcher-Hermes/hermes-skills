# Google Live Transcribe — Lifecycle X-Ray Analizi

**APK:** com.google.audio.hearing.visualization.accessibility.scribe
**Sürüm:** 8.7.880674799 (targetSdk 36, minSdk 32)
**Obfuscation:** R8 tam (tüm sınıf/metod isimleri kısa)

## Lifecycle Metod Haritası (MainActivity.smali)

| Metod | Satır (merge) | invoke-super | Ne Yapar |
|-------|--------------|--------------|----------|
| onCreate | ~11851 | Lfzv;->onCreate | UI kurulumu, listener'lar |
| onResume | ~16837 | Lfzv;->onResume | Transcription başlat/kontrol |
| onPause | ~16827 | Lfzv;->onPause | **Transcription DURDURUR (KRİTİK)** |
| onStop | ~19009 | Lfzv;->onStop | Cleanup (queue.remove + X()) |
| onDestroy | ~16330 | Lfzv;->onDestroy | Lgau cleanup |
| onStart | ~18894 | Lfzv;->onStart | (kod kısa) |

## onPause Kod Akışı (Boşaltılan Yer)

```
onPause()
├── Lgfq;->h()          → TRANSCRIPTION PAUSE (asıl durduran)
│   ├── l:Z kontrolü    → transcription aktifse devam
│   ├── n:Z kontrolü    → false ise q(Z)V çağır (motor kapat)
│   └── H()             → iç temizlik
├── sget Lgmw;->a       → ses ayarı singleton
├── Lgmw;->c:Z kontrol  → ses profili aktif mi?
└── Lgmw;->c()          → ses listener'ını temizle
```

## Anahtar Sınıflar

| Sınıf | Smali Dosyası | Rolü |
|-------|--------------|------|
| Lgfq | smali/gfq.smali (4771 satır) | **Transcription yöneticisi** — h()=pause, q(Z)=start/stop |
| Lgmw | smali/gmw.smali (837 satır) | Ses profili/volume yöneticisi — c:Z=aktif, c()=cleanup |
| Lggl | smali/ggl.smali | Ses seviyesi listener |
| Lggm | smali/ggm.smali | Ses callback arayüzü |
| Lgbi | smali/gbi.smali | Activity yaşam döngüsü queue |
| Lfzv | (parent class) | MainActivity'in parent'ı — muhtemelen BaseActivity |

## Obfuscated Lifecycle Metod Bulma

Obfuscated APK'lerde override edilen lifecycle metodlarını bulmak:

```bash
# MainActivity'de invoke-super çağrılarını tara
grep -n "invoke-super.*Lfzv;->" MainActivity.smali
```

Çıktıdaki her satır bir lifecycle override'ıdır:
```
onCreate, onDestroy, onPause, onResume, onStart, onStop
onNewIntent, onBackPressed, onSaveInstanceState
onConfigurationChanged, dispatchTouchEvent
```

Değiştirilecek metodun .method/.end method bloklarını bul, içindeki tüm invoke-super dışındaki satırları sil ve `.locals` sayısını 0'a düşür.

## Notlar

- `Lgwa;->C()` — onResume'da transcription başlatma/kontrol
- MainActivity.C field = Lgfq (transcription yöneticisi)
- MainActivity.r field = Lgbi (lifecycle queue listener)
- MainActivity.as field = Lggm (ses callback)
- appops RECORD_AUDIO foreground→allow yapmak onPause'u etkilemez — sadece Android izin katmanını açar

## Sürüm Geçmişi (dumpsys)

| Sürüm | VersionCode | Kaynak | Yüklenme |
|-------|-------------|--------|----------|
| 8.7.880674799 | 186096 | Play Store (com.android.vending) | 2026-06-13 |
| 8.3.739810924 | 164464 | Sistem önyüklü | Sistem görüntüsü |

İki versiyon yan yana durur: sistem bölümünde eski (8.3), kullanıcı bölümünde güncel (8.7).

## Sistem Uygulaması İmza Koruması — Deneyim

Live Transcribe Samsung'a **sistem uygulaması** olarak ön yüklü (`flags=[SYSTEM HAS_CODE... UPDATED_SYSTEM_APP]`). Yamalı APK yüklenemez:

| Denenen Yöntem | Sonuç |
|----------------|-------|
| `adb uninstall --user 0` | Success — ama sistem kaydı kalır |
| `adb reboot` sonrası yükleme | INSTALL_FAILED_UPDATE_INCOMPATIBLE — aynı hata |
| `adb install -r -d` (downgrade) | Aynı hata |
| APK'yı `/data/local/tmp/`'e push + pm install | Aynı hata |
| Dosya yöneticisi + manuel kurulum | Auto Blocker / Play Protect engeller |
| `pm disable` | SecurityException: Shell cannot change state |

**Karar:** Android 16 + One UI 8'de sistem uygulamalarına yama yapmak ROOT gerektirir. Root'suz çözüm mümkün değil.

## X-Ray Lifecycle Metodları (Detaylı)

### onPause() — Transcription Durdurma
```
.method protected final onPause()
    .locals 2
    invoke-super {p0}, Lfzv;->onPause()V

    # --- TRANSCRIPTION PAUSE (ANA DURDURUCU) ---
    iget-object v0, p0, .../MainActivity;->C:Lgfq;
    invoke-virtual {v0}, Lgfq;->h()V     # <-- transcription'ı duraklat

    # --- SES AYARI TEMİZLİĞİ ---
    sget-object v0, Lgmw;->a:Lgmw;
    iget-boolean v1, v0, Lgmw;->c:Z     # ses profili aktif mi?
    if-nez v1, :cond_0                   # değilse atla
    return-void

    :cond_0                              # aktifse temizle
    iget-object p0, .../MainActivity;->as:Lggm;
    invoke-virtual {v0}, Lgmw;->c()V      # listener temizle
    # ...
```

### Lgfq;->h() (gfq.smali:2466) — Transcription Pause Motoru
```
h()
├── monitor-enter (thread-safe)
├── l:Z kontrolü → transcription aktif değilse çık
├── n:Z kontrolü → false ise q(Z)V çağır (motoru kapat)
├── n:Z = true yap (pause flag)
└── H() → iç temizlik (private metod)
```

### Lgmw (gmw.smali) — Ses Ayarı Yöneticisi
Singleton. Constructor'da `Lgef;->d()` ile ses profili varlığı kontrolü → `c:Z` belirlenir.
- `a` sabiti: `c=0, d=2, e=Lgnc.a` (varsayılan profil)
- `b` sabiti: `c=1, d=3, e=Lgnc.b` (diğer profil)
- `c()`: listener'ı kaldır + shared preferences null

### onResume() — Transcription Başlatma (16837)
```
onResume()
├── AtomicBoolean set(false) → "paused" flag sıfırla
├── RECORD_AUDIO izin kontrolü (Lgbt.e())
│   └── izin yoksa → goto skip
├── Lgwa;->C() → transcription başlat/devam
└── (uzun, .locals 10)
```

### onStop() — Sadece Cleanup (19009)
```
onStop()
├── Lgbi.i queue → remove(this)
├── X() çağrısı → (?)
└── ScrollTextFlowLayout ile ilgili işlem
```

## Denenen Yöntemlerin Sonuçları

| Yöntem | Durum | Sebep |
|--------|-------|-------|
| onPause boşaltma + rebuild | ❌ Yüklenemedi | Sistem uygulaması imza koruması |
| appops set RECORD_AUDIO allow | ❌ Yetmedi | onPause kod seviyesinde durduruyor |
| Merge APK rebuild | ❌ Resource hataları | public.xml çakışması, false→anim/layout |
| --user 0 kaldır + reboot | ❌ Kayıt kaldı | Android 16 sistem imza önbelleği |
| Binary package rename | ❌ Denenmedi | Kullanıcı istemedi |
