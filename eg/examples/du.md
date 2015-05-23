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



### OSX

On OSX, the `coreutils` package will be necessary. Install it with:

    brew install coreutils

After having it installed, sort by size on disk in human readable units:

    du -h <files> | sort -h


