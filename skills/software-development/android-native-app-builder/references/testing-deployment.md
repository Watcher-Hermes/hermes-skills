## Testing & Deployment

APK build ettikten sonra test etmek için **CLI build tercih edilir** — Android Studio Gradle sync'i beklemekten daha hızlı ve güvenilirdir.

### A. CLI Build (Tercih Edilen)
```bash
cd <proje_dizini>
export ANDROID_HOME="/c/Users/<user>/AppData/Local/Android/Sdk"
./gradlew assembleDebug --no-daemon