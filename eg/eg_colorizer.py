import re

from colorama import Fore
from colorama import Style
from colorama import init

import pydoc


init()

COLOR_HASH = Fore.GREEN
COLOR_HEADING = Fore.RED + Style.BRIGHT
COLOR_CODE = Fore.RED
COLOR_BACKTICK = Fore.RED


def color_heading(text):
    return color_helper(
        text,
        '(^#)(.*)$',
        COLOR_HASH + r'\1' + COLOR_HEADING + r'\2'
    )


def color_block_indent(text):
    return color_helper(
        text,
        '^    (.*)$',
        COLOR_CODE + r'\1'
    )


def color_backticks(text):
    """untested"""
    return color_helper(
        text,
        '[^`]+',
        COLOR_BACKTICK + r'\1'
    )


def color_helper(text, pattern, repl):
    return re.sub(
        pattern,
        repl + Style.RESET_ALL,
        text,
        flags=re.MULTILINE
    )


test = Fore.RED + 'this is a test' + Style.RESET_ALL

title = """this is nothing
# find

next level"""

title = color_heading(title)

pydoc.pager(title)
