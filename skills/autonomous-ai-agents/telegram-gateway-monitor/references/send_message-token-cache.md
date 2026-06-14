# send_message Tool — Independent Token Cache

## Discovery (14 Haziran 2026)

While debugging a "bot was blocked by the user" error after a token change:

| Component | Token kullandığı yer | Değişiklikten etkilenir mi? |
|-----------|---------------------|---------------------------|
| `.env` dosyası | Okunduğu anın değeri | Evet — her zaman güncel |
| Gateway (`gateway run`) | `.env`'yi çalışma başında okur | Sadece restart sonrası |
| **`send_message` tool** | **Agent oturumu başlangıcında okur** | **HAYIR — yeni oturum gerekir** |

## Sorun

`send_message` tool'u, Hermes agent oturumu başlarken `.env`'den `TELEGRAM_BOT_TOKEN`'ı okur ve bu token'ı **tüm oturum boyunca cache'ler**. Eğer:

- Oturum `token_A` ile başladı
- `.env`'de `token_B` olarak değiştirildi
- Gateway `--replace` ile yeniden başlatıldı

→ `send_message` tool'u hala `token_A`'yı kullanır. Gateway "connected" gösterse bile, tool eski token'la hata alır.

## Belirtiler

```
# Gateway state'te her şey iyi:
Gateway: running PID: 23816
Telegram: connected Error: None

# Ama send_message hata verir:
Telegram send failed: Forbidden: bot was blocked by the user

# Halbuki direkt API ile aynı mesaj gider:
curl -s "https://api.telegram.org/bot<YENI_TOKEN>/sendMessage" ...
→ {"ok": true, "result": {"message_id": 4733, ...}}
```

## Tanı

Aradaki farkı anlamak için:
1. Gateway state'te `telegram.state = connected` ve `error_message = null`
2. `curl` ile token'ı doğrula: `getMe` çalışıyorsa token geçerli
3. `curl` ile direkt mesaj gönder: gidiyorsa **send_message tool cache'inde sorun var**
4. Yeni bir oturum başlat (`/new` veya `/reset`) → sorun düzelir mi? Düzeliyorsa cache sorunu kesin

## Geçici Çözüm

Yeni oturum başlatmadan mesaj göndermek gerekiyorsa, direkt Python API çağrısı yap:

```python
# scripts/send_tg.py — skill altinda mevcut
import json, urllib.request, urllib.parse

with open(r'C:\Users\marko\AppData\Local\hermes\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN=***            token = line.split('=', 1)[1]
            break

data = urllib.parse.urlencode({
    'chat_id': '6328823909',
    'text': 'Mesaj'
}).encode()

r = urllib.request.urlopen(f'https://api.telegram.org/bot{token}/sendMessage', data=data)
print(json.loads(r.read()))
```

## Kalıcı Çözüm

- Yeni token geldiğinde:
  1. `.env`'yi güncelle
  2. Gateway restart (`--replace` ile)
  3. Kullanıcıya söyle: **Yeni oturum başlatmak için `/reset` yaz**
  4. Veya bekle — bir sonraki oturumda otomatik düzelir
