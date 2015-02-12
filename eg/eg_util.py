import ConfigParser
import os
import subprocess

from collections import namedtuple


# Name of the environment variable where we look for the default pager
PAGER_ENV = 'PAGER'
DEFAULT_PAGER = 'less'

# The directory containing example files.
EXAMPLES_DIR = './examples'

# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'

# Version of eg, revved with each update.
VERSION = '0.0.0'

DEFAULT_EGRC_PATH = os.path.join('~', '.egrc')

# The default location of the example files.
DEFAULT_EG_EXAMPLES_IN_HOME = os.path.join('eg', 'examples')

# We need this just because the ConfigParser library requires it.
DEFAULT_SECTION = 'eg-config'

# Properties in the rc file.
EG_EXAMPLES_DIR = 'examples-dir'
CUSTOM_EXAMPLES_DIR = 'custom-dir'

# A basic struct containing configuration values.
#    examples_dir: path to the directory of examples that ship with eg
#    custom_dir: path to the directory where custom examples are found
Config = namedtuple('Config', ['examples_dir', 'custom_dir'])


def get_expanded_path(path):
    """Expand ~ and variables in a path."""
    result = path
    result = os.path.expanduser(result)
    result = os.path.expandvars(result)
    return result


def get_resolved_config_items(
    egrc_path,
    examples_dir,
    custom_dir
):
    """
    Create a Config namedtuple. Passed in values will override defaults.
    """
    # Set our default.
    if egrc_path is None:
        egrc_path = DEFAULT_EGRC_PATH
    # First get try to get any defaults from the .egrc
    egrc_path = get_expanded_path(egrc_path)

    config = Config(examples_dir=None, custom_dir=None)

    if os.path.isfile(egrc_path):
        config = get_config_tuple_from_egrc(egrc_path)

    # Now overwrite them as necessary.
    resolved_examples_dir = config.examples_dir
    resolved_custom_dir = config.custom_dir

    if examples_dir:
        resolved_examples_dir = examples_dir

    if custom_dir:
        resolved_custom_dir = custom_dir

    return Config(
        examples_dir=resolved_examples_dir,
        custom_dir=resolved_custom_dir
    )


def get_config_tuple_from_egrc(egrc_path):
    """
    Create a Config named tuple from the values specified in the .egrc.

    egrc_path must exist and point a file.
    """
    with open(egrc_path, 'r') as egrc:
        config = ConfigParser.RawConfigParser()
        valsread = config.readfp(egrc)

        print 'valsread: ' + str(valsread)

        examples_dir = config.get(DEFAULT_SECTION, EG_EXAMPLES_DIR)
        custom_dir = config.get(DEFAULT_SECTION, CUSTOM_EXAMPLES_DIR)

        return Config(examples_dir=examples_dir, custom_dir=custom_dir)


def pager_env_is_set():
    """Return True if a pager is specified by the environment variable."""
    pager = os.getenv(PAGER_ENV)
    if pager is None:
        return False
    else:
        return True


def get_pager():
    """Return the pager to be used with examples."""
    pager = DEFAULT_PAGER
    if pager_env_is_set():
        pager = os.getenv(PAGER_ENV)
    return pager


def handle_program(program, config):
    default_file_path = None
    custom_file_path = None

    if has_default_entry_for_program(program, config):
        default_file_path = get_default_file_path_for_program(
            program,
            config.examples_dir
        )

    if has_custom_entry_for_program(program, config):
        custom_file_path = get_custom_file_path_for_program(
            program,
            config.custom_dir
        )

    # Handle the case where we have nothing for them.
    if default_file_path is None and custom_file_path is None:
        print ('No entry found for ' +
               program +
               '. Run `eg --list` to see all available entries.')
        return

    pager = get_pager()
    open_pager_for_file(
        pager,
        default_file_path=default_file_path,
        custom_file_path=custom_file_path
    )


def get_default_file_path_for_program(program, examples_dir):
    """
    Return the file name and path for the program.

    examples_dir cannot be None

    Path is not guaranteed to exist. Just says where it should be if it
    existed. Returned paths are absolute.
    """
    if examples_dir is None:
        raise TypeError('examples_dir cannot be None')
    else:
        result = os.path.join(examples_dir, program + EXAMPLE_FILE_SUFFIX)
        result = get_expanded_path(result)
        return result


def get_custom_file_path_for_program(program, custom_dir):
    """
    Return a custom file path for the program. Returns the absolute path.

    custom_dir cannot be None.

    Path is not guaranteed to exist. Just says where it should be if it
    existed. Returned paths are absolute.
    """
    if custom_dir is None:
        raise TypeError('custom_dir cannot be None')
    else:
        result = os.path.join(custom_dir, program + EXAMPLE_FILE_SUFFIX)
        result = get_expanded_path(result)
        return result


def has_default_entry_for_program(program, config):
    """Return True if has standard examples for program, else False."""
    if config.examples_dir:
        file_path = get_default_file_path_for_program(
            program,
            config.examples_dir)
        print file_path
        return os.path.isfile(file_path)
    else:
        return False


def has_custom_entry_for_program(program, config):
    """Return True if has custom examples for a program, else false."""
    custom_path = get_custom_file_path_for_program(program, config.custom_dir)
    print custom_path
    return os.path.isfile(custom_path)


def open_pager_for_file(pager, default_file_path=None, custom_file_path=None):
    """
    Open pager to file_path. If a custom_file_path is also included, it will be
    shown before file_path in the same pager.
    """
    args = None
    if default_file_path and custom_file_path:
        args = ['cat', default_file_path, custom_file_path, '|', pager]
    elif default_file_path:
        args = [pager, default_file_path]
    elif custom_file_path:
        args = [pager, custom_file_path]
    else:
        print 'At least one file must be defined.'
    subprocess.call(args)
