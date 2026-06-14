# APK yükle (aynı komut)
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe install "C:\\Users\\marko\\Desktop\\LiveTranscriber.apk"
```

**Önemli not:** Eğer `adb.exe devices` emülatörü `localhost:XXXXX` olarak göstermişse (TCP/IP üzerinden), `adb install` doğrudan çalışır. Rapor formatı: "APK başarıyla yüklendi → uygulama açıldı → ekran görüntüsü alındı".

### D. Telegram ile APK Gönderme (Fiziksel Cihaza Kurulum İçin)

Kullanıcı APK'yı fiziksel telefonuna kurmak istediğinde doğrudan Telegram Bot API ile gönder:

```python
import re, requests