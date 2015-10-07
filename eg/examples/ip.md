# ip

To Display Device Attributes

    ip link show

To enable a network interface

    ip link set eth0 up

To disable a network interface

    ip link set eth0 down

Assign an IP address to an interface

    ip addr add 10.0.0.2/24 dev eth0

Delete the IP address from an interface

    ip addr del 10.0.0.2/24 dev eth0


View the Routing table

    ip route show

Set a Route to the Locally connected Network

    ip route add 10.0.0.0/24 dev eth0

Set a Route to a Different network

    ip route add 192.168.1.0/24 via 10.0.0.100

Set a Default Route

    ip route add default via 10.0.0.254 dev eth0

Delete Routes from the Routing table

    ip route delete 192.168.1.0/24 dev eth0



# Basic Usage
Display info about all network interfaces

    ip addr

Use `ip` command to display and configure the network parameters for host interfaces.

    ip OBJECT COMMAND
    ip [options] OBJECT COMMAND
    ip OBJECT help

# ARP

Show ARP cache

    ip n show

Add a new ARP entry. States: permanent|noarp|stale|reachable

    ip neigh add <IPAddress> lladdr <MAC/LLADDRESS> dev <DEVICE> nud <STATE>

Delete a ARP entry

    ip neigh del <IPAddress> dev <DEVICE>

Flush ARP entry

    ip -s -s n f <IPAddress>
