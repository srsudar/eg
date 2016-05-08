# grep

print all lines containing foo in input.txt

    grep "foo" input.txt


print all lines matching the regex "^start" in input.txt

    grep -e "^start" input.txt


print all lines containing bar by recursively searching a directory

    grep -r "bar" directory


print all lines containing bar ignoring case

    grep -i "bAr" input.txt


print 3 lines of context before and after each line matching "foo"

    grep -C 3 "foo" input.txt



# Basic Usage

Search each line in `input_file` for a match against `pattern` and print
matching lines:

    grep "<pattern>" <input_file>



# Find Lines NOT Matching

Print lines that do NOT match a pattern by using the `-v` flag. This will print
all lines that do NOT contain a z (`-v "z"`):

    grep -v "z" input.txt



# Print File Names

Show only the file names containing matches, rather than the matching lines
themselves, by using the `-l` flag:

    grep -r -l "target_pattern" directory


Show only the file names that do NOT contain matches by using the `-L` flag:

    grep -r -L "unwanted_pattern" directory



# Regular Expressions and `egrep`

Regular expressions can be passed to `grep` using the `-e` flag. `egrep` is
equivalent to using the `-e` flag.

The following file is used in the examples:

    $ cat input.txt
    1 2 3
    omega
    alpha foo
    alpha bar
    baz omega
    4 5 6


Match lines beginning (`^`) with `alpha` (`^alpha`):

    $ grep -e "^alpha" input.txt
    alpha foo
    alpha bar


Match lines ending (`$`) with `omega` (`omega$`):

    $ grep -e "omega$" input.txt
    omega
    baz omega


Match any line containing `a` and `o` separated by 0 or more characters (`.*`):

    $ grep -e "a.*o" input.txt
    alpha foo
    baz omega


Match any line containing `z` or `f` (`[zf]`):

    $ grep -e "[zf]" input.txt
    alpha foo
    baz omega


Match all lines with lower case or capital letters a through z (`[a-zA-Z]`):

    $ grep -e "[a-zA-Z]" input.txt
    omega
    alpha foo
    alpha bar
    baz omega


Match all lines containing numbers (`[0-9]`):

    $ grep -e "[0-9]" input.txt
    1 2 3
    4 5 6


Match all lines containing white space (`[[:space:]]`):

    $ grep -e "[[:space:]]" input.txt
    1 2 3
    alpha foo
    alpha bar
    baz omega
    4 5 6


# Fixed Expressions and `fgrep`

`fgrep` is faster than `grep` and `egrep` but only accepts fixed expressions.
This will match lines containing the exact sequence `.*` (`'.*'`). Quoting is
used to prevent shell expansion of the wildcard `*` character:

    fgrep '.*' input.txt



# Searching Compressed Files

`zgrep`, `zegrep`, and `zfgrep` act exactly like `grep`, `egrep`, and `fgrep`,
but they operate on compressed and gzipped files. The same examples shown above
will function with the `z*grep` utilities.


