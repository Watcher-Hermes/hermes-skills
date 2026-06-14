# Start WireGuard and enable on boot
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```