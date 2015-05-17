# tar

extract .tar file

    tar vfx archive.tar


unzip and extract .tar.gz or .tgz file

    tar vfxz g_zipped_archive.tar.gz


turn directory into a .tar file

    tar vfc tarred_directory.tar directory


turn directory into g-zipped directory

    tar vfcz z_zipped_directory.tar.gz directory



# Basic Usage

`vf` means verbosely list files (`v`) and use a file (`f`), not `stdin`.
These appear in most commands.

Untar a file:

    tar vfx <tar-file-to-extract>


Create a tar file from a directory:

    tar vfc <name-of-tar-file> <directory-to-tar>



# Remembering the Flags

`tar` is very finicky. Flags don't need to be prepended by a hyphen, but are
instead bundled into the first word on the command line. A leading hyphen will
break some implementations or require an order. For example, `tar vfx` might
work while with a hyphen it would require `tar -xvf`, with the `x` flag first.
You can get maximum portability is you never use the hyphens, so examples here
are shown without the hyphen.

You'll almost always want `vf`. `v` verbosely lists files as they are
manipulated, and `f` means you're reading from a file, not `stdin`. You can
remember `vf` if you remember that `tar` is Very Finicky: `vf`.

Extract things from a tar file with `x` for extraction. Compress things to a
tar file with `c` for compress.

And you'll have to just remember that g-zipping is `z` and b-zipping is `j`.



# Tarring

Compress directory (`c`) into g-zipped (`z`) directory:

    tar vfcz z_zipped_directory.tar.gz directory


Compress directory (`c`) into b-zipped (`j`) directory:

    tar vfcj b_zipped_directory.tar.bz2 directory


Compress directory (`c`) into xz-zipped (`J`) directory:

    tar vfcJ xz_zipped_directory.tar.xz directory



# Untarring

Untar (`x`) and unzip a g-zipped (`z`) file:

    tar vfxz g_zipped_archive.tar.gz


Untar (`x`) and unzip a b-zipped (`j`) file:

    tar vfxj b_zipped_archive.tar.bz2


Untar (`x`) and unzip an xz-zipped (`J`) file:

    tar vfxJ xz_zipped_archive.tar.xz



## Partial Untarring

Extract only part of the contents (`directory/foo.txt`) from a .tar file:

    tar vfx archived_directory.tar directory/foo.txt



# Display Contents

List (`t`) the contents of a tar file without untarring it:

    $ tar vft tarred_directory.tar
    drwxr-xr-x  0 tyrion group       0 Feb  4 14:54 directory/
    -rw-r--r--  0 tyrion group       0 Feb  4 14:54 directory/bar.txt
    -rw-r--r--  0 tyrion group       0 Feb  4 14:54 directory/foo.txt
