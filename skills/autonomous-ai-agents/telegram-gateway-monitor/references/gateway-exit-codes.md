# Gateway Exit Codes (Windows Scheduled Task)

## -1073741510 (0xC000013A)
- **Windows adı:** STATUS_CONTROL_C_EXIT
- **Anlamı:** Process CTRL+C veya taskkill ile sonlandırıldı, veya kendi kendine çöktü
- **Senaryo:** Gateway sessizce öldü, state.json "connected" kaldı

## 267009 (0x41271)
- **Anlamı:** Normal çalışma / başarılı restart
- **Senaryo:** Scheduled task çalışıyor, gateway process canlı

## 259 (0x103)
- **Windows adı:** STILL_ACTIVE
- **Anlamı:** Process hâlâ çalışıyor (scheduled task bekliyor)
- **Not:** Gateway state.json'daki PID ile eşleşmeli

## 0 (0x0)
- **Anlamı:** Başarılı tamamlanma
- **Not:** Gateway sürekli çalışan bir process olduğu için bu çıkış kodu normalde görülmez

## Diagnostic Komutu
```powershell
powershell.exe -NoProfile -Command "schtasks /Query /TN Hermes_Gateway /FO CSV | Select-Object -Skip 1"
```

## Scheduled Task Durum Kodları
| Status | Anlamı |
|--------|--------|
| Running | Gateway process canlı |
| Ready | Schedule'da bekliyor, process yok |
| Disabled | Task devre dışı |
