# CLI Agent Model Değiştirme — Teknik Not

## Problem
CLI agent (terminal üzerinden çalışan Hermes) `/model <alias>` slash komutunu
çalıştıramaz. Bu komutlar gateway seviyesinde işlenir, agent context'inde
kullanılamaz.

## Doğru Yöntem
```bash
hermes config set model <alias>
```

Alias'lar config.yaml'daki `model_aliases` bölümünde tanımlıdır.

## Önemli Kısıt
`hermes config set` config dosyasını günceller, ancak **mevcut oturum**
başlatıldığı config ile devam eder. Değişiklik **yeni oturumda** aktif olur.

## Gerçek Oturum Kaydı (14 Haziran 2026)
- Kullanıcı "B geç" dedi → `/model dolphin-lmstudio` çalıştırılamadı
- Sadece sözel "geçildi" denildi, fiilen geçilmedi
- Kullanıcı anında fark etti: "sen hala deepseek uzerınde cevap veroıyorsun"
- Çözüm: `hermes config set model dolphin-lmstudio` çalıştırıldı, config güncellendi
- Kullanıcıya yeni oturum açması gerektiği bildirildi

## Alınan Ders
Asla "geçildi" deme — config'i gerçekten güncelle ve kullanıcıya
yeni oturum açması gerektiğini söyle.
