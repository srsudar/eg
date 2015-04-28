import os
import pydoc

from eg import color


# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'

# Version of eg itself.
# Also bump in setup.py.
VERSION = '0.1.0'

# Flags for showing where the examples for commands are coming from.
FLAG_ONLY_CUSTOM = '+'
FLAG_CUSTOM_AND_DEFAULT = '*'

# This flag indicates that we should use the fallback pager.
FLAG_FALLBACK = 'pydoc.pager'


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
        color_config=config.color_config,
        pager_cmd=config.pager_cmd
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
    color_config=None,
    pager_cmd=None
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
        colorizer = color.EgColorizer(color_config)
        file_data = colorizer.colorize_text(file_data)

    page_string(file_data, pager_cmd)


def page_string(str_to_page, pager_cmd):
    """
    Page str_to_page via the pager. Tries to do a bit of fail-safe checking. For
    example, if the command starts with less but less doesn't appear to be
    installed on the system, it will resort to the pydoc.pager method.
    """
    # By default, we expect the command to be `less -R`. If that is the
    # pager_cmd, but they don't have less on their machine, odds are they're
    # just using the default value. In this case the pager will fail, so we'll
    # just go via pydoc.pager, which tries to do smarter checking that we don't
    # want to bother trying to replicate.
    # import ipdb; ipdb.set_trace()
    use_fallback_page_function = False
    if pager_cmd is None:
        use_fallback_page_function = True
    elif pager_cmd == FLAG_FALLBACK:
        use_fallback_page_function = True
    elif pager_cmd.startswith('less'):
        # stealing this check from pydoc.getpager()
        if hasattr(os, 'system') and os.system('(less) 2>/dev/null') != 0:
            # no less!
            use_fallback_page_function = True

    if use_fallback_page_function:
        pydoc.pager(str_to_page)
    else:
        # Otherwise, obey the user.
        pydoc.pipepager(str_to_page, cmd=pager_cmd)


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
