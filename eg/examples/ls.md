# ls

show contents of current directory

    ls


show contents of directory

    ls directory


show contents, hidden files, and stats in human readable form

    ls -alh


show extended time information

    ls -lT


show with color and indicators of file type

    ls -FG



# Basic Usage

Display the contents of a directory:

    ls <directory>



# Showing Hidden Files

The `-a` flag will show all files, including those that are hidden, or begin
with a dot. `.` means the current directory, and `..` means the parent
directory:

    $ ls -a
    .               ..              .hidden.txt     bar.txt



# Showing More Information

The `-l` flag will show extended information, including permissions, the number
of hard links to the file, owner, group, size in bytes, and date modified:

    $ ls -l
    total 16
    drwxr-xr-x  4 tyrion  group  136 Feb  7 12:09 directory
    -rwxr-xr-x  1 tyrion  group    0 Feb  3 14:06 executable
    -rw-r--r--  1 tyrion  group   15 Feb  3 14:01 foo.txt
    lrwxr-xr-x  1 tyrion  group    7 Feb  3 14:06 link-to-foo.txt -> foo.txt


Human-readable size formats with units can be shown with the `-h` flag:

    $ ls -lh
    total 16
    drwxr-xr-x  4 tyrion  group   136B Feb  7 12:09 directory
    -rwxr-xr-x  1 tyrion  group     0B Feb  3 14:06 executable
    -rw-r--r--  1 tyrion  group    15B Feb  3 14:01 foo.txt
    lrwxr-xr-x  1 tyrion  group     7B Feb  3 14:06 link-to-foo.txt -> foo.txt


Indicators of file type can be included with the `-F` flag:

    $ ls -F
    directory/    executable*    foo.txt    link-to-foo.txt@


Extended time format can be shown with the `-T` flag:

    $ ls -lT
    total 16
    drwxr-xr-x  4 tyrion  group  136 Feb  7 12:09:34 2015 directory
    -rwxr-xr-x  1 tyrion  group    0 Feb  3 14:06:15 2015 executable
    -rw-r--r--  1 tyrion  group   15 Feb  3 14:01:12 2015 foo.txt
    lrwxr-xr-x  1 tyrion  group    7 Feb  3 14:06:40 2015 link-to-foo.txt -> foo.txt



# Useful Aliases

`ls` is often aliased to make the defaults a bit more useful. Here are three
basic aliases. The second two can be remembered by "list long" and "list all":

    $ alias ls='ls -FG'
    $ alias ll='ls -lhF'
    $ alias la='ll -A'


