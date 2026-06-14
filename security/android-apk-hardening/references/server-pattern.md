# Server-Side Yetkilendirme Mimarisi

## Akış Diyagramı

```
┌─────────────────┐          ┌──────────────────┐          ┌─────────────────┐
│   Android Client │          │   Your Server     │          │  Google APIs     │
│                  │          │                   │          │                 │
│  1. POST /nonce  │─────────>│  2. nonce üret    │          │                 │
│                  │          │   (tek kullanım)  │          │                 │
│  3. nonce döner  │<─────────│                   │          │                 │
│                  │          │                   │          │                 │
│  4. Integrity API│          │                   │          │                 │
│     nonce+token  │          │                   │          │                 │
│                  │          │                   │          │                 │
│  5. POST premium │─────────>│  6. Token'ı ilet  │─────────>│  7. Doğrula      │
│     /data        │          │   (server-to-     │          │   (verdict)      │
│     token+nonce  │          │    server)        │<─────────│                  │
│                  │          │                   │          │                 │
│                  │          │  8. nonce eşleşir?│          │                 │
│                  │          │  9. verdict geçerli?         │                 │
│                  │          │  10. entitlement    │          │                 │
│                  │          │      var mı?       │          │                 │
│  11. premium     │<─────────│  11. veriyi dön /  │          │                 │
│      veri/null   │          │      403           │          │                 │
└─────────────────┘          └──────────────────┘          └─────────────────┘
```

## Kritik Noktalar

| Adım | Nerede Karar? | Atlanabilir mi? |
|------|---------------|-----------------|
| 1-3. Nonce al | Client ister, sunucu üretir | Client nonce alamazsa durur |
| 4. Integrity token | Client üretir (ham) | Client sahte token üretemez (imzalı) |
| 5-6. Token gönder | Client iletir | Token ham, sunucu çözer |
| 7-10. Doğrulama | **Sunucu** | ❌ Client'ta karar yok |
| 11. Veri | **Sunucu** | ❌ Atlanan if, veriyi var edemez |
