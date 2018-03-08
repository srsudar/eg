# zip

compress foo.txt, bar.txt and dir/ as compressed.zip

    zip -r compressed.zip foo.txt bar.txt dir/


compress dir/ as compressed.zip, ignoring the .git directory

    zip -r compressed.zip dir/ -x '*.git*'



# Basic Usage

Compress a number of files or directories:

    zip -r <output-file> <list-of-files>


