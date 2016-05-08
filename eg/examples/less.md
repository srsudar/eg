# less

page file to stdout

    less file.txt


page file starting at line 25

    less +25 file.txt


page file starting at first line containing "pattern"

    less +/"pattern" file.txt



# Basic Usage

Show the file on `stdout`, paging the input:

    less <file>


Once in `less` use `j` to scroll down, `k` to scroll up, and `q` to quit.

`gg` goes to the top of the file and `G` goes to the bottom.

Press `h` to get help and see the full list of commands.


