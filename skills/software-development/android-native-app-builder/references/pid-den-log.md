# PID'den log
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell logcat -d --pid=<PID>
```

### Servis Durumu Kontrolü
```bash
/c/Users/marko/AppData/Local/Android/Sdk/platform-tools/adb.exe shell dumpsys activity services com.package