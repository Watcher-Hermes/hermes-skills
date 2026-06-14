# Foreground Service Smali Şablonu

Android'de arka planda ses kaydı / sürekli işlem için foreground service zorunludur (Android 14+).

## Manifest Gereksinimleri

```xml
<!-- <manifest> içine: -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE"/>
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.WAKE_LOCK"/>

<!-- <application> içine: -->
<service android:name="com.package.RecordBgService"
    android:enabled="true"
    android:exported="false"
    android:foregroundServiceType="microphone"/>
```

## Smali — Tam Service Sınıfı

```smali
.class public Lcom/package/RecordBgService;
.super Landroid/app/Service;
.source "RecordBgService"

# direct methods
.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Landroid/app/Service;-><init>()V
    return-void
.end method

# virtual methods
.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    const/4 v0, 0x0
    return-object v0
.end method

.method public onCreate()V
    .locals 5
    invoke-super {p0}, Landroid/app/Service;->onCreate()V

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v1, 0x1a
    if-lt v0, v1, :cond_0

    const-string v0, "record_bg_channel"
    const-string v1, "Background Recording"
    const/4 v2, 0x2
    new-instance v3, Landroid/app/NotificationChannel;
    invoke-direct {v3, v0, v1, v2}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V

    const-class v1, Landroid/app/NotificationManager;
    invoke-virtual {p0, v1}, Lcom/package/RecordBgService;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Landroid/app/NotificationManager;
    invoke-virtual {v1, v3}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V
    :cond_0
    return-void
.end method

.method public onStartCommand(Landroid/content/Intent;II)I
    .locals 3
    invoke-virtual {p0}, Lcom/package/RecordBgService;->getApplicationContext()Landroid/content/Context;
    move-result-object v0

    new-instance v1, Landroid/app/Notification$Builder;
    const-string v2, "record_bg_channel"
    invoke-direct {v1, v0, v2}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    # icon ID — public.xml'den al: grep "ic_product_logo\\|app_icon" res/values/public.xml
    const v2, 0x7f080689
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setSmallIcon(I)Landroid/app/Notification$Builder;

    const-string v2, "Uygulama Adı"
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setContentTitle(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;

    const-string v2, "Background recording active"
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setContentText(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;

    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/app/Notification$Builder;->setOngoing(Z)Landroid/app/Notification$Builder;

    invoke-virtual {v1}, Landroid/app/Notification$Builder;->build()Landroid/app/Notification;
    move-result-object v1

    const/16 v2, 0x3e8
    invoke-virtual {p0, v2, v1}, Lcom/package/RecordBgService;->startForeground(ILandroid/app/Notification;)V

    const/4 v0, 0x1
    return v0
.end method
```

## OnCreate Enjeksiyonu (Application Subclass)

Obfuscated APK'de Application subclass'ının onCreate metodunun sonuna (return-void'den hemen önce):

```smali
    new-instance v0, Landroid/content/Intent;
    const-class v1, Lcom/package/RecordBgService;
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    invoke-virtual {p0, v0}, Lcom/package/AppClass;->startForegroundService(Landroid/content/Intent;)V
```

**ÖNEMLİ:** `startForegroundService` void döndüğü için `move-result` beklenmez. `startService` kullanma — foreground service type tanımlıysa `Context.startForegroundService() did not then call Service.startForeground()` hatası alınır.

## İcon ID Bulma

```bash
# Decompile edilmiş APK'de:
grep "icon\\|logo\\|ic_" _work/res/values/public.xml | head -10

# Örnek çıktı:
# <public type="drawable" name="ic_product_logo_live_transcribe" id="0x7f080689" />

# ID'yi smali'de kullan:
# const v2, 0x7f080689
```

## Bildirim Metinlerini APK'dan Çekme

```bash
grep "app_name\\|product_name\\|service_name" _work/res/values/strings.xml | head -5
```

Bildirim başlığı ve metni için uygulamanın kendi string'lerini kullan. Böylece dil desteği bozulmaz.

## Smali'de Class Reference

```
const-class vN, Lcom/package/RecordBgService;
```

Sınıf ismi büyük/küçük harf duyarlı. Manifest'teki `android:name` ile birebir aynı olmalı.
