# locate

find a file where any part of path matches foo

    locate foo


find a file where only the base file name itself, not the path, matches foo

    locate -b foo


ignore case

    locate -i FoO


count the number of files that match foo

    locate -c foo



# Basic Usage

`locate` uses a database to quickly find files matching a pattern:

    locate <pattern>


Not all files get included in the database used by `locate`. Only those that
can be seen by the world (i.e. those files where every parent directory has the
world permission set to readable). For this reason it is most reliably used to
find system files.



# Building the Database

`locate` relies on a database. Usually the system builds automatically, but it
may need to be initialized or updated manually.



## OSX 10.9

Update the database:

    $ cd /
    $ sudo /usr/libexec/locate.updatedb



## Linux

Update the database:

    sudo updatedb


