#!/usr/bin/python
import argparse
import eg_util
import sys


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='eg provides examples of common command usage.'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='show all the programs with eg entries.'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Display version information about eg'
    )

    parser.add_argument(
        'program',
        nargs='?',
        help='The program for which to display examples.'
    )

    parser.add_argument(
        '--config-file',
        nargs='?',
        help='Path to the .egrc file, if it is not in the default location.'
    )

    parser.add_argument(
        '--examples-dir',
        nargs='?',
        help='The location to the examples/ dir that ships with eg'
    )

    parser.add_argument(
        '--custom-dir',
        nargs='?',
        help='Path to a directory containing user-defined examples.'
    )

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
    else:
        config = eg_util.get_resolved_config_items(
            egrc_path=args.config_file,
            examples_dir=args.examples_dir,
            custom_dir=args.custom_dir
        )

        if args.list:
            # Show what's available.
            supported_programs = eg_util.get_list_of_all_supported_commands(
                config
            )
            msg_line_1 = 'Legend: '
            msg_line_2 = ('    ' +
                          eg_util.FLAG_ONLY_CUSTOM +
                          ' only custom files'
                          )
            msg_line_3 = ('    ' +
                          eg_util.FLAG_CUSTOM_AND_DEFAULT +
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

            for line in preamble:
                print line

            for program in supported_programs:
                print program
        elif args.version:
            print eg_util.VERSION
        else:

            eg_util.handle_program(args.program, config)
