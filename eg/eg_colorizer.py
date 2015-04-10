import re

from colorama import Fore
from colorama import Back
from colorama import Style
from colorama import init

import pydoc


init()


def handleTitle(text):
    return re.sub(
        '^#',
        Fore.RED + '#' + Style.RESET_ALL,
        text,
        flags=re.MULTILINE
    )


def handleTitle2(text):
    return re.sub(
        '(^#)',
        Fore.RED + r'\1' + Style.RESET_ALL,
        text,
        flags=re.MULTILINE
    )



test = Fore.RED + 'this is a test' + Style.RESET_ALL

title = """this is nothing
# find

next level"""

title = handleTitle2(title)

pydoc.pager(title)
