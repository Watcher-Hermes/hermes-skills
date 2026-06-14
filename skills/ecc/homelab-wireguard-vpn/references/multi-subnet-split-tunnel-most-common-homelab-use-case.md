# Multi-subnet split tunnel (most common homelab use case):
  AllowedIPs = 192.168.10.0/24, 192.168.20.0/24, 192.168.30.0/24, 10.8.0.0/24
  Routes all your VLANs through the tunnel; internet stays direct.
```