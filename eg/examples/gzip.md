# gzip

compress a file

    gzip file_to_compress


decompress a file

    gzip -d file_to_decompress


compress a file and keep original

    gzip --keep file_to_compress


decompress a file and keep original

    gzip --keep -d file_to_decompress



# Basic Usage

`gzip` by default deletes the file that is being compressed or decompressed. To
keep the original file use the `--keep` flag.


