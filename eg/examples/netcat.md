# netcat

listen on port 1337

    netcat -l 1337


send a file to the address 192.168.1.42 on port 1337

    cat file | netcat 192.168.1.42 1337


send a file to the address 192.168.1.42 on port 1337 with progress

    pv file | netcat 192.168.1.42 1337


check if port 80 is open without sending any data

    nc -vz 80


receive input on port 1337 and save as file

    netcat -l 1337 >file



# Basic Usage

Send what is read from stdin to an address and a port:

    netcat <address> <port>


Listen on a port and send it to stdout:

    netcat -l <port>


