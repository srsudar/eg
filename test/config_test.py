from eg import config
from mock import patch
from nose.tools import assert_equal
from nose.tools import assert_false
from nose.tools import assert_true


def test_config_returns_defaults_if_all_none_and_no_egrc():
    with patch('os.path.isfile', return_value=False):
        resolved_config = config.get_resolved_config_items(
            None,
            None,
            None,
            None,
            None,
            debug=False
        )

        default_color_config = config.get_default_color_config()

        assert_equal(resolved_config.examples_dir, config.DEFAULT_EXAMPLES_DIR)
        assert_equal(resolved_config.custom_dir, None)
        assert_equal(resolved_config.color_config, default_color_config)
        assert_equal(resolved_config.use_color, config.DEFAULT_USE_COLOR)
        assert_equal(resolved_config.pager_cmd, config.DEFAULT_PAGER_CMD)


def test_config_returns_egrc_values_if_present():
    """
    If values are present from an egrc, make sure we take them.

    Doesn't make sure they are extracted correctly from an egrc file.
    """
    with patch('os.path.isfile', return_value=True):
        examples_dir = 'test_eg_dir_from_egrc'
        custom_dir = 'test_custom_dir_from_egrc'
        test_color_config = _get_color_config_from_egrc_withdata()
        test_use_color = True
        test_pager_cmd = 'more baby'

        def_config = config.Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir,
            color_config=test_color_config,
            use_color=test_use_color,
            pager_cmd=test_pager_cmd
        )
        with patch(
            'eg.config.get_config_tuple_from_egrc',
            return_value=def_config
        ):
            resolved_config = config.get_resolved_config_items(
                None,
                None,
                None,
                None,
                None
            )
            assert_equal(resolved_config.examples_dir, examples_dir)
            assert_equal(resolved_config.custom_dir, custom_dir)
            assert_equal(resolved_config.color_config, test_color_config)
            assert_equal(resolved_config.use_color, test_use_color)
            assert_equal(resolved_config.pager_cmd, test_pager_cmd)


def test_config_uses_custom_egrc_path():
    """Make sure we use the passed in egrc path rather than the default."""
    with patch('os.path.isfile', return_value=True):
        def_config = config.Config(
            examples_dir='eg_dir',
            custom_dir='custom_dir',
            color_config=config.get_empty_color_config(),
            use_color=False,
            pager_cmd='less is more'
        )
        egrc_path = 'test/path/to/egrc'
        with patch(
            'eg.config.get_config_tuple_from_egrc',
            return_value=def_config
        ) as mocked_method:
            config.get_resolved_config_items(
                egrc_path,
                None,
                None,
                None,
                None,
                debug=False
            )
            mocked_method.assert_called_once_with(egrc_path)


def test_config_returns_values_passed_at_command_line():
    """
    Options passed in at the command line should override those in the egrc.
    """
    with patch('os.path.isfile', return_value=True):
        command_line_examples_dir = 'test_eg_dir_user_defined'
        command_line_custom_dir = 'test_custom_dir_user_defined'
        command_line_use_color = 'we_should_use_color'
        command_line_pager_cmd = 'command_line_says_pager_with_cat'
        egrc_examples_dir = 'egrc_examples_dir'
        egrc_custom_dir = 'egrc_custom_dir'
        egrc_use_color = 'the_egrc_says_yes_color'
        egrc_pager_cmd = 'the_egrc_pages_with_more'
        egrc_config = config.Config(
            examples_dir=egrc_examples_dir,
            custom_dir=egrc_custom_dir,
            color_config=config.get_default_color_config(),
            use_color=egrc_use_color,
            pager_cmd=egrc_pager_cmd
        )
        with patch(
            'eg.config.get_config_tuple_from_egrc',
            return_value=egrc_config
        ):
            actual = config.get_resolved_config_items(
                None,
                command_line_examples_dir,
                command_line_custom_dir,
                command_line_use_color,
                command_line_pager_cmd,
                debug=False
            )
            assert_equal(actual.examples_dir, command_line_examples_dir)
            assert_equal(actual.custom_dir, command_line_custom_dir)
            assert_equal(actual.use_color, command_line_use_color)
            assert_equal(actual.pager_cmd, command_line_pager_cmd)


def test_get_config_tuple_from_egrc_all_none_when_not_present():
    """
    Return correct data if the egrc has no data.

    We should return None for all values and an empty color_config if there is
    no data in the egrc.
    """
    actual = config.get_config_tuple_from_egrc('test/assets/egrc_nodata')

    empty_color_config = config.get_empty_color_config()

    target = config.Config(
        examples_dir=None,
        custom_dir=None,
        color_config=empty_color_config,
        use_color=None,
        pager_cmd=None
    )
    assert_equal(actual, target)


def test_get_config_tuple_from_egrc_when_present():
    """Make sure we extract values correctly from the egrc."""
    # These are the values hardcoded into the files.
    egrc_examples_dir = 'test/example/dir/in/egrc_withdata'
    egrc_custom_dir = 'test/custom/dir/in/egrc_withdata'
    egrc_use_color = True
    egrc_pager_cmd = 'more egrc'
    color_config_from_file = _get_color_config_from_egrc_withdata()

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

    with patch(
        'eg.config.get_expanded_path',
        side_effect=return_expanded_path
    ) as mock_expand:

        actual = config.get_config_tuple_from_egrc(
            'test/assets/egrc_withdata'
        )

        target = config.Config(
            examples_dir=egrc_examples_dir,
            custom_dir=egrc_custom_dir,
            color_config=color_config_from_file,
            use_color=egrc_use_color,
            pager_cmd=egrc_pager_cmd
        )
        assert_equal(actual, target)

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

    assert_equal(merged, second)


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

    assert_equal(merged, first)


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

    assert_equal(merged, target)


def test_default_color_config():
    """Make sure the default color config is set to the right values."""
    actual = config.get_default_color_config()

    assert_equal(actual.pound, config.DEFAULT_COLOR_POUND)
    assert_equal(actual.heading, config.DEFAULT_COLOR_HEADING)
    assert_equal(actual.code, config.DEFAULT_COLOR_CODE)
    assert_equal(actual.backticks, config.DEFAULT_COLOR_BACKTICKS)
    assert_equal(actual.prompt, config.DEFAULT_COLOR_PROMPT)

    assert_equal(actual.pound_reset, config.DEFAULT_COLOR_POUND_RESET)
    assert_equal(actual.heading_reset, config.DEFAULT_COLOR_HEADING_RESET)
    assert_equal(actual.code_reset, config.DEFAULT_COLOR_CODE_RESET)
    assert_equal(
        actual.backticks_reset,
        config.DEFAULT_COLOR_BACKTICKS_RESET
    )
    assert_equal(actual.prompt_reset, config.DEFAULT_COLOR_PROMPT_RESET)


def test_parse_bool_true_for_truthy_values():
    """We should parse both 'True' and 'true' to True."""
    assert_true(config._parse_bool_from_raw_egrc_value('True'))
    assert_true(config._parse_bool_from_raw_egrc_value('true'))


def test_parse_bool_false_for_non_truthy_values():
    """Make sure we parse the likely non-truthy things as false."""
    assert_false(config._parse_bool_from_raw_egrc_value(''))
    assert_false(config._parse_bool_from_raw_egrc_value(None))
    assert_false(config._parse_bool_from_raw_egrc_value('false'))
    assert_false(config._parse_bool_from_raw_egrc_value('False'))


def test_get_priority_first():
    """The first non-None value should always be returned."""
    target = 'alpha'
    actual = config.get_priority(target, 'second', 'third')
    assert_equal(target, actual)


def test_get_priority_second():
    """The second non-None should be returned if the first is None."""
    target = 'beta'
    actual = config.get_priority(None, target, 'third')
    assert_equal(target, actual)


def test_get_priority_third():
    """The last should be taken if the first two are None."""
    target = 'gamma'
    actual = config.get_priority(None, None, target)
    assert_equal(target, actual)


def test_get_priority_respect_false():
    """
    We should accept False as a priority-worthy value.

    False should be able to be specified and respected as non-None.
    """
    target = False
    actual = config.get_priority(False, 'second', 'third')
    assert_equal(target, actual)
