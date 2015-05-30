# rar

To compress the file

    rar a compressedfile.rar 0 1 2 3 4 5


To uncompress the file

    unrar x compressedfile.rar [In this situation we usually will use shopt -s extglob rm!(*.rar), since the file was uncompressed in this folder]


To uncompress the file to a Specific folder

    unrar e compressedfile.rar /directory/to/path 
