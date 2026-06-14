# Bot Blocked by User — Tanı ve Çözüm

## Hata
```
Telegram send failed: Forbidden: bot was blocked by the user
```

## Anlamı
- Bot token'ı **geçerli** — Telegram bot API'ye bağlanabiliyor
- Gateway state'te `"state":"connected"` ve `error_code:null`
- Ancak kullanıcı daha önce bot'u Telegram'da **bloklamış**
- Telegram, bloklanmış bir bot'un o kullanıcıya mesaj göndermesine izin vermez

## Ne İşe Yaramaz
- Gateway restart (`--replace`)
- Gateway state reset (`gateway_state.json` sıfırlama)
- Token değiştirme (mevcut token geçerli)
- Scheduled task yeniden başlatma

## Çözüm (kullanıcı tarafı)
1. Telegram'ı aç
2. Bot profiline git (sohbet listesinde veya aramada bul)
3. **Unblock** / **Engeli Kaldır** butonuna tıkla
4. `/start` yaz (opsiyonel)
5. Hermes'e haber ver, tekrar dene

## Tespit Süreci (14 Haziran 2026)
1. `send_message` dener → Forbidden hatası alır
2. `.env` kontrol edilir → token var
3. `gateway_state.json` kontrol edilir → `"state":"connected"`, hata yok
4. Gateway restart denerilir (`Start-ScheduledTask Hermes_Gateway`) → state değişmez
5. Manüel gateway çalıştırmayı dener → "Gateway already running (PID 3592)" alınır
   - State'te PID 15096 vardı ama gerçek PID 3592'ydi → PID çakışması
6. `--replace` ile gateway yeniden başlatılır → PID 6208, state "connected"
7. Tekrar `send_message` → hala Forbidden
8. Sonuç: Gateway sorunsuz, token geçerli — kullanıcı bot'u engellemiş

## Ders
- İlk belirti "Forbidden: bot was blocked" ise **altyapıya dokunma**, doğrudan kullanıcıya yönlendir
- Gateway state'te "connected" görülmesi güvenilir değil — state'teki PID her zaman gerçek PID'yi yansıtmaz
- `--replace` flag'i scheduled task'ten daha güvenilir restart sağlar
