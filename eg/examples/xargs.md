# xargs

do not split arguments on whitespace

    xargs -0

parallelize ls with at most 5 processes

    xargs -P 5 ls


# Basic Usage

`xargs` is used to pass arguments to commands:

    <command> | xargs <command>


# Explanation

`xargs` can be confusing.
