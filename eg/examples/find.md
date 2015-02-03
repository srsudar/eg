# find
    
    files
    ```
    $ find /dir/to/search -name 'file.txt'
    /dir/to/search/file.txt
    ```

    directories
    ```
    $ find /dir/to/search -type d -name 'directory'
    /dir/to/search/directory
    ```

    more info
    ```
    $ find /dir/to/search -name 'file.txt' -ls
    118871021  0 -rw-r--r--  1 staff  staff 0 Feb  2 11:14  /dir/to/search/file.txt
    ```

# Basic Usage

To find a basic file or directory:
`find <folder-to-search> -name <file-name-pattern>`

To find only a directory:
`find <folder-to-search> -type d -name <file-name-pattern>`


# Directories
> aliases: directories, directory, folder, folders

List only directories by specifying `-type d`.

```
$ find /dir/to/search -type d -name 'directory'
/dir/to/search/directory
```
