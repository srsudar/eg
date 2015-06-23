# chmod

give read, write, and execute permissions to everyone

    chmod a+rwx file.txt


remove group write and execute permissions

    chmod g-wx file.txt


give execute permission to the owning user

    chmod u+x file.txt


remove all permissions from non-owning user and non-group members

    chmod o-rwx file.txt



# Basic Usage

Add (`+`) permissions to a file:

    chmod <to-whom>+<permissions> <file>


Remove (`-`) permissions from a file:

    chmod <from-whom>-<permissions> <file>



# Flags

Permissions can belong to the owning user (`u`), the group (`g`), and other
people in the world (`o`). All of these at once can be referred to as (`a`).
`ugo` is equivalent to `a`.

Permissions can be read (`r`), write (`w`), and execute (`x`).

Permissions are added with `+` and removed with `-`.



## Bit Representation

Permissions can also be specified with numbers acting as bit masks. `7` is
`111`, which turns on `rwx`. `777` translates to `111111111`, which turns on
`rwx` for all three permissions holders. `chmod 777` is thus equivalent to
`chmod a+rwx`:

    $ chmod 777 file.txt
    $ ls -l
    total 0
    -rwxrwxrwx  1 tyrion  group  0 Feb  5 11:40 file.txt


`4` is `100`, which corresponds to the read permission. This command will give
read, write, and execute permissions to the owning user, and read permission to
the group and others in the world:

    $ chmod 744 file.txt
    $ ls -l
    total 0
    -rwxr--r--  1 tyrion  group  0 Feb  5 11:40 file.txt



# Adding Permissions

Add execute (`+x`) permissions to the owning user (`u`):

    $ ls -l
    total 0
    -rw-r--r--  1 tyrion  group  0 Feb  5 11:40 file.txt
    $ chmod u+x file.txt
    $ ls -l
    total 0
    -rwxr--r--  1 tyrion  group  0 Feb  5 11:40 file.txt



# Removing Permissions

Remove read (`-r`) from all permissions holders (`a`). `a-r` is equivalent to
`ugo`:

    $ ls -l
    total 0
    -rw-r--r--  1 tyrion  group  0 Feb  5 11:40 file.txt
    $ chmod a-r file.txt
    $ ls -l
    total 0
    --w-------  1 tyrion  group  0 Feb  5 11:40 file.txt


