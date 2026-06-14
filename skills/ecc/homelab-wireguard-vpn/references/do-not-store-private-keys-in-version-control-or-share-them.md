# Do not store private keys in version control or share them
sudo tee /etc/wireguard/wg0.conf << 'EOF'
[Interface]
Address = 10.8.0.1/24              # VPN subnet — server gets .1
ListenPort = 51820
PrivateKey = <paste_server_private_key_here>