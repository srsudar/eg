# nc

receive input on port 1337

    nc -l 1337


receive input on port 1337 on GNU nc implementation

    nc -l -p 1337


receive input on port 1337 without hanging up after a connection

    nc -k -l 1337


send a file to the address 192.168.1.42 on port 1337

    cat file | nc 192.168.1.42 1337


send a file to the address 192.168.1.42 on port 1337 with progress

    pv file | nc 192.168.1.42 1337


check if 127.0.0.1 is listening on port 80 but do not connect

    nc -vz 127.0.0.1 80



# Basic Usage

Send what is read from stdin to an address and a port:

    nc <address> <port>


Send what is read from stdin to an address and a port on the GNU implementation
of `nc`:

    nc <address> -p <port>


Listen on a port and send it to stdout:

    nc -l <port>


Listen on a port and send it to stdout on the GNU implementation of `nc`:

    nc -l -p <port>



# Compatibility

Usage for `nc`, or `netcat`, varies highly depending on your system. Some
implementations require both the `-l` and `-p` flags to listen on a port, for
instance, whereas others explicitly list using the `-l` and `-p` flags together
is an error. Use these examples as a starting point, but turn to `man` for the
specifics of your implementation.


