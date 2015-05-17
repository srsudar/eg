# netcat

listen on port 1337

    nc -l 1337


send a file to the address 192.168.1.42 on port 1337

    cat file | nc 192.168.1.42 1337


send a file to the address 192.168.1.42 on port 1337 with progress

    pv file | nc 192.168.1.42 1337


check if 127.0.0.1 is listening on port 80 but do not connect

    nc -vz 127.0.0.1 80


receive input on port 1337 and save as file

    nc -l 1337 >file



# Basic Usage

Send what is read from stdin to an address and a port:

    nc <address> <port>


Listen on a port and send it to stdout:

    nc -l <port>


