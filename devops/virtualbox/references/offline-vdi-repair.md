# Offline VDI Repair — Linux VM Network Kurtarma

## Ne zaman kullanılır

VM boot oluyor ama ağ gelmiyor (NetworkManager ↔ ifupdown çakışması, hatalı interfaces, sshd çalışmıyor) ve GRUB müdahalesi başarısız oluyor.

## Yöntem 1: Recovery VM + GRUB Müdahalesi (Önerilen)

Kali VDI'ını kullanarak yeni bir VM yarat, NAT + port forwarding ile SSH bağlan, sistemi onar.

### Adımlar

```bash
# 1. Yeni VM oluştur
VBoxManage createvm --name "kal_recovery" --register
VBoxManage modifyvm "kal_recovery" --memory 2048 --acpi on --boot1 disk
VBoxManage modifyvm "kal_recovery" --nic1 nat --natpf1 "ssh,tcp,,2223,,22"

# 2. Orijinal VDI'ı tak (mevcut VM'den önce çıkar)
VBoxManage storageattach "kal" --storagectl "SATA" --port 0 --device 0 --type hdd --medium none
VBoxManage storageattach "kal_recovery" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "C:\Users\marko\VirtualBox VMs\kal\kal.vdi"

# 3. Başlat ve GRUB'a müdahale et
VBoxManage startvm "kal_recovery" --type headless

# Bekle ~15sn, sonra GRUB edit modu için "e" tuşu
for i in $(seq 1 8); do
    VBoxManage controlvm "kal_recovery" keyboardputstring "e"
    sleep 0.5
done
# Aşağı ok ile linux satırına git
VBoxManage controlvm "kal_recovery" keyboardputscancode 50
VBoxManage controlvm "kal_recovery" keyboardputscancode d0
sleep 2
# Boot parametresi ekle
VBoxManage controlvm "kal_recovery" keyboardputstring " systemd.unit=multi-user.target"
sleep 1
# Ctrl+X ile boot et
VBoxManage controlvm "kal_recovery" keyboardputscancode 1d
VBoxManage controlvm "kal_recovery" keyboardputstring "x"
VBoxManage controlvm "kal_recovery" keyboardputscancode 9d

# 4. SSH ile bağlan (60-90sn bekle)
sshpass -p '1234' ssh -o StrictHostKeyChecking=no -p 2223 kali@127.0.0.1
```

### Sökme ve Disk'i Geri Verme

```bash
VBoxManage controlvm "kal_recovery" poweroff
VBoxManage storageattach "kal_recovery" --storagectl "SATA" --port 0 --device 0 --type hdd --medium none
VBoxManage unregistervm "kal_recovery" --delete

# Orijinal VM'e geri tak
VBoxManage storageattach "kal" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "C:\Users\marko\VirtualBox VMs\kal\kal.vdi"
```

## Yöntem 2: VHD Dönüşümü + Windows Mount

Bu yöntem VDI içindeki ext4 dosyasına doğrudan erişim sağlamaz (Windows ext4 okuyamaz). Sadece VBoxManage format değiştirme işe yarar.

### VHD'ye dönüştürme (başarılı)

```bash
# VDI → RAW → VHD
VBoxManage clonemedium "kal.vdi" "kal_raw.img" --format RAW
VBoxManage clonemedium "kal_raw.img" "kal_fix.vhd" --format VHD
```

**NOT:** Bu VHD'yi Windows'ta mount etmek için:
- `diskpart.exe` → Yönetici izni gerekir (UAC)
- `Mount-VHD` → Hyper-V modülü gerekir (genelde yok)
- WSL `losetup` → WSL2'de /mnt/c üzerinde çalışmaz! Dosyayı WSL filesystem'ine kopyalamak gerekir (25GB → çok yavaş)

### RAW image'da içerik arama (başarısız)

Python ile RAW image'da `/etc/network/interfaces` içeriğini bulmak mümkün değil — ext4 dosya içeriği fragmentli olabilir veya metadata bloklarında bulunmaz.

### WSL qemu-utils / libguestfs (başarısız)

WSL Kali'de `qemu-utils` ve `libguestfs` kurulumu apt-get update aşamasında çok yavaş (timeout 120 sn'de bile tamamlanmıyor). Bu yöntem pratik değil.

## Yöntem 3: Kali Live ISO ile Boot (potansiyel)

Kali ISO'su live mode'da boot edilip VDI diskini mount etmek için:
1. Yeni VM oluştur, Kali ISO'sunu DVD olarak tak, VDI'yı disk olarak tak
2. Live mode'da boot et (Kali ISO menu → Live)
3. `lsblk` ile disk partition'larını bul
4. `mount /dev/sdaX /mnt` ile root partition'ını mount et
5. `/mnt/etc/network/interfaces`'i düzenle

**Sorun:** Kali ISO 1.4GB, VirtualBox storage attach sırasında "medium" uyarısı verebilir. Çalışıyor ancak GRUB müdahalesi daha hızlı.

## Özet — En Hızlı Kurtarma Yolu

1. **Recovery VM + GRUB müdahalesi** (3-5 dk) ✅ ÖNERİLEN
2. Kali Live ISO + VDI mount (5-7 dk)
3. VHD çevir + Windows mount (çalışmıyor) ❌
4. WSL losetup (çok yavaş) ❌
