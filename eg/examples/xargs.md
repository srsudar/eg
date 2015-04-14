# xargs

print commands as they are executed

    xargs -t


parallelize ls with at most 5 processes

    xargs -P 5 ls


combine with find to remove all .txt files in directory

    find directory -name "*.txt" -print0 | xargs -0 -t rm



# Basic Usage

`xargs` is used to pass arguments to commands:

    <command_to_generate_arguments> | xargs <command_to_consume_arguments>



# Splitting Arguments

The `-n` command can specify how many arguments should be passed to `xargs` at
a time, splitting on whitespace. For example, this command will split the
`1 2 3 4 5 6` given to `echo` on whitespace and take two at a time (`-n 2`).
It will `echo` them back to `stdout`, printing the commands it is executing
(`-t`):

    $ echo 1 2 3 4 5 6
    1 2 3 4 5 6
    $ echo 1 2 3 4 5 6 | xargs -t -n 2 echo
    echo 1 2
    1 2
    echo 3 4
    3 4
    echo 5 6
    5 6


