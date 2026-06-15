# Hermes Agent Entegrasyon Deseni

Reymen Proje'de Nous Research Hermes Agent'ı entegre etmek için kullanılan desen.

## Mimari

```
C:\hermes\                         ← Hermes Agent (bağımsız repo)
  cli.py (731KB)                   ← Ana CLI
  agent/                           ← Agent runtime modülleri
  skills/                          ← 100+ skill
  apps/                            ← Uygulamalar
  cron/                            ← Zamanlanmış görevler
  .env                             ← Hermes config (Reymen'den senkronize)
  cli-config.yaml                  ← Hermes ayarları

Reymen Proje/
  hermes_cli.py                    ← Wrapper: env sync + Hermes CLI çağırma
  reyemen.bat                      ← "reyemen.bat hermes ..." ile erişim
```

## Wrapper (hermes_cli.py) İşleyişi

1. **Env senkronizasyonu**: Reymen .env'deki anahtarları Hermes .env'ye kopyala (boş/*** olanları doldur)
2. **Subprocess çağrısı**: `python C:\hermes\cli.py <args>` çalıştır
3. **Çıktı yönlendirme**: stdout/stderr kullanıcıya göster

```python
def env_aktar():
    reymen = {}  # Reymen .env'den oku
    hermes = []  # Hermes .env'yi güncelle
    # ... senkronizasyon mantığı

def hermes_cagir(args):
    subprocess.run([sys.executable, HERMES_CLI, *args])
```

## .bat Entegrasyonu

```
reyemen.bat hermes doctor         # Hermes sağlık kontrolü
reyemen.bat hermes gateway start  # Gateway başlat
reyemen.bat hermes skills list    # Skill listele
```

## Önemli

- Hermes Agent kendi reposunda kalır (taşınmaz)
- Yalnızca wrapper (hermes_cli.py) ve .bat referansı Reymen Proje'de
- Çift yönlü env senkronizasyonu: Reymen'de değişiklik → Hermes'e yansır
- Hermes .git (280MB) korunur — kendi git geçmişi bozulmaz
