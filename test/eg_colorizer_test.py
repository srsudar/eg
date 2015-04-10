import os

from collections import namedtuple
from colorama import Fore
from colorama import Style
from eg import eg_colorizer
from mock import Mock
from mock import patch
from nose.tools import assert_equal


# The flags in the test file marking where substitutions should/can occur.
SubFlags = namedtuple(
    'SubFlags',
    [
        'pound',
        'pound_reset',
        'heading',
        'heading_reset',
        'code',
        'code_reset',
        'backticks',
        'backticks_reset',
        'prompt',
        'prompt_reset'
    ]
)

SUB_FLAGS = SubFlags(
    pound='{POUND}',
    pound_reset='{POUND_RESET}',
    heading='{HEADING}',
    heading_reset='{HEADING_RESET}',
    code='{CODE}',
    code_reset='{CODE_RESET}',
    backticks='{BACKTICKS}',
    backticks_reset='{BACKTICKS_RESET}',
    prompt='{PROMPT}',
    prompt_reset='{PROMPT_RESET}'
)


FIND_FILE_WITH_SUBS = os.path.join(
    os.path.dirname(__file__),
    'assets',
    'find_example_substitute.md'
)


def get_clean_find_file():
    """Get the test file for find as pure markdown."""
    # Defaults are empty strings, so this works.
    raw_file = get_raw_find_test_file()
    cleaned_file = get_data_with_subs(raw_file)
    return cleaned_file


def get_raw_find_test_file():
    """Read the test file in and return it as a string."""
    with open(FIND_FILE_WITH_SUBS, 'r') as f:
        data = f.read()
    return data


def get_data_with_subs(
        string,
        pound='',
        heading='',
        code='',
        backticks='',
        pound_reset='',
        heading_reset='',
        code_reset='',
        backticks_reset='',
        prompt='',
        prompt_reset=''
):
    """
    Return string with substitutions made. By default, with no parameters, will
    simply remove all substitution flags, replacing them all with the empty
    string.

    This substitutes things manually, without using regular expressions. The
    reset_strings are provided to try and allow testing only some of the
    colorizations at a time. For example, if you are just colorizing the
    headings, you'll want the reset escape sequence there. You won't want them
    for the block indents, however, or else you'd end up with things like:

        code code RESET
        code line two RESET

    which obviously wouldn't make sense.
    """
    data = string
    data = data.replace(SUB_FLAGS.pound, pound)
    data = data.replace(SUB_FLAGS.pound_reset, pound_reset)
    data = data.replace(SUB_FLAGS.heading, heading)
    data = data.replace(SUB_FLAGS.heading_reset, heading_reset)
    data = data.replace(SUB_FLAGS.code, code)
    data = data.replace(SUB_FLAGS.code_reset, code_reset)
    data = data.replace(SUB_FLAGS.backticks, backticks)
    data = data.replace(SUB_FLAGS.backticks_reset, backticks_reset)
    data = data.replace(SUB_FLAGS.prompt, prompt)
    data = data.replace(SUB_FLAGS.prompt_reset, prompt_reset)
    return data


def test_colorize_heading():
    """Makes sure we colorize things like '# find' correctly"""
    color_config = eg_colorizer.ColorConfig(
        Fore.CYAN,
        Fore.WHITE,
        Fore.YELLOW,
        Fore.MAGENTA,
        Fore.BLACK
    )

    clean = get_clean_find_file()

    raw_file = get_raw_find_test_file()
    target = get_data_with_subs(
        raw_file,
        pound=color_config.pound,
        pound_reset=Style.RESET_ALL,
        heading=color_config.heading,
        heading_reset=Style.RESET_ALL
    )

    colorizer = eg_colorizer.EgColorizer(color_config)

    actual = colorizer.colorize_heading(clean)

    assert_equal(actual, target)
