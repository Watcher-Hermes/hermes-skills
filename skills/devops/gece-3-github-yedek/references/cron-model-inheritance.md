# Cron Job Model Inheritance (400 Hatası)

## Tanı

Cron job çalıştığında şu hata düşerse:

```
RuntimeError: Error code: 400 - {'error': {'message': '<virgüllü model listesi> is not a valid model ID', 'code': 400}}
```

**Sebep**: Job'da `model: null` → scheduler oturumdaki model konfigürasyonunu miras alır.
Oturumda birden çok model varsa (fallback zinciri), hepsi virgülle birleştirilip
tek model olarak API'ya gönderilir. API geçerli bir model ID'si beklemez.

## Teşhis

1. `cronjob(action='list')` ile job'ı kontrol et:
   - `model: null` → model miras alınıyor, sorun var
   - `provider: null` → provider da miras alınıyor

2. Hata çıktısı: cron çıktı klasörü `C:\Users\marko\AppData\Local\hermes\cron\output\<job_id>/` altında
   en son `.md` dosyasının sonunda `## Error` bölümü.

3. Model listesi miras alımı, session başlatılırken belirlenir.
   Değişirse (örneğin: `/model` komutu ile), mevcut job'lar güncellenmez.

## Çözüm

```python
from hermes_tools import cronjob

cronjob(
    action='update',
    job_id='<JOB_ID>',       # cronjob list'ten al
    model={'model': '<TEK_MODEL>', 'provider': '<PROVIDER>'}
)
```

Örnek:
```python
cronjob(
    action='update',
    job_id='6b3a7cd39da0',
    model={'model': 'deepseek/deepseek-v4-flash', 'provider': 'openrouter'}
)
```

## Doğrulama

Güncellemeden sonra:
1. `cronjob(action='run', job_id='...')` ile hemen çalıştır
2. Çıktı klasörüne yeni dosya gelene kadar bekle (~30-90 sn)
3. Yeni dosyada `## Error` bölümü OLMADIĞINI doğrula
4. `last_status: error` → HALA hatalıysa, çıktıyı oku

## Notlar

- Job'a model atanmışsa (`model` alanı dolu), model listesi değişse bile
  etkilenmez — kendi modelini kullanır.
- Model güncellemesinden sonra bir sonraki schedule'a kadar beklemek gerekmez;
  `run` action'ı job'ı hemen tetikler.
- Bu sorun yalnızca **cron job**'ları etkiler. Normal sohbet oturumları
  model listesini doğru işler (API her model'i sırayla dener).
