# find
    
files in searchdir named file.txt

    find ./searchdir -name file.txt


only directories in searchdir

    find ./searchdir -type d


show more info

    find ./searchdir -name 'file.txt' -ls



# Basic Usage

Find files and directories matching a given name.

    find <searchdir> -name <name>



# By Name

Search `/searchdir` for files and directories named `file.txt`:

    find ./searchdir -name file.txt



## Case Insensitive

Use `-iname` for case insensitive name searching.

    $ find ./searchdir -iname file.txt
    ./searchdir/file.txt
    ./searchdir/bar/FiLe.TxT



## Wildcards

Wildcards are supported with quotes.

Find files starting with `prefix`:

    $ find ./searchdir -name "prefix*"
    ./searchdir/prefix.txt
    ./searchdir/prefixAndMore.txt



# By Type

## Files only

Will find files (`-type f`) but not directories named `foo`:

    find ./searchdir -type f foo



## Directories and Folders

List only directories by specifying `-type d`.

    $ find ./searchdir -type d -name 'directory'
    ./searchdir/directory



# Size

Use the `-size` flag followed by a number and a unit. Without a unit it matches
blocks.

Find entries exactly two bytes (`-size 2c`). `c` stands for character:

    find ./searchdir -size 2c


Find files exactly 2 kilobytes (`-size 2k`):

    find ./searchdir -size 2k


Find files exactly 2 megabytes (`-size 2M`):

    find ./searchdir -size 2M



## Ranges

Prefix a size with `+` for >= that value and `-` for <= that value.

Find files greater than 5k (`-size +5k`):

    find /dir/to/search +5k


Find files less than 5k (`-size -5k`):

    find /dir/to/search -5k



# Depth

Find files and directories only two levels deep (`-depth 2` or `-d 2`):

    $ find ./one -depth 2
    ./one/two
    ./one/foo.txt


Find only files (`-type f`) >= two levels (`-mindepth 2`) and <= three levels
(`-maxdepth 3`) deep.

    $ find ./one -type f -mindepth 2 -maxdepth 3
    ./one/twoLevels.txt
    ./one/two/threeLevels.txt



# Boolean Operators

Flags are ANDed by default, but can also achieve OR and NOT functionality.



## AND

List files greater bigger than 500k (`+500k`) and named `bigFile.txt`
(`-name bifile.txt`). These two commands are equivalent:
    
    $ find ./searchdir -size +500k -name bigFile.txt
    $ find ./searchdir -size +500k -and -name bigFile.txt


## OR

List files bigger than 500k (`+500k`) or those that are named `smallFile.txt`
(`-or -name smallFile.txt`):

    find ./searchdir -size +500k -or -name smallFile.txt


## NOT

List files bigger than 50 megabytes (`-size +50M`) that are not named
`unwanted.txt` (`-not -name unwanted.txt`):

    find ./searchdir -size +50M ! -name unwanted.txt


