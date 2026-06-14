##
# KeepAliveService — 24 saat foreground servis + WakeLock
#
# Bir Android APK'ya enjekte edilecek foreground service.
# Amaç: Uygulamanın ekran kilitliyken bile çalışmasını sağlamak.
#
# Paket adını uygulamaya göre değiştir.
##

.class public ***REMOVED-BASE64***;
.super Landroid/app/Service;
.source "PG"

.field private static final CHANNEL_ID:Ljava/lang/String; = "keep_alive_24h"
.field private static final NOTIFICATION_ID:I = 0x7b
.field private wakeLock:Landroid/os/PowerManager$WakeLock;


.method public constructor <init>()V
    .registers 1
    .prologue
    invoke-direct {p0}, Landroid/app/Service;-><init>()V
    return-void
.end method


.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .registers 3
    .param p1, "intent"
    .prologue
    const/4 v0, 0x0
    return-object v0
.end method


.method public onCreate()V
    .registers 6
    .prologue
    invoke-super {p0}, Landroid/app/Service;->onCreate()V

    # create notification channel
    new-instance v0, Landroid/app/NotificationChannel;
    const-string v1, "keep_alive_24h"
    const-string v2, "24 Saat Kayit"
    const/4 v3, 0x2
    invoke-direct {v0, v1, v2, v3}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V
    const-string v1, "Canli Transkript 7/24 kayit modunda"
    invoke-virtual {v0, v1}, Landroid/app/NotificationChannel;->setDescription(Ljava/lang/String;)V

    # register channel
    const-string v1, "notification"
    invoke-virtual {p0, v1}, Lcom/.../KeepAliveService;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Landroid/app/NotificationManager;
    invoke-virtual {v1, v0}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V

    # acquire PARTIAL_WAKE_LOCK (0x1) — CPU stays on, screen can sleep
    const-string v0, "power"
    invoke-virtual {p0, v0}, Lcom/.../KeepAliveService;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/os/PowerManager;
    const/4 v1, 0x1
    const-string v2, "Hermes:KeepAlive24h"
    invoke-virtual {v0, v1, v2}, Landroid/os/PowerManager;->newWakeLock(ILjava/lang/String;)Landroid/os/PowerManager$WakeLock;
    move-result-object v0
    iput-object v0, p0, Lcom/.../KeepAliveService;->wakeLock:Landroid/os/PowerManager$WakeLock;

    # 24 hours = 86400s = 0x15180
    iget-object v0, p0, Lcom/.../KeepAliveService;->wakeLock:Landroid/os/PowerManager$WakeLock;
    const-wide/32 v1, 0x15180
    invoke-virtual {v0, v1, v2}, Landroid/os/PowerManager$WakeLock;->acquire(J)V

    return-void
.end method


.method public onStartCommand(Landroid/content/Intent;II)I
    .registers 9
    .param p1, "intent"
    .param p2, "flags"
    .param p3, "startId"
    .prologue

    new-instance v0, Landroid/app/Notification$Builder;
    const-string v1, "keep_alive_24h"
    invoke-direct {v0, p0, v1}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;Ljava/lang/String;)V
    const-string v1, "Canli Transkript"
    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setContentTitle(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
    move-result-object v0
    const-string v1, "7/24 kayit modunda calisiyor"
    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setContentText(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
    move-result-object v0
    # ICON ID: greple res/values/public.xml'den bul
    const v1, 0x7f080689
    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setSmallIcon(I)Landroid/app/Notification$Builder;
    move-result-object v0
    const/4 v1, 0x1
    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setOngoing(Z)Landroid/app/Notification$Builder;
    move-result-object v0
    invoke-virtual {v0}, Landroid/app/Notification$Builder;->build()Landroid/app/Notification;
    move-result-object v0

    # startForeground(NOTIFICATION_ID, notification)
    const/16 v1, 0x7b
    invoke-virtual {p0, v1, v0}, Lcom/.../KeepAliveService;->startForeground(ILandroid/app/Notification;)V

    # return START_STICKY (1)
    const/4 v0, 0x1
    return v0
.end method


.method public onDestroy()V
    .registers 2
    .prologue
    iget-object v0, p0, Lcom/.../KeepAliveService;->wakeLock:Landroid/os/PowerManager$WakeLock;
    if-eqz v0, :cond_a
    iget-object v0, p0, Lcom/.../KeepAliveService;->wakeLock:Landroid/os/PowerManager$WakeLock;
    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->release()V
    :cond_a
    invoke-super {p0}, Landroid/app/Service;->onDestroy()V
    return-void
.end method
