## Important hint
`getopts` stops on the first non-option argument, so you need to shift-out those non-option arguments before using them in `getopts`.
Say you call to a function like `myfunc scan -a -q`, just invoking `while getopts "aq" arg; do` would not process a single option
as it would stop at `scan`. So it should be done like this:

    local arg OPTIND    # make sure especially OPTIND does not collide with a global getopts
    OPTIND=1            # optionally reset it to its default (not needed if local)
    shift               # shift beyond the "scan"
    while getopts "aq" arg; do  # now we can call to getopt
      ..
    done

## Parse command line options

    while getopts "f:bn:d:" OPT; do # the colon indicates: f,n and d require an argument
     case $OPT in
       f) DIRS=$OPTARG ;;           # -f <filename_with_dirs>
       b) ZIP="j"; EXT="tbz" ;;     # -b use bzip (no arguments)
       n) PREFIX=$OPTARG ;;         # -n <Prefix>
       d) DIR=$OPTARG ;;            # -d <directory>
       :) echo "Die Option -$OPTARG benoetigt ein Argument" ; exit 1 ;;
       *) echo "Ungueltiger Parameter: -$OPTARG" ; exit 1 ;;
     esac
    done

## Using long options
What is described in [this man page](https://linux.die.net/man/1/getopt) does not apply to the built-in `getopts`. The bash built-in does not support longopts.
A workaround is [described here](https://stackoverflow.com/a/30026641/2533433) (and more in the other answers to that SO question):

    # Transform long options to short ones
    for arg in "$@"; do
      shift
      case "$arg" in
        '--help')   set -- "$@" '-h'   ;;
        '--number') set -- "$@" '-n'   ;;
        '--rest')   set -- "$@" '-r'   ;;
        '--ws')     set -- "$@" '-w'   ;;
        *)          set -- "$@" "$arg" ;;
      esac
    done

    # Default behavior
    number=0; rest=false; ws=false

    # Parse short options
    OPTIND=1
    while getopts "hn:rw" opt
    do
      case "$opt" in
        'h') print_usage; exit 0 ;;
        'n') number=$OPTARG ;;
        'r') rest=true ;;
        'w') ws=true ;;
        '?') print_usage >&2; exit 1 ;;
      esac
    done
    shift $(expr $OPTIND - 1) # remove options from positional parameters

Another variant is [described here](https://stackoverflow.com/a/7680682/2533433), using the trick of adding `-:` to `$OPTSPEC`:

    optspec=":hv-:"
    while getopts "$optspec" optchar; do
        case "${optchar}" in
            -)
                case "${OPTARG}" in
                    loglevel)
                        val="${!OPTIND}"; OPTIND=$(( $OPTIND + 1 ))
                        echo "Parsing option: '--${OPTARG}', value: '${val}'" >&2;
                        ;;
                    loglevel=*)
                        val=${OPTARG#*=}
                        opt=${OPTARG%=$val}
                        echo "Parsing option: '--${opt}', value: '${val}'" >&2
                        ;;
                    *)
                        if [ "$OPTERR" = 1 ] && [ "${optspec:0:1}" != ":" ]; then
                            echo "Unknown option --${OPTARG}" >&2
                        fi
                        ;;
                esac;;
            h)
                echo "usage: $0 [-v] [--loglevel[=]<value>]" >&2
                exit 2
                ;;
            v)
                echo "Parsing option: '-${optchar}'" >&2
                ;;
            *)
                if [ "$OPTERR" != 1 ] || [ "${optspec:0:1}" = ":" ]; then
                    echo "Non-option argument: '-${OPTARG}'" >&2
                fi
                ;;
        esac
    done

Or, [a bit shorter](https://stackoverflow.com/a/28466267/2533433):

    die() { echo "$*" >&2; exit 2; }  # complain to STDERR and exit with error
    needs_arg() { if [ -z "$OPTARG" ]; then die "No arg for --$OPT option"; fi; }

    while getopts ab:c:-: OPT; do
      # support long options: https://stackoverflow.com/a/28466267/519360
      if [ "$OPT" = "-" ]; then   # long option: reformulate OPT and OPTARG
        OPT="${OPTARG%%=*}"       # extract long option name
        OPTARG="${OPTARG#$OPT}"   # extract long option argument (may be empty)
        OPTARG="${OPTARG#=}"      # if long option argument, remove assigning `=`
      fi
      case "$OPT" in
        a | alpha )    alpha=true ;;
        b | bravo )    needs_arg; bravo="$OPTARG" ;;
        c | charlie )  needs_arg; charlie="$OPTARG" ;;
        ??* )          die "Illegal option --$OPT" ;;  # bad long option
        ? )            exit 2 ;;  # bad short option (error reported via getopts)
      esac
    done
    shift $((OPTIND-1)) # remove parsed options and args from $@ list

