# touch

create an empty file

    touch empty_file.txt


update the access time of a file to the current instant

    touch old_file.txt


update the access time of the file to Dec 25, 1999, 2:25:33pm

    touch -t 199912251425.33 file.txt



# Basic Usage

Update the access time of a file or create a new file if it doesn't exist:

    touch <file>



# Update to Specific Access Time

The `-t` flag can be used to set the access time to a particular date in the
format `YYYYMMDDhhmm.ss`. Times are specified using a 24-hour format. The
following command sets the access time of `foo.txt` to Dec 25, 1999, at
2:25:33pm (`-t 199912251425.33`):

    $ ls -lT
    total 0
    -rw-r--r--  1 tyrion  group  0 Feb  7 12:32:07 2015 foo.txt
    $ touch -t 199912251425.33 foo.txt
    $ ls -lT
    total 0
    -rw-r--r--  1 tyrion  group  0 Dec 25 14:25:33 1999 foo.txt


