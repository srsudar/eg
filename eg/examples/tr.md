# tr

replace g with y and p with o

    $ echo "tgripn" | tr gp yo
    tyrion

remove consecutive target duplicates

    $ echo "abcdeeefffggghhh" | tr -s efg
    abcdefghhh

delete target characters

    $ echo "teyfrigon" | tr -d efg
    tyrion

delete numeric digits

    $ echo "111alpha222" | tr -d "[:digit:]"
    alpha

delete letters

    $ echo "111alpha222" | tr -d "[:alpha:]"
    111222

delete whitespace

    $ echo "t y    r i o n" | tr -d "[:blank:"]
    tyrion

delete everything except given characters

    $ echo "t y   rxxigggo  n" | tr -Cd nioryt
    tyrion

shortcut to replace multiple characters with a single character

    $ echo "abcdef" | tr abc "[x*2]y"
    xxydef

# Basic Usage

Transform all `a`s to `b`s:

    tr a b


