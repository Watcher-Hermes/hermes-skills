---
name: vm-web-terminal-ui
description: >
  Flask + Paramiko web-based SSH terminal for headless VMs.
  Build a dark-themed browser UI with command buttons, status
  indicator, real-time output display, and auto-reconnect logic.
  User opens a .bat shortcut, interacts via browser, no GUI needed.
version: 1.0.0
author: marko
license: MIT
metadata:
  hermes:
    tags: [flask, paramiko, ssh, web-terminal, kali, vm]
audience: user
    platform: windows
    lang: turkish
---

# VM Web Terminal UI — Flask + Paramiko

## Kullanım Amacı

Bir VM'ye (Kali, Ubuntu, herhangi bir Linux) SSH bağlantısı kurup,
web tarayıcı üzerinden komut göndermek için Flask tabanlı arayüz.

**Ne zaman kullanılır:**
- VM çalışıyor ama SSH terminaline direkt erişim yok
- Kullanıcı komutları tarayıcıdan yazmak istiyor
- VM headless modda çalışıyor, GUI yok
- Sık kullanılan komutlar için butonlar olsun isteniyor

## Mimari

```
Windows Host (Hermes)
  └─ Flask server (localhost:5050)
       └─ Paramiko SSH client
            └─ Kali VM (192.168.0.19:22 - bridged)
                 └─ shell / tmux
```

- Flask, Windows'ta Python ile çalışır
- Paramiko ile Kali'ye SSH bağlanır
- Web arayüzü: HTML + CSS (dark tema) + JavaScript (fetch API)
- Masaüstü kısayolu (.bat) ile tek tıkla başlatılır

## Kurulum Adımları

### 1. Bağımlılıkları kur

```bash
pip install flask paramiko
```

Flask ve paramiko'nun yüklü olduğunu doğrula:
```bash
python -c "import flask; import paramiko; print('OK')"
```

### 2. Ana Flask uygulamasını yaz

Dosya: `C:\Users\marko\Desktop\kali-terminal-ui.py`

**Temel yapı:**
```python
from flask import Flask, render_template_string, jsonify, request
import paramiko

app = Flask(__name__)
KALI_HOST = "192.168.0.19"    # VM'nin IP'si (bridged)
KALI_PORT = 22
KALI_USER = "kali"
KALI_PASS = "1234"
client = None

def ssh_connect():
    global client
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(KALI_HOST, port=KALI_PORT, username=KALI_USER,
                       password=KALI_PASS, timeout=5)
        return True
    except Exception as e:
        client = None
        return False

@app.route("/")
def index():
    # HTML template with dark terminal theme
    return render_template_string("""...""")

@app.route("/status")
def status():
    connected = client is not None and client.get_transport() is not None and client.get_transport().is_active()
    return jsonify({"connected": connected})

@app.route("/exec", methods=["POST"])
def exec_cmd():
    cmd = request.json.get("cmd", "")
    if not client or not client.get_transport().is_active():
        return jsonify({"error": "SSH baglantisi yok"}), 503
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return jsonify({"output": out, "error": err})

if __name__ == "__main__":
    ssh_connect()
    app.run(host="127.0.0.1", port=5050, debug=False)
```

### 3. HTML Template — Dark Terminal Tema

Arayüz içermelidir:
- **Başlık:** "Kali Terminal" veya VM adı
- **Status göstergesi:** Yeşil/daire (bağlı) veya kırmızı/kare (bağlı değil)
- **Durum yazısı:** "Bağlı" / "Bağlı Değil" + IP adresi
- **Hızlı komut butonları:** whoami/ip, disk alanı, RAM, process, uptime, arp-scan, OS info, tmux son
- **Komut giriş kutusu:** Text input + "Gönder" butonu
- **Çıktı alanı:** `<pre>` etiketi, dark arkaplan, yeşil font

Butonlar bağlı değilken disabled olmalı, bağlanınca aktifleşmeli.

Örnek buton-komut eşleşmeleri:
```javascript
const PRESET_COMMANDS = {
    "whoami/ip": "whoami && hostname -I",
    "disk": "df -h /",
    "ram": "free -h",
    "process": "ps aux --sort=-%mem | head -15",
    "uptime": "uptime && last -15",
    "arp-scan": "sudo arp-scan -l 2>&1",
    "OS info": "uname -a && cat /etc/os-release | head -5",
    "tmux son": "tmux capture-pane -t hermes -p -S -50"
};
```

CSS renk paleti:
- Arkaplan: `#1a1a2e` veya `#0d0d0d`
- Metin: `#00ff00` (terminal yeşili) veya `#e0e0e0`
- Butonlar: `#16213e` arkaplan, `#0f3460` hover
- Status yeşil: `#00ff88`, status kırmızı: `#ff4444`
- Font: `'Courier New', monospace`

### 4. Masaüstü Kısayolu (.bat)

Dosya: `C:\Users\marko\Desktop\kali-terminal-ui.bat`

```batch
@echo off
title Kali Terminal UI
echo Kali Terminal UI baslatiliyor...
cd /d C:\Users\marko\Desktop
start http://localhost:5050
python kali-terminal-ui.py
pause
```

Bu `.bat` dosyası:
1. Flask sunucusunu başlatır
2. Varsayılan tarayıcıda `http://localhost:5050` açar
3. Kullanıcı tarayıcıyı kullandıktan sonra Ctrl+C ile durdurur

### 5. Test Adımları

1. VM'in çalıştığını doğrula:
   ```bash
   VBoxManage list runningvms
   ```

2. SSH ile bağlanabildiğini doğrula:
   ```bash
   sshpass -p 'kali' ssh -o ConnectTimeout=5 kali@192.168.0.19 "whoami"
   ```

3. Flask sunucusunu başlat:
   ```bash
   cd /c/Users/marko/Desktop && python kali-terminal-ui.py
   ```

4. Tarayıcıda `http://localhost:5050` aç

5. Status endpoint'ini kontrol et:
   ```bash
   curl http://localhost:5050/status
   # Expected: {"connected": true/false}
   ```

6. Komut gönderme testi:
   ```bash
   curl -X POST http://localhost:5050/exec -H "Content-Type: application/json" -d '{"cmd":"whoami"}'
   # Expected: {"output": "kali\n", "error": ""}
   ```

## Önemli Kod Desenleri

### SSH Bağlantı Kontrolü

```python
def is_connected():
    return (client is not None and
            client.get_transport() is not None and
            client.get_transport().is_active())
```

Her komut gönderme isteğinde ve status sorgusunda bu kontrol yapılmalı.

### Hata Yönetimi

```python
try:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
except paramiko.SSHException as e:
    return jsonify({"error": f"SSH hatasi: {str(e)}"}), 500
except socket.timeout:
    return jsonify({"error": "Komut zamani asimi (15sn)"}), 504
```

### Buton Disable/Enable Mantığı (JavaScript)

```javascript
function updateUI(connected) {
    document.querySelectorAll("button[data-cmd]").forEach(b => b.disabled = !connected);
    document.getElementById("cmd-input").disabled = !connected;
    document.getElementById("send-btn").disabled = !connected;
    // Status indicator
    const dot = document.getElementById("status-dot");
    dot.className = connected ? "status-green" : "status-red";
    document.getElementById("status-text").textContent =
        connected ? `Bağlı (${vm_ip})` : "Bağlı Değil";
}
```

## Kullanıcı Format Tercihi

Kali'den komut çıktısı aktarırken:
- Sadece çıktıyı göstermek yeterli değil — **banker/terminal benzeri adım adım hangi komutların hangi sırayla çalıştığını** da göster.
- Her adımda komutun kendisini (`$ komut` veya `ADIM N — açıklama: komut`) terminalde yazıldığı gibi yaz, ardından çıktısını ver.
- Kullanıcı "bu işlem çıktısı ben kali linux ne aşamalar yazılarak bulunduğunu görmek istiyorum" dedi — süreci şeffaf görmek istiyor, sadece özet değil.
- Ağ taraması referans komut seti: `references/network-scanning-kali.md`

## Telegram Hermes → Kali Komut Gönderme Akışı

Flask sunucusu çalışırken, Telegram'daki Hermes `execute_code` üzerinden Kali'ye komut gönderebilir. Bu, web UI dışında ikinci bir erişim kanalıdır.

```python
# Kali'de komut çalıştır — Telegram Hermes'ten
import urllib.request, json
data = json.dumps({"cmd": "whoami && hostname -I"}).encode()
req = urllib.request.Request("http://localhost:5050/exec", data=data, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=30)
print(resp.read().decode())
# Çıktı: {"output": "kali\n192.168.0.19\n", "error": ""}
```

**Kritik:** Kali'de default shell **zsh**. Çok satırlı komutlar ve tırnak içinde `$()` kullanımı hata verir. Komutları tek satırda `&&` ile birleştir, tek tırnak kullan:

```
# DOĞRU: echo '=== BASLIK ===' && whoami && hostname -I
# YANLIŞ: echo "=== $BASLIK ===" && ... (zsh bozulur)
```

**Timeout ayarı:** Ağ taraması gibi uzun komutlar için `timeout=60` veya daha yüksek ayarla. Paramiko varsayılanı 15sn.

**Bağlantı koptuğunda:** `/status` endpoint'ini kontrol et:
```python
urllib.request.urlopen("http://localhost:5050/status").read()
# {"connected": false} ise Flask'ı yeniden başlat (.bat dosyasına çift tıkla)
```

## Pitfall'lar

1. **Guest Additions yok:** `guestproperty`'den IP alınamaz. Ağ taraması (nmap/arp), bridged subnet ping sweep veya VBoxManage NIC listesi ile IP bulunur.
2. **VM çalışıyor ama SSH zaman aşımı:** Kali'de NetworkManager vs interfaces çakışması olabilir. `systemctl mask networking` + `systemctl enable --now NetworkManager` çözümü dene. Ayrıca bridged IP değişmiş olabilir — host-only yerine bridged (192.168.0.x) subnet'te ara.
3. **Host-only bridged IP değişirse:** KALI_HOST sabit kodlu. DHCP bridged IP değişince kodu güncelle. IP bulmak için: Windows'ta `arp -a | grep 08-00-27` veya ping sweep yap; VBox arayüzsüz ise `for i in $(seq 1 254); do ping -n 1 -w 1 192.168.0.$i | grep -q TTL && echo 192.168.0.$i; done`.
4. **VBoxManage "already locked" hatası:** VM poweroff durumunda bile kilitli kalabilir. Çözüm: `taskkill.exe //F //IM VBoxSVC.exe && taskkill.exe //F //IM VirtualBox.exe`, 2sn bekle, sonra `VBoxManage startvm "kal" --type headless`. `discardstate` genelde aynı kilitten geçemediği için işe yaramaz.
4. **Flask restart gerekirse:** Arka planda çalışıyorsa önce process kill et, sonra yeniden başlat.
5. **Windows firewall:** localhost:5050'e erişim genelde açıktır. Bloklanırsa güvenlik duvarına `127.0.0.1:5050` için izin ekle.
6. **Paramiko exec_command** timeout parametresi alır ama session timeout değildir. Çok uzun süren komutlar için ayrı thread'de çalıştır.
7. **Her komut yeni bir shell açar** — `cd` gibi stateful komutlar çalışmaz. Tmux oturumu kullanarak kalıcı shell tutulabilir.
8. **zsh `===` reddeder:** Kali'de default shell zsh. `echo "=== metin ==="` çalışmaz — zsh `==` işaretini glob operatörü olarak algılar. `echo` ile basit süsleme: `echo "---- metin ----"` kullan.
9. **send-keys + bash/MSYS boşluk sorunu:** Tmux `send-keys`'e bash/MSYS üzerinden boşluklu string göndermek, boşlukları yutar. Sebebi: bash'ın komut ayrıştırması ile tmux `send-keys` argüman işlemesi arasındaki etkileşim. `-l` (literal) flag'i de çözemez. `C-m` (Enter) ayrı argüman olarak değil, literal string olarak gider. Çözüm: tmux kullanmadan `sshpass ssh -o StrictHostKeyChecking=no kali@IP 'komut'` ile doğrudan `exec_command()` tarzında tek tek komut çalıştır — her `terminal()` çağrısı Kali'de bir shell oturumu açar, boşluk sorunsuz çalışır.
10. **zsh'te `?` glob çakışması:** `echo "tararsam?"` gibi komutlar zsh'ta `no matches found` hatası verir. `?` karakteri glob wildcard'ıdır. Çözüm: `echo` içinde kullanma veya kaçış karakteri ekle (`\?`). Alternatif: `printf '%s\n' "..."` kullan.
11. **ssh ile interaktif komut gösterme yöntemi:** Terminalde her adımı ayrı `terminal()` çağrısı ile çalıştır. Kullanıcıya hangi komutların hangi sırayla çalıştırıldığını göstermek için önce açıklama echo'su, sonra asıl komut. Örnek:
    ```bash
    sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@192.168.0.19 'echo "ADIM 1: arp-scan ile ag taramasi"'
    sshpass -p 'kali' ssh -o StrictHostKeyChecking=no kali@192.168.0.19 'sudo arp-scan --interface eth1 --localnet'
    ```
    Bu yöntem tmux'tan daha güvenilir çünkü her komut ayrı bir shell oturumunda çalışır ve boşluklar korunur.

## Başarı Kriterleri

- [ ] Flask sunucusu başlatılabilir (`python kali-terminal-ui.py`)
- [ ] Tarayıcıda arayüz yüklenir (localhost:5050)
- [ ] Status göstergesi bağlantı durumunu doğru gösterir
- [ ] Butonlar bağlı değilken disabled, bağlanınca aktif
- [ ] Komut gönderme çalışır
- [ ] Çıktı düzgün görüntülenir
- [ ] Masaüstü kısayolu (.bat) çalışır
- [ ] Ctrl+C ile temiz kapanır

## Template Reference

Tüm HTML + CSS + JS template'i için: `templates/kali-terminal-template.html`

## Referans Dosyaları

- `references/network-scanning-kali.md` — Ağ taraması komut seti (nmap, arp-scan, iw)
- `references/android-backdoor-termux.md` — S22/Android backdoor kurulumu (Termux + SSH + GPS)
