## Proje Yapısı
```
<proje_adi>/
├── build.gradle.kts (root — sadece plugin declaration)
├── settings.gradle.kts (repo + include(":app"))
├── gradle.properties (android.useAndroidX=true)
├── local.properties (sdk.dir)
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew + gradlew.bat
└── app/
    ├── build.gradle.kts (android plugin + dependencies)
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/<package>/MainActivity.java
        └── res/
            ├── layout/activity_main.xml
            └── values/
                ├── strings.xml
                └── themes.xml
```