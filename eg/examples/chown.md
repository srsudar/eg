# chown

change user

    sudo chown username file.txt


change user recursively for all files

    sudo chown -R username directory


change user and group

    sudo chown username:groupname file.txt


change group

    sudo chown :groupname file.txt



# Basic Usage

The caller needs to be a super-user to perform `chown`. Examples are shown
using `sudo`, which is not required if the user is a super-user.

Change the ownership of a file:

    sudo chown <user> <file>


