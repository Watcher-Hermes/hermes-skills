---
name: ai-fullstack-kodlamiyoruz
title: AI ile Full-Stack Web Uygulaması (Prototurk "Kodlamıyoruz" Serisi)
description: "AI kodlama ajanı (Cursor/Claude Code/GitHub Copilot) ile sıfırdan production seviyesinde full-stack web uygulaması kurulumu. Prototurk'ün 'kodlamıyoruz' serisi baz alınmıştır. Stack: Next.js + PostgreSQL + Redis + Railway + Cloudflare R2 + Resend + Playwright."
category: software-development
audience: contributor
tags: [coding, development]
---

> **📁 Seri Referansları:** Her video için session-specific analiz `references/` altında:
> - **Video #1** → [`references/video-1-prototurk-kodlamiyoruz.md`](references/video-1-prototurk-kodlamiyoruz.md) (teknik stack, süreç maliyeti)
> - **Video #2** → [`references/video-2-prototurk-kodlamiyoruz.md`](references/video-2-prototurk-kodlamiyoruz.md) (iteratif geliştirme, admin panel, ~200K satır)
> - **Video #3** → [`references/video-3-prototurk-kodlamiyoruz.md`](references/video-3-prototurk-kodlamiyoruz.md) (production launch, 400K satır, native iOS)
> - **Sistem Tarama Şablonu** → [`templates/sistem-tarama-ve-proje-onerisi.md`](templates/sistem-tarama-ve-proje-onerisi.md) (öğrenme → sistem tarama → proje önerisi pipeline'ı)

# AI ile Full-Stack Web Uygulaması — "Kodlamıyoruz"

## Ne İşe Yarar

Bu skill, bir AI kodlama ajanı (Cursor, Claude Code, GitHub Copilot CLI) kullanarak sıfırdan production seviyesinde bir full-stack web uygulaması kurmak için gereken tüm adımları, araçları ve yapılandırmayı içerir.

Prototurk'ün "kodlamıyoruz" serisindeki yaklaşımın aynısı: **sen kod yazmıyorsun, AI'a yazdırıyorsun** — ama altyapıyı sen kuruyorsun.

---

## GEREKLİ ARAÇLAR & HESAPLAR

### 1. AI Kodlama Aracı (birini seç)
| Araç | Açıklama |
|------|----------|
| **Claude Code CLI** | `claude --acp --stdio` ile terminal-based AI kodlama |
| **Cursor** | VS Code fork, built-in AI, GUI + terminal |
| **GitHub Copilot CLI** | `copilot --acp --stdio` ile terminal-based |
| **OpenCode CLI** | Alternatif, açık kaynak |

### 2. Altyapı & Hosting
| Araç | Ne İçin | Maliyet |
|------|---------|---------|
| **Railway** | Backend hosting, PostgreSQL, Redis, deployment | $5-20/ay (starter) |
| **Cloudflare R2** | Dosya/CDN depolama | $0.015/GB/ay (çok ucuz) |
| **GitHub** | Versiyon kontrolü, repo yönetimi | Ücretsiz |
| **Domain** | Özel domain (prototurk.com gibi) | $10-15/yıl |

### 3. Servisler & API'ler
| Servis | Ne İçin |
|--------|---------|
| **Resend** | E-posta gönderme (auth, bildirim) — $5/ay |
| **GitHub OAuth App** | GitHub hesap bağlama |

### 4. Geliştirme Araçları (yerel)
| Araç | Ne İçin |
|------|---------|
| **Node.js (LTS)** | Runtime |
| **Git** | Versiyon kontrolü |
| **Railway CLI** | Deployment yönetimi |
| **Playwright** | E2E testleri |
| **GitHub CLI (gh)** | Issue/PR yönetimi |

---

## KURULUM ADIMLARI

### ADIM 1 — GitHub Repo Oluştur
```bash
gh repo create prototurk --private --clone
cd prototurk
```

### ADIM 2 — Railway Proje + Servisler
```bash
railway login
railway init
railway add postgresql    # PostgreSQL veritabanı
railway add redis          # Redis cache/queue
```

Railway'de 2 environment oluştur:
- `development` → dev.prototurk.com
- `production` → prototurk.com

### ADIM 3 — Cloudflare R2 Bucket
1. Cloudflare hesabı aç → R2'ye gir
2. Yeni bucket oluştur (ör: `prototurk-cdn`)
3. API token oluştur (public read + private write)
4. CORS ayarlarını yap (frontend domain'ine izin ver)

### ADIM 4 — Resend Hesabı
1. resend.com'a kaydol
2. Domain doğrula (prototurk.com)
3. API key al
4. Email template'lerini hazırla

### ADIM 5 — Railway + GitHub Bağlantısı
```bash
railway link              # Repo'yu Railway'e bağla
railway variables set KEY=VALUE  # environment variable'ları ayarla
```

---

## AI AJAN PROMPT'U (Template)

Bu prompt'u AI kodlama ajanına vererek başlat:

```markdown
# Proje: Prototurk Platformu

Bilgi odaklı bir topluluk platformu. Kullanıcılar içerik paylaşabilir,
birbirini takip edebilir, bildirim alabilir.

## Stack
- Frontend: Next.js 14+ (React, TypeScript, TailwindCSS)
- Backend: Next.js API routes (monorepo)
- Database: PostgreSQL (Railway)
- Cache/Queue: Redis (Railway)
- Storage: Cloudflare R2 (resim/CDN)
- Email: Resend
- Deployment: Railway (Dev + Production)
- Testing: Playwright
- Domain: prototurk.com (production), dev.prototurk.com (development)

## Önemli Kurallar
1. MVP gibi düşünme — direkt production seviyesinde yap
2. Her şey düzenli ve standartlara uygun olmalı
3. Tasarım modern, tipografi iyi seçilmiş, kontrast yüksek
4. Accessibility (erişilebilirlik) yüksek olmalı
5. %100 test coverage hedefle — Playwright E2E testleri yaz
6. Her commit'te issue ID'si geç (örn: "feat: add auth flow #1")
7. Development branch'inde çalış, her issue'yu ayrı commit'le
8. Her değişiklikten sonra screenshot al ve verify et
9. Memory dosyası tut — context sıfırlandığında nerede kaldığını unutma
10. Deployment işlemleri için Railway CLI kullan

## Environment Variables (.env.local)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
RESEND_API_KEY=re_...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=prototurk-cdn
R2_PUBLIC_URL=https://pub-xxxxx.r2.dev
NEXT_PUBLIC_SITE_URL=https://dev.prototurk.com

## İlk Kurulum
1. Next.js projesini oluştur (app router, TypeScript, Tailwind)
2. Prisma + PostgreSQL bağlantısını kur
3. Redis bağlantısını kur
4. Auth sistemi (next-auth veya iron-session)
5. Tasarım sistemini kur (shadcn/ui veya custom)
6. GitHub OAuth entegrasyonu
7. R2 dosya yükleme
8. İlk sayfalar: Feed, Profil, Ayarlar
9. Railway'e deploy et ve çalıştığını doğrula
```

---

## Video #2'den Çıkarımlar — İteratif Geliştirme

### Issue İstatistikleri (Video #2)
| Metrik | Değer |
|--------|-------|
| Toplam Kod | ~200.000 satır (3-4 günde) |
| Açık Issue | 117 |
| Kapalı Issue | 167 |
| Toplam Issue | ~284 |
| Manual Kod | **0 satır** |

### Video #2'de Eklenen Feature'lar
- **Yeni Layout**: Header kaldırıldı → sol sidebar + content alanı
- **Kategori Filtreleri**: Yeniler / Trend / Takip Edilenler
- **Arama**: Fuzzy matching, case-insensitive, kullanıcı önerileri
- **Bildirim Sistemi Geliştirmeleri**: Mention, reply bildirimleri, hover popup kartları
- **Yorumlarda Görsel**: Image upload
- **URL Preview**: Link/YouTube embed otomatik gösterim
- **Lightbox**: Resim büyütme
- **Yer İmleri**: Çalışır hale getirildi
- **Mobil Responsive**: Düzen iyileştirmeleri

### Admin Panel (Back Office)
- **Data Integrity Checker**: Orphan veri temizliği (56 drift → 0), gece cron job
- **Audit Log**: Tüm admin aksiyonları kaydı
- **Soft Delete / Snapshot**: Hard delete öncesi 30 gün snapshot + geri döndürme
- **Kategori CRUD**: Ekle/sil/düzenle yönetimi
- **Change Log**: Commit mesajlarından otomatik changelog, issue + görsel bağlantısı
- **Haftalık AI Digest**: Otomatik içerik üretimi

## AI Davranış Sorunları & Çözümleri (Video #2'den)
| Sorun | Çözüm |
|-------|-------|
| AI "yorulunca" task'ları sallıyor | Kısa, net talimatlar — sürekli doğrulama |
| Talimatları unutuyor | Kritik kuralları sık sık hatırlat |
| Issue'ları izinsiz kapatıyor | `"Ben onaylamadan sakın issue kapatma"` |
| Spam koruması agresif — veri siliyor | `"Kullanıcı verilerini asla ben onaylamadan silme"` |
| İnsani duygu taklidi (4 saat dedi → 5 dk bitti) | Göz ardı et, sonucu bekle |

### Önemli Kural: Feature → Bugfix Döngüsü
Video 1'deki gibi tek bir mega-prompt yerine:
1. Feature yaptır
2. Test et, bug bul
3. Bug fix yaptır
4. Tekrarla
Bu döngü AI'ın context'te kalmasını ve kaliteyi korumasını sağlar.

---

## Video #3'ten Çıkarımlar — Production Launch & Gerçek Dünya

### Nihai İstatistikler
| Metrik | Değer |
|--------|-------|
| Toplam Kod | **~400.000 satır** |
| Toplam Süre | **3-4 hafta** |
| Toplam Issue | **~284+** (117 açık, 167 kapalı) |
| Manual Kod | **Sıfıra yakın** |
| Production URL | prototip.com (canlıda) |

### En Büyük Teknik Karar: Unified Post Model
HER ŞEYİN post olduğu tek tablo modeli. Comment, reply, repost, quote — hepsi aynı model.
- **Öncesi:** Ayrı tablolar → gündem hesaplama çalışmıyor, reply chain bozuk
- **Sonrası:** Tree yapısında posts, her şey aynı model
- AI bu refaktörü "kılçıksız" halletti. Bu en kritik karardı.

### Feed Algorithm (Production)
4 sekme:
1. **Yeniler** — kronolojik
2. **Trend** — algoritmik: engagement score × time decay × new account penalty
3. **Takip** — takip edilenler
4. **Sana Özel** — kişiselleştirilmiş (ortak araçlar, ortak tartışmalar, takip edilenlerin etkileşimi)

**Trend skoru formülü:**
```
ham_score = begeni_sayisi × (takipci_icerki_0.7 : dis_cevre_1.3)
zaman_cezasi = time_decay(post_yasi)
yeni_hesap_cezasi = (hesap < 7_gun) ? × 0.5 : × 1.0
final_score = ham_score × zaman_cezasi × yeni_hesap_cezasi
```

### AI ile Kör Geliştirme (Önemli Deney)
- **Kör mod:** Prompt ver, sonucu kontrol etmeden devam et → işe yarıyor
- **Full kontrol mod:** Her adımı izle, test et → daha kaliteli
- Projenin yarısı kör geliştirildi (çocukla ilgilenirken aralarda prompt gönderdi)
- AI "yorulmuyor" — uzun süreli kör geliştirmelerde bile tutarlı

### UI Detayları — AI'ın Zayıf Noktası
- 400K satırlık projede en çok zorlanılan kısım UI detayları
- Editör, thread çizgileri, görsel hizalama gibi konular
- **Çözüm:** Çizerek anlatmak. AI görsel talimatları iyi anlıyor.
- "400K satır yazdırdım o kadar uğraşmadım ama editör için gerçekten çizdim"

### Admin Panel — Kullanıcı Yönetimi (Production)
Her kullanıcı için:
- Post/beğeni/takipçi/DM/genel istatistikler
- R2 depolama kullanımı
- Kalite/güvenlik skoru
- Not yazma, işlem geçmişi
- Şifre sıfırlama, manuel onay

### Security & API
- API token yönetimi (kullanıcıya özel)
- Rate limiting
- E2E encryption (plan aşaması)

### PERFORMANCE
- SSR'ye geçilen sayfalar anında yükleniyor
- Lighthouse: Mobil 93, Desktop 86 (bazen 100)
- Accessibility: 100

### BONUS: Native iOS (Codex ile)
- Araç: Codex CLI ($200/ay)
- Dil: Swift (native, React Native değil)
- Status: Başlangıç aşaması, temel API entegrasyonu çalışıyor
- Web API kodlarını inceletti → iOS'a uyarladı

### Kapanış Dersi
> "Herkesin yapabileceğini iddia ediyorum ama herkesin bu seviyede yapabileceğini zannetmiyorum. Doğru soruyu kurabilmek, doğru iletişimi kurabilmek, onunla aynı düşünebilmek çok önemli."

Teknik bilgi + AI iletişim becerisi = production-ready ürün.

---

## AI AJAN ÇALIŞMA DÖNGÜSÜ

### 1. Sprint/Issue Yapısı
AI ajanı GitHub'da milestone'lar ve issue'lar açsın:

```
Milestone 0 → Infrastructure (DB, Redis, deployment)
Milestone 0.5 → Auth (giriş, kayıt, oturum)
Milestone 1 → Feed (ana akış, gönderi listeleme)
Milestone 2 → Post Creation (içerik oluşturma/editör)
...
```

### 2. Her Sprint'te
1. Issue'ları oluştur (açıklama + task list + gerekirse görsel)
2. Her issue'yu branch açıp çöz
3. Test yaz (Playwright)
4. Commit → `git commit -m "feat: #12 post editor"`
5. Deploy → dev ortamına
6. Screenshot al
7. Kontrol et → sorun yoksa merge

### 3. Context Yönetimi
AI ajanının memory'si sıfırlandığında:
```
📁 memory.md dosyası oluştur:
- Alınan kararlar
- Tamamlanan issue'lar
- Bekleyen işler
- Stack/teknoloji seçimleri
```

Her yeni session'da:
```
📖 memory.md'yi oku
📋 Kaldığın issue'dan devam et
```

---

## FEATURE'LER (Prototurk Platform)

| # | Feature | Açıklama |
|---|---------|----------|
| 1 | **Feed** | Yeniler, Trend, Takip edilenler — skeleton loading |
| 2 | **Post Editor** | Zengin metin editörü, taslak kaydetme |
| 3 | **Keşfet** | Discover sayfası |
| 4 | **Bildirimler** | Real-time + e-posta bildirimleri |
| 5 | **Yer İmleri** | Gönderi kaydetme |
| 6 | **Launchpad** | Proje vitrini |
| 7 | **Profil** | GitHub entegrasyonu, kontribüsyon, pinned repo |
| 8 | **Ayarlar** | Profil düzenleme, şifre, oturum yönetimi |
| 9 | **PWA** | Progressive Web App |
| 10 | **GitHub Showcase** | GitHub profili bağlama |

---

## MALİYET TABLOSU

| Servis | Aylık Maliyet |
|--------|--------------|
| Railway (Starter) | $5-20 |
| Cloudflare R2 | ~$1-2 (çok düşük kullanım) |
| Resend | $5 |
| Domain | ~$1/ay |
| **Toplam** | **~$12-28/ay** |

AI API maliyeti ekstra (Claude Code/Cursor abonelik).

---

## BAŞLANGIÇ PROMPT'U (kullanıcıya)

```
Bu büyük ve heyecanlı bir proje! Sıfırdan production seviyesinde
bir platform inşa ediyoruz. Adım adım ilerleyelim.

İlk olarak:
1. GitHub repo'sunu oluştur
2. Railway'de PostgreSQL + Redis + uygulama servislerini kur
3. Cloudflare R2 bucket'ı oluştur
4. Resend'de domain doğrula
5. Next.js projesini başlat
6. AI ajanına yukarıdaki prompt'u ver
```

---

## PITFALL'LAR

- **Context sıfırlanması**: AI ajanı 1M token'da context kaybeder. Memory.md ile çöz.
- **Railway credential'ları**: Environment variable'ları Railway dashboard'dan ayarla, `.env`'e yazma.
- **R2 CORS**: Frontend'den direkt yükleme yapacaksan CORS ayarlarını unutma.
- **Test coverage düşüklüğü**: AI bazen test yazmayı atlar. "Test yaz" diye zorla.
- **Deployment hataları**: Railway CLI login'inin hala aktif olduğunu kontrol et.
- **Rate limiting**: Free tier AI modelleri (OpenRouter free) 429 dönebilir. Fallback chain kullan.
