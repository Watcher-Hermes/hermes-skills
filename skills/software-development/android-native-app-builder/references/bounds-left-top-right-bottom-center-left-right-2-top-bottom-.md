# bounds="[left,top][right,bottom]" → center = ((left+right)/2, (top+bottom)/2)
```

### 3. Tıkla
```bash
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell input tap <center_x> <center_y>
```

### İzin Sırası (LiveTranscriber örneği)
İzin dialogları **sırayla** gelir. Birini yanıtlamadan diğeri görünmez:
1. **RECORD_AUDIO** → "While using the app" (center 720,1590)
2. **POST_NOTIFICATIONS** (Android 13+) → "Allow" (center 720,1695)
   - Foreground Service çalıştırmak için bildirim izni zorunlu

**Pitfall:** BAŞLAT butonuna basınca önce MİKROFON izni gelir, sonra BİLDİRİM izni gelir. İkinci izin gelene kadar `uiautomator dump` ile UI'yi tekrar kontrol et. Arada `sleep 3-5` bırak.

**Kısayol — ADB ile tüm izinleri tek seferde ver (UI tıklamaya gerek kalmaz):**
```bash
adb shell pm grant com.package android.permission.RECORD_AUDIO
adb shell pm grant com.package android.permission.POST_NOTIFICATIONS