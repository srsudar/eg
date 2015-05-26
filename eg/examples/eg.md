# eg

see example usage for the find command

    eg find


turn off colorized output

    eg --no-color find


list all available commands

    eg --list


specify and egrc file to use when showing examples

    eg -f=/path/to/egrc find


specify alternate directory for custom examples

    eg -c=/path/to/custom/examples_dir find


use less with the -R flag to page output

    eg --pager-cmd='less -R' find


# Basic Usage

Show examples for a command:

    eg <command>



# Configuration File

`eg` can be configured using an rc file. By convention, this is expected to be
found at `~/.egrc`. The supported sections are `eg-config`, `color`, and
`substitutions`.

`examples-dir` is the directory where `eg` looks for default examples. Under
normal circumstances this is provided by the installation and does not require
configuration. `custom-dir` is where use-specified examples be be found. A file
named `awk.md` and located in the directory specified by `custom-dir` will be
paged before the default examples when `eg awk` is invoked.

Custom colors can be specified in the `color` section. The reset family of
options are used to terminate a region of colorized output. Normal users will
have no reason to change them from their default values of `\x1b[0m`, which
removes all formatting.

Regex-based substitutions can be specified in the `[substitutions]` section.
They must be named and follow the a list-based syntax that will be applied
using Python's `re` module: `[pattern, replacement, is_multiline]`.

The three types of formatting are applied in the order: color, squeeze,
substitutions.

Below is a valid egrc with every option specified:

    [eg-config]
    # Lines starting with # are treated as comments
    examples-dir = /path/to/examples/dir
    custom-dir = /path/to/custom/dir
    color = true
    squeeze = true
    pager-cmd = 'less -R'

    [color]
    pound = '\x1b[30m\x1b[1m'
    heading = '\x1b[38;5;172m'
    code = '\x1b[32m\x1b[1m'
    prompt = '\x1b[36m\x1b[1m'
    backticks = '\x1b[34m\x1b[1m'
    pound_reset = '\x1b[0m'
    heading_reset = '\x1b[0m'
    code_reset = '\x1b[0m'
    prompt_reset = '\x1b[0m'
    backticks_reset = '\x1b[0m'

    [substitutions]
    # This will remove all four-space indents.
    remove-indents = ['^    ', '', True]


