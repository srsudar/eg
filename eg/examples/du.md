# du

show size of foo.txt in human readable units

    du -h foo.txt


show size of directory in human readable units without listing contents

    du -sh directory



# Basic Usage

Show the size on disk in human readable units, as opposed to blocks:

    du -h <file>



## Sort by Human-Readable Size on Disk

By default `du` displays file size in blocks. This allows easy sorting by
piping to `sort`:

    du <files> | sort


However, this will fail when the `-h` flag is used to show disk usage in
human-readable units, as 1G is lexicographically before 1M, even though 1M is
smaller than 1G. This can be overcome by system-dependent usage of the `sort`
command.



### Linux

Sort by size on disk in human readable units (`-h`):

    du -h <files> | sort -h



### OSX

On OSX, the `coreutils` package will be necessary. Install it with:

    brew install coreutils


After having it installed, the `gsort` command will be available, which can
sort by human readable units (`-h`):

    du -h <files> | gsort -h


