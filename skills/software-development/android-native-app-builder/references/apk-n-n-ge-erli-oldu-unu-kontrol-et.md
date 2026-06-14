# APK'nın geçerli olduğunu kontrol et
/path/to/build-tools/35.0.1/aapt2 dump badging "C:\\Users\\marko\\Desktop\\Uygulama.apk" | grep -E "^package:|minSdkVersion:|targetSdkVersion:|native-code:"
```

- `native-code:` satırı yoksa → APK saf Java/Kotlin, tüm mimarilerde çalışır
- `native-code: armeabi-v7a` gibi bir satır varsa → sadece ARM cihazlarda çalışır
- Debug APK'ler Play Store'dan değil, manuel kurulum içindir — bu normaldir