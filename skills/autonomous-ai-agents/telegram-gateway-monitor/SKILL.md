---
name: telegram-gateway-monitor
description: >
title: "Telegram Gateway Monitor"
  Telegram bağlantı izleme ve otomatik kurtarma döngüsü.
  Bağlantı 30 dakikada bir kontrol edilir, test mesajı gönderilir,
  hata alınırsa otomatik onarım adımları uygulanır ve sonuç kaydedilir.
  Hedef listeleme ve gönderme için `hermes send --list` + `hermes send --to <target>` kullanılır.
version: 1.1.1
author: marko
license: MIT
metadata:
  hermes:
    tags: [telegram, gateway, monitor, watchdog, reconnect]
category: autonomous-ai-agents
audience: user
tags: [agents, ai, automation, telegram, tor]
related_skills: [hermes-agent]
---

# Telegram Gateway Monitor

## Kural

Bu skill; Telegram bağlantısının kopmaması ve kurulumun "her 30 dakikada bir test edilip hata alındığında otomatik düzeltilmeye çalışılması" için tasarlanmıştır.

## Yeni Bot Token'ı ile Tam Sıfırlama Akışı

Kullanıcı "bot engellendi" hatası alıp yeni token verdiğinde (veya herhangi bir token değişikliğinde) şu adımlar **kesin sırayla** uygulanır:

1. **Token'ı .env'ye Python ile yaz** — PowerShell'de tırnak içeren token'lar bozulur:
   ```python
   import re
   with open('/c/Users/marko/AppData/Local/hermes/.env', 'r') as f:
       content = f.read()
   content = re.sub(r'^TELEGRAM_BOT_TOKEN=*** 'TELEGRAM_BOT_TOKEN=*** content, flags=re.MULTILINE)
   with open('/c/Users/marko/AppData/Local/hermes/.env', 'w') as f:
       f.write(content)
   ```
   ⚠️ `***` karakteri token'da varsa f-string kullanma, string concatenation yap.

2. **Token'ı doğrula:**
   ```
   grep "TELEGRAM_BOT_TOKEN" /c/Users/marko/AppData/Local/hermes/.env | xxd
   ```
   Token tam olmalı, sonunda `0a` (newline) olmalı.

3. **Gateway state'i sıfırla** — `gateway_state.json`'u aşağıdaki içerikle değiştir:
   ```json
   {"pid":null,"kind":"hermes-gateway","gateway_state":"stopped","platforms":{"telegram":{"state":"disconnected","error_code":null,"error_message":null}}}
   ```
   Veya script: `scripts/reset_gateway_state.py` (varsa kullan)

4. **Gateway'i --replace ile başlat:**
   ```
   cd /c/Users/marko/AppData/Local/hermes/hermes-agent
   HERMES_HOME=/c/Users/marko/AppData/Local/hermes /c/Users/marko/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -m hermes_cli.main gateway run --replace
   ```

5. **20 sn bekle, sonra state'i kontrol et:**
   ```
   cat /c/Users/marko/AppData/Local/hermes/gateway_state.json
   ```
   `"state":"connected"` ve `"error_message":null` görene kadar bekle.

6. **Bot username'ini API'den bul** (kullanıcıya bildirmek için):
   ```
   curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
   ```
   `result.username` = `@bot_username`, `result.first_name` = bot adı

7. **Test mesajı gönder:**
   ```
   hermes send --to "telegram:Q !" "Test mesajı"
   ```
   - `Forbidden: bot was blocked by the user` → kullanıcıya bot @username'ini söyle, Telegram'da unblock yapmasını iste
   - Başarılı → gateway çalışıyor, sorun yok

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

## Telegram test mesajı içeriği

- Başarı: `[telegram-watchdog] Bağlantı testi başarılı.`
- Düzeltme sonrası başarı: `[telegram-watchdog] Bağlantı testi başarılı. Otomatik onarım uygulandı.`
- Son çare başarısızlık: `[telegram-watchdog] Bağlantı testi başarısız. Otomatik onarım denendi ancak sorun devam ediyor.`

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

## send_message Tool Token Cache

`send_message` tool'u, gateway'den **bağımsız** olarak kendi token cache'ine sahiptir. Oturum başlangıcında `.env`'yi okur ve tüm oturum boyunca aynı token'ı kullanır. Gateway restart (`--replace`) bu cache'i etkilemez.

**Belirti:** Gateway "connected", direkt API çalışıyor, ama `send_message` "bot was blocked" hatası veriyor.

**Tanı ve çözüm:** `references/send_message-token-cache.md`

**Acil durum scripti:** `scripts/send_tg.py` — direkt Python API çağrısı yapar, `send_message` cache'ini bypass eder.

## Kazanımlar / Operasyon Notları (sessiz ve güvenli kullanım için)

- Windows'ta aynı anda birden fazla Telegram bağlantı testi gönderme.
- "Gateway already running (PID X)" mesajı alınınca:
  1. O PID'yi öldür: `powershell.exe -NoProfile -Command "Stop-Process -Id <PID> -Force"`
  2. State'i sıfırla (scripts/reset_gateway_state.py)
  3. `--replace` ile başlat
- Eğer gateway_state.json'daki PID çalışmıyorsa state yanıltıcı olabilir. Önce gateway log'unda hangi PID'nin gerçekten çalıştığını kontrol et.
- Eğer `Not Found` alırsan yanlış yol, eşleşmeyen PowerShell sırası ya da özel mod anahtarı sorunu olabilir.
- Güncellenmiş tekrar-okuma kuralı: `OLLAMA_VISION.md`'ye git, oradaki kuralı güncelle ve ek çözüm yapma.

## Not

- Cron job bu skill'i yükleyip her 30 dakikada bir çalıştıracaktır.
- Kullanıcı bu kuralı ve cron job'u silmemiştir; koru ve çalıştır.

## .env kalıcılığı kuralı

`.env` dosyasındaki değişiklikler **tek seferlik değildir**. Her `.env` düzenlemesi şu şekilde sıralanmalı:
1. `.env` dosyasına kaydet.
2. Değişikliği Hermes skill olarak kaydet.
3. Değişikliği Obsidian vault'a not olarak ekle.
Kalıcı hafıza (MEMORY/USER) ilk kontrol noktası burası olmalıdır.

## Obsidian kayıt

Kullanıcının Obsidian vault yolunu `.env`'de güncelle:
- Anahtar: `OBSIDIAN_VAULT_PATH`
- Not dosyası: `<vault>/Telegram Gateway Monitor.md`

Her test sonrasında aşağıdaki satırı bu dosyaya ekle:
- `- <tarih> <saat> — <sonuç>` (örn. `2026-06-02 19:36 — Telegram bağlantı testi başarılı.`)
