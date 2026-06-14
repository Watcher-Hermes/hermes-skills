# Obfuscated APK'lerde Lifecycle Metodlarını Bulma

## Problem

Google/AOSP uygulamaları R8/Proguard ile obfuscated edilmiştir.
Smali'de sınıf isimleri (a, b, c) ve metod isimleri anlamsızdır.
Ancak **override edilen Activity metodları** (`onPause`, `onResume`, `onCreate`, vb.)
isimlerini korur çünkü Android framework'ü reflection ile çağırır.

## Lifecycle Metodlarını Bulma

### Yöntem 1: invoke-super pattern (EN GÜVENİLİR)

Obfuscated süper sınıfı bul:
```smali
.class public Lcom/package/MainActivity;
.super Lfzv;     # <-- obfuscated parent
```

Parent'ın lifecycle metodlarına yapılan invoke-super çağrılarını ara:
```bash
grep -n "invoke-super.*Lfzv;->" MainActivity.smali | grep -E "onPause|onResume|onStop|onStart|onCreate|onDestroy|onRestart"
```

Çıktı örneği:
```
16827:    invoke-super {p0}, Lfzv;->onPause()V
16890:    invoke-super {p0}, Lfzv;->onResume()V
18894:    invoke-super {p0}, Lfzv;->onStart()V
19062:    invoke-super {p0}, Lfzv;->onStop()V
```

### Yöntem 2: Android framework override pattern

```bash
# Doğrudan override edilen metodları bul:
grep -n "\.method.*onPause\|\.method.*onResume\|\.method.*onStop" MainActivity.smali
```

## onPause/onStop Boşaltma (Davranış Değiştirme)

### Ne zaman kullanılır:
- "Ekran kilitlenince kaydı durdurma" özelliğini kapatmak
- Uygulama minimize edildiğinde çalışmaya devam etmesini sağlamak
- Herhangi bir "arka plana geçince dur" davranışını devre dışı bırakmak

### Adımlar:

1. **OnPause metodunu bul** (Yöntem 1 ile)
2. **Metodun tam içeriğini oku** — içindeki invoke çağrılarını anla
3. **Tüm gövdeyi sil**, sadece invoke-super + return-void bırak
4. **.locals değerini 0'a düşür**

### Örnek: Google Live Transcribe (com.google.audio.hearing.visualization.accessibility.scribe)

Orijinal onPause (satır 16823, 19108 satırlık MainActivity.smali):
```smali
.method protected final onPause()V
    .locals 2
    invoke-super {p0}, Lfzv;->onPause()V
    iget-object v0, p0, .../MainActivity;->C:Lgfq;
    invoke-virtual {v0}, Lgfq;->h()V        # transcription durdurma
    sget-object v0, Lgmw;->a:Lgmw;
    iget-boolean v1, v0, Lgmw;->c:Z
    if-nez v1, :cond_0
    return-void
    :cond_0
    # ... ekran kilidi ile ilgili ek kodlar
    return-void
.end method
```

Yamalı hali:
```smali
.method protected final onPause()V
    .locals 0
    invoke-super {p0}, Lfzv;->onPause()V
    return-void
.end method
```

### Önemli Notlar:

- `Lgfq;->h()` transcription durdurma metodu olabilir
- `Lgmw;->c:Z` ekran kilidi durumu boolean'ı olabilir
- **onPause'u boşaltmak = uygulama minimize edilince de kayıt devam eder**
- **onStop'u da boşaltmak gerekebilir** — bazı uygulamalar onStop'u kullanır
- İstenmeyen yan etki: kullanıcı uygulamadan net şekilde çıkınca da kayıt sürer

## Alternatif: appops ile Arka Plan İzni

APK modding yapmadan önce ADB ile dene:
```bash
adb shell "appops set com.target.package RECORD_AUDIO allow"
```

Bu, uygulamanın arka planda ses kaydetmesine izin verir.
Uygulama zaten açıkken değişiklik yapılırsa restart gerekebilir.
