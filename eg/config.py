import ast
import os

from collections import namedtuple
from eg import substitute

# Support Python 2 and 3.
try:
    import ConfigParser
except:
    from configparser import ConfigParser


# Environment variables to try for accessing an editor.
ENV_VISUAL = 'VISUAL'
ENV_EDITOR = 'EDITOR'

# The directory containing example files, relative to the eg executable. The
# directory structure is assumed to be:
# eg.py*
# eg_util.py
# examples/
#    |- cp.md, etc
DEFAULT_EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'examples')
DEFAULT_CUSTOM_DIR = None
DEFAULT_EGRC_PATH = os.path.join('~', '.egrc')
DEFAULT_USE_COLOR = True

# We're using less -R to support color on Unix machines, which by default don't
# let their output from less be colorized. Other options:
# -M: show line number information in the bottom of screen (current/pages X%)
# -F: automatically quit less if the entire example fits on the first screen
# -X: do not use init/deinit strings; in other words: do not clear the screen
# -K: exit less in response to Ctrl-C
DEFAULT_PAGER_CMD = 'less -RMFXK'

DEFAULT_SQUEEZE = False
DEFAULT_EDITOR_CMD = None

# We need this just because the ConfigParser library requires it.
DEFAULT_SECTION = 'eg-config'

# Properties in the rc file.
EG_EXAMPLES_DIR = 'examples-dir'
CUSTOM_EXAMPLES_DIR = 'custom-dir'
USE_COLOR = 'color'
PAGER_CMD = 'pager-cmd'
SQUEEZE = 'squeeze'
EDITOR_CMD = 'editor-cmd'

# A basic struct containing configuration values.
#    examples_dir: path to the directory of examples that ship with eg
#    custom_dir: path to the directory where custom examples are found
#    use_color: True if we should colorize output, else False
#    color_config: the config object specifying which colors to use
#    pager_cmd: the command to use to page output
#    squeeze: True if we should remove blank lines, else false
#    subs: a list of Substitution objects to apply to the output
Config = namedtuple(
    'Config',
    [
        'examples_dir',
        'custom_dir',
        'use_color',
        'color_config',
        'pager_cmd',
        'squeeze',
        'subs',
        'editor_cmd',
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

# The name of the section in the config file containing substitutions.
SUBSTITUTION_SECTION = 'substitutions'


def inform_if_paths_invalid(egrc_path, examples_dir, custom_dir, debug=True):
    """
    If egrc_path, examples_dir, or custom_dir is truthy and debug is True,
    informs the user that a path is not set.

    This should be used to verify input arguments from the command line.
    """
    if (not debug):
        return

    if (egrc_path):
        _inform_if_path_does_not_exist(egrc_path)

    if (examples_dir):
        _inform_if_path_does_not_exist(examples_dir)

    if (custom_dir):
        _inform_if_path_does_not_exist(custom_dir)


def get_egrc_config(cli_egrc_path):
    """
    Return a Config namedtuple based on the contents of the egrc.

    If the egrc is not present, it returns an empty default Config.

    This method tries to use the egrc at cli_egrc_path, then the default path.

    cli_egrc_path: the path to the egrc as given on the command line via
        --config-file
    """
    resolved_path = get_priority(cli_egrc_path, DEFAULT_EGRC_PATH, None)
    expanded_path = get_expanded_path(resolved_path)

    # Start as if nothing was defined in the egrc.
    egrc_config = get_empty_config()

    if os.path.isfile(expanded_path):
        egrc_config = get_config_tuple_from_egrc(expanded_path)

    return egrc_config


def get_resolved_config(
    egrc_path,
    examples_dir,
    custom_dir,
    use_color,
    pager_cmd,
    squeeze,
    debug=True,
):
    """
    Create a Config namedtuple. Passed in values will override defaults.

    This function is responsible for producing a Config that is correct for the
    passed in arguments. In general, it prefers first command line options,
    then values from the egrc, and finally defaults.

    examples_dir and custom_dir when returned from this function are fully
    expanded.
    """
    # Call this with the passed in values, NOT the resolved values. We are
    # informing the caller only if values passed in at the command line are
    # invalid. If you pass a path to a nonexistent egrc, for example, it's
    # helpful to know. If you don't have an egrc, and thus one isn't found
    # later at the default location, we don't want to notify them.
    inform_if_paths_invalid(egrc_path, examples_dir, custom_dir)

    # Expand the paths so we can use them with impunity later.
    examples_dir = get_expanded_path(examples_dir)
    custom_dir = get_expanded_path(custom_dir)

    # The general rule is: caller-defined, egrc-defined, defaults. We'll try
    # and get all three then use get_priority to choose the right one.

    egrc_config = get_egrc_config(egrc_path)

    resolved_examples_dir = get_priority(
        examples_dir,
        egrc_config.examples_dir,
        DEFAULT_EXAMPLES_DIR
    )
    resolved_examples_dir = get_expanded_path(resolved_examples_dir)

    resolved_custom_dir = get_priority(
        custom_dir,
        egrc_config.custom_dir,
        DEFAULT_CUSTOM_DIR
    )
    resolved_custom_dir = get_expanded_path(resolved_custom_dir)

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

    # There is no command line option for this, so in this case we will use the
    # priority: egrc, environment, DEFAULT.
    environment_editor_cmd = get_editor_cmd_from_environment()
    resolved_editor_cmd = get_priority(
        egrc_config.editor_cmd,
        environment_editor_cmd,
        DEFAULT_EDITOR_CMD
    )

    color_config = None
    if resolved_use_color:
        default_color_config = get_default_color_config()
        color_config = merge_color_configs(
            egrc_config.color_config,
            default_color_config
        )

    resolved_squeeze = get_priority(
        squeeze,
        egrc_config.squeeze,
        DEFAULT_SQUEEZE
    )

    # Pass in None, as subs can't be specified at the command line.
    resolved_subs = get_priority(
        None,
        egrc_config.subs,
        get_default_subs()
    )

    result = Config(
        examples_dir=resolved_examples_dir,
        custom_dir=resolved_custom_dir,
        color_config=color_config,
        use_color=resolved_use_color,
        pager_cmd=resolved_pager_cmd,
        editor_cmd=resolved_editor_cmd,
        squeeze=resolved_squeeze,
        subs=resolved_subs,
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
        squeeze = None
        subs = None
        editor_cmd = None

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

        if config.has_option(DEFAULT_SECTION, EDITOR_CMD):
            editor_cmd_raw = config.get(DEFAULT_SECTION, EDITOR_CMD)
            editor_cmd = ast.literal_eval(editor_cmd_raw)

        color_config = get_custom_color_config_from_egrc(config)

        if config.has_option(DEFAULT_SECTION, SQUEEZE):
            squeeze_raw = config.get(DEFAULT_SECTION, SQUEEZE)
            squeeze = _parse_bool_from_raw_egrc_value(squeeze_raw)

        if config.has_section(SUBSTITUTION_SECTION):
            subs = get_substitutions_from_config(config)

        return Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir,
            color_config=color_config,
            use_color=use_color,
            pager_cmd=pager_cmd,
            editor_cmd=editor_cmd,
            squeeze=squeeze,
            subs=subs,
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


def get_editor_cmd_from_environment():
    """
    Gets and editor command from environment variables.

    It first tries $VISUAL, then $EDITOR, following the same order git uses
    when it looks up edits. If neither is available, it returns None.
    """
    result = os.getenv(ENV_VISUAL)
    if (not result):
        result = os.getenv(ENV_EDITOR)
    return result


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
    to parse the value as a raw string literal, allowing escape sequences in
    the egrc.
    """
    if not config.has_option(COLOR_SECTION, option):
        return None
    else:
        return ast.literal_eval(config.get(COLOR_SECTION, option))


def parse_substitution_from_list(list_rep):
    """
    Parse a substitution from the list representation in the config file.
    """
    # We are expecting [pattern, replacement [, is_multiline]]
    if type(list_rep) is not list:
        raise SyntaxError('Substitution must be a list')
    if len(list_rep) < 2:
        raise SyntaxError('Substitution must be a list of size 2')

    pattern = list_rep[0]
    replacement = list_rep[1]

    # By default, substitutions are not multiline.
    is_multiline = False
    if (len(list_rep) > 2):
        is_multiline = list_rep[2]
        if type(is_multiline) is not bool:
            raise SyntaxError('is_multiline must be a boolean')

    result = substitute.Substitution(pattern, replacement, is_multiline)
    return result


def get_substitutions_from_config(config):
    """
    Return a list of Substitution objects from the config, sorted
    alphabetically by pattern name. Returns an empty list if no Substitutions
    are specified. If there are problems parsing the values, a help message
    will be printed and an error will be thrown.
    """
    result = []
    pattern_names = config.options(SUBSTITUTION_SECTION)
    pattern_names.sort()
    for name in pattern_names:
        pattern_val = config.get(SUBSTITUTION_SECTION, name)
        list_rep = ast.literal_eval(pattern_val)
        substitution = parse_substitution_from_list(list_rep)
        result.append(substitution)
    return result


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


def get_empty_config():
    """
    Return an empty Config object with no options set.
    """
    empty_color_config = get_empty_color_config()
    result = Config(
        examples_dir=None,
        custom_dir=None,
        color_config=empty_color_config,
        use_color=None,
        pager_cmd=None,
        editor_cmd=None,
        squeeze=None,
        subs=None
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


def get_default_subs():
    """
    Get the list of default substitutions. We're not storing this as a module
    level object like the other DEFAULT values, as lists are mutable, and we
    could get into trouble by modifying that list and not having it remain
    empty as might be expected.
    """
    return []
