# Video #3 — Production Launch & Native iOS (AI ile Production Seviyesinde Proje Çıkardık — 400K satır kod)

**Video:** https://youtu.be/GzJNuF5tmGk
**Seri:** Kodlamıyoruz 3. Bölüm (aslında 4.)
**Yayın:** PROTOTURK
**Süre:** ~3-4 haftalık toplam geliştirme süresi

---

## Özet

PROTOTURK projesi production'a çıktı. prototip.com (prototurk.com) canlıda. Toplam 400.000 satır kod, ~284 issue, neredeyse sıfır hata. Bu videoda production öncesi yapılanlar, canlıya geçiş süreci ve sonrası anlatılıyor. Ayrıca bir de native iOS uygulaması Codex ile yaptırılmaya başlanmış.

---

## Production Öncesi Yapılanlar

### Major Refactor: Unified Post Model
- **Öncesi:** `posts`, `comments`, `replies` ayrı tablolar → gündem hesaplama, reply chain, alıntılama hep sorunlu
- **Sonrası:** HER ŞEY post. Comment diye bir şey yok, reply diye bir şey yok. Tek bir `posts` tablosu, altında post'lar (tree yapısı)
- **Kazanım:** Gündem hesaplama çalışır hale geldi, yeniden paylaşma/cevap verme tek modelde birleşti
- Kod: "Çok büyük bir refaktördü, AI kılçıksız halletti"

### Feed Algorithm — 4 Sekmeli Akış
- **Yeniler** — kronolojik
- **Trend** — algoritmik sıralama
- **Takip** — takip edilenlerin post'ları
- **Sana Özel** — kişiselleştirilmiş (aynı araçları kullanan, aynı tartışmalara katılan, takip ettiğin kişilerin etkileşimde olduğu)

### Trending Algorithm (Detaylı)
- **Ham Score:** Beğeni × (0.7 veya 1.3)
  - 0.7 = yazarı takip edenler için (yakın çevre)
  - 1.3 = takip etmeyenler için (yeni kitle)
  - Yani yeni insanların ilgisini çeken içerikler daha yüksek puan alır
- **Time Decay:** Post eskidikçe puan düşer
- **New Account Penalty:** 7 günden eski hesaplar × 0.5 (spam önleme, dinamik gün sayısı)
- **Örnek:** 1310 ham skor → time decay + new account penalty → 0.14'e düşebilir
- **Admin panelinde:** Her trend'in neden trend olduğu görünür (hangi faktörler etkili)

### Hashtag & Topic (Gündem) Sistemi
- Post'lardan otomatik toplanan etiketler
- Spam/stop-word filtresi ("teşekkür ederim", "selam" gibi kelimeler gündemden çıkarılır)
- En az 3-4 kişinin konuştuğu konular gündem olur
- **Editörde autocomplete:** "@prototurk" yazınca daha önce kullanılmış etiketler önerilir

### Editor (Yazma Deneyimi)
- Mention ve hashtag autocomplete (canlı öneri)
- Gerçekten çizerek, anlatarak AI'a anlatılmış
- "400K satır kod yazdırdım o kadar uğraşmadım ama editör için tek seferde çizerek anlattım"

### Mesajlaşma (DM) İyileştirmeleri
- Arşiv
- Sabitleme
- Silme
- Sessize alma
- Filtreler: Gruplarım, Okunmamışlar, Tümü
- Arama: kişi veya mesaj içinde

### Admin Panel — Kullanıcı Detay Sayfası
Her kullanıcı için:
- **Genel profil:** post sayısı, takipçi/takip, beğeni, yer imi, repost, DM sayısı
- **Depolama:** R2 ayak izi (kaç MB/GB kaplıyor)
- **Kalite/Güvenlik:** problem var mı, hesap durumu
- **Aksiyonlar:** profil düzenleme, şifre sıfırlama emaili, manuel onay
- **Admin notları:** elle not yazabilme
- **İşlem geçmişi:** yapılan tüm admin işlemleri log'u
- **Sosyal istatistikler:** en çok mesajlaştığı kişiler, son 24 saat aktivite

### SSR Performans İyileştirmeleri
- Bazı sayfalar Server-Side Rendering'e geçirildi
- Lighthouse skorları:
  - **Mobil:** 93 (Accessibility 100)
  - **Desktop:** 86 (bazen 90-100)
  - SEO: no-index nedeniyle 69 (index'te 100 olur)
- Sayfa yenilemede orta kısım yenilenmiyor — SSR cache sayesinde anında geliyor

### API & Security
- **Rate Limiting:** API istek sınırlaması
- **API Token Sistemi:** Kullanıcılara özel token
  - Kullanıcı kendi token'ını görebilir, silebilir, yenileyebilir
  - Rest API token oluşturma
- **End-to-End Encryption planı:** DM'ler için (henüz yok, plan aşamasında)

---

## AI ile Çalışma Deneyimi — Çıkarımlar

### "Kör Geliştirme" vs "Full Kontrol"
| Mod | Deneyim |
|-----|---------|
| **Kör geliştirme** (yarısı) | Kızıyla ilgilenirken 5-10 sn'de bir prompt'u kontrol edip gönderdi. Sonucu beklemeden devam. "Çok fazla kontrol etmeden, sadece yapsın istedim." |
| **Full kontrol** (diğer yarısı) | Her adımı izledi, tek tek kontrol etti, gerektiğinde düzeltti. |

### AI'ın Güçlü Olduğu Alanlar
- Büyük refaktörler (unified post model)
- Tutarlı kod üretimi (284 issue boyunca)
- Hata oranı sıfıra yakın
- Hız: 3-4 haftada 400K satır

### AI'ın Zorlandığı Alanlar
- **UI/UX detayları:** "Bazı konularda gerçekten tek uğraşmanız gerekiyor. Gerekirse çizerek, ederek anlatmanız gerekiyor."
- **Editor** gibi karmaşık UI'lar — çizimle anlatmak gerekti
- **Trend/thread çizgileri** gibi görsel detaylar

### Önemli Tespit (Kapanış Mesajı)
> "Gerçekten ne yaptığını bilmek çok önemli. Herkesin yapabileceğini iddia ediyorum ama herkesin bu seviyede yapabileceğini zannetmiyorum. Doğru soruyu kurabilmek, doğru iletişimi kurabilmek, onunla aynı düşünebilmek çok önemli."

### Recap: 3 Haftalık Deneyim
- **Süre:** 3-4 hafta
- **Toplam kod:** ~400K satır
- **Issue:** ~284+
- **Manual müdahale:** Sıfıra yakın (UI detayları hariç)
- **Sonuç:** production-ready, neredeyse sıfır bug
- **Connection:** AI'la proje çıkarmak mümkün, ama teknik bilgi + doğru iletişim şart

---

## BONUS: Native iOS App (Codex ile)

Son anda Codex'e native iOS app yaptırılmaya başlanmış:
- **Araç:** Codex CLI ($200/aylık)
- **Dil:** Swift (native, React Native değil)
- **Yöntem:** Web API'sindeki kodları Codex'e inceletti → sonra iOS'a uyarladı
- **Durum:** Çok başında, temel yapı çalışıyor
  - API'ye bağlı
  - Swift native özellikleri kullanıyor
  - Twitter klonu tasarım
  - Editör kısmı henüz yapılmadı
- **Plan:** Yakında iOS uygulaması da gelecek

---

## Feature Roadmap (Production Sonrası)
- [x] Production launch (prototip.com)
- [x] 4-sekmeli feed (Yeniler/Trend/Takip/Sana Özel)
- [x] Trend algoritması (engagement × time decay × new account penalty)
- [x] Unified post model (comment = post)
- [x] Hashtag/topic/gündem sistemi
- [x] Editor autocomplete (mention/hashtag)
- [x] DM iyileştirmeleri (archive, pin, mute, filter, search)
- [x] Admin kullanıcı detay sayfası
- [x] SSR performans optimizasyonu
- [x] API token yönetimi
- [x] Rate limiting
- [ ] E2E encryption (plan)
- [ ] iOS native app (Codex ile başlandı)
