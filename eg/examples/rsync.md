# rsync


copy the folder source_dir and its content into destination_dir

    rsync -av source_dir destination_dir


copy the contents of source_dir (trailing slash) into destination_dir

    rsync -av source_dir/ destination_dir


move the contents of source_dir into destination_dir

    rsync -av --remove-source-files source_dir/ destination_dir


update the contents of destination_dir to be the same as source_dir

    rsync -av --delete source_dir/ destination_dir


copy the contents of source_dir to a remote machine

    rsync -av source_dir/ user@remote_machine:/path/to/destination_dir


copy the contents of source_dir to a remote machine with non-default ssh port

    rsync -av -e "ssh -p 8888" source_dir/ user@remote:/path/to/destination_dir


move the contents from remote machine to local machine

    rsync -av --remove-source-files user@remote:source_dir/ destination_dir


see what actions would be performed without changing any files

    rsync -av --delete --dry-run source_dir/ destination_dir



# Basic usage

`rsync` can be used copy files and to make two directories identical.  Most of
the time you will want the `-a` flag, which stands for archive, and the `-v`
flag to verbosely list what exactly it is doing.

To copy contents of one directory to another run the command without the
`--delete` flag. This can increase the number of files in the destination
directory, but will never remove any files in the destination directory. A
trailing slash when specifying the source directory indicates to copy the
contents rather than the directory itself:

    rsync -av <source_dir>/ <destination_dir>


To make the contents of the two directories identical, use the `--delete` flag.
This will remove any files in the destination directory that are not present in
the source directory:

    rsync -av <source_dir>/ <destination_dir>


