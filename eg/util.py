import json
import os
import pydoc
import subprocess

from eg import color
from eg import substitute


# The file name suffix expected for example files.
EXAMPLE_FILE_SUFFIX = '.md'

# Version of eg itself.
# Also bump in setup.py.
VERSION = '1.0.0'

# Flags for showing where the examples for commands are coming from.
FLAG_ONLY_CUSTOM = '+'
FLAG_CUSTOM_AND_DEFAULT = '*'

# This flag indicates that we should use the fallback pager.
FLAG_FALLBACK = 'pydoc.pager'

# The name of the file storing mappings of aliases to programs with entries.
ALIAS_FILE_NAME = 'aliases.json'


def _inform_cannot_edit_no_custom_dir():
    """
    Inform the user that a custom dir has not be specified, and thus an edit
    cannot be performed.
    """
    msg = """
    You've requested to edit custom examples for a command, but no custom
    directory has been found. The value must be set and the directory must
    exist.

    Custom examples are shown before the default examples and are under your
    control. You must specify where to save them before editing them. This can
    be done at the command line (with the `-c` or `--custom-dir` flags) or via
    the `custom-dir` option in your egrc. A minimal egrc might look like:

    [eg-config]
    custom-dir = ~/.eg/
    """
    print(msg)


def edit_custom_examples(program, config):
    """
    Edit custom examples for the given program, creating the file if it does
    not exist.
    """
    if (not config.custom_dir) or (not os.path.exists(config.custom_dir)):
        _inform_cannot_edit_no_custom_dir()
        return

    # resolve aliases
    resolved_program = get_resolved_program(program, config)
    custom_file_path = get_file_path_for_program(
        resolved_program,
        config.custom_dir
    )
    subprocess.call([config.editor_cmd, custom_file_path])


def handle_program(program, config):
    default_file_path = None
    custom_file_path = None

    # try to resolve any aliases
    resolved_program = get_resolved_program(program, config)

    if has_default_entry_for_program(resolved_program, config):
        default_file_path = get_file_path_for_program(
            resolved_program,
            config.examples_dir
        )

    if has_custom_entry_for_program(resolved_program, config):
        custom_file_path = get_file_path_for_program(
            resolved_program,
            config.custom_dir
        )

    # Handle the case where we have nothing for them.
    if default_file_path is None and custom_file_path is None:
        print(
            'No entry found for ' +
            program +
            '. Run `eg --list` to see all available entries.'
        )
        return

    raw_contents = get_contents_from_files(
        default_file_path,
        custom_file_path
    )

    formatted_contents = get_formatted_contents(
        raw_contents,
        use_color=config.use_color,
        color_config=config.color_config,
        squeeze=config.squeeze,
        subs=config.subs
    )

    page_string(formatted_contents, config.pager_cmd)


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


def get_contents_from_files(default_file_path, custom_file_path):
    """
    Take the paths to two files and return the contents as a string. If
    custom_file_path is valid, it will be shown before the contents of the
    default file.
    """
    file_data = ''

    if custom_file_path:
        file_data += _get_contents_of_file(custom_file_path)

    if default_file_path:
        file_data += _get_contents_of_file(default_file_path)

    return file_data


def page_string(str_to_page, pager_cmd):
    """
    Page str_to_page via the pager.
    """
    # By default, we expect the command to be `less -R`. If that is the
    # pager_cmd, but they don't have less on their machine, odds are they're
    # just using the default value. In this case the pager will fail, so we'll
    # just go via pydoc.pager, which tries to do smarter checking that we don't
    # want to bother trying to replicate.
    use_fallback_page_function = False
    if pager_cmd is None:
        use_fallback_page_function = True
    elif pager_cmd == FLAG_FALLBACK:
        use_fallback_page_function = True

    try:
        if use_fallback_page_function:
            pydoc.pager(str_to_page)
        else:
            # Otherwise, obey the user.
            pydoc.pipepager(str_to_page, cmd=pager_cmd)
    except KeyboardInterrupt:
        pass


def _get_contents_of_file(path):
    """Get the contents of the file at path. The file must exist."""
    with open(path, 'r') as f:
        result = f.read()
        return result


def _is_example_file(file_name):
    """
    True if the file_name is an example file, else False.
    """
    return file_name.endswith(EXAMPLE_FILE_SUFFIX)


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

    Aliases are shown as
    alias -> resolved, with resolved having its '*' or '+' as expected. Aliases
    that shadow custom-only file names are expected to be shown instead of the
    custom file names. This is intentional, as that is the behavior for file
    resolution--an alias will hide a custom file.
    """
    default_files = []
    custom_files = []

    if config.examples_dir and os.path.isdir(config.examples_dir):
        default_files = os.listdir(config.examples_dir)
    if config.custom_dir and os.path.isdir(config.custom_dir):
        custom_files = os.listdir(config.custom_dir)

    # Now filter so we only have example files, not things like aliases.json.
    default_files = [path for path in default_files if _is_example_file(path)]
    custom_files = [path for path in custom_files if _is_example_file(path)]

    def get_without_suffix(file_name):
        """
        Return the file name without the suffix, or the file name itself
        if it does not have the suffix.
        """
        return file_name.split(EXAMPLE_FILE_SUFFIX)[0]

    default_files = [get_without_suffix(f) for f in default_files]
    custom_files = [get_without_suffix(f) for f in custom_files]

    set_default_commands = set(default_files)
    set_custom_commands = set(custom_files)

    alias_dict = get_alias_dict(config)

    both_defined = set_default_commands & set_custom_commands
    only_default = set_default_commands - set_custom_commands
    only_custom = set_custom_commands - set_default_commands

    all_commands = both_defined | only_default | only_custom

    command_to_rep = {}
    for command in all_commands:
        rep = None
        if command in both_defined:
            rep = command + ' ' + FLAG_CUSTOM_AND_DEFAULT
        elif command in only_default:
            rep = command
        elif command in only_custom:
            rep = command + ' ' + FLAG_ONLY_CUSTOM
        else:
            raise NameError('command not in known set: ' + str(command))
        command_to_rep[command] = rep

    result = []
    all_commands_and_aliases = all_commands.union(alias_dict.keys())
    for command in all_commands_and_aliases:
        if command in alias_dict:
            # aliases get precedence
            target = alias_dict[command]
            rep_of_target = command_to_rep[target]
            result.append(command + ' -> ' + rep_of_target)
        else:
            rep = command_to_rep[command]
            result.append(rep)

    result.sort()
    return result


def get_squeezed_contents(contents):
    """
    Squeeze the contents by removing blank lines between definition and example
    and remove duplicate blank lines except between sections.
    """
    line_between_example_code = substitute.Substitution(
        '\n\n    ',
        '\n    ',
        True
    )
    lines_between_examples = substitute.Substitution('\n\n\n', '\n\n', True)
    lines_between_sections = substitute.Substitution(
        '\n\n\n\n', '\n\n\n', True
    )

    result = contents
    result = line_between_example_code.apply_and_get_result(result)
    result = lines_between_examples.apply_and_get_result(result)
    result = lines_between_sections.apply_and_get_result(result)
    return result


def get_colorized_contents(contents, color_config):
    """Colorize the contents based on the color_config."""
    colorizer = color.EgColorizer(color_config)
    result = colorizer.colorize_text(contents)
    return result


def get_substituted_contents(contents, substitutions):
    """
    Perform a list of substitutions and return the result.

    contents: the starting string on which to beging substitutions
    substitutions: list of Substitution objects to call, in order, with the
        result of the previous substitution.
    """
    result = contents
    for sub in substitutions:
        result = sub.apply_and_get_result(result)
    return result


def get_formatted_contents(
    raw_contents,
    use_color,
    color_config,
    squeeze,
    subs
):
    """
    Apply formatting to raw_contents and return the result. Formatting is
    applied in the order: color, squeeze, subs.
    """
    result = raw_contents

    if use_color:
        result = get_colorized_contents(result, color_config)

    if squeeze:
        result = get_squeezed_contents(result)

    if subs:
        result = get_substituted_contents(result, subs)

    return result


def get_resolved_program(program, config_obj):
    """
    Take a program that may be an alias for another program and return the
    resolved program.

    It only ever resolves a single level of aliasing, so does not support
    aliasing to an alias.

    Returns the original program if the program is not an alias.
    """
    alias_dict = get_alias_dict(config_obj)
    if program in alias_dict:
        return alias_dict[program]
    else:
        return program


def get_alias_dict(config_obj):
    """
    Return a dictionary consisting of all aliases known to eg.

    The format is {'alias': 'resolved_program'}.

    If the aliases file does not exist, returns an empty dict.
    """
    if not config_obj.examples_dir:
        return {}

    alias_file_path = _get_alias_file_path(config_obj)
    if not os.path.isfile(alias_file_path):
        return {}

    alias_file_contents = _get_contents_of_file(alias_file_path)
    result = json.loads(alias_file_contents)
    return result


def _get_alias_file_path(config_obj):
    """
    Return the file path for the aliases dict.
    """
    return os.path.join(config_obj.examples_dir, ALIAS_FILE_NAME)
