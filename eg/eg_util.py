import eg_colorizer
import os
import pydoc


# Name of the environment variable where we look for the default pager
PAGER_ENV = 'PAGER'
DEFAULT_PAGER = 'less'


# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'

# Version of eg itself.
# Also bump in setup.py.
VERSION = '0.0.2'

# Flags for showing where the examples for commands are coming from.
FLAG_ONLY_CUSTOM = '+'
FLAG_CUSTOM_AND_DEFAULT = '*'


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
        print (
            'No entry found for ' +
            program +
            '. Run `eg --list` to see all available entries.'
        )
        return

    open_pager_for_file(
        default_file_path=default_file_path,
        custom_file_path=custom_file_path,
        use_color=config.use_color,
        color_config=config.color_config
    )


def get_file_path_for_program(program, dir_to_search):
    """
    Return the file name and path for the program.

    examples_dir cannot be None

    Path is not guaranteed to exist. Just says where it should be if it
    existed. Paths must be fully expanded before being passed in (i.e. no ~ or
    variables).
    """
    if dir_to_search is None:
        raise TypeError('examples_dir cannot be None')
    else:
        result = os.path.join(dir_to_search, program + EXAMPLE_FILE_SUFFIX)
        return result


def has_default_entry_for_program(program, config):
    """Return True if has standard examples for program, else False."""
    if config.examples_dir:
        file_path = get_file_path_for_program(
            program,
            config.examples_dir
        )
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


def open_pager_for_file(
    default_file_path=None,
    custom_file_path=None,
    use_color=False,
    color_config=None
):
    """
    Open pager to file_path. If a custom_file_path is also included, it will be
    shown before file_path in the same pager.
    """
    file_data = ''

    if custom_file_path:
        file_data += _get_contents_of_file(custom_file_path)

    if default_file_path:
        file_data += _get_contents_of_file(default_file_path)

    if use_color:
        colorizer = eg_colorizer.EgColorizer(color_config)
        file_data = colorizer.colorize_text(file_data)

    pydoc.pager(file_data)


def _get_contents_of_file(path):
    """Get the contents of the file at path. The file must exist."""
    with open(path, 'r') as f:
        result = f.read()
        return result


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
