# ip

display device attributes

    ip link show


enable a network interface

    ip link set eth0 up


disable a network interface

    ip link set eth0 down


assign an IP address to an interface

    ip addr add 10.0.0.2/24 dev eth0


delete the IP address from an interface

    ip addr del 10.0.0.2/24 dev eth0


view the routing table

    ip route show


set a route to the locally connected network

    ip route add 10.0.0.0/24 dev eth0


set a route to a different network

    ip route ass 192.168.1.0/24 via 10.0.0.100


set a default route

    ip route add default via 10.0.0.254


delete routes from the routing table

    ip route delete 192.168.1.0/24 dev eth0



# Basic Usage

Display info about all network interfaces:

    ip addr


Use the `ip` command to display and configure the network parameters for host
interfaces. The first argument after `ip` is referred to as the OBJECT. Type
`ip` to see the list of valid OBJECT arguments on your machine. Typing `help`
after the OBJECT will provide more detailed information. This will display
information about the `addr` OBJECT:

    ip addr help



# Address Resolution Protocol (ARP)

Show ARP cache:

    ip neigh show


Add a new ARP entry. Valid STATE arguments are  `permanent`, `noarp`, `stale`,
and `reachable`:

    ip neigh add <IPAddress> lladdr <MAC/LLADDRESS> dev <DEVICE> nud <STATE>


Delete ARP entry:

    ip neigh del <IPAddress> dev <DEVICE>


Flush ARP entry:

    ip -s -s n f <IPAddress>



# OSX

`ip` is not available by default on OSX. Install `iproute2mac` to make `ip`
available (`brew install iproute2mac`). This is a similar tool to `ip` on
Linux, but it is not identical and some examples here may not work.


