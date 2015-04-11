import re

from collections import namedtuple
from colorama import Fore
from colorama import Style
from colorama import init

import pydoc

# Default colors
DEFAULT_COLOR_HASH = Fore.GREEN
DEFAULT_COLOR_HEADING = Fore.RED + Style.BRIGHT
DEFAULT_COLOR_CODE = Fore.RED
DEFAULT_COLOR_BACKTICK = Fore.RED

# A struct with color values
ColorConfig = namedtuple(
    'ColorConfig',
    [
        'pound',
        'heading',
        'code',
        'backticks',
        'prompt',
        'pound_reset',
        'heading_reset',
        'code_reset',
        'backticks_reset',
        'prompt_reset'
    ]
)


class EgColorizer():

    def __init__(self, color_config):
        init()
        self.color_config = color_config

    def colorize_heading(self, text):
        return self.color_helper(
            text,
            '(^#+)(.*)$',
            (
                self.color_config.pound +
                r'\1' +
                self.color_config.pound_reset +
                self.color_config.heading +
                r'\2' +
                self.color_config.heading_reset
            )
        )

    def colorize_block_indent(self, text):
        return self.color_helper(
            text,
            '^    (\$?)(.*)$',
            (
                '    ' +
                self.color_config.prompt +
                r'\1' +
                self.color_config.prompt_reset +
                self.color_config.code +
                r'\2' +
                self.color_config.code_reset
            )
        )

    def colorize_backticks(self, text):
        """untested"""
        return self.color_helper(
            text,
            '`([^`]+)`',
            (
                '`' +
                self.color_config.backticks +
                r'\1' +
                self.color_config.backticks_reset +
                '`'
            )
        )

    def color_helper(self, text, pattern, repl):
        return re.sub(
            pattern,
            repl,
            text,
            flags=re.MULTILINE
        )


#test = Fore.RED + 'this is a test' + Style.RESET_ALL

#title = """this is nothing
# find

#next level"""

#title = color_heading(title)

#pydoc.pager(title)
