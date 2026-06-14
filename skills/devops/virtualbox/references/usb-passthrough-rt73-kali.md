# RT73 USB WiFi → Kali VM Passthrough

## Device

- **Adapter**: RT73 USB Wireless LAN Card (Ralink RT73 chipset)
- **VID:PID**: 148F:2573
- **Revision**: 0001
- **Speed**: HighSpeed (USB 2.0)
- **Use OHCI/EHCI** — xHCI (USB 3.0) not needed and may cause boot issues

## Filter setup

```bash
VBoxManage usbfilter add 0 --target "kal" \
  --name "RT73 USB Wireless" \
  --vendorid 148F \
  --productid 2573 \
  --revision 0001
```

## Verification from VBox.log

Successful attach looks like:
```
VUSB: Attached '000001af412d7710[proxy 148f:2573]' to port 1 on RootHub#0 (HighSpeed)
EHCI: USB Operational
```

## Known issues

### 1. Wi-Fi passthrough kills VM network
When USB WiFi is attached at boot, Kali's NetworkManager may switch the default route to the USB WiFi interface. Since the WiFi is not connected to any network, the host-only/NAT interfaces lose their default gateway. Result: SSH/ping stop responding.

**Recovery**:
1. Remove USB filter: `VBoxManage usbfilter remove 0 --target kal`
2. Poweroff: `VBoxManage controlvm kal poweroff`
3. Wait 5s, restart
4. If still unreachable after 60s boot → console login needed:
   - Open VirtualBox GUI, start VM in windowed mode
   - Login: kali / 1234 (or configured password)
   - Run: `sudo dhclient eth1` and `sudo systemctl restart ssh`
5. If host-only adapter itself is stuck:
   - Kill VBoxSVC: `Stop-Process -Name VBoxSVC -Force`
   - Wait 5s, restart VM

### 2. VDI read-only lock after repeated cycles
Multiple `poweroff` → `startvm` cycles can leave VDI locked with `VERR_VD_IMAGE_READ_ONLY`.
```
VBoxManage.exe: error: Failed to open image '...kal.vdi' for writing due to wrong permissions (VERR_VD_IMAGE_READ_ONLY)
```
**Fix**: `Stop-Process -Name VBoxSVC -Force`, wait 5s, try again. Filesystem readonly attribute (`attrib`) will show `False` but VBoxSVC holds stale lock.

### 3. Host-only network unreachable after VM restart
If `ping 192.168.56.101` times out but host-only adapter on Windows shows:
```
IPAddress: 192.168.56.1
Status: Up
```
The problem is inside the VM's network config, not VirtualBox's. Console recovery needed.

## SSH command recipe
```bash
sshpass -p '<password>' /c/Windows/System32/OpenSSH/ssh.exe \
  -o StrictHostKeyChecking=no \
  -o ConnectTimeout=10 \
  kali@192.168.56.101 "<command>"
```

## Execution pattern on Windows/git-bash

PowerShell inline commands with `$_` fail when run via bash because bash interprets `$_` as a variable. Use separate `.ps1` files with `powershell.exe -File`:

```powershell
# Write to file
$script = @"
Get-PnpDevice | Where-Object { \$_.Class -eq 'Net' } | Select-Object FriendlyName,InstanceId | Format-List
"@
Set-Content -Path "C:\Users\marko\Desktop\list_wifi.ps1" -Value $script

# Execute
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\marko\Desktop\list_wifi.ps1"
```
