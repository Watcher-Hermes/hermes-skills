# Kali Linux Ağ Taraması — Komut Seti

WiFi ağındaki (`192.168.0.0/24`) cihazları bulmak için Kali VM'den çalıştırılan komutlar.

## Ön Koşul

Kali bridged modda çalışıyor, eth1 (bridged) IP `192.168.0.19/24` üzerinden ana ağa bağlı.
eth0 (host-only) ayrı subnet (192.168.56.x) — tarama için eth1 kullanılmalı.

## Komut Sırası

### 1. ARP tablosu (en hızlı, zaten bilinenler)

```bash
arp -n
```

Çıktı: aktive ARP girişlerini gösterir. Sadece daha önce iletişim kurulan cihazlar listelenir.
Amaç: hızlı bakış, tam liste vermez.

### 2. ICMP ping sweep (tüm subnet)

```bash
for i in $(seq 1 254); do
  ping -c 1 -W 1 192.168.0.$i >/dev/null 2>&1 &&
    echo "$i alive" &
done
wait
```

Çıktı: sadece IP numaraları (canlı olanlar). MAC adresi vermez.

### 3. Nmap ping sweep (önerilen — MAC + vendor)

```bash
sudo nmap -sn 192.168.0.0/24
```

Detaylı:
```bash
sudo nmap -sn 192.168.0.0/24 | grep -E "Nmap|Host|MAC"
```

Çıktı:
- Her canlı host için IP, MAC adresi, vendor (üretici adı)
- Süre: ~3-4 saniye (254 host ping)
- Vendor bilgisi cihaz tipini tahmin etmeye yardımcı olur (Hikvision = kamera vs.)

### 4. arp-scan (alternatif, MAC + vendor)

```bash
sudo arp-scan --interface eth1 --localnet
```

Notlar:
- `--interface eth1` mecburi — eth0'da IP yok
- `ieee-oui.txt` / `mac-vendor.txt` permission denied uyarıları normaldir, yine de çalışır
- Çıktı: IP + MAC + vendor (nmap'ten daha kısa format)
- 3 hostlu bir ağda bile tüm /24'ü tarar (254 host)

## Bulunan Cihazlar (örnek)

| IP | MAC | Vendor | Muhtemel |
|----|-----|--------|----------|
| 192.168.0.1 | 98:F2:17:02:03:4F | Castlenet Tech | Modem/Router |
| 192.168.0.16 | B8:C6:AA:FD:52:D6 | Earda Tech | Akıllı ev cihazı |
| 192.168.0.17 | E0:BA:AD:17:B1:84 | Hikvision | IP Kamera |
| 192.168.0.19 | 08:00:27:BC:0E:BA | Oracle/VirtualBox | Kali VM |
| 192.168.0.20 | 88:F4:DA:D3:24:3A | Intel Corp | Windows host |

## Pitfall'lar

- `arp-scan` vendor dosyasına erişemezse `Permission denied` basar, yok say
- Ping sweep'te 254 host için fork beklemek gerek — arka planda çalıştır (`&`)
- Nmap `-sn` genelde root gerektirir, `sudo` ile çalıştır
- Bridged ağda IP değişebilir (DHCP) — önce Kali'nin güncel IP'sini kontrol et

## zsh Tuzakları (Kali Default Shell)

Kali'de default shell **zsh**'dir. Windows bash/MSYS üzerinden SSH ile komut gönderirken bu tuzaklara dikkat:

### 1. `===` glob hatası

```bash
# HATA - zsh:1: == not found
ssh kali@... 'echo "=== ADIM 1 ==="'

# DOĞRU - tire/alt çizgi kullan
ssh kali@... 'echo "---- ADIM 1 ----"'
```

Sebep: zsh `=` işaretini string operatörü olarak yorumlar, tek tırnak işe yaramaz.

### 2. `?` glob hatası

```bash
# HATA - zsh:1: no matches found: tararsam?
ssh kali@... 'echo "tararsam?"'

# DOĞRU - soru işareti yok
ssh kali@... 'echo "tararsam"'
```

Sebep: `?` zsh'ta tek karakter wildcard'ıdır.

### 3. Boşluklu string'ler (güvenilir yöntem)

Windows bash/MSYS üzerinden SSH'ta boşluklu komutlar şöyle çalışır:

```bash
# DOĞRU - çift tırnak içinde string
sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@IP 'echo "Bu calisir"'

# DOĞRU - argüman ayrı
sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@IP echo Bu da calisir

# DOĞRU - tek tırnak ile değişken yoksa
sshpass -p 'kali' ssh kali@IP 'sudo nmap -sn 192.168.0.0/24'

# Her komut ayrı bir terminal() çağrısı olmalı - boşluk korunur
```

### 4. tmux send-keys ile boşluk SORUNU (kullanma)

```bash
# CALISMIYOR - boşluklar yutulur
ssh kali@... 'tmux send-keys -t hermes "echo merhaba dunya" Enter'

# Cikti: echo merhaba dunya (boşluksuz: echo merhabadunya)

# Bunun yerine dogrudan ssh exec kullan
ssh kali@... 'echo merhaba dunya'
```

Sebep: MSYS/bash + SSH + tmux send-keys arasındaki argüman ayrıştırma katmanları boşlukları yutar. `-l` literal flag'i ve `C-m` argümanı da işe yaramaz — Enter literal string olarak gömülür.

### 5. sudo komutlarında tty

`sudo` gerektiren komutlar (arp-scan, nmap) için `sshpass` yeterlidir, ayrıca `-tt` flag'ine gerek yoktur. Ancak çıktıdaki `WARNING: Cannot open MAC/Vendor file ieee-oui.txt: Permission denied` mesajları normaldir — arp-scan yine de çalışır.

## Doğrudan SSH ile Adım Adım Komut Gösterme

```bash
# KALI TERMINALINDE YAZILAN KOMUTLAR:
# (her biri ayrı terminal() çağrısı)

# Adım 1 - Açıklama
sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@192.168.0.19 'echo "ADIM 1: arp-scan ile ag taramasi"'

# Adım 2 - Asıl komut
sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@192.168.0.19 'sudo arp-scan --interface eth1 --localnet'

# Adım 3 - Sıradaki adım
sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@192.168.0.19 'echo "ADIM 2: ARP tablosu"'

# Adım 4
sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@192.168.0.19 'arp -n'
```

Bu yöntem tmux'tan daha güvenilirdir çünkü her komut ayrı bir shell oturumunda çalışır, boşluklar korunur, timeout yönetimi basittir.
