# hexdump

show file byte content in hex with hex offset

    hexdump in_hex.txt


show file content in a more human readable manner

    hexdump -e '7/ "%5_ad:%-5_c" "\n"' human_readable.txt



# Basic Usage

Show the byte content of a file in hex:

    hexdump <file>



# Advanced Formatting

The output of `hexdump` can be highly customized with the `-e` flag.

The following file is used in this example:

    $ cat abc.txt
    a b
    c
    1 2 3


This command prints seven bytes (`7/`) and delimits these bytes with a
new line (`\n`). It shows the input offset of each byte in decimal (`_ad`)
padded to five characters (`%5`). Then display a colon (`:`) and the character
itself (`_c`) padded to five trailing characters (`%-5`):

    $ hexdump -e '7/ "%5_ad:%-5_c" "\n"' abc.txt
        0:a        1:         2:b        3:\n       4:c        5:\n       6:1
        7:         8:2        9:        10:3       11:\n        :          :    


