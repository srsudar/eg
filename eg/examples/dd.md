# dd

copy original.txt to copy.txt

    dd if=./original.txt of=copy.txt


skip the first five bytes of original.txt and print the rest to stdout

    dd bs=1 skip=5 if=./original.txt



# Basic Usage

`dd` is a powerful tool. If used incorrectly it can destroy a disk, so be very
careful with the input and output files you specify.

Copy what is read on stdin to stdout:

    dd


Copy an input file to an output file:

    dd if=<input-file> of=<output-file>



# Skipping Leading Bytes

`dd` can be used to skip the beginning bytes of a file, which can be useful
when manually interacting with file formats that include a compressed file
after some human readable bytes.

This command will set the input and output block size to 1 byte (`bs=1`) and
will skip the first 24 blocks (`skip=24`), printing file from 25 bytes onward
to stdout:

    dd if=inFile.txt bs=1 skip=24


This command also prints the file from 25 bytes onwards, but does so using a 24
byte block size (`bs=24`) and skipping one block (`skip=1`):

    dd if=inFile.txt bs=24 skip=1


