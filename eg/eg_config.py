import ast
import os

from collections import namedtuple

# Support Python 2 and 3.
try:
    import ConfigParser
except:
    from configparser import ConfigParser


# The directory containing example files, relative to the eg executable. The
# directory structure is assumed to be:
# eg.py*
# eg_util.py
# examples/
#    |- cp.md, etc
DEFAULT_EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'examples')
DEFAULT_EGRC_PATH = os.path.join('~', '.egrc')
DEFAULT_USE_COLOR = True

# We're using less -R to support color on Unix machines, which by default don't
# let their output from less be colorized.
DEFAULT_PAGER_CMD = 'less -R'

# We need this just because the ConfigParser library requires it.
DEFAULT_SECTION = 'eg-config'

# Properties in the rc file.
EG_EXAMPLES_DIR = 'examples-dir'
CUSTOM_EXAMPLES_DIR = 'custom-dir'
USE_COLOR = 'color'
PAGER_CMD = 'pager-cmd'

# A basic struct containing configuration values.
#    examples_dir: path to the directory of examples that ship with eg
#    custom_dir: path to the directory where custom examples are found
Config = namedtuple(
    'Config',
    [
        'examples_dir',
        'custom_dir',
        'use_color',
        'color_config',
        'pager_cmd'
    ]
)

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

# Default colors. These are intentionally simple to try and accomodate more
# terminals. This is mostly envisioned as a unix tool, so we're not going to
# worry about windows output.
_BRIGHT = '\x1b[1m'
_BLACK = '\x1b[30m'
_RED = '\x1b[31m'
_CYAN = '\x1b[36m'
_GREEN = '\x1b[32m'
_BLUE = '\x1b[34m'
_RESET_ALL = '\x1b[0m'
DEFAULT_COLOR_POUND = _BLACK + _BRIGHT
DEFAULT_COLOR_HEADING = _RED + _BRIGHT
DEFAULT_COLOR_PROMPT = _CYAN + _BRIGHT
DEFAULT_COLOR_CODE = _GREEN + _BRIGHT
DEFAULT_COLOR_BACKTICKS = _BLUE + _BRIGHT
DEFAULT_COLOR_POUND_RESET = _RESET_ALL
DEFAULT_COLOR_HEADING_RESET = _RESET_ALL
DEFAULT_COLOR_PROMPT_RESET = _RESET_ALL
DEFAULT_COLOR_CODE_RESET = _RESET_ALL
DEFAULT_COLOR_BACKTICKS_RESET = _RESET_ALL

CONFIG_NAMES = ColorConfig(
    pound='pound',
    heading='heading',
    code='code',
    backticks='backticks',
    prompt='prompt',
    pound_reset='pound_reset',
    heading_reset='heading_reset',
    code_reset='code_reset',
    backticks_reset='backticks_reset',
    prompt_reset='prompt_reset'
)

# The name of the section in the config file containing colors.
COLOR_SECTION = 'color'


def get_resolved_config_items(
    egrc_path,
    examples_dir,
    custom_dir,
    use_color,
    pager_cmd,
    debug=True
):
    """
    Create a Config namedtuple. Passed in values will override defaults.

    use_color: false if should not colorize output. true by default
    """
    # Expand the paths so we can use them with impunity later.
    egrc_path = get_expanded_path(egrc_path)
    examples_dir = get_expanded_path(examples_dir)
    custom_dir = get_expanded_path(custom_dir)

    # Print helpful failures.
    if egrc_path and debug:
        _inform_if_path_does_not_exist(egrc_path)
    if examples_dir and debug:
        _inform_if_path_does_not_exist(examples_dir)
    if custom_dir and debug:
        _inform_if_path_does_not_exist(custom_dir)

    # The general rule is: caller-defined, egrc-defined, defaults. We'll try and
    # get all three then use get_priority to choose the right one.

    resolved_egrc_path = get_priority(egrc_path, DEFAULT_EGRC_PATH, None)
    resolved_egrc_path = get_expanded_path(resolved_egrc_path)

    # Start as if nothing was defined in th egrc.
    empty_color_config = get_empty_color_config()
    egrc_config = Config(
        examples_dir=None,
        custom_dir=None,
        color_config=empty_color_config,
        use_color=None,
        pager_cmd=None
    )

    if os.path.isfile(resolved_egrc_path):
        egrc_config = get_config_tuple_from_egrc(resolved_egrc_path)

    resolved_examples_dir = get_priority(
        examples_dir,
        egrc_config.examples_dir,
        DEFAULT_EXAMPLES_DIR
    )
    resolved_custom_dir = get_priority(
        custom_dir,
        egrc_config.custom_dir,
        None
    )

    resolved_use_color = get_priority(
        use_color,
        egrc_config.use_color,
        DEFAULT_USE_COLOR
    )

    resolved_pager_cmd = get_priority(
        pager_cmd,
        egrc_config.pager_cmd,
        DEFAULT_PAGER_CMD
    )

    color_config = None
    if resolved_use_color:
        default_color_config = get_default_color_config()
        color_config = merge_color_configs(
            egrc_config.color_config,
            default_color_config
        )

    result = Config(
        examples_dir=resolved_examples_dir,
        custom_dir=resolved_custom_dir,
        color_config=color_config,
        use_color=resolved_use_color,
        pager_cmd=resolved_pager_cmd
    )

    return result


def get_config_tuple_from_egrc(egrc_path):
    """
    Create a Config named tuple from the values specified in the .egrc. Expands
    any paths as necessary.

    egrc_path must exist and point a file.

    If not present in the .egrc, properties of the Config are returned as None.
    """
    with open(egrc_path, 'r') as egrc:
        try:
            config = ConfigParser.RawConfigParser()
        except AttributeError:
            config = ConfigParser()
        config.readfp(egrc)

        # default to None
        examples_dir = None
        custom_dir = None
        use_color = None
        pager_cmd = None

        if config.has_option(DEFAULT_SECTION, EG_EXAMPLES_DIR):
            examples_dir = config.get(DEFAULT_SECTION, EG_EXAMPLES_DIR)
            examples_dir = get_expanded_path(examples_dir)

        if config.has_option(DEFAULT_SECTION, CUSTOM_EXAMPLES_DIR):
            custom_dir = config.get(DEFAULT_SECTION, CUSTOM_EXAMPLES_DIR)
            custom_dir = get_expanded_path(custom_dir)

        if config.has_option(DEFAULT_SECTION, USE_COLOR):
            use_color_raw = config.get(DEFAULT_SECTION, USE_COLOR)
            use_color = _parse_bool_from_raw_egrc_value(use_color_raw)

        if config.has_option(DEFAULT_SECTION, PAGER_CMD):
            pager_cmd_raw = config.get(DEFAULT_SECTION, PAGER_CMD)
            pager_cmd = ast.literal_eval(pager_cmd_raw)

        color_config = get_custom_color_config_from_egrc(config)

        return Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir,
            color_config=color_config,
            use_color=use_color,
            pager_cmd=pager_cmd
        )


def get_expanded_path(path):
    """Expand ~ and variables in a path. If path is not truthy, return None."""
    if path:
        result = path
        result = os.path.expanduser(result)
        result = os.path.expandvars(result)
        return result
    else:
        return None


def get_priority(first, second, third):
    """
    Return the items based on priority and their truthiness. If first is
    present, it will be returned. If only second and third, second will be
    returned. If all three are absent, will return None.
    """
    if first is not None:
        return first
    elif second is not None:
        return second
    else:
        return third


def _inform_if_path_does_not_exist(path):
    """
    If the path does not exist, print a message saying so. This is intended to
    be helpful to users if they specify a custom path that eg cannot find.
    """
    expanded_path = get_expanded_path(path)
    if not os.path.exists(expanded_path):
        print('Could not find custom path at: {}'.format(expanded_path))


def get_custom_color_config_from_egrc(config):
    """
    Get the ColorConfig from the egrc config object. Any colors not defined
    will be None.
    """
    pound = _get_color_from_config(config, CONFIG_NAMES.pound)
    heading = _get_color_from_config(config, CONFIG_NAMES.heading)
    code = _get_color_from_config(config, CONFIG_NAMES.code)
    backticks = _get_color_from_config(config, CONFIG_NAMES.backticks)
    prompt = _get_color_from_config(config, CONFIG_NAMES.prompt)
    pound_reset = _get_color_from_config(config, CONFIG_NAMES.pound_reset)
    heading_reset = _get_color_from_config(
        config,
        CONFIG_NAMES.heading_reset
    )
    code_reset = _get_color_from_config(config, CONFIG_NAMES.code_reset)
    backticks_reset = _get_color_from_config(
        config,
        CONFIG_NAMES.backticks_reset
    )
    prompt_reset = _get_color_from_config(config, CONFIG_NAMES.prompt_reset)

    result = ColorConfig(
        pound=pound,
        heading=heading,
        code=code,
        backticks=backticks,
        prompt=prompt,
        pound_reset=pound_reset,
        heading_reset=heading_reset,
        code_reset=code_reset,
        backticks_reset=backticks_reset,
        prompt_reset=prompt_reset
    )

    return result


def _get_color_from_config(config, option):
    """
    Helper method to uet an option from the COLOR_SECTION of the config.

    Returns None if the value is not present. If the value is present, it tries
    to parse the value as a raw string literal, allowing escape sequences in the
    egrc.
    """
    if not config.has_option(COLOR_SECTION, option):
        return None
    else:
        return ast.literal_eval(config.get(COLOR_SECTION, option))


def get_default_color_config():
    """Get a color config object with all the defaults."""
    result = ColorConfig(
        pound=DEFAULT_COLOR_POUND,
        heading=DEFAULT_COLOR_HEADING,
        code=DEFAULT_COLOR_CODE,
        backticks=DEFAULT_COLOR_BACKTICKS,
        prompt=DEFAULT_COLOR_PROMPT,
        pound_reset=DEFAULT_COLOR_POUND_RESET,
        heading_reset=DEFAULT_COLOR_HEADING_RESET,
        code_reset=DEFAULT_COLOR_CODE_RESET,
        backticks_reset=DEFAULT_COLOR_BACKTICKS_RESET,
        prompt_reset=DEFAULT_COLOR_PROMPT_RESET
    )
    return result


def get_empty_color_config():
    """Return a color_config with all values set to None."""
    empty_color_config = ColorConfig(
        pound=None,
        heading=None,
        code=None,
        backticks=None,
        prompt=None,
        pound_reset=None,
        heading_reset=None,
        code_reset=None,
        backticks_reset=None,
        prompt_reset=None
    )
    return empty_color_config


def merge_color_configs(first, second):
    """
    Merge the color configs.

    Values in the first will overwrite non-None values in the second.
    """
    # We have to get the desired values first and simultaneously, as nametuple
    # is immutable.
    pound = get_priority(first.pound, second.pound, None)
    heading = get_priority(first.heading, second.heading, None)
    code = get_priority(first.code, second.code, None)
    backticks = get_priority(first.backticks, second.backticks, None)
    prompt = get_priority(first.prompt, second.prompt, None)
    pound_reset = get_priority(
        first.pound_reset,
        second.pound_reset,
        None
    )
    heading_reset = get_priority(
        first.heading_reset,
        second.heading_reset,
        None
    )
    code_reset = get_priority(
        first.code_reset,
        second.code_reset,
        None
    )
    backticks_reset = get_priority(
        first.backticks_reset,
        second.backticks_reset,
        None
    )
    prompt_reset = get_priority(
        first.prompt_reset,
        second.prompt_reset,
        None
    )

    result = ColorConfig(
        pound=pound,
        heading=heading,
        code=code,
        backticks=backticks,
        prompt=prompt,
        pound_reset=pound_reset,
        heading_reset=heading_reset,
        code_reset=code_reset,
        backticks_reset=backticks_reset,
        prompt_reset=prompt_reset
    )

    return result


def _parse_bool_from_raw_egrc_value(raw_value):
    """
    Parse the value from an egrc into a boolean.
    """
    truthy_values = ['True', 'true']
    return raw_value in truthy_values
