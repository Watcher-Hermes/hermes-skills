## Zorunlu adımlar

1. `.env`'ye yeni bir `TELEGRAM_BOT_TOKEN` yazıldığında **her zaman** şu adımları sırasıyla uygula:
    - `.env` yolu: `C:\Users\marko\AppData\Local\hermes\.env`
    - PowerShell ile dışarıdan gateway restart: `powershell.exe -NoProfile -Command "Start-ScheduledTask -TaskName Hermes_Gateway"`
      - Not: linux/workarounds veya `schtasks /Run` bash içinde güvenilir çalışmaz.
    - Bekleme: restart sonrası bağlanma için 15-20 saniye bekle.
    - Önce hedefi listele: `hermes send --list telegram` (çıktıda `telegram:Q ! (dm)` gibi bir hedef görünür)
    - Hedefi tırnak içinde kullan: `hermes send --to "telegram:Q !" "[telegram-watchdog] Bağlantı testi başarılı."`
    - ⚠️ `telegram:Q !` içindeki `!` shell'de özel anlam taşır — **tırnak içine almak zorunludur**, aksi halde hata alırsın.
2. Token doğrulama ve hata ayıklama:
    - Test mesajı düzgün gittiyse tamam.
    - "Not Found"/InvalidToken gelirse ne `.env`'ye ne de gateway yapısına müdahale et.
    - Sonuç: kullanıcıya yeni bir bot token iste; yeni token ile sadece Adım 1'i baştan uygula.
    - **"bot was blocked by the user"** (Forbidden) hatası:
      - Bu bir **kullanıcı tarafı** sorunudur. Bot token'ı geçerli, gateway bağlı, hata yok.
      - **Bot username'ini API'den çek** (kullanıcıya söylemek için):
        ```
        curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
        ```
        `result.username` ve `result.first_name` değerlerini kullanıcıya bildir.
      - Kullanıcı Telegram'da bot profilini açıp **Unblock / Engeli Kaldır** yapmalıdır.
      - Gateway restart, token değişikliği veya state reset ÇÖZMEZ. Kullanıcıya net bir şekilde bildir.
      - Örnek: "Bot @kullanici_adi (isim) — Telegram'da bulup Unblock yap, sonra dene."
3. Gateway state takibi ve restart:
    - `C:\Users\marko\AppData\Local\hermes\gateway_state.json` içindeki Telegram state `connected` olana kadar kontrol et.
    - **ÖNCE PID kontrolü:** gateway_state.json'daki PID ile `tasklist`'te görünen PID'yi karşılaştır. Eğer state'teki PID çalışmıyorsa, başka bir PID'de gateway zaten çalışıyor olabilir.
      - Gateway log'una bak: gateway örneği çalıştırmayı dene, "Gateway already running (PID X)" mesajı alırsan o PID doğru olan.
      - Doğru PID'yi öldür: `powershell.exe -NoProfile -Command "Stop-Process -Id <PID> -Force -ErrorAction SilentlyContinue"`
    - **Temiz restart (--replace ile):**
      ```
      cd /c/Users/marko/AppData/Local/hermes/hermes-agent
      HERMES_HOME=/c/Users/marko/AppData/Local/hermes /c/Users/marko/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -m hermes_cli.main gateway run --replace
      ```
      `--replace` eski gateway instance'ını otomatik öldürür ve yeniden başlatır.
    - **State reset (sadece --replace çalışmazsa):**
      1. `gateway_state.json` içinde `platforms.telegram.state`'i `"disconnected"` yap, `pid`'yi `null` yap
      2. Ardından `--replace` ile gateway'i başlat
      3. 15-20 sn bekle, state'i tekrar kontrol et
    - Eski hatalı token hatası (`115309...JhnYh` gibi) kalıntıysa, gateway process'ini öldür: `taskkill /F /PID <pid>` ardından scheduled task'ı tekrar başlat.
4. Nihai durumu raporla:
    - "Telegram bağlantı testi başarılı."
    - "Telegram bağlantı testi başarısız ve otomatik onarım denendi."