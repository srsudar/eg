# scp

copy a local file to another machine

    scp original.txt username@host:~/directory/copy.txt


copy a remote file to the local directory

    scp username@host:~/original.txt ./copy.txt


recursively copy a local directory to another machine

    scp -r directory username@host:~/directory_copy



# Basic Usage

Securely copy a file to another machine:

    scp <original_file> <username>@<host>:<path_to_copy>



# Copying to Another Machine

Use `scp` to copy a file (`original.txt`) as user `tyrion` on machine
`casterly_rock.com` (`tyrion@casterly_rock.com`). The file will be copied to
`~/directory` as `copy.txt`:

    $ scp original.txt tyrion@casterly_rock.com:~/directory/copy.txt
    tyrion@casterly_rock.com's password:
    original.txt


