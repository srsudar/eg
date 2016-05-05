# ln

make a symlink to `foo.txt`

    ln -s foo.txt link-to-foo.txt



# Basic Usage

Make anchor a link to target:

    ln -s <target> <anchor>



# Symbolic Links (symlinks)

Make it symbolic with the `-s` flag:

    $ ln -s foo.txt link-to-foo.txt
    $ ls -lF
    total 8
    -rw-r--r--  1 tyrion  group  0 Feb  3 14:13 foo.txt
    lrwxr-xr-x  1 tyrion  group  7 Feb  3 14:14 link-to-foo.txt@ -> foo.txt



# Hard Links

Omit the `-s` flag:

    $ ln foo.txt hard-link-to-foo.txt
    $ ls -lF
    total 0
    -rw-r--r--  2 tyrion  group     0B Feb  3 14:13 foo.txt
    -rw-r--r--  2 tyrion  group     0B Feb  3 14:13 hard-link-to-foo.txt


