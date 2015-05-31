# od

show character with helpful names and offset in decimal

    od -a -Ad chars.txt


show human readable 16 per line

    od -Ad -tc human_readable.txt


show escaped characters (\n new line, \t tab, etc)

    od -i chars.txt


show character with helpful names and no offset

    od -a -An chars.txt


show as single hex characters

    od -t x1 single_hex.txt


start after 500kb and only show 30 bytes

    od -j 500k -N 30 bigfile.txt



# Basic Usage

Show the byte contents of a file in octal with octal offsets:

    od <file>



# Showing Byte Contents of Files

By default `od` displays the offset and values of files in octal. This can be
modified with flags. The following file is used in these examples:

    $ cat abc.txt
    a b
    c
    1 2 3


Show the contents of the file with useful names (`-a`) and offset in decimal
(`-Ad`):

    $ od -a -Ad abc.txt
    0000000    a  sp   b  nl   c  nl   1  sp   2  sp   3  nl
    0000012


Show the contents of the file with characters escaped in the C style(`-c`) and
the offset in hex (`-Ax`):

    $ od -c -Ax abc.txt
    0000000    a       b  \n   c  \n   1       2       3  \n
    000000c


