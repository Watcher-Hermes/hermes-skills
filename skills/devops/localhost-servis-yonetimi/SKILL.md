---
name: localhost-servis-yonetimi
description: >-
  Manage localhost services, ports, health checks, and desktop shortcuts
  for HTTP services (Hermes Studio, LM Studio, Streamlit, n8n, etc.)
version: 1.0.0
author: hermes-agent
license: MIT
metadata:
  hermes:
    tags: [localhost, port, servis, dashboard, shortcut, windows]
audience: maintainer
related_skills: []
---

# Localhost Servis Yönetimi

## Overview

Hermes'in çalıştırdığı yerel HTTP servislerini yönetmek için:
- Port durumu kontrolü (açık/kapalı)
- Servis başlatma/durdurma
- Masaüstü kısayol oluşturma
- README ile dokümantasyon

## Desktop Shortcut Location

Windows masaüstü kısayolları için DOĞRU YOL:
```
C:\Users\marko\OneDrive\Desktop\Hermes-Localhosts\
```

NOT: `C:\Users\marko\Desktop` veya `C:\Users\marko\OneDrive\Masaüstü` DEĞİL.

## Known Services

| Port | Servis | Durum | Başlatma |
|------|--------|-------|----------|
| 8648 | Hermes Studio | `npm install -g hermes-web-ui && hermes-web-ui start` |
| 1234 | LM Studio API | LM Studio uygulaması → Settings → Local Server |
| 8501 | Streamlit | Mevcut bir Streamlit uygulaması çalışıyorsa |
| 5678 | n8n | `n8n start --port=5678` (background) |
| 8082 | Web App | Belirlenmedi |
| 7000 | Servis | Belirlenmedi |

## Port Health Check

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(('localhost', PORT))
    print("ACIK")
except:
    print("KAPALI")
finally:
    s.close()
```

## Creating Desktop Shortcuts (.url)

Windows .url dosyası formatı:

```
[InternetShortcut]
URL=http://localhost:PORT
```

Hedef klasöre yaz:

```python
with open(f"{desktop}/Hermes-Localhosts/{name}.url", "w") as f:
    f.write(f"[InternetShortcut]\nURL={target}\n")
```

## Pitfalls

1. **YANLIŞ MASAÜSTÜ YOLU** — Asla `C:\Users\marko\Desktop` kullanma. Doğru yol: `C:\Users\marko\OneDrive\Desktop`
2. **Port değişebilir** — n8n ve Hermes Studio alternatif portta başlatılabilir; kontrol et
3. **Servis başlatma onayı** — Yeni servis başlatmadan önce kullanıcıya sor
4. **n8n background** — n8n `&` ile değil, `terminal(background=true)` ile başlat
