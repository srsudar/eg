# ping

check if www.google.com is reachable

    ping www.google.com


stop pinging after 10 seconds

    ping -w 10 www.google.com


wait 3 seconds between packets

    ping -i 3 www.google.com


send only 2 packets then stop

    ping -c 2 www.google.com


send a packet size of 10 bytes instead of the default 56

    ping -s 10 www.google.com



# Basic Usage

Use the ICMP protocol to check if a host is reachable:

    ping <host>


By default `ping` sends 56 bytes in a packet plus 8 bytes of header, for a
total of 64 bytes. This can be adjusted with the size (`-s`) option:

    ping -s <size> <host>


Use `<CTRL>-c` to stop `ping`.


