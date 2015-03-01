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

# Flags for showing where the examples for commands are coming from.
FLAG_ONLY_CUSTOM = '+'
FLAG_CUSTOM_AND_DEFAULT = '*'

# A basic struct containing configuration values.
#    examples_dir: path to the directory of examples that ship with eg
#    custom_dir: path to the directory where custom examples are found
Config = namedtuple('Config', ['examples_dir', 'custom_dir'])


def get_expanded_path(path):
    """Expand ~ and variables in a path. If path is not truthy, return None."""
    if path:
        result = path
        result = os.path.expanduser(result)
        result = os.path.expandvars(result)
        return result
    else:
        return None


def _get_priority(first, second, third):
    """
    Return the items based on priority and their truthiness. If first is
    present, it will be returned. If only second and third, second will be
    returned. If all three are absent, will return None.
    """
    if first:
        return first
    elif second:
        return second
    elif third:
        return third
    else:
        return None


def _inform_if_path_does_not_exist(path):
    """
    If the path does not exist, print a message saying so. This is intended to
    be helpful to users if they specify a custom path that eg cannot find.
    """
    expanded_path = get_expanded_path(path)
    if not os.path.isfile(expanded_path):
        print 'Could not find custom path at: ' + expanded_path


def get_resolved_config_items(
    egrc_path,
    examples_dir,
    custom_dir
):
    """
    Create a Config namedtuple. Passed in values will override defaults.
    """
    # Expand the paths so we can use them with impunity later.
    egrc_path = get_expanded_path(egrc_path)
    examples_dir = get_expanded_path(examples_dir)
    custom_dir = get_expanded_path(custom_dir)

    # Print helpful failures.
    if egrc_path:
        _inform_if_path_does_not_exist(egrc_path)
    if examples_dir:
        _inform_if_path_does_not_exist(examples_dir)
    if custom_dir:
        _inform_if_path_does_not_exist(custom_dir)

    # The general rule is: caller-defined, egrc-defined, defaults. We'll try and
    # get all three then use _get_priority to choose the right one.

    resolved_egrc_path = _get_priority(egrc_path, DEFAULT_EGRC_PATH, None)
    resolved_egrc_path = get_expanded_path(resolved_egrc_path)

    egrc_config = Config(examples_dir=None, custom_dir=None)
    if os.path.isfile(resolved_egrc_path):
        egrc_config = get_config_tuple_from_egrc(resolved_egrc_path)

    resolved_examples_dir = _get_priority(
        examples_dir,
        egrc_config.examples_dir,
        DEFAULT_EXAMPLES_DIR
    )
    resolved_custom_dir = _get_priority(
        custom_dir,
        egrc_config.custom_dir,
        None
    )

    result = Config(
        examples_dir=resolved_examples_dir,
        custom_dir=resolved_custom_dir
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
        config = ConfigParser.RawConfigParser()
        config.readfp(egrc)

        # default to None
        examples_dir = None
        custom_dir = None

        if config.has_option(DEFAULT_SECTION, EG_EXAMPLES_DIR):
            examples_dir = config.get(DEFAULT_SECTION, EG_EXAMPLES_DIR)
            examples_dir = get_expanded_path(examples_dir)

        if config.has_option(DEFAULT_SECTION, CUSTOM_EXAMPLES_DIR):
            custom_dir = config.get(DEFAULT_SECTION, CUSTOM_EXAMPLES_DIR)
            custom_dir = get_expanded_path(custom_dir)

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
        default_file_path = get_file_path_for_program(
            program,
            config.examples_dir
        )

    if has_custom_entry_for_program(program, config):
        custom_file_path = get_file_path_for_program(
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


def get_file_path_for_program(program, dir_to_search):
    """
    Return the file name and path for the program.

    examples_dir cannot be None

    Path is not guaranteed to exist. Just says where it should be if it
    existed. Returned paths are absolute.
    """
    if dir_to_search is None:
        raise TypeError('examples_dir cannot be None')
    else:
        result = os.path.join(dir_to_search, program + EXAMPLE_FILE_SUFFIX)
        result = get_expanded_path(result)
        return result


def has_default_entry_for_program(program, config):
    """Return True if has standard examples for program, else False."""
    if config.examples_dir:
        file_path = get_file_path_for_program(
            program,
            config.examples_dir)
        return os.path.isfile(file_path)
    else:
        return False


def has_custom_entry_for_program(program, config):
    """Return True if has custom examples for a program, else false."""
    if config.custom_dir:
        custom_path = get_file_path_for_program(
            program,
            config.custom_dir
        )
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


def get_list_of_all_supported_commands(config):
    """
    Generate a list of all the commands that have examples known to eg. The
    format of the list is the command names. The fact that there are examples
    for 'cp', for example, would mean that 'cp' was in the list.

    The format of the list contains additional information to say if there are
    only default examples, only custom examples, or both:

        cp    (only default)
        cp *  (only custom)
        cp +  (default and custom)
    """
    default_files = []
    custom_files = []

    if config.examples_dir and os.path.isdir(config.examples_dir):
        default_files = os.listdir(config.examples_dir)
    if config.custom_dir and os.path.isdir(config.custom_dir):
        custom_files = os.listdir(config.custom_dir)

    # Now we get tricky. We're going to output the correct information by
    # iterating through each list only once. Keep pointers to our position in
    # the list. If they point to the same value, output that value with the
    # 'both' flag and increment both. Just one, output with the appropriate flag
    # and increment.

    ptr_default = 0
    ptr_custom = 0

    result = []

    def get_without_suffix(file_name):
        """
        Return the file name without the suffix, or the file name itself
        if it does not have the suffix.
        """
        return file_name.split(EXAMPLE_FILE_SUFFIX)[0]

    while ptr_default < len(default_files) and ptr_custom < len(custom_files):
        def_cmd = default_files[ptr_default]
        cus_cmd = custom_files[ptr_custom]

        if def_cmd == cus_cmd:
            # They have both
            result.append(
                get_without_suffix(def_cmd) +
                ' ' +
                FLAG_CUSTOM_AND_DEFAULT
            )
            ptr_default += 1
            ptr_custom += 1
        elif def_cmd < cus_cmd:
            # Only default, as default comes first.
            result.append(get_without_suffix(def_cmd))
            ptr_default += 1
        else:
            # Only custom
            result.append(get_without_suffix(cus_cmd) + ' ' + FLAG_ONLY_CUSTOM)
            ptr_custom += 1

    # Now just append.
    for i in range(ptr_default, len(default_files)):
        def_cmd = default_files[i]
        result.append(get_without_suffix(def_cmd))

    for i in range(ptr_custom, len(custom_files)):
        cus_cmd = custom_files[i]
        result.append(get_without_suffix(cus_cmd) + ' ' + FLAG_ONLY_CUSTOM)

    return result
