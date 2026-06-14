# Windows PID Canlılık Kontrolü — Güvenilir Yöntemler

## Keşif (2026-06-11)

Gateway watchdog cron job sırasında fark edildi: `gateway_state.json` PID 19152
gösteriyordu ama aşağıdaki komutlar hatalıydı:

```bash
# ❌ FALSE NEGATIVE — Git Bash'te güvenilmez
tasklist /FI "PID eq 19152" /FO CSV    # → "PID not found" döndü (aslında canlıydı)
wmic process where "name='python.exe'"  # → hiçbir şey döndürmedi
```

Doğru yöntem:

```powershell
# ✅ GÜVENİLİR — PowerShell Get-Process
powershell.exe -NoProfile -Command "Get-Process -Id 19152 -ErrorAction SilentlyContinue | Format-List Id,ProcessName,StartTime"
# → Id=19152, ProcessName=python, StartTime=10.06.2026 22:22:03
```

## Neden?

- Git Bash (MSYS2) içinde `tasklist` ve `wmic` PID filtrelerinde
  Python process'lerini (python.exe) bazen false negative döndürür.
- Sebep: MSYS2'nin Windows process tablosunu çevirme şeklindeki farklılık.
- `Get-Process` PowerShell cmdlet'i doğrudan WMI/CIM üzerinden çalıştığı
  için her zaman güvenilirdir.

## Güvenilirlik Sıralaması

| Yöntem | Komut | Güvenilirlik |
|--------|-------|-------------|
| ✅ | `Get-Process -Id <PID>` (PowerShell) | Her zaman doğru |
| ✅ | `hermes gateway status` (main.py) | Çalışan process'i her zaman görür |
| ⚠️ | `tasklist /FI "PID eq X"` (Git Bash) | Bazen false negative (Python) |
| ❌ | `wmic process where "name='python.exe'"` | Bazen boş döner |

## Öneri

PID canlılık kontrolünde sıra:
1. Önce `hermes gateway status` dene (en hızlı, en güvenilir)
2. Onay gerekiyorsa `Get-Process -Id <PID>` PowerShell ile
3. `tasklist` ve `wmic`'e sadece ilk iki yöntem çalışmazsa başvur
