# Trunk port to router/uplink (tagged for all VLANs)
/interface bridge port
add bridge=bridge interface=ether1 frame-types=admit-only-vlan-tagged