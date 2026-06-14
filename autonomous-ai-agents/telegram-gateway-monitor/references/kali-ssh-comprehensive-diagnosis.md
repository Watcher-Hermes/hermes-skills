# Kali SSH Comprehensive Diagnosis — Cron Job Context

## Observed Pattern (2026-06-07)

Kali VM "kal" was `VMState=running` but SSH was completely unreachable.

### What was tried:
1. **192.168.56.103** (configured in skill) → Connection timed out
2. **192.168.56.100** → **ICMP alive** (ping responded) but SSH **Connection refused**
3. **192.168.56.101** → Connection timed out
4. **192.168.56.102** → Connection timed out

### Diagnosis:
- .100 ping responds → host-only adapter is working, Kali has some network presence
- But SSH refused → sshd is NOT running on Kali, OR Kali booted without proper network stack
- `.100` could be the DHCP lease on host-only subnet (DHCP gave .100 instead of expected .101 or .103)

### Root Cause Likelihood:
1. **NetworkManager/ifupdown conflict** (most likely) — `/etc/network/interfaces` with `auto eth0` causes NetworkManager to mark eth0 as "unmanaged", networking.service hangs at boot, DHCP never completes, SSH never starts.
2. **sshd not running/listening** — Kali booted but sshd.service failed or is masked.
3. **iptables block** — Rare, but possible if ufw/iptables rules block port 22.

### Host-Only Subnet Quick Scan Command:
```bash
for ip in 192.168.56.{100..105}; do ping -n 1 -w 500 $ip 2>/dev/null && echo "$ip alive"; done
```

This is faster than nmap for a small subnet and gives immediate ICMP feedback.

### Cron Job Behavior:
When this happens during a cron run (no user present), the gateway monitor should:
1. Detect Kali SSH is down (timeout after ConnectTimeout=10)
2. Check if Kali VM is running (`VBoxManage list runningvms`)
3. If running but SSH down → fall back to Windows host management
4. The `gateway_state_watchdog.py` (no-agent, 2-min cycle) handles state issues regardless of which host manages the gateway
