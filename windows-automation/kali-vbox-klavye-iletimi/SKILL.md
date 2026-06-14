---
name: kali-vbox-klavye-iletimi
description: VirtualBox VM icindeki Kali Linux terminaline klavye girisini VBoxManage keyboardputstring ile yapma + USB WiFi passthrough ve cevre ag taramasi.
---

# Kali VirtualBox Klavye Iletimi

## ÖNEMLİ — İlk Tercih Guest Control Olmalı

Terminal açmak veya komut çalıştırmak için **önce guestcontrol dene**, keyboardputstring sonra:
- GuestControl: `VBoxManage guestcontrol "kal" start --exe "/usr/bin/qterminal" --username kali --password kali`
- GuestControl çalışmazsa (Guest Additions yoksa) keyboardputstring'e düş
- Detaylar için `virtualbox` skill'inde "Guest Control" bölümüne bak

VirtualBox VM'deki Kali Linux terminaline klavye girisini VBoxManage ile yap.

## ZORUNLU ILK ADIM — Ekran Kontrolu

Kali VM'e komut gondermeden ONCE:

1. **Ekran goruntusu al**:
   ```bash
   "C:\\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" screenshotpng "C:\\Users\\marko\\Desktop\\kali_desktop.png"
   ```

2. **vision_analyze ile kontrol et**: Masaustu acik mi? Terminal penceresi gorunuyor mu?
   - Eger **login ekrani** gorunuyorsa → kullanici adi `kali` ve sifre `1234` ile gir
   - Eger **masaustu** aciksa (taskbar, ikonlar, terminal penceresi) → dogrudan komut yaz
   - VM kapaliysa → once `startvm` ile baslat

3. **Eger terminal aciksa** (imlec bekliyor) → `keyboardputstring` ile dogrudan komut yaz, `$'\n'` ile Enter gonder

4. **SSH gereksiz**: Masaustu acikken terminale yazmak icin SSH'e gerek yok. `keyboardputstring` yeterli.

## Ne Zaman Kullanilir

- Kullanicinin VM terminalinde yazilan komutlari gormesi gerektiginde
- `keyboardputstring` ile dogrudan VM'e klavye gonderimi istendiginde
- Terminal UI / SSH ciktisi yerine VM ekraninda goruntuleme gerektiginde

## Prerequisites

- VirtualBox VM "kal" (veya dogru VM adi) mevcut olmali
- VBoxManage.exe yolu: `C:\Program Files\Oracle\VirtualBox\VBoxManage.exe`
- VM calisiyor durumda olmali

## Komutlar

### Tek satir yazma
```bash
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring "komut buraya"
```

### Enter tusu gonderme
```bash
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
```

### Zincirleme (birden fazla satir)
```bash
"VBoxManage.exe" controlvm "kal" keyboardputstring "komut1" && sleep 1 && "VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
```

### Ekrani temizleme
```bash
"VBoxManage.exe" controlvm "kal" keyboardputstring "clear" && "VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
```

## KULLANICI KURALLARI (DEGISTIRILEMEZ)

1. **ONCE EKRANA BAK**: Her VM komutundan once `screenshotpng` al, `vision_analyze` ile kontrol et. Terminal aciksa direkt yaz, login ekraniysa sifre gir, VM kapaliysa baslat.

2. **SSH ARKADA, VBoxManage ONCE**: Karmasik islemleri SSH ile arka planda calistir, sonuclari `keyboardputstring` ile VM terminaline yaz. SSH sadece data almak icin.

3. **help ile COZUM ARA**: VM'de bir komut calismazsa veya sonuc beklendigi gibi degilse, once Kali'de `--help`, `man`, veya `help` dene. Disaridan arastirma yapmadan once VM icinde cozum ara.

4. **TURKCE Q KLAVYE HATASI**: `keyboardputstring` ile `kali` yazarken dikkat — TURKCE 'i' (ı) degil, INGILIZCE 'i' (i) kullan. `kali` = k-a-l-i (4 ASCII karakter). `kalı` = k-a-l-ı (Turkce 'ı', isaretsiz). Yanlis yazarsan login ekraninda kalirsin.
   - Cozum: `keyboardputstring` ile sadece ASCII karakterleri kullan. Ozel Turkce karakterlerden kacin.

## Dikkat Edilecekler

1. **Yonlendirme (`>` , `|`) sorunu**: `>` , `|` gibi ozel karakterler `keyboardputstring` ile gonderildiginde VM terminalinde dogru calismayabilir. Karmasik komutlar icin once SSH ile calistir, sonucu `echo` ile VM'e yazdir.

2. **Bekleme suresi**: Her komuttan sonra `sleep N` ile yeterli sure ver. ozellikle `nmap`, `arp-scan` gibi uzun sureli komutlarda 3-5 saniye beklenmeli.

3. **Enter ayri gonderilmeli**: `keyboardputstring` sadece metin gonderir, Enter tusu ayrica `$'\n'` ile gonderilmelidir.

4. **Dosyaya yonlendirme calismaz**: `komut > /tmp/cikti.txt` gibi yonlendirmeler `keyboardputstring` ile calismaz. Bunun yerine SSH ile calistir, sonra `echo` ile VM'e ozeti yazdir.

## SSH + VBoxManage Birlikte Kullanim

Karmasik islemleri SSH ile arka planda calistir, sonucu `echo` komutlariyla VM terminaline yazdir:

```bash
# 1. SSH ile komutu calistir, ciktiyi al
CIKTI=$(sshpass -p 'kali' ssh kali@192.168.0.19 'sudo nmap -sn 192.168.0.0/24 2>&1')

# 2. Ozeti VM terminaline yazdir
"VBoxManage.exe" controlvm "kal" keyboardputstring "echo 'Ozet: 6 cihaz bulundu'"
"VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
```

## Ag Tarama Karsilastirmasi (arp-scan vs nmap)

| Ozelik | arp-scan | nmap -sn |
|--------|----------|----------|
| Sure | ~1.8 sn | ~3.5 sn |
| Cihaz sayisi | 7 (daha fazla) | 6 |
| Vendor bilgisi | Yok | Var |
| Protokol | ARP (L2) | ICMP+TCP (L3) |
| Kendini listeler | Hayir | Evet |

**Tavsiye**: Once `arp-scan` ile hizli on tarama, sonra `nmap -sn` ile vendor detayi.

## Ornek: VirtualBox'a dogrudan komut yazip calistirma

```bash
# Adim 1: Giris mesaji
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring "echo Merhaba, ben Hermes" && "C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
sleep 1

# Adim 2: Ag tarama
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring "sudo arp-scan --interface eth1 --localnet" && "C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
sleep 3

# Adim 3: Detayli tarama
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring "sudo nmap -sn 192.168.0.0/24" && "C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
sleep 5
```

## USB WiFi Passthrough (Ralink RT2501/RT2573 + benzeri)

Fiziksel bir USB WiFi adaptörünü Windows host'tan Kali VM'e passthrough yapma.

### Adim Adim Pipeline

```bash
# 1. Windows'ta USB aygitini bul
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" list usbhost
# Cikti: VendorId 0x148f, ProductId 0x2573 (Ralink)

# 2. USB filtresi ekle (VM KAPALIYKEN)
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" usbfilter add 0 \
  --target "kal" \
  --name "Ralink WiFi" \
  --vendorid 148f \
  --productid 2573

# 3. xHCI (USB 3.0) kontrolcuyu etkinlestir
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" modifyvm "kal" --usbxhci on

# 4. VM'i baslat
"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe" startvm "kal" --type headless

# 5. Kali'de dogrula (SSH ile)
sshpass -p 'kali' ssh kali@<IP> 'lsusb | grep -i ralink'
# Beklenen: Bus 001 Device 002: ID 148f:2573 Ralink Technology, Corp. RT2501/RT2573

# 6. Driver/firmware kontrol
sshpass -p 'kali' ssh kali@<IP> 'dmesg | grep -iE "rt73|ralink|firm"'
# rt73usb driver + rt73.bin firmware (v1.7)
```

### WiFi Arayuzunu Yapilandirma

```bash
# Arayuz adini bul
ssh kali@<IP> 'iw dev'
# wlan0

# Arayuzu aktif et
ssh kali@<IP> 'sudo ip link set wlan0 up'

# Power save kapat (arama icin onemli)
ssh kali@<IP> 'sudo iw dev wlan0 set power_save off'

# Bolge kodunu ayarla (YOKSA passive-scan olur, hic ag bulunmaz!)
ssh kali@<IP> 'sudo iw reg set DE'
# veya: sudo iw reg set TR
```

### Cevre WiFi Ag Tarama

```bash
# AKTIF TARAMA — tum kanallari tara (ONERILEN)
ssh kali@<IP> 'sudo iw dev wlan0 scan'
# Bu, kanal 1-13 arasi tum aglari bulur. Telefon hotspot'lari da gorur.

# SADECE su anki kanalda tara (KISITLI!)
ssh kali@<IP> 'sudo iw dev wlan0 scan -u'
# -u flag'i sadece o anki aktif kanali tarar. Diger kanallardaki aglari KACIRIR.
# Ornek: Kanal 1'deyken kanal 11'deki telefon hotspot'ini goremezsin.

# veya eski API:
ssh kali@<IP> 'sudo iwlist wlan0 scanning'
```

### VBoxManage ile Kali Ekraninda Gosterme

```bash
# SSH'den alinan sonuclari echo ile VM ekranina yaz
"VBoxManage.exe" controlvm "kal" keyboardputstring "echo 'TURKSAT-KABLONET-U0JG-2.4G'"
"VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
"VBoxManage.exe" controlvm "kal" keyboardputstring "echo '  Sinyal: -22 dBm'"
"VBoxManage.exe" controlvm "kal" keyboardputstring $'\n'
```

### Ralink RT2501/RT2573 Karakteristigi

| Ozelik | Deger |
|--------|-------|
| Chipset | rt2573 |
| Driver | rt73usb |
| Firmware | rt73.bin (v1.7) |
| Frekans | 2.4 GHz (sadece b/g) |
| Maks hiz | 54 Mbps |
| Kanal | 1-13 |

### Dikkat Edilecekler

1. **Bolge kodu kritik**: `iw reg set` yapilmazsa country=00 olur, tum kanallar PASSIVE-SCAN modunda calisir. Bu durumda arayuz sadece beacon duydugu aglari gorebilir — hicbir ag bulunamayabilir. Her zaman `iw reg set DE`/`TR` ile aktif taramayi etkinlestir.

2. **`iwlist` vs `iw scan`**: `iwlist` wireless extensions kullanir (Wi-Fi 7'de calismaz). `iw dev wlan0 scan -u` nl80211 ile daha guncel ve guvenilir. Ilki calismazsa ikinciyi dene.

3. **USB filtresi VM kapaliyken eklenmeli**: Running VM'e filtre eklenemez, once poweroff.

4. **xHCI controller**: VirtualBox varsayilan olarak OHCI/EHCI kullanir. USB 3.0 adaptorler icin `--usbxhci on` sart. Ralink gibi eski USB 2.0 adaptorlerde de bazen gerekebilir.

5. **VM reset sonrasi IP degisimi**: Kali bridged DHCP kullaniyorsa VM reset sonrasi yeni IP alabilir. MAC adresinden IP bul:
   ```bash
   arp -a | grep "08-00-27"
   ```

6. **`iw dev wlan0 scan` bos donerse**: Arayuz down olabilir (`ip link set wlan0 up`), power save acik olabilir (`set power_save off`), veya bolge kodu ayarlanmamis olabilir (`iw reg set DE`).

7. **`-u` flag'i kandirir**: `iw dev wlan0 scan -u` SADECE su anki kanali tarar. Telefon hotspot'i gibi baska kanaldaki aglari bulamazsin. Her zaman `-u` OLMADAN tara (`iw dev wlan0 scan`). Gercek tarama 5-15 saniye surer.

8. **Telefon hotspot'i AP olarak gorunur**: Telefonun WiFi erisim noktasi (hotspot) aciksa, Kali bunu normal bir AP gibi gorur — STA (istasyon) degil. SSID'si hotspot adi neyse o olarak listelenir. Sinyal seviyesi cok yuksekse (-12 dBm gibi) yaninda demektir.

## Problem Giderme

- **`VBoxManage: command not found`**: Tam yol kullan: `"C:\Program Files/Oracle/VirtualBox/VBoxManage.exe"`
- **`keyboardputstring` calismiyor**: VM'in calistigini kontrol et: `"VBoxManage.exe" list runningvms`
- **Karmasik komut calismiyor**: Ozel karakterlerden kurtul, komutu basitlestir
- **Cikti gelmiyor**: `sleep` suresini artir, komutun bitmesini bekle
- **USB WiFi Kali'de gorunmuyor**: xHCI acik mi kontrol et (`showvminfo`), filtre dogru mu, VM yeniden baslatildi mi
- **`lsusb`'de var ama `iw dev`'de yok**: Driver yuklenmemis olabilir — `dmesg | grep rt73` ile kontrol et
- **`iwlist wlan0 scanning`: No scan results**: Once `iw reg set DE`, sonra `ip link set wlan0 up`, sonra `iw dev wlan0 scan -u` dene
6. **WiFi adaptor cok yavas / sadece 2.4 GHz**: Ralink RT2501/RT2573 802.11 b/g — 5 GHz desteklemez

## Referans Dosyalari

- `references/sinyal-konum-tahmini.md` — WiFi sinyal seviyesinden (RSSI) cihaz konumu tahmin etme
- `references/kullanici-cihazlari.md` — Kullaniciya ait Samsung telefonlarin WiFi hotspot bilgileri (SSID, MAC, sifre, kanal)
