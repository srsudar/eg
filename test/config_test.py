import os

from eg import config
from eg import substitute
from mock import patch
from nose.tools import assert_raises

# Support python 2 and 3
try:
    import ConfigParser
except ImportError:
    from configparser import ConfigParser


PATH_EGRC_WITH_DATA = os.path.join(
    'test',
    'assets',
    'egrc_withdata'
)
PATH_EGRC_NO_DATA = os.path.join(
    'test',
    'assets',
    'egrc_nodata'
)
PATH_EGRC_SINGLE_SUB = os.path.join(
    'test',
    'assets',
    'egrc_single_substitution'
)


def _create_dummy_egrc_config():
    """
    Return a dummy Config object as if constructed from an egrc.
    """
    egrc_examples_dir = 'egrc_examples_dir'
    egrc_custom_dir = 'egrc_custom_dir'
    egrc_use_color = 'the_egrc_says_yes_color'
    egrc_pager_cmd = 'the_egrc_pages_with_more'
    egrc_squeeze = 'egrc_says_squeeze'
    egrc_subs = ['sub1', 'sub2']
    egrc_editor_cmd = 'vim from egrc'

    result = config.Config(
        examples_dir=egrc_examples_dir,
        custom_dir=egrc_custom_dir,
        color_config=config.get_default_color_config(),
        use_color=egrc_use_color,
        pager_cmd=egrc_pager_cmd,
        squeeze=egrc_squeeze,
        subs=egrc_subs,
        editor_cmd=egrc_editor_cmd,
    )
    return result


@patch('os.path.isfile', return_value=True)
@patch('eg.config.get_config_tuple_from_egrc')
def test_config_returns_egrc_values_if_present(mock_get_config, mock_isfile):
    """
    If values are present from an egrc, make sure we take them.

    Doesn't make sure they are extracted correctly from an egrc file.
    """
    examples_dir = 'test_eg_dir_from_egrc'
    custom_dir = 'test_custom_dir_from_egrc'
    test_color_config = _get_color_config_from_egrc_withdata()
    test_use_color = True
    test_pager_cmd = 'more baby'
    test_editor_cmd = 'vim is the best'
    test_squeeze = True
    test_subs = ['alpha', 'beta']

    def_config = config.Config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        color_config=test_color_config,
        use_color=test_use_color,
        pager_cmd=test_pager_cmd,
        editor_cmd=test_editor_cmd,
        squeeze=test_squeeze,
        subs=test_subs,
    )

    mock_get_config.return_value = def_config

    resolved_config = config.get_resolved_config(
        None,
        None,
        None,
        None,
        None,
        None,
    )

    assert resolved_config.examples_dir == examples_dir
    assert resolved_config.custom_dir == custom_dir
    assert resolved_config.color_config == test_color_config
    assert resolved_config.use_color == test_use_color
    assert resolved_config.pager_cmd == test_pager_cmd
    assert resolved_config.editor_cmd == test_editor_cmd
    assert resolved_config.squeeze == test_squeeze
    assert resolved_config.subs == test_subs


def _call_get_resolved_config_with_defaults(
    egrc_path=None,
    examples_dir=None,
    custom_dir=None,
    use_color=None,
    pager_cmd=None,
    squeeze=None,
    debug=False,
):
    """
    Wraps config.get_resolved_config_items with default values to allow callers
    to set fewer variables.
    """
    return config.get_resolved_config(
        egrc_path=egrc_path,
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        use_color=use_color,
        pager_cmd=pager_cmd,
        squeeze=squeeze,
        debug=debug,
    )


@patch('eg.config._inform_if_path_does_not_exist')
def test_inform_if_paths_invalid_selectively_informs(mock_inform):
    """
    We should only inform the user if the values are truthy.
    """
    config.inform_if_paths_invalid(None, None, None)

    assert mock_inform.call_count == 0

    egrc_path = 'egrc'
    ex_dir = 'ex dir'
    cu_dir = 'custom'

    config.inform_if_paths_invalid(egrc_path, ex_dir, cu_dir)

    assert mock_inform.call_count == 3
    mock_inform.assert_any_call(egrc_path)
    mock_inform.assert_any_call(ex_dir)
    mock_inform.assert_any_call(cu_dir)


@patch('os.path.isfile', return_value=True)
@patch('eg.config.inform_if_paths_invalid')
@patch('eg.config.get_config_tuple_from_egrc')
@patch('eg.config.get_expanded_path')
def test_get_resolved_config_uses_custom_egrc_path(
    mock_expand, mock_get_config, mock_inform, mock_isfile
):
    """Make sure we use the passed in egrc path rather than the default."""
    egrc_path = 'test/path/to/egrc'
    expanded_path = egrc_path + '/expanded'
    mock_expand.return_value = expanded_path
    _call_get_resolved_config_with_defaults(egrc_path=egrc_path)
    # We should have expanded the path as well as tried to retrieve the tuple
    # with the path.
    mock_expand.return_value = expanded_path
    mock_get_config.assert_called_once_with(expanded_path)


def test_get_egrc_config_reads_from_command_line():
    """
    get_egrc_config should use the command line path if it is provided.
    """
    cli_path = 'path/from/command/line'
    expected = 'mock config from egrc'

    _assert_about_get_egrc_config(
        cli_path=cli_path, path_to_expand=cli_path, expected_config=expected
    )


def test_get_egrc_config_uses_default():
    """
    get_egrc_config should use the default path if not provided on the command
    line.
    """
    expected = 'mock config from default position'

    _assert_about_get_egrc_config(
        cli_path=None,
        path_to_expand=config.DEFAULT_EGRC_PATH,
        expected_config=expected,
    )


def test_get_egrc_returns_empty_if_no_egrc():
    """
    We should return an empty config if no file is given.
    """
    expected = config.get_empty_config()

    _assert_about_get_egrc_config(
        cli_path=None,
        path_to_expand=config.DEFAULT_EGRC_PATH,
        expected_config=expected,
        is_file=False,
    )


@patch('eg.config.get_config_tuple_from_egrc')
@patch('eg.config.get_expanded_path')
@patch('os.path.isfile')
def _assert_about_get_egrc_config(
    mock_isfile,
    mock_expand,
    mock_get_config,
    cli_path=None,
    path_to_expand=None,
    is_file=True,
    expected_config=None
):
    expanded_path = path_to_expand + 'expanded'

    mock_isfile.return_value = is_file
    mock_expand.return_value = expanded_path
    mock_get_config.return_value = expected_config

    actual = config.get_egrc_config(cli_path)

    assert actual == expected_config

    mock_expand.assert_called_once_with(path_to_expand)
    mock_isfile.assert_called_once_with(expanded_path)

    if (is_file):
        mock_get_config.assert_called_once_with(expanded_path)


@patch('eg.config.get_expanded_path')
@patch('eg.config.get_egrc_config')
def test_get_resolved_config_calls_expand_paths(
    mock_get_egrc_config, mock_expand
):
    """
    We expect the examples_dir and custom_dir to be expanded.
    """
    def pretend_to_expand(path):
        if (path):
            return path + '/expanded'
        else:
            return None

    mock_get_egrc_config.return_value = config.get_empty_config()
    mock_expand.side_effect = pretend_to_expand

    # We are going to check against the default values, as the other paths have
    # an opportunity to already be expanded at this point. The function that
    # parses from the egrc returns the values expanded, eg.
    expected_examples_dir = pretend_to_expand(config.DEFAULT_EXAMPLES_DIR)
    expected_custom_dir = pretend_to_expand(config.DEFAULT_CUSTOM_DIR)

    actual = _call_get_resolved_config_with_defaults()

    assert actual.examples_dir == expected_examples_dir
    assert actual.custom_dir == expected_custom_dir


@patch('eg.config.get_editor_cmd_from_environment')
@patch('eg.config.inform_if_paths_invalid')
@patch('eg.config.get_egrc_config')
def _assert_about_get_resolved_config(
    mock_get_egrc_config,
    mock_inform,
    mock_get_editor,
    cli_egrc_path=None,
    cli_examples_dir=None,
    cli_custom_dir=None,
    cli_use_color=None,
    cli_pager_cmd=None,
    cli_squeeze=None,
    egrc_config=None,
    environment_editor_cmd=None,
    expected_config=None,
):
    """
    Helper for assertions surrounding get_resolved_config.
    """
    mock_get_egrc_config.return_value = expected_config
    mock_get_editor.return_value = environment_editor_cmd

    actual = config.get_resolved_config(
        cli_egrc_path,
        cli_examples_dir,
        cli_custom_dir,
        cli_use_color,
        cli_pager_cmd,
        cli_squeeze,
        debug=False
    )

    assert actual.examples_dir == expected_config.examples_dir
    assert actual.custom_dir == expected_config.custom_dir
    assert actual.use_color == expected_config.use_color
    assert actual.color_config == expected_config.color_config
    assert actual.pager_cmd == expected_config.pager_cmd
    assert actual.squeeze == expected_config.squeeze
    assert actual.subs == expected_config.subs
    assert actual.editor_cmd == expected_config.editor_cmd

    mock_get_egrc_config.assert_called_once_with(cli_egrc_path)
    mock_get_editor.assert_called_once_with()


def test_get_resolved_config_prioritizes_cli():
    """
    Options passed in at the command line should override those in the egrc.
    """
    cli_examples_dir = 'test_eg_dir_user_defined'
    cli_custom_dir = 'test_custom_dir_user_defined'
    cli_use_color = 'we_should_use_color'
    cli_pager_cmd = 'command_line_says_pager_with_cat'
    cli_squeeze = 'command_line_wants_to_squeeze'

    egrc_config = _create_dummy_egrc_config()

    expected = config.Config(
        examples_dir=cli_examples_dir,
        custom_dir=cli_custom_dir,
        use_color=cli_use_color,
        color_config=egrc_config.color_config,
        pager_cmd=cli_pager_cmd,
        squeeze=cli_squeeze,
        subs=egrc_config.subs,
        editor_cmd=egrc_config.editor_cmd,
    )

    _assert_about_get_resolved_config(
        cli_egrc_path=None,
        cli_examples_dir=cli_examples_dir,
        cli_custom_dir=cli_custom_dir,
        cli_use_color=cli_use_color,
        cli_pager_cmd=cli_pager_cmd,
        cli_squeeze=cli_squeeze,
        egrc_config=egrc_config,
        environment_editor_cmd=None,
        expected_config=expected,
    )


def test_get_resolved_config_defaults_to_egrc():
    """
    When no command line options are passed, we should prefer those in the
    egrc.
    """
    egrc_config = _create_dummy_egrc_config()

    # The second level of priority for editor_cmd is the environment variable,
    # so we include that here rather than from the egrc. Slightly hacky.
    editor_cmd = 'value from env'

    _assert_about_get_resolved_config(
        egrc_config=egrc_config,
        environment_editor_cmd=editor_cmd,
        expected_config=egrc_config,
    )


def test_get_resolved_config_falls_back_to_defaults():
    """
    When no cli arguments or egrc arguments are present, we should use the raw
    defaults.
    """
    empty_config = config.get_empty_config()

    expected = config.Config(
        examples_dir=config.DEFAULT_EXAMPLES_DIR,
        custom_dir=config.DEFAULT_CUSTOM_DIR,
        use_color=config.DEFAULT_USE_COLOR,
        color_config=config.get_default_color_config(),
        pager_cmd=config.DEFAULT_PAGER_CMD,
        squeeze=config.DEFAULT_SQUEEZE,
        subs=config.get_default_subs(),
        editor_cmd=config.DEFAULT_EDITOR_CMD,
    )

    _assert_about_get_resolved_config(
        egrc_config=empty_config,
        environment_editor_cmd=None,
        expected_config=expected
    )


def test_get_config_tuple_from_egrc_all_none_when_not_present():
    """
    Return correct data if the egrc has no data.

    We should return None for all values and an empty color_config if there is
    no data in the egrc.
    """
    actual = config.get_config_tuple_from_egrc(PATH_EGRC_NO_DATA)

    empty_color_config = config.get_empty_color_config()

    target = config.Config(
        examples_dir=None,
        custom_dir=None,
        color_config=empty_color_config,
        use_color=None,
        pager_cmd=None,
        squeeze=None,
        subs=None,
        editor_cmd=None,
    )
    assert actual == target


@patch('eg.config.get_expanded_path')
def test_get_config_tuple_from_egrc_when_present(mock_expand):
    """
    Make sure we extract values correctly from the egrc.
    """
    # These are the values hardcoded into the files.
    egrc_examples_dir = 'test/example/dir/in/egrc_withdata'
    egrc_custom_dir = 'test/custom/dir/in/egrc_withdata'
    egrc_use_color = True
    egrc_pager_cmd = 'more egrc'
    egrc_editor_cmd = 'vim egrc'
    color_config_from_file = _get_color_config_from_egrc_withdata()
    egrc_squeeze = True
    # Order matters--we apply substitutions alphabetically.
    egrc_subs = [
        substitute.Substitution(r'    ', r'', False),
        substitute.Substitution('\n\n\n', '\n\n', True)
    ]

    def return_expanded_path(*args, **kwargs):
        if args[0] == egrc_examples_dir:
            return egrc_examples_dir
        elif args[0] == egrc_custom_dir:
            return egrc_custom_dir
        else:
            raise TypeError(
                args[0] +
                ' was an unexpected path--should be ' +
                egrc_examples_dir +
                ' or ' +
                egrc_custom_dir
            )

    mock_expand.side_effect = return_expanded_path

    actual = config.get_config_tuple_from_egrc(PATH_EGRC_WITH_DATA)

    expected = config.Config(
        examples_dir=egrc_examples_dir,
        custom_dir=egrc_custom_dir,
        color_config=color_config_from_file,
        use_color=egrc_use_color,
        pager_cmd=egrc_pager_cmd,
        squeeze=egrc_squeeze,
        subs=egrc_subs,
        editor_cmd=egrc_editor_cmd,
    )

    assert actual == expected

    mock_expand.assert_any_call(egrc_examples_dir)
    mock_expand.assert_any_call(egrc_custom_dir)


def _get_color_config_from_egrc_withdata():
    """Get the color_config that is defined in the egrc_withdata test file."""
    test_color_config = config.ColorConfig(
        pound='\x1b[32m',
        heading='heading_val',
        code='code_val',
        backticks='backticks_val',
        prompt='prompt_val',
        pound_reset='pound_reset_val',
        heading_reset='heading_reset_val',
        code_reset='code_reset_val',
        backticks_reset='backticks_reset_val',
        prompt_reset='prompt_reset_val'
    )
    return test_color_config


def test_merge_color_configs_first_all_none():
    second = config.get_default_color_config()

    first = config.ColorConfig(
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

    merged = config.merge_color_configs(first, second)

    assert merged == second


def test_merge_color_configs_take_all_first():
    second = config.get_default_color_config()

    first = config.ColorConfig(
        pound='pound_color',
        heading='heading_color',
        code='code_color',
        backticks='backticks_color',
        prompt='prompt_color',
        pound_reset='p_reset',
        heading_reset='h_reset',
        code_reset='c_reset',
        backticks_reset='b_reset',
        prompt_reset='prmpt_reset'
    )

    merged = config.merge_color_configs(first, second)

    assert merged == first


def test_merge_color_configs_mixed():
    second = config.get_default_color_config()

    first = config.ColorConfig(
        pound='pound_color',
        heading=None,
        code='code_color',
        backticks=None,
        prompt=None,
        pound_reset=None,
        heading_reset=None,
        code_reset=None,
        backticks_reset=None,
        prompt_reset=None
    )

    merged = config.merge_color_configs(first, second)

    target = config.ColorConfig(
        pound=first.pound,
        heading=second.heading,
        code=first.code,
        backticks=second.backticks,
        prompt=second.prompt,
        pound_reset=second.pound_reset,
        heading_reset=second.heading_reset,
        code_reset=second.code_reset,
        backticks_reset=second.backticks_reset,
        prompt_reset=second.prompt_reset
    )

    assert merged == target


def test_default_color_config():
    """Make sure the default color config is set to the right values."""
    actual = config.get_default_color_config()

    assert actual.pound == config.DEFAULT_COLOR_POUND
    assert actual.heading == config.DEFAULT_COLOR_HEADING
    assert actual.code == config.DEFAULT_COLOR_CODE
    assert actual.backticks == config.DEFAULT_COLOR_BACKTICKS
    assert actual.prompt == config.DEFAULT_COLOR_PROMPT

    assert actual.pound_reset == config.DEFAULT_COLOR_POUND_RESET
    assert actual.heading_reset == config.DEFAULT_COLOR_HEADING_RESET
    assert actual.code_reset == config.DEFAULT_COLOR_CODE_RESET
    assert actual.backticks_reset == config.DEFAULT_COLOR_BACKTICKS_RESET
    assert actual.prompt_reset == config.DEFAULT_COLOR_PROMPT_RESET


def test_parse_bool_true_for_truthy_values():
    """We should parse both 'True' and 'true' to True."""
    assert config._parse_bool_from_raw_egrc_value('True') == True
    assert config._parse_bool_from_raw_egrc_value('true') == True


def test_parse_bool_false_for_non_truthy_values():
    """Make sure we parse the likely non-truthy things as false."""
    assert config._parse_bool_from_raw_egrc_value('') == False
    assert config._parse_bool_from_raw_egrc_value(None) == False
    assert config._parse_bool_from_raw_egrc_value('false') == False
    assert config._parse_bool_from_raw_egrc_value('False') == False


def test_get_priority_first():
    """The first non-None value should always be returned."""
    target = 'alpha'
    actual = config.get_priority(target, 'second', 'third')
    assert target == actual


def test_get_priority_second():
    """The second non-None should be returned if the first is None."""
    target = 'beta'
    actual = config.get_priority(None, target, 'third')
    assert target == actual


def test_get_priority_third():
    """The last should be taken if the first two are None."""
    target = 'gamma'
    actual = config.get_priority(None, None, target)
    assert target == actual


def test_get_priority_respect_false():
    """
    We should accept False as a priority-worthy value.

    False should be able to be specified and respected as non-None.
    """
    target = False
    actual = config.get_priority(False, 'second', 'third')
    assert target == actual


def test_parse_substitution_from_list_without_is_multiline():
    """
    Make sure we can parse a list without the is_multiline option set, i.e.
    just a two element list.
    """
    target = substitute.Substitution('foo', 'bar', False)
    list_rep = ['foo', 'bar']
    actual = config.parse_substitution_from_list(list_rep)
    assert actual == target


def test_parse_substitution_from_list_with_is_multiline():
    """
    We should be able to parse a Subsitution if is_multiline is set.
    """
    target = substitute.Substitution('patt', 'repl', True)
    list_rep = ['patt', 'repl', True]
    actual = config.parse_substitution_from_list(list_rep)
    assert actual == target


def test_parse_substitution_error_if_not_list():
    """
    Raise a SyntaxError if the value is not a list.
    """
    assert_raises(SyntaxError, config.parse_substitution_from_list, 'foo_str')


def test_parse_substitution_error_if_wrong_length():
    """
    Raise a SyntaxError if the list is less than two long.
    """
    assert_raises(
        SyntaxError,
        config.parse_substitution_from_list,
        ['foo']
    )


def test_parse_substitution_error_if_third_element_not_bool():
    """
    Raise a SyntaxError if the third element in the list is not a boolean.
    """
    assert_raises(
        SyntaxError,
        config.parse_substitution_from_list,
        ['foo', 'bar', 'intentionally_not_a_bool']
    )


def test_get_substitution_from_config_finds_single_substitution():
    """
    Retrieve a single substitution from the config. Integration test--actually
    pulls from a file.
    """
    # This is hardcoded matching the value in the file.
    single_sub = substitute.Substitution('foo', 'bar', False)
    target = [single_sub]

    config_obj = _get_egrc_config(PATH_EGRC_SINGLE_SUB)

    actual = config.get_substitutions_from_config(config_obj)
    assert actual == target


def test_get_substitution_from_config_finds_multiple_substitutions():
    """
    Retrieve multiple substitutions from a config in the appropriate order.
    Integration test--actually pulls from a file.
    """
    # These are hardcoded matching the value in the file. They will be sorted
    # alphabetically by pattern name.
    first_sub = substitute.Substitution(r'    ', r'', False)
    second_sub = substitute.Substitution('\n\n\n', '\n\n', True)
    target = [first_sub, second_sub]

    config_obj = _get_egrc_config(PATH_EGRC_WITH_DATA)

    actual = config.get_substitutions_from_config(config_obj)
    assert actual == target


def _get_egrc_config(egrc_path):
    """
    Return a config object based on the config file at the given path.
    """
    with open(egrc_path, 'r') as egrc:
        try:
            config = ConfigParser.RawConfigParser()
        except AttributeError:
            config = ConfigParser()
        config.readfp(egrc)
    return config
