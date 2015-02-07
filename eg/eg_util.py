import os
import subprocess

# Name of the environment variable where we look for the default pager
PAGER_ENV = 'PAGER'

# The directory containing example files.
EXAMPLES_DIR = 'examples'

# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'


def show_usage():
    print 'usage: eg <program>'


def pager_env_is_set():
    """Return True if a pager is specified by the environment variable."""
    pager = os.getenv(PAGER_ENV)
    if pager is None:
        return False
    else:
        return True


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
