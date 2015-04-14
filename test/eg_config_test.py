from eg import eg_config
from mock import patch
from nose.tools import assert_equal
from nose.tools import assert_false
from nose.tools import assert_true


def test_config_returns_defaults_if_all_none_and_no_egrc():
    with patch('os.path.isfile', return_value=False):
        config = eg_config.get_resolved_config_items(
            None,
            None,
            None,
            None,
            debug=False
        )

        default_color_config = eg_config.get_default_color_config()

        assert_equal(config.examples_dir, eg_config.DEFAULT_EXAMPLES_DIR)
        assert_equal(config.custom_dir, None)
        assert_equal(config.color_config, default_color_config)
        assert_equal(config.use_color, eg_config.DEFAULT_USE_COLOR)


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

        def_config = eg_config.Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir,
            color_config=test_color_config,
            use_color=test_use_color
        )
        with patch(
            'eg.eg_config.get_config_tuple_from_egrc',
            return_value=def_config
        ):
            config = eg_config.get_resolved_config_items(None, None, None, None)
            assert_equal(config.examples_dir, examples_dir)
            assert_equal(config.custom_dir, custom_dir)
            assert_equal(config.color_config, test_color_config)
            assert_equal(config.use_color, test_use_color)


def test_config_uses_custom_egrc_path():
    """Make sure we use the passed in egrc path rather than the default."""
    with patch('os.path.isfile', return_value=True):
        def_config = eg_config.Config(
            examples_dir='eg_dir',
            custom_dir='custom_dir',
            color_config=eg_config.get_empty_color_config(),
            use_color=False
        )
        egrc_path = 'test/path/to/egrc'
        with patch(
            'eg.eg_config.get_config_tuple_from_egrc',
            return_value=def_config
        ) as mocked_method:
            eg_config.get_resolved_config_items(
                egrc_path,
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
        egrc_examples_dir = 'egrc_examples_dir'
        egrc_custom_dir = 'egrc_custom_dir'
        egrc_use_color = 'the_egrc_says_yes_color'
        egrc_config = eg_config.Config(
            examples_dir=egrc_examples_dir,
            custom_dir=egrc_custom_dir,
            color_config=eg_config.get_default_color_config(),
            use_color=egrc_use_color
        )
        with patch(
            'eg.eg_config.get_config_tuple_from_egrc',
            return_value=egrc_config
        ):
            actual = eg_config.get_resolved_config_items(
                None,
                command_line_examples_dir,
                command_line_custom_dir,
                command_line_use_color,
                debug=False
            )
            assert_equal(actual.examples_dir, command_line_examples_dir)
            assert_equal(actual.custom_dir, command_line_custom_dir)
            assert_equal(actual.use_color, command_line_use_color)


def test_get_config_tuple_from_egrc_all_none_when_not_present():
    """
    Return correct data if the egrc has no data.

    We should return None for all values and an empty color_config if there is
    no data in the egrc.
    """
    actual = eg_config.get_config_tuple_from_egrc('test/assets/egrc_nodata')

    empty_color_config = eg_config.get_empty_color_config()

    target = eg_config.Config(
        examples_dir=None,
        custom_dir=None,
        color_config=empty_color_config,
        use_color=None
    )
    assert_equal(actual, target)


def test_get_config_tuple_from_egrc_when_present():
    """Make sure we extract values correctly from the egrc."""
    # These are the values hardcoded into the files.
    egrc_examples_dir = 'test/example/dir/in/egrc_withdata'
    egrc_custom_dir = 'test/custom/dir/in/egrc_withdata'
    egrc_use_color = True
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
        'eg.eg_config.get_expanded_path',
        side_effect=return_expanded_path
    ) as mock_expand:

        actual = eg_config.get_config_tuple_from_egrc(
            'test/assets/egrc_withdata'
        )

        target = eg_config.Config(
            examples_dir=egrc_examples_dir,
            custom_dir=egrc_custom_dir,
            color_config=color_config_from_file,
            use_color=egrc_use_color
        )
        assert_equal(actual, target)

        mock_expand.assert_any_call(egrc_examples_dir)
        mock_expand.assert_any_call(egrc_custom_dir)


def _get_color_config_from_egrc_withdata():
    """Get the color_config that is defined in the egrc_withdata test file."""
    test_color_config = eg_config.ColorConfig(
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
    second = eg_config.get_default_color_config()

    first = eg_config.ColorConfig(
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

    merged = eg_config.merge_color_configs(first, second)

    assert_equal(merged, second)


def test_merge_color_configs_take_all_first():
    second = eg_config.get_default_color_config()

    first = eg_config.ColorConfig(
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

    merged = eg_config.merge_color_configs(first, second)

    assert_equal(merged, first)


def test_merge_color_configs_mixed():
    second = eg_config.get_default_color_config()

    first = eg_config.ColorConfig(
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

    merged = eg_config.merge_color_configs(first, second)

    target = eg_config.ColorConfig(
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
    actual = eg_config.get_default_color_config()

    assert_equal(actual.pound, eg_config.DEFAULT_COLOR_POUND)
    assert_equal(actual.heading, eg_config.DEFAULT_COLOR_HEADING)
    assert_equal(actual.code, eg_config.DEFAULT_COLOR_CODE)
    assert_equal(actual.backticks, eg_config.DEFAULT_COLOR_BACKTICKS)
    assert_equal(actual.prompt, eg_config.DEFAULT_COLOR_PROMPT)

    assert_equal(actual.pound_reset, eg_config.DEFAULT_COLOR_POUND_RESET)
    assert_equal(actual.heading_reset, eg_config.DEFAULT_COLOR_HEADING_RESET)
    assert_equal(actual.code_reset, eg_config.DEFAULT_COLOR_CODE_RESET)
    assert_equal(
        actual.backticks_reset,
        eg_config.DEFAULT_COLOR_BACKTICKS_RESET
    )
    assert_equal(actual.prompt_reset, eg_config.DEFAULT_COLOR_PROMPT_RESET)


def test_parse_bool_true_for_truthy_values():
    """We should parse both 'True' and 'true' to True."""
    assert_true(eg_config._parse_bool_from_raw_egrc_value('True'))
    assert_true(eg_config._parse_bool_from_raw_egrc_value('true'))


def test_parse_bool_false_for_non_truthy_values():
    """Make sure we parse the likely non-truthy things as false."""
    assert_false(eg_config._parse_bool_from_raw_egrc_value(''))
    assert_false(eg_config._parse_bool_from_raw_egrc_value(None))
    assert_false(eg_config._parse_bool_from_raw_egrc_value('false'))
    assert_false(eg_config._parse_bool_from_raw_egrc_value('False'))


def test_get_priority_first():
    """The first non-None value should always be returned."""
    target = 'alpha'
    actual = eg_config.get_priority(target, 'second', 'third')
    assert_equal(target, actual)


def test_get_priority_second():
    """The second non-None should be returned if the first is None."""
    target = 'beta'
    actual = eg_config.get_priority(None, target, 'third')
    assert_equal(target, actual)


def test_get_priority_third():
    """The last should be taken if the first two are None."""
    target = 'gamma'
    actual = eg_config.get_priority(None, None, target)
    assert_equal(target, actual)


def test_get_priority_respect_false():
    """
    We should accept False as a priority-worthy value.

    False should be able to be specified and respected as non-None.
    """
    target = False
    actual = eg_config.get_priority(False, 'second', 'third')
    assert_equal(target, actual)
