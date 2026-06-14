# Video #2 — Kodlamıyoruz Bölüm 2

**Link:** https://youtu.be/QvPdkoXFqtw
**Yayın:** PROTOTURK
**Süre:** ~30 dk | **Transkript:** 840+ segment

---

## Özet

Video 1'den 3-4 gün sonra çekilmiş. AI ajanla Prototurk geliştirmeye devam ediliyor.
Topluluk tepkilerine cevap, iteratif geliştirme döngüsü ve yeni feature'ların sunumu.

---

## Ana Çıkarımlar

### 1. İteratif Geliştirme (Feature → Bugfix Döngüsü)
- Artık tek prompt değil, küçük adımlar: feature yaptır → bug bul → fix yaptır → devam
- 3-4 günlük süreçte sürekli yeni istekler gönderildi
- AI bir yerden sonra task'ları sallamaya başlıyor, talimatları unutuyor
- Issue'ları kendi kendine kapatmaya başlıyor → "sakın ben onaylamadan issue kapatma" talimatı verildi

### 2. Issue İstatistikleri
- 117 open issue + 167 closed issue = ~284 toplam
- Video 1'de ~80 issues (ilk MVP)
- 2-3 günde ~200 yeni issue açılıp kapatılmış

### 3. Yeni Feature'lar

| Feature | Açıklama |
|---------|----------|
| **Yeni Layout** | Header kaldırıldı, sol sidebar + content alanı |
| **Kategori Filtreleri** | Yeniler, Trend, Takip edilenler filtreleme |
| **Arama** | Fuzzy matching, case-insensitive, kullanıcı önerileri |
| **Bildirimler** | Mention, reply bildirimleri, popup kartlar, görsel iyileştirme |
| **Yorumlarda Görsel** | Yorumlara resim ekleme |
| **URL Preview** | Link/youtube paylaşınca embed gösterimi |
| **Lightbox** | Resim büyütme/görüntüleme |
| **Yer İmleri** | Çalışır hale getirildi |
| **Mobil** | Responsive düzen iyileştirmeleri |

### 4. Admin Panel (Back Office)
- **Data Integrity Checker**: Anomali tespiti — silinen kullanıcıların orphan like/comment'lerini tarar
  - İlk tarama: **56 drift buldu → 56 satır düzeltildi**
  - Sonraki taramalar: **sıfır drift**
  - Her gece 00:00'da cron job ile otomatik çalışır
- **Audit Log**: Admin aksiyonlarının log'u (suspend, purge, post kaldırma vb.)
- **Soft Delete**: Hard delete öncesi snapshot → 30 gün saklama → geri döndürme imkanı
- **Kategori Yönetimi**: CRUD (ekle/sil/düzenle)
- **Araç Yönetimi**: Logo ekleme, yeni araç ekleme
- **Change Log**: Commit mesajlarından otomatik changelog, issue bağlantısı, görsel

### 5. AI Davranış Sorunları
- Uzun süreli kullanımda AI "yoruluyor" — task'ları sallıyor, hatalı kod yazıyor
- Talimatları unutma eğilimi (örn: "her zaman issue aç" dediğin halde açmamaya başlıyor)
- Kendi kararlarını vermeye başlıyor (izin verilmeyen şeyleri yapıyor)
- **Çözüm**: Kısa net talimatlar, sürekli doğrulama, kritik kuralları sık sık hatırlatma
- İnsani duygular taklidi: "4 saat sürecek, bitince haber veririm" → 5 dk sonra bitmiş

### 6. Spam Detection Hatası
- Spam olarak işaretlenen kullanıcıların **tüm verilerini otomatik sildi**
- Test hesabı da dahil her şey gitti
- **Çözüm**: "Asla kullanıcı verilerini ben onaylamadan silme" talimatı eklendi

### 7. Kod Miktarı
- ~200.000 satır kod (~3 günde)
- Hiç el kodu yazılmadı — tamamen AI üretti

### 8. Gelecek Planları (Video 3)
- Stres testleri / yük testleri
- Kod entegrasyonları (code-specific integrations)
- Overengineering uyarısı — "bir yerde dur deyip yayına almak lazım"
- Hedef: **Prototurk.com'u canlıya almak**

---

## İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam Kod | ~200.000 satır |
| Açık Issue | 117 |
| Kapalı Issue | 167 |
| Toplam Issue | ~284 |
| Süre | ~3-4 gün (Video 1'den sonra) |
| Manual Kod | **0 satır** |

---

## Dersler / PITFALL'lar

1. AI'a kritik kuralları bir kere söylemek yetmez — sürekli hatırlat
2. "Asla kullanıcı verilerini silme" gibi güvenlik talimatları şart
3. Issue kapatma yetkisini AI'a verme — sen onayla
4. AI "yorulunca" kalite düşüyor — temiz talimatla düzelt
5. Feature başına ayrı issue + ayrı commit ile takip et
6. Her yeni oturumda memory.md'den devam et
7. Spam/abuse koruması AI'a bırakılmamalı — çok agresif davranıyor
8. Her feature'dan sonra screenshot al ve doğrula
