# WiFi Sinyal Seviyesinden Konum/Konum Tahmini

## Pratik Tablo (2.4 GHz, ev ici)

| Sinyal (dBm) | Mesafe | Anlami |
|-------------|--------|--------|
| -10 ila -30 | 0-3 m | Yan yana, ayni masa/oda |
| -30 ila -50 | 3-10 m | Ayni katta, yakin oda |
| -50 ila -65 | 10-25 m | 1-2 duvar otesi |
| -65 ila -80 | 25-50 m | Uzak, birden cok duvar |
| -80 alti | >50 m | Cok zayif, sinyal kaybi yuksek |

## Dogrulugu Etkileyen Faktorler

- **Tx gucu**: Telefon hotspot'lari genelde 20 dBm (100 mW), bazi cihazlar 17 dBm (50 mW)
- **Anten kazanci**: Telefonun WiFi anteni cep telefonu formundadir, yonlu olabilir
- **Duvarlar**: Beton duvar ~10-15 dB, alci duvar ~3-5 dB, cam ~1 dB zayiflama
- **Mobilya**: Su dolu nesneler (akvaryum) cok zayiflatir, metal daha cok
- **Girisim**: Diger WiFi aglari, bluetooth, mikrodalga sinyali gurultu ekler

## Hesaplama

```
Mesafe ≈ 10 ^ ((TxPower_dBm - RSSI_dBm) / (10 * n))
```

- n=2: Acik alan (free space)
- n=2.5: Ev ici, az gurultulu
- n=3-4: Ofis, cok gurultulu, cok duvarli

Samsung S22 Plus icin TxPower≈20 dBm, n≈2.5

## Ornek: S 22 PLAS, -26 dBm

```
Mesafe = 10 ^ ((20 - (-26)) / (10 * 2.5))
       = 10 ^ (46 / 25)
       = 10 ^ 1.84
       ≈ 69 metre  (FORMULDE YANILTI: path loss negatif cikinca anlamsiz)
```

**Gercek**: -26 dBm seviyesinde cihaz yan yanadir (0-3 m). Formul path loss'un negatif olmasi durumunda (<30 dB) free space modeli gecerli degildir — cihaz fiziksel olarak cok yakindir.

**Pratik kural**: RSSI > -35 dBm ise cihaz ayni odada, gorus mesafesindedir.
