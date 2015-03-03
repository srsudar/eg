# wc

count the lines, words, and bytes in a file

    wc lines_words_bytes.txt


count the lines in a file

    wc -l lines.txt


count the words in a file

    wc -w words.txt


count the bytes in a file

    wc -c bytes.txt


count the characters in a file, supporting unicode etc

    wc -m multi_byte_characters.txt



# Basic Usage

Show the lines and words in a file:

    wc <file>



# Counting Lines and Words

The following file is used in this example:

    $ cat 3words_2lines.txt
    123 567
    89


By default `wc` counts lines, words, and bytes:

    $ wc 3words_2lines.txt
    2       3      11 3words_2lines.txt


This file has 2 lines, 3 words (separated by whitespace), and 11 bytes (the
characters, whitespace, and line endings).


