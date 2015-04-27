import argparse
import pydoc
import sys

from eg import config
from eg import util


def run_eg():

    parser = argparse.ArgumentParser(
        description='eg provides examples of common command usage.'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Display version information about eg'
    )

    parser.add_argument(
        '--config-file',
        help='Path to the .egrc file, if it is not in the default location.'
    )

    parser.add_argument(
        '--examples-dir',
        help='The location to the examples/ dir that ships with eg'
    )

    parser.add_argument(
        '--custom-dir',
        help='Path to a directory containing user-defined examples.'
    )

    parser.add_argument(
        '--pager-cmd',
        help='String literal that will be invoked to page output.'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='Show all the programs with eg entries.'
    )

    parser.add_argument(
        '--color',
        action='store_true',
        dest='use_color',
        default=None,
        help='Colorize output.'
    )

    parser.add_argument(
        '--no-color',
        action='store_false',
        dest='use_color',
        help='Do not colorize output.'
    )

    parser.add_argument(
        'program',
        nargs='?',
        help='The program for which to display examples.'
    )

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
    elif not args.version and not args.list and not args.program:
        print(
            'you must specify a program or pass the --list or --version flags'
        )
    else:
        resolved_config = config.get_resolved_config_items(
            egrc_path=args.config_file,
            examples_dir=args.examples_dir,
            custom_dir=args.custom_dir,
            use_color=args.use_color,
            pager_cmd=args.pager_cmd
        )

        if args.list:
            # Show what's available.
            supported_programs = util.get_list_of_all_supported_commands(
                resolved_config
            )
            msg_line_1 = 'Legend: '
            msg_line_2 = ('    ' +
                          util.FLAG_ONLY_CUSTOM +
                          ' only custom files'
                          )
            msg_line_3 = ('    ' +
                          util.FLAG_CUSTOM_AND_DEFAULT +
                          ' custom and default files'
                          )
            msg_line_4 = '    ' + '  only default files (no symbol)'
            msg_line_5 = ''
            msg_line_6 = 'Programs supported by eg: '

            preamble = [
                msg_line_1,
                msg_line_2,
                msg_line_3,
                msg_line_4,
                msg_line_5,
                msg_line_6
            ]

            complete_message = '\n'.join(preamble)
            complete_message += '\n' + '\n'.join(supported_programs)

            pydoc.pager(complete_message)
        elif args.version:
            print(util.VERSION)
        else:
            util.handle_program(args.program, resolved_config)


# We want people to be able to use eg without pip, by so we'll allow this to be
# invoked directly.
if __name__ == '__main__':
    run_eg()
