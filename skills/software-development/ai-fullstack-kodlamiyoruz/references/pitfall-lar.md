## PITFALL'LAR

- **Context sıfırlanması**: AI ajanı 1M token'da context kaybeder. Memory.md ile çöz.
- **Railway credential'ları**: Environment variable'ları Railway dashboard'dan ayarla, `.env`'e yazma.
- **R2 CORS**: Frontend'den direkt yükleme yapacaksan CORS ayarlarını unutma.
- **Test coverage düşüklüğü**: AI bazen test yazmayı atlar. "Test yaz" diye zorla.
- **Deployment hataları**: Railway CLI login'inin hala aktif olduğunu kontrol et.
- **Rate limiting**: Free tier AI modelleri (OpenRouter free) 429 dönebilir. Fallback chain kullan.