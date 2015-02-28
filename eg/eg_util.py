import ConfigParser
import os
import subprocess

from collections import namedtuple


# Name of the environment variable where we look for the default pager
PAGER_ENV = 'PAGER'
DEFAULT_PAGER = 'less'

# The directory containing example files, relative to the eg executable. The
# directory structure is assumed to be:
# eg.py*
# eg_util.py
# examples/
#    |- cp.md, etc

DEFAULT_EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'examples')
DEFAULT_EGRC_PATH = os.path.join('~', '.egrc')

# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'

# Version of eg, revved with each update.
VERSION = '0.0.0'

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
    # Set our defaults, which we'll overwrite as necessary.
    #import ipdb; ipdb.set_trace()
    if egrc_path is None:
        egrc_path = DEFAULT_EGRC_PATH
    else:
        # they have specified an egrc file. Fail verbosely to try and be
        # helpful.
        expanded_path = get_expanded_path(egrc_path)
        if not os.path.isfile(expanded_path):
            print 'Could not find custom egrc at: ' + expanded_path

    if examples_dir is None:
        examples_dir = DEFAULT_EXAMPLES_DIR

    # First try to get any defaults from the .egrc
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

    If not present in the .egrc, properties of the Config are returned as None.
    """
    with open(egrc_path, 'r') as egrc:
        config = ConfigParser.RawConfigParser()
        config.readfp(egrc)

        # default to None
        examples_dir = None
        custom_dir = None

        if config.has_option(DEFAULT_SECTION, EG_EXAMPLES_DIR):
            examples_dir = config.get(DEFAULT_SECTION, EG_EXAMPLES_DIR)

        if config.has_option(DEFAULT_SECTION, CUSTOM_EXAMPLES_DIR):
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
    if config.custom_dir:
        custom_path = get_custom_file_path_for_program(
            program,
            config.custom_dir
        )
        print custom_path
        return os.path.isfile(custom_path)
    else:
        return False


def open_pager_for_file(pager, default_file_path=None, custom_file_path=None):
    """
    Open pager to file_path. If a custom_file_path is also included, it will be
    shown before file_path in the same pager.
    """
    if default_file_path and custom_file_path:
        cat = subprocess.Popen(
            ('cat', custom_file_path, default_file_path),
            stdout=subprocess.PIPE
        )
        subprocess.call(
            (pager),
            stdin=cat.stdout
        )
        cat.wait()
    elif default_file_path:
        subprocess.call([pager, default_file_path])
    elif custom_file_path:
        subprocess.call([pager, custom_file_path])
    else:
        print 'At least one file must be defined.'
