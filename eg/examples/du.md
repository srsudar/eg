# du

show size of foo.txt in human readable units

    du -h foo.txt


show size of directory in human readable units without listing contents

    du -sh directory



# Basic Usage

Show the size on disk in human readable units, as opposed to blocks:

    du -h <file>



## Sort by size on disk



### Linux

Sort by size on disk in human readable units:

    du -h <files> | sort -h


Using `-h` makes `sort` take size units into account:

    $ du -h *
    2.0M    a.log
    512K    b.log
    1.0G    c.log

    $ du -h * | sort
    1.0G    c.log
    2.0M    a.log
    512K    b.log

    $ du -h * | sort -h
    512K    b.log
    2.0M    a.log
    1.0G    c.log



### OSX

On OSX, the `coreutils` package will be necessary. Install it with:

    brew install coreutils

After having it installed, the `gsort` command will be available:

    du -h <files> | gsort -h


