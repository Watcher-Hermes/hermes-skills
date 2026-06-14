@echo off
REM HERMES HAFTALIK BAKIM STARTUP
REM Bilgisayar acilinca calisir, gun Carsamba ise flag olusturur

for /f "tokens=3" %%a in ('wmic path win32_localtime get dayofweek') do set gun=%%a
set gun=%gun: =%

if "%gun%"=="3" (
    echo [Hermes] Carsamba - Haftalik bakim flag'i olusturuluyor...
    echo %date% %time% > "%USERPROFILE%\AppData\Local\hermes\haftalik-bakim.flag"

    REM Gateway calismiyorsa baslat
    schtasks /Query /TN Hermes_Gateway /FO CSV 2>nul | findstr /C:"Running" >nul
    if errorlevel 1 (
        echo [Hermes] Gateway baslatiliyor...
        powershell -NoProfile -Command "Start-ScheduledTask -TaskName Hermes_Gateway"
    ) else (
        echo [Hermes] Gateway zaten calisiyor
    )
    echo [Hermes] Hazir - Cron job bakimi tetikleyecek.
) else (
    echo [Hermes] Bugun Carsamba degil (%gun%), bakim atlandi.
)
