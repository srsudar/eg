# cut

split lines on ':' and show second column

    cut -d ':' -f2 input.txt


split on tab and show columns 2-8

    cut -f 2-8 input.txt


show 2nd character of every line

    cut -c 2 characters.txt

show characters 1-10 of every line

    cut -c 1-10 characters.txt



# Basic Usage

Split on a delimiter and print certain fields:

    cut -d '<delimiter>' -f <fields> <file>



# Specifying the Delimiter and Fields

Fields are specified by a number, starting at 1. Fields can be separated by a
`,` and provided a range with (`-`).

The following file is used in these examples:

    $ cat cut.txt
    a b:foo:c d
    bar:baz 2:last


Split on spaces (`-d ' '`) and show every column from 2 onward (`-f 2-`):

    $ cut -d ' ' -f 2- cut.txt
    b:foo:c d
    2:last


Split on colons (`-d ':'`) and show the first and third columns (`-f 1,3`):

    $ cut -d ':' -f 1,3 cut.txt
    a b:c d
    bar:last


Split on `a` (`-d 'a'`) and show the first through third columns (`-f 1-3`):

    $ cut -d 'a' -f 1-3 cut.txt
    a b:foo:c d
    bar:baz 2:l


