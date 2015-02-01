import sys
import os

# Name of the environment variable where we look for the default pager
PAGER_ENV = 'PAGER'

FLAG_NO_EXAMPLES = -1
FLAG_NO_SUBSECTION = -2


def show_usage():
    print 'usage: eg <program> <subsection>'


def pager_env_is_set():
    """Return True if a pager is specified by the environment variable."""
    pager = os.getenv(PAGER_ENV)
    if pager is None:
        return False
    else:
        return True


def has_entry_for_program(program):
    """Return True if has examples for program, else False."""
    pass


def get_line_number_of_subsection(program, subsection):
    """
    Return the line number of the given subsection in program.

    Returns FLAG_NO_EXAMPLES if program does not point to a program that
    contains examples. I.e. returns FLAG_NO_EXAMPLES if
    has_entry_for_program(program) returns false.

    If a subsection or an alias for a subsection exists, returns the line
    number for the start of the subsection. If a subsection or alias for the
    subsection is not found, returns FLAG_NO_SUBSECTION.

    This returns flags to try and be more efficient than having to read the
    file multiple times.
    """
    pass
