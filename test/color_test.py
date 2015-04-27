import os

from collections import namedtuple
from eg import color
from eg import config
from mock import patch
from nose.tools import assert_equal

# Some hardcoded real colors.
_YELLOW = '\x1b[33m'
_MAGENTA = '\x1b[35m'
_BLACK = '\x1b[30m'
_GREEN = '\x1b[32m'


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
    color_config = config.ColorConfig(
        'P',
        'H',
        _YELLOW,
        _MAGENTA,
        _BLACK,
        'RES',
        'RES',
        '',
        '',
        ''
    )

    clean = get_clean_find_file()

    raw_file = get_raw_find_test_file()
    target = get_data_with_subs(
        raw_file,
        pound=color_config.pound,
        pound_reset=color_config.pound_reset,
        heading=color_config.heading,
        heading_reset=color_config.heading_reset
    )

    colorizer = color.EgColorizer(color_config)

    actual = colorizer.colorize_heading(clean)

    assert_equal(actual, target)


def test_colorize_block_indents():
    """Makes sure we colorize block indents correctly."""
    color_config = config.ColorConfig(
        _BLACK,
        _MAGENTA,
        'C',
        _YELLOW,
        'P',
        '',
        '',
        'res',
        '',
        'res'
    )

    clean = get_clean_find_file()

    raw_file = get_raw_find_test_file()
    target = get_data_with_subs(
        raw_file,
        code=color_config.code,
        code_reset=color_config.code_reset,
        prompt=color_config.prompt,
        prompt_reset=color_config.prompt_reset
    )

    colorizer = color.EgColorizer(color_config)

    actual = colorizer.colorize_block_indent(clean)

    assert_equal(actual, target)


def test_colorize_backticks():
    """Makes sure we colorize backticks correctly."""
    color_config = config.ColorConfig(
        _BLACK,
        _MAGENTA,
        _YELLOW,
        'B',
        _GREEN,
        '',
        '',
        '',
        'res',
        ''
    )

    clean = get_clean_find_file()

    raw_file = get_raw_find_test_file()
    target = get_data_with_subs(
        raw_file,
        backticks=color_config.backticks,
        backticks_reset=color_config.backticks_reset,
    )

    colorizer = color.EgColorizer(color_config)

    actual = colorizer.colorize_backticks(clean)

    assert_equal(actual, target)


def test_colorize_text_calls_all_sub_methods():
    """colorize_text should call all of the helper colorize methods."""
    with patch(
        'eg.color.EgColorizer.colorize_heading',
        return_value='text-heading'
    ) as heading:
        with patch(
            'eg.color.EgColorizer.colorize_block_indent',
            return_value='text-heading-indent'
        ) as indent:
            with patch(
                'eg.color.EgColorizer.colorize_backticks',
                return_value='text-heading-indent-backticks'
            ) as backticks:
                colorizer = color.EgColorizer(None)
                text = 'text'
                actual = colorizer.colorize_text(text)
                heading.assert_called_once_with(text)
                indent.assert_called_once_with('text-heading')
                backticks.assert_called_once_with('text-heading-indent')
                assert_equal('text-heading-indent-backticks', actual)
