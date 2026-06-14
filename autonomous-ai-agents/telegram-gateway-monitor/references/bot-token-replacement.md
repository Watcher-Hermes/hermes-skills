# Bot Token Değiştirme Prosedürü (14 Haziran 2026)

## Bağlam

Kullanıcı bot engelleyince yeni Telegram bot token'ı verdi. Bu dokümanda token değişikliğiyle ilgili tüm adımlar kayıtlıdır.

## Tam Akış

1. **Token'ı .env'ye yaz** — Python ile (PowerShell tırnak sorunu çıkarır):
   ```
   python -c "
   import re
   with open('/c/Users/marko/AppData/Local/hermes/.env', 'r') as f:
       content = f.read()
   content = re.sub(r'^TELEGRAM_BOT_TOKEN=.*', 'TELEGRAM_BOT_TOKEN=<YENI_TOKEN>', content, flags=re.MULTILINE)
   with open('/c/Users/marko/AppData/Local/hermes/.env', 'w') as f:
       f.write(content)
   "
   ```

2. **Token'ı doğrula** — hex dump ile:
   ```
   grep "TELEGRAM_BOT_TOKEN" /c/Users/marko/AppData/Local/hermes/.env | xxd
   ```
   Sonunda `0a` (newline) olmalı, `***` varsa f-string hatası var demektir.

3. **Gateway state'i sıfırla**:
   ```python
   import json
   path = r'C:\Users\marko\AppData\Local\hermes\gateway_state.json'
   state = {
       'pid': None,
       'kind': 'hermes-gateway',
       'gateway_state': 'stopped',
       'platforms': {
           'telegram': {
               'state': 'disconnected',
               'error_code': None,
               'error_message': None
           }
       }
   }
   with open(path, 'w') as f:
       json.dump(state, f)
   ```

4. **Gateway'i --replace ile başlat**:
   ```
   cd ***REMOVED-BASE64***-agent
   HERMES_***REMOVED-BASE64*** ***REMOVED-BASE64***-agent/venv/Scripts/python.exe -m hermes_cli.main gateway run --replace
   ```

5. **20 sn bekle, state'i kontrol et**:
   ```
   cat ***REMOVED-BASE64***_state.json
   ```
   `"state":"connected"` ve `"error_message":null` görene kadar bekle.

6. **Bot username'ini bul** (kullanıcıya söylemek için):
   ```
   curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
   ```
   `result.username` = `@Pasa_38_bot`, `result.first_name` = `Pasa_55^`

7. **Test et**:
   ```
   hermes send --to "telegram:Q !" "Test mesajı"
   ```
   Eğer `Forbidden: bot was blocked by the user` → kullanıcıya @botusername söyle, Telegram'da unblock yapmasını iste.

## Bilinen Hatalar

- `Forbidden: bot was blocked by the user` — Bu bir **kullanıcı tarafı** sorunu. Gateway çalışıyor, token geçerli, bağlantı var. Kullanıcı Telegram'da botu bulup unblock yapmalı.
- `***` karakter token'da — f-string kullanma. String concatenation veya normal format() kullan.

## Not

Bu akış 14 Haziran 2026'da aşağıdaki token'la test edildi:
- Token: 8925395268:AAF3WdpIN91cHI6IfOOlKF1gNoUNe7qrwUM
- Bot: @Pasa_38_bot (Pasa_55^)
- Sonuç: Gateway connected, ama bot blocked — kullanıcıdan unblock beklendi.
