# tr

translate g -> y and p -> o

    tr gp yo


remove duplicate (squeeze) e and f characters

    tr -s ef


delete e, f, and g characters

    tr -d efg


replace lower case letters with upper case

    tr '[a-z]' '[A-Z']



# Basic Usage

Transform characters in `<1st>` to the characters in `<2nd>`:

    tr <1st> <2nd>



# Translating or Replacing Characters

Replace g with y and p with o:

    $ echo "tgripn" | tr gp yo
    tyrion


Shortcut (`[x*2]`) to replace multiple characters with a single character:

    $ echo "abcdef" | tr abc "[x*2]y"
    xxydef



# Removing Characters

Delete (`-d`) target characters (`efg`):

    $ echo "teyfrigon" | tr -d efg
    tyrion


Delete (`-d`) numeric digits (`[:digit:]`):

    $ echo "111alpha222" | tr -d "[:digit:]"
    alpha


Delete (`-d`) letters (`[:alpha:]`):

    $ echo "111alpha222" | tr -d "[:alpha:]"
    111222


Delete (`-d`) whitespace (`[:blank:]`):

    $ echo "t y    r i o n" | tr -d "[:blank:]"
    tyrion


Delete (`-d`) everything except (`-C`) the given characters (`nioryt`):

    $ echo "t y   rxxigggo  n" | tr -Cd nioryt
    tyrion


## Duplicates

Remove (`-s` for "squeeze") consecutive target duplicates (`efg`):

    $ echo "abcdeeefffggghhh" | tr -s efg
    abcdefghhh


