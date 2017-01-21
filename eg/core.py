import argparse
import pydoc
import sys

from eg import config
from eg import util


_MSG_BAD_ARGS = 'specify a program or pass the --list or --version flags'


def _show_version():
    """Show the version string."""
    print(util.VERSION)


def _show_list_message(resolved_config):
    """
    Show the message for when a user has passed in --list.
    """
    # Show what's available.
    supported_programs = util.get_list_of_all_supported_commands(
        resolved_config
    )
    msg_line_1 = 'Legend: '
    msg_line_2 = (
        '    ' +
        util.FLAG_ONLY_CUSTOM +
        ' only custom files'
    )
    msg_line_3 = (
        '    ' +
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


def _handle_no_editor():
    """
    Handles the case where a user has requested to edit a file the custom
    examples for a command but we haven't been able to resolve a command to
    open an editor.
    """
    print(
        'could not find editor: set $VISUAL, $EDITOR, or specify in .egrc'
    )


def _parse_arguments():
    """
    Constructs and parses the command line arguments for eg. Returns an args
    object as returned by parser.parse_args().
    """
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
        '-f',
        '--config-file',
        help='Path to the .egrc file, if it is not in the default location.'
    )

    parser.add_argument(
        '-e',
        '--edit',
        action='store_true',
        help="""Edit the custom examples for the given command. If editor-cmd
        is not set in your .egrc and $VISUAL and $EDITOR are not set, prints a
        message and does nothing."""
    )

    parser.add_argument(
        '--examples-dir',
        help='The location to the examples/ dir that ships with eg'
    )

    parser.add_argument(
        '-c',
        '--custom-dir',
        help='Path to a directory containing user-defined examples.'
    )

    parser.add_argument(
        '-p',
        '--pager-cmd',
        help='String literal that will be invoked to page output.'
    )

    parser.add_argument(
        '-l',
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
        '-s',
        '--squeeze',
        action='store_true',
        default=None,
        help='Show fewer blank lines in output.'
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
        # Too few arguments. We can't specify this using argparse alone, so we
        # have to manually check.
        parser.print_help()
        parser.exit()
    elif not args.version and not args.list and not args.program:
        parser.error(_MSG_BAD_ARGS)
    else:
        return args


def run_eg():
    args = _parse_arguments()

    resolved_config = config.get_resolved_config(
        egrc_path=args.config_file,
        examples_dir=args.examples_dir,
        custom_dir=args.custom_dir,
        use_color=args.use_color,
        pager_cmd=args.pager_cmd,
        squeeze=args.squeeze
    )

    if args.list:
        _show_list_message(resolved_config)
    elif args.version:
        _show_version()
    elif args.edit:
        if not resolved_config.editor_cmd:
            _handle_no_editor()
        else:
            util.edit_custom_examples(args.program, resolved_config)
    else:
        util.handle_program(args.program, resolved_config)


# We want people to be able to use eg without pip, by so we'll allow this to be
# invoked directly.
if __name__ == '__main__':
    run_eg()
