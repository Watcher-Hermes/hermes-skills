# WSL2 Kali Decision Reference

Use this when user wants keyboard/terminal access to Kali and wants to avoid VirtualBox networking/SSH troubleshooting.

## Decision rule
```
goal == terminal/scripted access:
  install/use WSL2 Kali via `wsl --install -d kali-linux`
goal == GUI Kali in VirtualBox:
  continue with VirtualBox Kali + Host-Only/NAT networking
```

## Why this exists
VirtualBox Linux guest networking often blocks Host-Only IP detection and SSH access, leading to repeated failures. WSL2 provides direct terminal access without VirtualBox GuestInfo or port-forward complexity.

## Install steps
- `wsl --install -d kali-linux`
- Default Kali user is usually `kali`/`kali`
- Confirm with: `wsl -d kali-linux whoami` / `wsl -d kali-linux ip addr`
