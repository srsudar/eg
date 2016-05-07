# cp

copy a file

    cp original.txt copy.txt


copy a directory

    cp -R directory directory_copy


prompt if will overwrite existing file

    cp -i foo.txt directoryWithFoo/



# Basic Usage

Copy a file:

    cp <original_file> <copied_file>


Copy a directory using the recursive (`-R`) flag:

    cp -R <original_directory> <copied_directory>



# Directories

Behavior differs if the argument that is the directory being copied ends with a
`/`. If it does end with a `/` the contents are copied as opposed to the
directory itself. For example, `cp -R foo/ bar` will take the contents of the
`foo` directory and copy them into `bar`, while `cp -R foo bar` will copy `foo`
itself and put it into `bar`.


