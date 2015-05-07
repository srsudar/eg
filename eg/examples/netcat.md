# netcat

send a file to the address *192.168.1.42* on port *1337*

    cat file | netcat 192.168.1.42 1337

send a file to the address *192.168.1.42* on port *1337* with progress

    pv file | netcat 192.168.1.42 1337

receive a file on port *1337*

    netcat -l -p 1337 > file



# Basic Usage

Send what is read from *stdin*:

    netcat <address> <port>

Receive a file and send it to *stdout*:

    netcat -l -p <port>


