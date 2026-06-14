# Scheduled Task Console Window Prevention

## Problem

Bir Windows Scheduled Task `python.exe` ile bir script çalıştırdığında,
her tetiklenişte bir **terminal penceresi (cmd.exe)** açılır ve script
bitince kapanır. Kullanıcı bunu "5-10 dakikada bir terminal açılıp kapanıyor"
olarak görür.

Bu özellikle sık çalışan task'lar için can sıkıcıdır (Hermes-GuvenlikIzleme
her 2 dakikada bir çalışır).

## Sebep

`python.exe` bir **Console subsystem** executable'ıdır — Windows, console
uygulamaları için otomatik olarak bir terminal penceresi oluşturur.

`pythonw.exe` ise **Windows subsystem** executable'ıdır — terminal penceresi
açmaz, arka planda sessizce çalışır.

Her ikisi de **aynı Python yorumlayıcısıdır**, tek fark subsystem flag'idir.

## Çözüm: Scheduled Task'ı pythonw.exe ile değiştir

Task'ın "Task To Run" alanındaki `python.exe` yolunu `pythonw.exe` ile
değiştir:

```powershell
schtasks /change /tn "TaskAdi" /tr "C:\path\to\venv\Scripts\pythonw.exe C:\path\to\script.py"
```

### Doğrulama

```powershell
schtasks /query /fo LIST /v /tn "TaskAdi" | findstr "Task To Run"
# Çıktıda pythonw.exe görmelisin
```

## Notlar

- `pythonw.exe` her zaman `python.exe` ile aynı dizinde bulunur
- Script çıktısı (stdout/stderr) görünmez olur — hata ayıklama için
  script'in kendi log mekanizması olmalı
- GUI uygulamaları, servisler, watchdog script'leri için idealdir
- Task hala aynı kullanıcı oturumunda çalışır, sadece pencere açılmaz

## Hermes-GuvenlikIzleme Örneği

Önce:
```
python.exe C:\Users\marko\.hermes\scripts\security_monitor.py
```

Sonra:
```
pythonw.exe C:\Users\marko\.hermes\scripts\security_monitor.py
```
