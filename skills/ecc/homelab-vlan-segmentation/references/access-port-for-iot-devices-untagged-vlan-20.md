# Access port for IoT devices (untagged VLAN 20)
/interface bridge port
add bridge=bridge interface=ether3 pvid=20 frame-types=admit-only-untagged-and-priority-tagged