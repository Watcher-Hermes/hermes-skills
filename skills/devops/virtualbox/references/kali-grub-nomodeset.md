# Kali Linux — GRUB nomodeset Fix (VirtualBox Black Screen)

## Problem
Kali boots to a blinking cursor / black screen inside VirtualBox after a fresh or updated install.

## Cause
Kali (GNOME) + VirtualBox GPU initialization mismatch.

## Quick VM-side fix

Recommended settings before boot:
- graphicscontroller: vboxvga
- vram: 128
- accelerate3d: off
- x86-pae: on

## Manual one-time boot bypass

1. Boot VM and wait for GRUB menu.
2. Press `E` to edit the boot entry.
3. Find the `linux` line.
4. Append `nomodeset` to the end of that line.
5. Press `F10` to boot.

## Persistent fix from Kali desktop

Once Kali boots successfully:
```bash
sudo nano /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset"
sudo update-grub
```

## Troubleshooting

- If GUI edits in VirtualBox keep failing due to session locks, close VirtualBox and rerun `VBoxManage`.
- If `VBoxManage modifyvm` still reports a lock, stop `VirtualBoxVM.exe` and retry after a few seconds.
