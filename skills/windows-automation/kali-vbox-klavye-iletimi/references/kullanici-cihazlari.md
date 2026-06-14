# Kullanici Cihazlari — WiFi Spotlari

## Samsung Galaxy S22 (S22)

| Ozelik | Deger |
|--------|-------|
| SSID | S22 |
| Sifre | 2428496953 |
| Bant | 2.4 GHz |
| MAC | Rastgele (Randomized MAC) |
| Not | Kucuk model, hotspot adi "S22" |

## Samsung Galaxy S22 Plus (S22 PLAS)

| Ozelik | Deger |
|--------|-------|
| SSID | S 22 PLAS |
| Kanal | 6 (2.437 GHz) |
| Sinyal | -26 dBm (yaninda) |
| Koruma | WPA2-PSK CCMP |
| Standart | 802.11b/g (maks 54 Mbps) |
| HT/VHT | Yok (hotspot modu eski b/g) |
| MAC | 26:5A:10:B6:25:C8 (Rastgele, IEEE'de kayitli degil) |
| Tuvalet/Sifre | Kullanici bilmiyor, sorma |
| Not | Plus model, hotspot adi "S 22 PLAS" — arada bosluk var |

## Samsung Galaxy S22 Ultra (S22+)

| Ozelik | Deger |
|--------|-------|
| SSID | S22+ |
| Durum | Henuz hic gorulmedi — hotspot genelde kapali |
| Not | Ultra model, genelde spot acmiyor |

## Onemli Notlar

1. **MAC adresleri rastgeledir (Randomized MAC)**: Samsung One UI varsayilan olarak hotspot MAC'ini her acilista randomize eder. Bir daha acildiginda farkli MAC ile gorunecek.

2. **S22 PLAS SSID'inde bosluk var**: `grep "S 22 PLAS"` calismaz (bash arguman bolmesi). Tek alternatif: dosyaya kaydet, sonra Python/tam dosya icinde ara, veya `S22PLAS` deseniyle grep yap.

3. **SSH'ten scan ederken grep hilesi**: Bozuk `grep 'S 22 PLAS'` icin:
   ```bash
   sudo iw dev wlan0 scan > /tmp/scan.txt && grep -A 30 "S 22 PLAS" /tmp/scan.txt
   ```
   NOT: `sudo sh -c "iw dev wlan0 scan > /tmp/scan.txt"` ile yonlendirme calisir, sudo yonlendirme hakki icin.
