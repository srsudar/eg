# ls

show contents of current directory

    $ ls
    directory     executable      foo.txt       link-to-foo.txt

show contents, hidden files, and stats

    $ ls -al
    total 16
    drwxr-xr-x   6 sudars  staff  204 Feb  3 14:06 .
    drwxr-xr-x  10 sudars  staff  340 Feb  3 14:00 ..
    drwxr-xr-x   3 sudars  staff   68 Feb  3 14:00 directory
    -rwxr-xr-x   1 sudars  staff    0 Feb  3 14:06 executable
    -rw-r--r--   1 sudars  staff   15 Feb  3 14:01 foo.txt
    lrwxr-xr-x   1 sudars  staff    7 Feb  3 14:06 link-to-foo.txt -> foo.txt

show contents with color and indicating file type

    $ ls -FG
    directory/       executable*      foo.txt          link-to-foo.txt@

show contents of `directory`

    $ ls directory
    bar.txt
    
