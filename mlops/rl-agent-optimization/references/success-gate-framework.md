# RL Success Gate — 30-Day Kazanç Değerlendirmesi

## Amaç

RL/MAB sisteminin KAZANÇ üretip üretmediğini ölçen bitiş çizgisi. Bu olmadan sistem sonsuza kadar "altyapı iyileştirme" döngüsünde kalır, asıl kazancı hiç teslim etmez.

## 4 Başarı Kriteri

| # | Metrik | Su_an | Hedef |
|---|--------|-------|-------|
| 1 | MAB karar payı (MAB/toplam) | %10 | >= %30 |
| 2 | MAB isabet (pozitif reward orani) | olculmedi | >= %70 |
| 3 | Beta sagligi (beta>=5 skill sayisi) | 6 skill | <= 3 |
| 4 | Seed verimi (pilot 15'ten dogru kategoride secilen) | 0/15 | >= 10/15 |

## Karar Kuralı

- **4/4 gecerse:** Sistem kazanc uretiyor → shadow'dan canliya gec, seed'i kademeli buyut
- **2-3 gecerse:** Tutmayanlari tek tek ele al, 30 gun daha uzat, ama yeni ozellik EKLEME
- **0-1 gecerse:** Sistem bu haliyle calismiyor. SADELESTIR (MAB'i kaldir, sadece kural katmani) ya da projeyi durdur

## Görev Adımları

1. Dosyayi `rl_observation/rl_success_gate.json` altina kaydet (degismez referans)
2. Her gece 20:00 cron raporuna 4 metrigin GUNCEL degerini ekle
3. 30 gun sonra (14 Temmuz) otomatik KAZANC DEGERLENDIRME raporu uret
4. Degerlendirme gunune kadar bu kriterleri DEGISTIRME
