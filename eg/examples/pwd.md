# pwd

print the current working directory

    pwd



# Basic Usage

Print the current working directory:

    pwd



# Resolve Symbolic Links

Show the physical location of the current working directory by using the `-P`
flag:

    $ ls -aF
    total 8
    drwxr-xr-x  2 tyrion  group  68 Feb  3 16:05 directory/
    lrwxr-xr-x  1 tyrion  group   9 Feb  3 16:05 link-to-directory@ -> directory
    $ cd /Users/tyrion/link-to-directory
    $ pwd
    /Users/tyrion/link-to-directory
    $ pwd -P
    /Users/tyrion/directory


