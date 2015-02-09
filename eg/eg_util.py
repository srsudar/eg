import os
import subprocess

# Name of the environment variable where we look for the default pager
PAGER_ENV = 'PAGER'
DEFAULT_PAGER = 'less'

# The directory containing example files.
EXAMPLES_DIR = './examples'

# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'

# Version of eg, revved with each update.
VERSION = '0.0.0'

EGRC_FILE_NAME = '.egrc'


def show_usage():
    print 'usage: eg <program>'


def pager_env_is_set():
    """Return True if a pager is specified by the environment variable."""
    pager = os.getenv(PAGER_ENV)
    if pager is None:
        return False
    else:
        return True


def get_pager():
    """Return the pager to be used with examples."""
    pager = DEFAULT_PAGER
    if pager_env_is_set():
        pager = os.getenv(PAGER_ENV)
    return pager


def handle_program(program):
    if not has_entry_for_program(program):
        print 'No entry found for ' + program + '. Rerun with --list to see all available entries.'
        return
    file_path = get_file_path_for_program(program)
    pager = get_pager()
    open_pager_for_file(pager, file_path)


def get_file_path_for_program(program):
    """
    Return the file name and path for the program. It returns the file relative
    to the eg/ directory.

    For example, passing find would return "examples/find.txt". This does not
    ensure that the file exists, merely that if it does exist, this is where it
    should be.
    """
    return EXAMPLES_DIR + '/' + program + EXAMPLE_FILE_SUFFIX


def has_entry_for_program(program):
    """Return True if has examples for program, else False."""
    file_path = get_file_path_for_program(program)
    print file_path
    return os.path.isfile(file_path)


def open_pager_for_file(pager, file_path):
    """
    Open pager scrolled to line_number.

    pager should be the user's preferred executable pager.
    line_number should be a valid line number >0.

    If pager does not support opening to an offset, it will just open the
    pager.
    """
    subprocess.call([pager, file_path])


def get_path_to_rc_file():
    result = os.path.expanduser('~/' + EGRC_FILE_NAME)
    return result
