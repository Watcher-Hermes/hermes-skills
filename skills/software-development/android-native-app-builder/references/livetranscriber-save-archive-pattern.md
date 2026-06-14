# LiveTranscriber — Süresiz Kayıt + TXT Arşiv Deseni

Bu desen, SpeechRecognizer tabanlı bir Android uygulamasına süresiz kayıt
ve transkriptleri tarihli TXT dosyalarına otomatik kaydetme özelliği ekler.

## 1. Süresiz Kayıt (TranscriptionService.java)

### Zaman Aşımlarını Maksimuma Çıkar
```java
recognizerIntent.putExtra(
    RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 30000);
recognizerIntent.putExtra(
    RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 20000);
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    recognizerIntent.putExtra(
        RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 100);
}
```

### Hatalarda Anında Restart (onError)
```java
// SINIRSIZ KAYIT: her hatada hemen yeniden başlat
if (isListening) {
    restartListening();
    broadcastStatus("Dinleniyor...");
}
```
- `ERROR_NO_MATCH` / `ERROR_SPEECH_TIMEOUT` → bekletmeden restart
- `ERROR_NETWORK` / `ERROR_SERVER` → hata göster + restart
- Delay kullanma (500ms Thread.sleep kaldırıldı)

### Sonuçlarda Sürekli Döngü (onResults)
```java
if (isListening) {
    restartListening();
}
```

## 2. TXT Dosyaya Kaydetme (MainActivity.java)

### stopService() içinde otomatik kaydet
```java
private void stopService() {
    String text = fullTranscript.toString().trim();
    if (!text.isEmpty()) {
        saveTranscript(text);
    }
    // ... servisi durdur ...
}
```

### saveTranscript() metodu
```java
private void saveTranscript(String text) {
    String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm",
        Locale.getDefault()).format(new Date());
    String fileName = "transkript_" + timestamp + ".txt";

    File archiveDir;
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        archiveDir = new File(getExternalFilesDir(null), "Transkriptler");
    } else {
        archiveDir = new File(
            Environment.getExternalStorageDirectory(), "Transkriptler");
    }
    archiveDir.mkdirs();

    File file = new File(archiveDir, fileName);
    try (FileWriter writer = new FileWriter(file)) {
        writer.write("=== Canlı Transkript ===\n");
        writer.write("Tarih: " + new SimpleDateFormat("dd.MM.yyyy HH:mm",
            Locale.getDefault()).format(new Date()) + "\n");
        writer.write("========================\n\n");
        writer.write(text);
        writer.write("\n\n=== Kayıt Sonu ===\n");
        Toast.makeText(this, "Kaydedildi: " + fileName,
            Toast.LENGTH_LONG).show();
    } catch (IOException e) {
        Toast.makeText(this, "Kaydetme hatası: " + e.getMessage(),
            Toast.LENGTH_LONG).show();
    }
}
```

### Gerekli Import'lar
```java
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
```

## 3. Arşiv Klasörü

- **Android 10+ (scoped storage):** `/storage/emulated/0/Android/data/<paket>/files/Transkriptler/`
- **Android 9 ve altı:** `/storage/emulated/0/Transkriptler/`
- **Dosya adı formatı:** `transkript_2026-06-11_08-15.txt`
- **İçerik formatı:**
  ```
  === Canlı Transkript ===
  Tarih: 11.06.2026 08:15
  ========================

  <transkript metni>

  === Kayıt Sonu ===
  ```

## 4. Emülatör Testi

ADB ile izinleri doğrudan ver (dialog atlatmak için):
```bash
adb shell pm grant com.livetranscriber android.permission.RECORD_AUDIO
adb shell pm grant com.livetranscriber android.permission.POST_NOTIFICATIONS
```

UI dump ile buton koordinatlarını bul:
```bash
adb shell uiautomator dump /sdcard/ui.xml
adb pull /sdcard/ui.xml .
# XML'den text + bounds regex ile koordinat çıkar
adb shell input tap <x> <y>
```

OCR ile emülatör ekranını kontrol et:
```python
import pytesseract, cv2
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
img = cv2.imread('emu_screen.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray, lang='eng+tur')
```

## 5. Ekran Durumları (OCR ile Doğrulanan)

| Buton | Sonuç |
|-------|-------|
| BAŞLAT | "Dinleniyor..." |
| DURDUR | "Durduruldu" |
| TEMİZLE | "Temizlendi" |
| KOPYALA | "Metin kopyalandı" (Toast) |
| Kayıt tamam | "Kaydedildi: transkript_....txt" (Toast) |
