# awk

print lines matching `foo`

    awk '/foo/' input.txt


match foo, split on whitespace, and print the first element in the split array

    awk '/foo/ { print $1 }' input.txt


use `:` as the field delimiter

    awk -F:



# Basic Usage

Print a subset of lines from a file:

    awk '/<pattern>/' <inputfile>


The forward slashes around `<pattern>` are required for POSIX-style regular
expressions.

Wrap everything going to `awk` in single quotes and give it the name of an
input file.

More complicated processing of matching lines can go in curly braces. For
example, this command will print each line that matches foo:

    awk '/foo/ { print }' input.txt



# Print Matching Lines

`awk` prints lines by default, so no command prints the whole matching line.
`$0` is special and means the whole matching line. The following three commands
are all equivalent. Each will print every line from a file matching `foo`
(`/foo/`) (output is not shown):

    $ awk '/foo/' input.txt
    $ awk '/foo/ { print }' input.txt
    $ awk '/foo/ { print $0 }' input.txt



# Columns and Fields

`awk` divides each lines into an array of "fields", much like `split`. By
default it splits on whitespace.

Fields are referred to by a `$` and an index. `$2` means the second field in
the line.

Fields are 1-indexed--i.e. `$2` would refer to the second column in a file.

`thrones.txt`:

    Tyrion   Lannister    555.360.1234
    Jamie    Lannister    555.360.9876
    Jon      Snow         555.206.4444
    Arya     Stark        555.206.1111


Match lines containing `Lannister`, print the first field (split on
whitespace):

    $ awk '/Lannister/ { print $1 }' thrones.txt
    Tyrion
    Jamie



# For Loops

For loops can be used to do things like print all the fields in a line. Here
`NF` is the number of fields on every line in the file `input.txt`. We match
all lines (by not giving a pattern) and print all fields, splitting on
whitespace by default:

    awk '{ for (i = 1; i < NF; i++) print $i }' input.txt


