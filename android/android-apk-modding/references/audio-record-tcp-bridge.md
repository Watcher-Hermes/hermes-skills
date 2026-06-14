# AudioRecord + TCP Bridge — APK Modding Alternatifi

## Ne Zaman Kullanilir
APK modding ile cozulemeyen durumlarda:
- Android SpeechRecognizer API'si arka planda calismiyor (Android 10+ sinirlandirmasi)
- Google Cloud Speech imza dogrulamasi yuzunden custom imzali APK calismiyor
- Sistem uygulamasi imza korumasini asamadik (package rename de ise yaramadi)
- Kullanici "uygulamaya yeni ozellik ekleme, sadece ayar degistir" dedi

## Cozum: Islemeyi Windows PC'ye Tasima

```
Telefon (mikrofon)             Windows PC
─────────────────        ─────────────────────
AudioRecord                   Python TCP Server
  ↓ Ham PCM 16kHz               ↓ Ses chunk'larini al
  ↓ TCP socket (WiFi)           ↓ Whisper/faster-whisper ile transkript et
  ↓ Boyut+veri protokolu        ↓ Transkripti geri gonder
  ↓ Ekranda goster              ↓ (veya dosyaya kaydet)
```

## Telefon Tarafi (Android - Java)

SpeechRecognizer yerine:

```java
// TranscriptionService.java — onStartCommand icinde:
new Thread(() -> {
    Socket socket = new Socket("192.168.0.20", 9999);  // PC IP
    OutputStream out = socket.getOutputStream();
    BufferedReader in = new BufferedReader(
        new InputStreamReader(socket.getInputStream()));

    // AudioRecord baslat
    AudioRecord recorder = new AudioRecord(
        MediaRecorder.AudioSource.MIC, 16000,
        AudioFormat.CHANNEL_IN_MONO,
        AudioFormat.ENCODING_PCM_16BIT, 4096);
    recorder.startRecording();

    byte[] buffer = new byte[4096];
    while (isRunning) {
        int read = recorder.read(buffer, 0, buffer.length);
        if (read > 0) {
            // 4 byte boyut + PCM veri
            byte[] size = ByteBuffer.allocate(4)
                .putInt(read).array();
            out.write(size);
            out.write(buffer, 0, read);
        }
    }
}).start();

// Cevap thread'i:
new Thread(() -> {
    String line;
    while ((line = in.readLine()) != null) {
        broadcastResult(line);  // TextView'e yaz
    }
}).start();
```

## Windows Tarafi (Python)

```python
# live_bridge.py — TCP server + faster-whisper
import socket, struct
import whisper  # veya faster-whisper

model = whisper.load_model("tiny")  # 1GB VRAM, hizli
server = socket.socket()
server.bind(("0.0.0.0", 9999))
server.listen()

while True:
    conn, addr = server.accept()
    audio_data = bytearray()
    while True:
        header = conn.recv(4)
        if not header: break
        size = struct.unpack(">I", header)[0]
        chunk = conn.recv(size)
        audio_data.extend(chunk)
        if len(audio_data) > 16000 * 2 * 5:  # 5 sn buffer
            result = model.transcribe(bytes(audio_data), language="tr")
            if result.get("text", "").strip():
                conn.sendall((result["text"] + "\n").encode())
            audio_data = bytearray()
```

## Gereksinimler
- Android: `INTERNET` ve `RECORD_AUDIO` izinleri (manifest'te mevcut)
- Windows: Python + faster-whisper (`pip install faster-whisper`)
- Telefon ve PC **ayni WiFi aginda** olmali
- PC IP'si sabit olmali veya her seferinde guncellenmeli

## Avantajlar
- Android'in background sinirlandirmasindan etkilenmez (AudioRecord foreground service'te calisir)
- Windows'ta RTX 4070 CUDA ile hizli transkripsiyon
- Telefonun CPU/bataryasina yuk binmez
- APK modding gerektirmez (kendi uygulaman, istedigin gibi degistirirsin)

## Dezavantajlar
- WiFi baglantisi gerektirir
- PC acik olmalidir
- Latency eklenir (~1-3 sn)
- PC IP'si degisirse telefonda guncellemek gerekir
