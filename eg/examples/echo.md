# echo

print hello to stdout

    echo hello


print hello without a trailing newline

    echo -n hello


print multiple words to stdout

    echo hello world


print the value of the EDITOR environment variable

    echo ${EDITOR}


ignore special characters using single quotes

    echo 'hello \ there?'


print without variable substitution

    echo 'print ${EDITOR} exactly'



# Basic Usage

Print a string to standard out, followed by a new line:

    echo <string>


`echo` obeys shell quoting. Single quotes are strong quotes. They prevent all
characters from being interpreted as control characters and prevent variables
from being substituted. Double quotes allow variable and command substitution
but otherwise ignore control characters:

    $ echo 'What is your ${EDITOR}?'
    What is your ${EDITOR}?
    $ echo "What is your ${EDITOR}?"
    What is your vi -e?
    $ echo 'Your current directory is `pwd`'
    Your current directory is `pwd`
    $ echo "Your current directory is `pwd`"
    Your current directory is /Users/tyrion



# Note on Referencing Variables

In these examples, when the environment variable `EDITOR` is referenced it is
surrounded by curly braces: `${EDITOR}`. In the examples shown above, `$EDITOR`
would accomplish the same thing. Since variable substitution is performed using
a mechanism like string search and replace, not using braces to refer to
variables can be more error prone. Curly braces are shown for robustness as in
general they should be preferred.
