# Smali Sözdizimi Kısa Notu

Smali = Dalvik bytecode'un assembly gösterimi. APK decompile edilince her .class dosyası bir .smali dosyasına dönüşür.

## Temel Yapı

```
.class <access_flags> <class_descriptor>
.super <super_class_descriptor>
.source "<source_file>"

# fields
.field <access_flags> <name>:<type_descriptor>

# methods
.method <access_flags> <name>(<param_types>)<return_type>
    .locals <register_count>
    <instructions>
    return-void
.end method
```

## Tip Tanımlayıcıları (Descriptor)

| Tip | Kod |
|-----|-----|
| boolean | Z |
| byte | B |
| char | C |
| short | S |
| int | I |
| long | J |
| float | F |
| double | D |
| void | V |
| String | Ljava/lang/String; |
| Array | [I (int[]) veya [[B (byte[][]) |
| Object | Lpaket/adi/SinifAdi; |

Örnekler:
- `(I)V` → void metod(int)
- `(Ljava/lang/String;I)Z` → boolean metod(String, int)
- `(Landroid/content/Context;)Landroid/content/Intent;` → Intent metod(Context)

## Register'lar

| Register | Anlamı |
|----------|--------|
| v0–vN | Yerel register'lar (locals ile tanımlanır) |
| p0 | this (static olmayan metodlarda ilk parametre) |
| p1–pN | Metod parametreleri |

**Önemli:** p0 aslında vN+1'dir. `.locals 5` varsa p0 = v5, p1 = v6, ...

Register sayısı `.locals X` ile belirlenir. Kullandığın en yüksek register numarası X-1'i geçemez. Statik metodlarda p0 yoktur.

## Sık Kullanılan Talimatlar

### Yükleme / Saklama
| Talimat | İşlev |
|---------|-------|
| `const v0, 0x1` | v0 = 1 |
| `const/4 v0, 0x1` | v0 = 1 (4-bit, daha küçük encoding) |
| `const/16 v0, 0x100` | v0 = 256 (16-bit) |
| `const-string v0, "metin"` | v0 = "metin" |
| `const-class v0, Landroid/app/Service;` | v0 = Service.class |
| `const-wide v0, 0x1000L` | long constant |

### Nesne İşlemleri
| Talimat | İşlev |
|---------|-------|
| `new-instance v0, Ljava/lang/StringBuilder;` | Yeni StringBuilder oluştur |
| `new-array v0, v1, [I` | int[v1] boyutunda dizi oluştur |
| `check-cast v0, Ljava/lang/String;` | Tip dönüşümü (cast) |
| `instance-of v0, v1, Ljava/lang/String;` | instanceof kontrolü |

### Metod Çağrıları
| Talimat | Ne Zaman |
|---------|----------|
| `invoke-virtual` | Sanal metod (normal çağrı) |
| `invoke-super` | Superclass'ın metodu |
| `invoke-direct` | Constructor / private metod |
| `invoke-static` | Statik metod |
| `invoke-interface` | Interface metodu |

Kullanım:
```smali
invoke-virtual {v0, v1}, Lcom/example/Foo;->method(Ljava/lang/String;)I
#          regs hedef    class            metod imzası
move-result v2
#       ^ return değeri varsa
```

### Koşul / Dal
| Talimat | Koşul |
|---------|-------|
| `if-eq v0, v1, :label` | v0 == v1 |
| `if-ne v0, v1, :label` | v0 != v1 |
| `if-lt v0, v1, :label` | v0 < v1 |
| `if-ge v0, v1, :label` | v0 >= v1 |
| `if-gt v0, v1, :label` | v0 > v1 |
| `if-le v0, v1, :label` | v0 <= v1 |
| `if-eqz v0, :label` | v0 == 0 |
| `if-nez v0, :label` | v0 != 0 |
| `goto :label` | Atla |

### Dönüş
| Talimat | İşlev |
|---------|-------|
| `return-void` | void dön |
| `return v0` | v0 dön |
| `return-object v0` | Object dön (v0 bir object ise) |
| `return-wide v0` | long/double dön |

### Dizi İşlemleri
| Talimat | İşlev |
|---------|-------|
| `aget v0, v1, v2` | v0 = v1[v2] |
| `aput v0, v1, v2` | v1[v2] = v0 |
| `array-length v0, v1` | v0 = v1.length |

### Alan Okuma/Yazma
| Talimat | İşlev |
|---------|-------|
| `iget v0, v1, Lcom/example/Foo;->field:I` | v0 = v1.field |
| `iput v0, v1, Lcom/example/Foo;->field:I` | v1.field = v0 |
| `sget v0, Lcom/example/Foo;->STATIC_FIELD:I` | v0 = StaticField |
| `sput v0, Lcom/example/Foo;->STATIC_FIELD:I` | StaticField = v0 |

## Foreground Service Başlatma (OnCreate Enjeksiyonu)

Application subclass'ının onCreate'ine eklemek için (invoke-super'dan hemen sonra veya return-void'den önce):

```smali
    new-instance v0, Landroid/content/Intent;
    const-class v1, Lcom/package/KeepAliveService;
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    invoke-virtual {p0, v0}, Lcom/package/ApplicationClass;->startForegroundService(Landroid/content/Intent;)V
```

**UYARI:** `startForegroundService` void döner — smali'de `move-result` kullanma. manifest'te `foregroundServiceType` tanımlı service'lerde `startService()` crash üretir; `startForegroundService()` zorunludur.

Detaylı foreground service smali şablonu için `references/foreground-service-smali.md` dosyasına bak.

## Register Sayısı Hesaplama

```smali
.method public onCreate()V
    .locals 5          # v0..v4 kullanılabilir
    # p0 = this
    # v0, v1, v2, v3, v4
    invoke-super {p0}, ...
    # yukarıdaki servis start: v0, v1 kullanılıyor = 2 register
    # locals 5 yeterli. locals 1 olsaydı HATA.
.end method
```

## Alt Sınıf İç Sınıf Erişimi

```smali
# InnerClass'a erişim
iget-object v0, p0, Lcom/package/OuterClass;->innerField:Lcom/package/OuterClass$InnerClass;
```

## Yaygın Hatalar

| Hata | Sebep |
|------|-------|
| `Invalid register: v{...} out of range` | `.locals X` yetersiz, register sayısını artır |
| `Unsigned short value out of range` | const/4, const/16 ile taşan değer — daha geniş variant kullan |
| `Invalid method signature` | invoke satırında class reference yanlış |
| `method not referenced` | .class tanımı ile invoke'daki class reference uyuşmuyor |

## Kaynak

Detaylı referans: https://github.com/JesusFreke/smali/wiki
