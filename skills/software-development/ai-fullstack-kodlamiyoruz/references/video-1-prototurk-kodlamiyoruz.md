# Video #1 Referansı — PROTOTURK "kodlamıyoruz - 1. bölüm"

**URL:** https://www.youtube.com/watch?v=0Dsaa9hvUTE
**Tarih:** 2026-06-10
**Kanal:** PROTOTURK
**Başlık:** "kodlamıyoruz - 1. bölüm"

## Özet
Full-stack web uygulamasının AI coding agent'lerle (Claude Code/Cursor) sıfırdan inşası. Geliştirici neredeyse hiç kod yazmıyor — tüm kod AI tarafından üretiliyor.

## Tech Stack
| Bileşen | Teknoloji |
|---------|-----------|
| Frontend | Next.js + TypeScript + Tailwind |
| Backend | Next.js API routes |
| Database | PostgreSQL (Railway) |
| Cache/Queue | Redis (Railway) |
| File Storage | Cloudflare R2 |
| Email | Resend |
| E2E Testing | Playwright |
| AI Agent | Claude Code + GitHub Copilot |
| Deployment | Railway |

## Süreç
- 10 sprint, 80+ GitHub issue
- ~34M token tüketimi
- Toplam maliyet ~$2,350 (AI API + deployment)
- 0 manuel kod yazımı (sadece prompt mühendisliği)

## Kullanıcıdan Gelen Talimat
- "Bu uygulamadan yapacağız" — kullanıcı bu videodaki yaklaşımı kendi projesinde uygulayacak
- "Hangi uygulamalar gerek, ne yazılım gerekli belirle ve skill oluştur" — video analiz edilip `ai-fullstack-kodlamiyoruz` skill'i oluşturuldu
- Diğer 2 video beklemede — video #2 ve #3 geldiğinde skill genişletilecek

## Önemli Notlar
- Video 3 bölümlük bir serinin ilk videosu
- Kullanıcı bu seriyi takip ederek AI + full-stack proje geliştirmeyi öğrenmek istiyor
- `ai-fullstack-kodlamiyoruz` skill'i ana kaynak; bu dosya session-specific detayları içerir
