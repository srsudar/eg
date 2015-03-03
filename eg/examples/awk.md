# awk

print lines matching `foo`

    $ awk '/foo/' input.txt
    first line foo
    second line foo
    FOURTH LINE foo


match foo, split on whitespace, and print the first element in the split array

    $ awk '/foo/ { print $1 }' input.txt
    first
    second
    FOURTH



# Basic Usage

Print a subset of lines from a file. 

    awk '/<pattern>/' <inputfile>

    
The forward slashes around `<pattern>` are required for POSIX-style regular
expressions.

Wrap everything going to `awk` in single quotes and give it the name of an
input file.

More complicated processing of matching lines can go in curly braces. This will
print each line that matches foo:

    awk '/foo/ { print }' input.txt

    

# Print Matching Lines

`awk` prints lines by default, so no command prints the whole matching line.
`$0` is special and means the whole matching line. The following three commands
are all equivalent. Each will print every line from a file matching `foo`
(`/foo/`):

    $ awk '/foo/' input.txt
    $ awk '/foo/ { print }' input.txt
    $ awk '/foo/ { print $0 }' input.txt



# Columns and Fields

`awk` divides each lines into an array of "fields", much like `split`. By
default it splits on whitespace.

Fields are referred to by a `$` and an index. `$2` means the second field in
the line.

Fields are 1-indexed--i.e. `$2` would refer to the second colum in a file.

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



# Print All Fields

`awk -F: ' { for (i = 1; i < NF; i++) print $i }'`

Split lines into field on `:` (`-F:`).

Print all fields using a for loop. `NF` is the number of fields in the line,
`print $2` will print the second field.

This command will print your path, assuming it is colon-delimited:

`echo $PATH | awk -F: ' { for (i = 1; i < NF; i++) print $i }'`
