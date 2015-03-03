# ifconfig

display information about network interfaces

    ifconfig


display MAC addresses

    ifconfig | grep ether


set a new MAC address to en0

    sudo ifconfig en0 ether aa:bb:cc:dd:ee:ff


display local IP addresses

    ifconfig | grep 'inet ' | grep -v '127.0.0.1' | cut -d' ' -f2



# Basic Usage

Display basic information:

    ifconfig


Set network parameters:

    sudo ifconfig <interface> <family> <new_address>


