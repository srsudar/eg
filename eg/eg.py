#!/usr/bin/python
import argparse
import eg_util


if __name__ == '__main__':

    print __file__

    parser = argparse.ArgumentParser(description='Provide examples of command usage')

    parser.add_argument(
        '--list',
        action='store_true',
        help='show all the programs with eg entries'
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
    print args
    print args.custom_dir

    config = eg_util.get_resolved_config_items(
        egrc_path=args.config_file,
        examples_dir=args.examples_dir,
        custom_dir=args.custom_dir
    )

    eg_util.handle_program(args.program, config)
