# Kali Linux — VirtualBox Erişim Notları

## Varsayılan bilgiler

- Kullanıcı: kali
- Parola: kali
- SSH servisi genelde kapalı olabilir.
- Guest Additions kurulu olmayabilir.

## SSH'yi açmak (eğer yoksa)

```bash
sudo systemctl enable --now ssh
```

## NAT + port forwarding örnek regle

```bash
VBoxManage modifyvm "kal" --natpf1 "ssh,tcp,127.0.0.1,2222,10.0.2.15,22"
```

Not: Bu kural VM kapalıyken yazılabilir. Açıkken `VM locked` hatası alınır.

## SSH bağlantı testi

```bash
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 kali@127.0.0.1 -p 2222 echo CONNECT_OK
```

## VRDP açmak

```bash
# 1) VM'yi kapat (VRDP değişikliği yalnızca kapalı varken çalışır)
VBoxManage controlvm "kal" acpipowerbutton

# 2) Düzenle
VBoxManage modifyvm "kal" --vrde on --vrdeport 5000

# 3) Başlat
VBoxManage startvm "kal" --type headless

# 4) Bağlan
mstsc.exe /v:127.0.0.1:5000 /u:kali /p:kali
```

## Ekran görüntüsü ile doğrulama

VirtualBox MMA penceresi görünüyorsa VM çalışıyor demektir.
Kali pencereri görünmüyorsa headless modda çalışıyor olabilir. Ekran görüntüsü ve GUI oturum kontrolü yap.
