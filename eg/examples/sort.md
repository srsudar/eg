# sort

sort the lines of unsorted.txt

    sort unsorted.txt


sort the lines ignoring leading whitespace

    sort -b ignore_whitespace.txt


reverse the sort order

    sort -r reverse.txt


check if file is sorted

    sort -c check_me.txt

Use sort in the pipeline
    
    cat /etc/passwd | sort -t ':' -k 3 -n 

Use the space to separate

    sort -t ' ' -k 1

Use the sort command to sort the English file

    sort -f (which ignore the case)


# Basic Usage

Sort the lines of a file:

    sort <file>


