---
name: virtualbox
description: Manage VirtualBox VMs from Windows host via Hermes. Use for VM status, start/stop, networking, and remote access.
triggers:
  - virtualbox
  - vboxmanage
  - kali linux vm
  - vm management
  - ssh to vm
  - connect to vm
---

# VirtualBox VM Management

## When to Use

Triggers: User mentions VirtualBox, VM, VBoxManage, Kali Linux VM, wants to enter/connect to a VM, or asks about VM status.

## Quick Paths

### 1. Check VM status
```bash
VBoxManage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
subprocess.run([VBoxManage, "showvminfo", VM_NAME, "--machinereadable"])
# Read VMState= line
```

### 2. Start VM
```bash
# Headless (no window):
VBoxManage startvm <name> --type headless

# GUI (windowed):
VBoxManage startvm <name> --type gui
```

### 3. Networking diagnosis

```bash
# List host-only adapters
VBoxManage list hostonlyifs

# Check VM NICs
VBoxManage showvminfo <name> | grep -E "NIC|Network"
```

Common configurations:
- **NAT only**: VM gets 10.0.2.15, host sees nothing. Requires port forwarding for inbound connections.
- **Host-Only**: Host and VM on same private subnet (e.g. 192.168.56.0/24). Easier SSH.
- **NAT + Host-Only**: Best of both.

### 4. Remote access options

| Method | Requires | Notes |
|--------|----------|-------|
| SSH | NAT port forwarding **OR** Host-Only adapter | Kali default user often `kali`/`kali` |
| VRDP (RDP) | `--vrde on` + port | VM must be **powered off** to modify |
| Shared clipboard | Guest Additions installed | One-way: Host→Guest or bidirectional |

## Pitfalls

- **VM locked error**: `VBoxManage modifyvm` fails if VM is running (locked for session). Always power off first: `VBoxManage controlvm <name> acpipowerbutton` or disable from GUI.
- **Stale lock after GUI crash**: If modify/start still fails after closing VirtualBox, kill `VirtualBoxVM.exe`, wait a few seconds, then retry. This clears orphaned session locks.
- **USB passthrough breaks VM networking**: Passing a USB WiFi adapter to a Kali VM can destabilize the VM's network stack. Kali's NetworkManager may try to use the USB WiFi as the primary interface and drop the host-only/NAT connection. Symptoms: SSH/ping stop responding even after removing the USB filter. VBox.log shows "Attached" for the USB device but VM becomes unreachable.
  - **Fix**: Remove USB filter physically from the VM settings (`VBoxManage usbfilter remove 0 --target <vm>`), poweroff cleanly, restart, wait for boot, then SSH in via host-only. If still unreachable after 60s boot, use VirtualBox GUI console to diagnose: `sudo dhclient eth1 && systemctl restart ssh` from the VM console.
- **Multiple poweroff/startup cycles corrupting VDI lock**: Rapid `controlvm poweroff` → `startvm` cycles can leave VDI in a read-only locked state with `VERR_VD_IMAGE_READ_ONLY`. Fix: `Stop-Process -Name VBoxSVC -Force`, wait 5s, then retry. The VDI file's filesystem attributes may show `False` for IsReadOnly but VBoxSVC still holds a stale lock.
- **VBoxManage hostonlyif commands hanging**: `VBoxManage hostonlyif remove` and `hostonlyif create` can hang indefinitely if VBoxSVC is in a bad state. Kill VBoxSVC first, then retry. If still hangs, the host-only adapter is fine — the problem is inside the VM's network config, not VirtualBox's.
- **Kali black screen after boot**: Common with Kali + GNOME + older VirtualBox graphics defaults. Preferred fix: set `--graphicscontroller vboxvga`, `--vram 128`, `--accelerate3d off`, and append `nomodeset` to GRUB. See [kali-grub-nomodeset.md](references/kali-grub-nomodeset.md).
- **SSH refused**: VM may not have sshd running. On Kali: `sudo systemctl enable --now ssh`. If NAT only, port forwarding must be configured **before** VM boot.
- **NAT port forwarding rules**: Set with `--natpf1 "ssh,tcp,127.0.0.1,2222,10.0.2.15,22"`. Note guest IP (right side) must be the VM's actual NAT IP (usually 10.0.2.15).
- **VRDP port conflicts**: Default 3389 may conflict with Windows RDP. Use high port (e.g. 5000).
- **Host-Only DHCP**: May be disabled. Set static IP in VM or enable DHCP on host-only network.
- **GuestInfo IP may be unavailable**: `VBoxManage guestproperty get <vm> "/VirtualBox/GuestInfo/Net/*/V4/IP"` can return `No value set!` even on an otherwise healthy VM. When GuestInfo IP retrieval fails, use alternative discovery methods: try SSH with the expected NAT default (10.0.2.15), inspect host-only lease tables, or use network scanning from the host.
- **PATH-less VBoxManage on Windows**: `VBoxManage.exe` is usually under `C:\Program Files\Oracle\VirtualBox\VBoxManage.exe`, not on PATH by default. Use that path explicitly.
- **Elevated execution quoting failure**: PowerShell quoting through `-ArgumentList '...'` often fails (`positional parameter cannot be found`). Running elevated through `cmd.exe` avoids this class of quoting bug.
- **UAC elevation cannot capture stdout directly**: UAC-spawned elevated processes do not return stdout through the invoking shell. Use a file-redirection strategy instead of trying to capture output inline.\n- **Keyboardputstring race condition**: Chaining `keyboardputstring` commands without sufficient `sleep` between them causes the next command to be typed before the previous one finishes executing (e.g. typing `sudo nmap -sn` then immediately typing `echo bitti` on the same prompt line). Always sleep 1-2s between simple commands, 3-8s for longer scans.
- **Long compound commands silently drop text**: Shell constructs like `echo '...' && echo '...' && echo '...'` sent as a single `keyboardputstring` call can truncate or drop characters because VirtualBox's keyboard buffer is limited. **Split every logical command into its own call** with sleep between:
  ```bash
  # WRONG — gets truncated or merged
  "$VBOX" controlvm "$VM" keyboardputstring "echo '1' && echo '2' && echo '3'"

  # RIGHT — separate calls with sleep
  "$VBOX" controlvm "$VM" keyboardputstring "echo '1'"
  "$VBOX" controlvm "$VM" keyboardputstring $'\n'
  sleep 1
  "$VBOX" controlvm "$VM" keyboardputstring "echo '2'"
  "$VBOX" controlvm "$VM" keyboardputstring $'\n'
  ```\n- **Tmux send-keys space stripping via git-bash**: When sending commands to a Kali tmux session via `ssh ... 'tmux send-keys -t hermes \"command\" Enter'`, git-bash (MSYS) or zsh may strip spaces from within quoted strings, turning `\"echo hello\"` into `echohello`. This happens because the ssh wrapper / shell serialization mangles the quoting.\n  - **Best fix**: Use `sshpass -p 'pass' ssh kali@host 'command'` directly — one command per SSH call, bypasses tmux entirely. Works reliably.\n  - **Alternative**: Use `VBoxManage keyboardputstring` for VM-console typing (no quoting issues, but no output capture).\n  - **Tmux with heredoc**: Use `ssh -tt kali@host <<'EOF' ... EOF` and inside the heredoc use `tmux send-keys -t hermes -l \"literal text\" C-m` with the `-l` literal flag.\n- **GRUB müdahale için keyboardputstring zamanlaması**: Kali boot'ta GRUB'a müdahale etmek için VBoxManage kontrol komutları kullanılır. Zamanlama kritiktir:
  1. `VBoxManage controlvm <vm> reset` — VM'i resetle
  2. Hemen (0.5 sn aralıkla) 5-8 kere `keyboardputstring "e"` gönder — GRUB menüsünde "edit" moduna girer
  3. 3 sn bekle, sonra `keyboardputscancode 50 d0` (aşağı ok) ile linux satırına git (gerekirse 2-3 kere)
  4. `keyboardputstring " systemd.unit=multi-user.target"` ile boot parametresi ekle (networking servisi takılmasın)
  5. `keyboardputscancode 1d` (Ctrl basılı), `keyboardputstring "x"`, `keyboardputscancode 9d` (Ctrl bırak) ile boot et
  - **Not:** GRUB timeout varsayılan 5 sn. İlk "e" tuşu bu süre içinde gönderilmezse GRUB otomatik boot eder ve müdahale şansı kaybedilir.
  - **Alternatif:** Her zamanlama tutmayabilir. Başarısız olursa tekrar dene.
  - **GUI mod:** `--type gui` ile başlatıp browser_vision ile GRUB ekranını görmek daha güvenilir.

### 5. Direct keyboard input to VM terminal (keyboardputstring)

Send keystrokes directly into the VM's own terminal (not SSH — this types into the VirtualBox console window). Useful for:
- Typing commands into the VM's physical terminal when SSH is unavailable or the user wants to see keys being typed
- Bypassing SSH for educational/demo purposes
- Automating boot-time GRUB edits (see GRUB section above)

**Basic usage:**
```bash
VBOX="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
VM="kal"

# Type a command and press Enter
"$VBOX" controlvm "$VM" keyboardputstring "echo Merhaba, ben Hermes"
"$VBOX" controlvm "$VM" keyboardputstring $'\n'

# Chain multiple commands with delays
"$VBOX" controlvm "$VM" keyboardputstring "sudo arp-scan --interface eth1 --localnet"
"$VBOX" controlvm "$VM" keyboardputstring $'\n'
sleep 3  # wait for arp-scan to complete
```

**Important notes:**
- **No output capture**: `keyboardputstring` only types — you cannot read the VM's screen output from the host. The user sees the result on the VM's display.
- **No feedback loop**: You cannot verify the command ran successfully via this method. For verifiable execution, use SSH instead.
- **Timing with sleep**: Long-running commands (nmap, arp-scan) need appropriate `sleep` between chained commands to avoid typing the next command before the previous one finishes.
- **Special characters**: `$'\n'` represents Enter. For Ctrl combinations, use `keyboardputscancode` (scan codes, not strings).
- **PATH note**: VBoxManage is NOT on PATH by default on Windows. Always use the full path: `"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"`
- **VM must be running**: `controlvm` requires the VM to be in a running state. Start the VM first.

### keyboardputscancode — Keyboard shortcuts (modifier keys)

`keyboardputscancode` sends raw PS/2 scancodes instead of character strings. Use this when you need to send **keyboard shortcuts with modifier keys** (Ctrl, Alt, Shift, Super) — things `keyboardputstring` cannot do because it only sends printable characters.

**Hex scancodes for common keys:**

| Key | Press | Release |
|-----|-------|---------|
| Ctrl (Left) | `1d` | `9d` |
| Alt (Left) | `38` | `b8` |
| Shift (Left) | `2a` | `aa` |
| Super/Windows | `5b` | `db` |
| T | `14` | `94` |
| Enter | `1c` | `9c` |
| Escape | `01` | `81` |
| Arrow Up | `48` | `c8` |
| Arrow Down | `50` | `d0` |
| Arrow Left | `4b` | `cb` |
| Arrow Right | `4d` | `cd` |
| Space | `39` | `b9` |
| Tab | `0f` | `8f` |

**Pattern — press modifiers first, release in reverse order:**

```python
from subprocess import run as r

vbox = r'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
vm = 'kal'

def sc(hex_codes):
    r([vbox, 'controlvm', vm, 'keyboardputscancode'] + hex_codes)

# Ctrl+Alt+T (open terminal on Kali/GNOME)
sc(['1d', '38', '14'])   # press: Ctrl + Alt + T
import time; time.sleep(0.1)
sc(['94', 'b8', '9d'])   # release: T + Alt + Ctrl (reverse order)

# Alt+F4 (close active window)
sc(['38', '3e'])         # press: Alt + F4
time.sleep(0.1)
sc(['be', 'b8'])         # release: F4 + Alt

# Ctrl+Alt+F1 (switch to TTY1)
sc(['1d', '38', '05'])
time.sleep(0.1)
sc(['85', 'b8', '9d'])
```

**Common Linux VM keyboard shortcuts:**

| Shortcut | Action | Scancode (press then release) |
|----------|--------|-------------------------------|
| Ctrl+Alt+T | Open terminal (GNOME/KDE/Xfce) | `1d 38 14` → `94 b8 9d` |
| Ctrl+Alt+F1..F6 | Switch to TTY1..TTY6 | `1d 38 05..0a` → `85..8a b8 9d` |
| Ctrl+Alt+F7 | Switch back to GUI | `1d 38 07` → `87 b8 9d` |
| Super | GNOME Activities / KDE menu | `5b` → `db` |
| Alt+F4 | Close active window | `38 3e` → `be b8` |
| Ctrl+C | Send SIGINT | `1d 2e` → `ae 9d` |
| Ctrl+Shift+T | New terminal tab | `1d 2a 14` → `94 aa 9d` |

**When to use scancodes vs. keyboardputstring:**
- **keyboardputstring** → typing text commands, single-line input, Enter via `$'\n'`
- **keyboardputscancode** → keyboard shortcuts (Ctrl+Alt+T), modifier-only combos, function keys, arrow key navigation

**Common use cases:**
```bash
# Clear screen first
"$VBOX" controlvm "$VM" keyboardputstring "clear"
"$VBOX" controlvm "$VM" keyboardputstring $'\n'
sleep 1

# Echo a separator
"$VBOX" controlvm "$VM" keyboardputstring "echo ===== TARAMA BASLIYOR ====="
"$VBOX" controlvm "$VM" keyboardputstring $'\n'
sleep 1

# Run a scan command
"$VBOX" controlvm "$VM" keyboardputstring "sudo nmap -sn 192.168.0.0/24"
"$VBOX" controlvm "$VM" keyboardputstring $'\n'
# Wait for nmap to finish (adjust based on subnet size)
sleep 6
```

**Pitfalls:**
- **Bash/zsh quoting on Windows git-bash**: `$'\\n'` syntax works in git-bash (MSYS) but NOT in PowerShell or cmd.exe. If running elevated, use cmd.exe with a different quoting strategy (echo newline or use `keyboardputscancode 1c 9c` for Enter).
- **Race conditions — EN ÖNEMLİ SORUN**: If you type too fast without adequate `sleep`, the next command gets typed into the previous command's output area or prompt line — effectively creating a malformed command or writing to a non-shell context. Required sleep durations:
  - Simple `echo` commands: 1-2 sn
  - `arp-scan`, `iwlist` gibi kısa taramalar: 3-5 sn
  - `nmap -sn` gibi subnet taramaları: 6-10 sn
  - Ping sweep loop: 15-60 sn (254 IP)
  - `apt-get install`, `systemctl restart`: 10-20 sn
- **Long compound commands fail**: Multi-part shell commands (% `echo '...' && echo '...' && echo '...'`) chained into a single `keyboardputstring` call often fail because the VirtualBox keyboard buffer cannot handle the full string. Instead, split into separate calls with sleep between each:
  ```
  "$VBOX" controlvm "kal" keyboardputstring "echo Baslik 1"
  "$VBOX" controlvm "kal" keyboardputstring $'\\n'
  sleep 1
  "$VBOX" controlvm "kal" keyboardputstring "echo Baslik 2"
  "$VBOX" controlvm "kal" keyboardputstring $'\\n'
  ```
- **No visual confirmation**: The user must confirm the output appeared on-screen. They use it for demonstration/education purposes; if something goes wrong, they'll tell you to retry.
- **Cannot type interactive passwords**: `sudo` without NOPASSWD will prompt for a password on-screen. Configure NOPASSWD in `/etc/sudoers` first if you need to run sudo commands via keyboardputstring.
- **Shell operators do NOT work**: `>`, `|`, `$()`, backticks, `&&` (sometimes), and other shell metacharacters are sent as literal text, not interpreted. Use SSH for redirected/pipe'd commands.
- **No output capture**: `keyboardputstring` is a one-way operation — you type keys but cannot read the VM screen. For verifiable execution or when the user needs proof, use SSH instead.

### 6. Guest Control — VBoxManage guestcontrol (ÖNCELİKLİ)

`VBoxManage guestcontrol`, VM'in içinde doğrudan komut/program çalıştırmanı sağlar.
**keyboardputstring'ten ÖNCE tercih edilir** çünkü:
- Çıktıyı yakalayabilirsin (`--wait-stdout` ile)
- Zamanlama sorunu yok (sleep gerekmez)
- Login ekranındayken bile çalışır (oturum açar)
- Git Bash yol dönüşümü için `MSYS2_ARG_CONV_EXCL="*"` kullan

**İki alt komut:**

| Komut | Kullanım | Çıktı |
|-------|----------|-------|
| `run` | Çalıştır + çıktıyı bekle | `--wait-stdout` ile yakalanabilir |
| `start` | GUI uygulaması başlat (arka planda) | Çıktı yok, sadece başlat |

**Örnek 1 — Kali'de terminal aç (EN SIK KULLANIM):**

Kali'de terminal açmak için `keyboardputstring` + Ctrl+Alt+T yerine guestcontrol kullan — çok daha güvenilir:

```bash
# Kali'de hangi terminal var?
MSYS2_ARG_CONV_EXCL="*" "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" \
  guestcontrol "kal" run --exe "/usr/bin/ls" --username kali --password kali \
  --wait-stdout -- -la /usr/bin/ | grep -i term

# Kali'de qterminal başlat (GUI)
MSYS2_ARG_CONV_EXCL="*" "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" \
  guestcontrol "kal" start --exe "/usr/bin/qterminal" --username kali --password kali

# Alternatif: x-terminal-emulator (sembolik link)
MSYS2_ARG_CONV_EXCL="*" "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" \
  guestcontrol "kal" start --exe "/usr/bin/x-terminal-emulator" --username kali --password kali
```

**Örnek 2 — Kali'de komut çalıştır ve çıktıyı al:**

```bash
MSYS2_ARG_CONV_EXCL="*" "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" \
  guestcontrol "kal" run --exe "/usr/bin/whoami" --username kali --password kali --wait-stdout
# Çıktı: kali

MSYS2_ARG_CONV_EXCL="*" "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" \
  guestcontrol "kal" run --exe "/bin/hostname" --username kali --password kali --wait-stdout
# Çıktı: kal
```

**Önemli notlar:**

- `MSYS2_ARG_CONV_EXCL="*"` **ZORUNLUDUR** — Git Bash (MSYS) yoksa `/usr/bin/qterminal` yolunu `C:/Program Files/Git/usr/bin/qterminal`'e çevirir ve hata alırsın. Bu ortam değişkeni tüm yol dönüşümünü devre dışı bırakır.
- `run` ile `--wait-stdout` kullanılır (çıktıyı yakalamak için)
- `start` ile `--wait-stdout` yoktur (GUI için)
- Guest session başarıyla açılır (`Successfully started guest session`) ama binary bulunamazsa hata alırsın
- Kali'de bilinen terminal emülatörleri: `qterminal` (öncelikli), `x-terminal-emulator`
- `xfce4-terminal`, `xterm`, `gnome-terminal` Kali'de olmayabilir
- `run` ile çıktı almak için komutun **non-interactive** olması gerekir
- Guest session için VM'in çalışıyor olması yeterli — login ekranında olması sorun değil

**Örnek 3 — Guest Control ile uygulama başlatma akışı:**

```python
# Python ile güvenilir yol dönüşümü
import subprocess, os

vbox = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
env = {**os.environ, "MSYS2_ARG_CONV_EXCL": "*"}
vm, user, pwd = "kal", "kali", "kali"

# GUI uygulaması başlat (start)
subprocess.run([
    vbox, "guestcontrol", vm, "start",
    "--exe", "/usr/bin/qterminal",
    "--username", user, "--password", pwd
], env=env)

# Komut çalıştır + çıktı al (run)
r = subprocess.run([
    vbox, "guestcontrol", vm, "run",
    "--exe", "/usr/bin/ls",
    "--username", user, "--password", pwd,
    "--wait-stdout", "--", "-la", "/usr/bin/",
], env=env, capture_output=True, text=True)
print(r.stdout)
```

## Kullanıcı Çalışma Stili (ÖNEMLİ)

Bu kullanıcı için geçerli kurallar:
- **Kendi çözümünü üret** — "nasıl yapayım?" diye sorma, direkt uygula
- **Adım adım anlatma** — yaptığını raporla ama açıklama yapma
- **Sadece sonucu söyle** — başarılı/başarısız, oldu bitti

"keyboardputstring" bölümünün başlığı `### 5. Direct keyboard input` olarak kalsın, yeni bölümüm 6 numara.

### 7. USB passthrough (Windows host → Linux VM)

Identify USB device on Windows host:
```powershell
# Find by USB VID/PID
Get-PnpDeviceProperty -InstanceId 'USB\VID_148F&PID_2573\*' -KeyName 'DEVPKEY_Device_HardwareIds'

# Find by network class
Get-PnpDevice | Where-Object { $_.Class -eq 'Net' } | Select-Object FriendlyName,InstanceId | Format-List
```

Add USB filter (VM must be off or device not yet captured):
```bash
VBoxManage usbfilter add 0 --target "<vm-name>" \
  --name "RT73 USB Wireless" \
  --vendorid 148F \
  --productid 2573 \
  --revision 0001
```

Verify filter and attachment:
```bash
# Check filter exists
VBoxManage showvminfo <vm-name> | grep -A 10 "USB Device Filters"

# Check attachment in boot log (after VM started)
grep -i "USB\|<vendorid>\|<productid>\|attach" "C:/Users/<user>/VirtualBox VMs/<vm>/Logs/VBox.log"
```

**Known good config for RT73 (Ralink) USB WiFi:**
- VID 148F, PID 2573
- HighSpeed on RootHub (OHCI/EHCI controller)
- xHCI (USB 3.0) controller NOT needed — RT73 is USB 2.0 HighSpeed
- Works with VirtualBox default OHCI+EHCI controllers

**⚠️ WiFi passthrough danger**: USB WiFi passthrough can destabilize the VM's own networking (see Pitfalls). Best practice: set up USB filter while VM is off, start VM, expect it to take slightly longer on first boot as the new USB device is detected. If the VM becomes unreachable, the fix is removing the filter + console recovery.

## Recommended Workflow

1. Inspect VM state (`showvminfo --machinereadable`). Kullanıcıya sorma, direkt yap.
2. If powered off: start headless, wait 30-60s for boot; or GUI with `--type gui` if user wants to see it
3. If need to run something inside VM: **prefer guestcontrol** (`run` with `--wait-stdout`) over keyboardputstring
4. If need to open terminal in VM GUI: **prefer guestcontrol** (`start --exe /usr/bin/qterminal`) over Ctrl+Alt+T
5. Fallback: keyboardputstring/scancode only if guestcontrol unavailable or Guest Additions missing
6. Verify networking: `showvminfo` for NICs, `guestproperty get` for IP
7. Test connection (SSH `nc` probe or `ssh -o ConnectTimeout=5`)
8. If all else fails: use screenshot + visual analysis to confirm boot state, then guide user

## Scripts

### `scripts/manage_vm.py`
Helper for common operations: start/stop, VRDP toggle, port forward, SSH test.

## References

- [kali-access.md](references/kali-access.md) — Kali-specific notes: default creds, sshd setup, VRDP config caveats.
- [kali-grub-nomodeset.md](references/kali-grub-nomodeset.md) — Kali GRUB nomodeset fix.
- [usb-passthrough-rt73-kali.md](references/usb-passthrough-rt73-kali.md) — RT73 USB WiFi passthrough to Kali VM, recovery from broken networking after USB passthrough.
- [offline-vdi-repair.md](references/offline-vdi-repair.md) — VM unreachable? Recovery VM + GRUB müdahale + offline VDI onarım yöntemleri (NetworkManager-ifupdown çakışması, hatalı interfaces, vs.)
- [wsl2-kali.md](references/wsl2-kali.md) — WSL2 Kali distribution setup and usage on Windows host.