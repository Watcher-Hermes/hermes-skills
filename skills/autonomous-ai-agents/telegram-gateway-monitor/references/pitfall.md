## Pitfall

- **Telegram sorunlarında İLK iş bu skill'i yükle.** Kullanıcı "skill var ne oldu" derse — haklıdır. Telegram bağlantı sorunlarında önce `telegram-gateway-monitor` skill'ini `skill_view()` ile oku, adımları uygula.
- **Gateway env var adı karışıklığı:** Gateway `TELEGRAM_ALLOWED_USERS` bekler (sonu `_USERS` ile biter). `.env`'de `TELEGRAM_ALLOWLIST` varsa gateway onu görmez ve "Unauthorized user" hatası verir. Gateway "connected" gösterir ama tüm kullanıcıları unauthorized olarak reddeder.
  - **Çözüm:** `.env`'de `TELEGRAM_ALLOWED_USERS=<chat_id>` kullan, `TELEGRAM_ALLOWLIST` değil.
  - **Yedek:** `GATEWAY_ALLOW_ALL_USERS=true` ekle — bu gateway'in tüm kullanıcılara izin vermesini sağlar (geliştirme ortamı için güvenli).
- **Gateway iki .env dosyası okur:** 
  1. `~/.hermes/.env` (öncelikli — `C:\Users\marko\.hermes\.env`)
  2. `C:\Users\marko\AppData\Local\hermes\.env`
  - Gateway başlarken `~/.hermes/.env` yoksa allowlist ayarlarını göremez. Bu dosya mevcut değilse oluşturulmalı ve içine `TELEGRAM_ALLOWED_USERS=...` yazılmalıdır.
- **Title generator 401 hatası → API key geçersiz.** Gateway `connected` ve allowlist doğru olsa bile, `title_generator` 401 hatası alınıyorsa gateway'in kullandığı API key geçersizdir (`DEEPSEEK_API_KEY=*** gibi). Gateway-error.log'da `"Your api key: ****... is invalid"` şeklinde görünür. Çözüm: `.env`'deki API key'i gerçek değerle değiştir, sonra Gateway'i restart et.
- Telekom gateway yeniden başlatma komutu **dışarıdan** çalıştırılmalı; gateway içinden gönderilirse reddedilir.
  - Windows için güvenirlidir: `powershell.exe -NoProfile -Command "Start-ScheduledTask -TaskName Hermes_Gateway"`.
- "T/F" sesi varsayılan Telegram hedefi listelemede `telegram:Q ! (dm)` olarak görünür; bu hedef mevcut değilse ana Telegram hedefini kullan.
- `.env` okuma: linux PATH ve Windows YAML/CRLF ayrıntıları nedeniyle varsayılan `~/.hermes/.env` çoğu sistemde SIKINTI çıkarır.
  - Bu ortamda doğru yol: `/c/Users/marko/AppData/Local/hermes/.env`
  - `cat /c/Users/marko/AppData/Local/hermes/.env | grep <KEY> || true` kullan.
- Telegram iletimi bir sonraki adım olarak yapılmalı.
- **Obsidian log satırı eklerken `mcp_obsidian_vault_append` kullan** — Bu MCP tool'u encoding sorunları olmadan satır ekler, Türkçe karakterleri (ö/ş/ı/ğ/ü/ç) bozmaz. `write_file`'a göre daha basit: sadece path + content ver, tool gerisini halleder.
  - **Önerilen sıra:**
    1. **İlk tercih:** `mcp_obsidian_vault_append(path="Telegram Gateway Monitor.md", content="- <tarih> <saat> — <sonuç>")` — tek satır ekleme, encoding sorunsuz.
    2. **Yedek:** `write_file` ile oku+yeniyi ekle+baştan yaz — `mcp_obsidian_vault_append` çalışmazsa kullan.
    3. **Son çare:** `[System.IO.File]::AppendAllText(path, text, [System.Text.Encoding]::UTF8)` PowerShell ile — ama bash içindeki quote kaosu nedeniyle tercih edilmez.
  - ⚠️ **write_file yol formatı:** `write_file` tool'u **native Windows yolu** bekler (`C:\Users\marko\...`). MSYS tarzı `/c/Users/marko/...` yolu verilirse tool `C:\c\Users\marko\...` olarak yanlış çözümler. `terminal()` içinde `/c/Users/...` çalışır ama `write_file`/`read_file`/`patch` tool'larında `C:\Users\...` kullan. `mcp_obsidian_vault_append` ise vault-relative path bekler, MSYS veya Windows yolu değil.