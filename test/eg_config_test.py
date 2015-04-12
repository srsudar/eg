from eg import eg_config
from mock import patch
from nose.tools import assert_equal


def test_config_returns_defaults_if_all_none_and_no_egrc():
    with patch('os.path.isfile', return_value=False):
        config = eg_config.get_resolved_config_items(
            None,
            None,
            None,
            debug=False
        )

        default_color_config = eg_config.get_default_color_config()

        assert_equal(config.examples_dir, eg_config.DEFAULT_EXAMPLES_DIR)
        assert_equal(config.custom_dir, None)
        assert_equal(config.color_config, default_color_config)


def test_config_returns_egrc_values_if_present():
    """
    If values are present, make sure we take them. Doesn't make sure they are
    extracted correctly.
    """
    with patch('os.path.isfile', return_value=True):
        examples_dir = 'test_eg_dir_from_egrc'
        custom_dir = 'test_custom_dir_from_egrc'
        test_color_config = _get_color_config_from_egrc_withdata()

        def_config = eg_config.Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir,
            color_config=test_color_config
        )
        with patch(
            'eg.eg_config.get_config_tuple_from_egrc',
            return_value=def_config
        ):
            config = eg_config.get_resolved_config_items(None, None, None)
            assert_equal(config.examples_dir, examples_dir)
            assert_equal(config.custom_dir, custom_dir)
            assert_equal(config.color_config, test_color_config)


def test_config_uses_custom_egrc_path():
    """Make sure we use the passed in egrc path rather than the default."""
    with patch('os.path.isfile', return_value=True):
        def_config = eg_config.Config(
            examples_dir='eg_dir',
            custom_dir='custom_dir',
            color_config=eg_config.get_empty_color_config()
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
                debug=False
            )
            mocked_method.assert_called_once_with(egrc_path)


def test_config_returns_passed_in_values_for_dirs():
    """
    Directories passed in at the command line should override those in the
    egrc.
    """
    with patch('os.path.isfile', return_value=True):
        command_line_examples_dir = 'test_eg_dir_user_defined'
        command_line_custom_dir = 'test_custom_dir_user_defined'
        egrc_examples_dir = 'egrc_examples_dir'
        egrc_custom_dir = 'egrc_custom_dir'
        egrc_config = eg_config.Config(
            examples_dir=egrc_examples_dir,
            custom_dir=egrc_custom_dir,
            color_config=None
        )
        with patch(
            'eg.eg_config.get_config_tuple_from_egrc',
            return_value=egrc_config
        ):
            actual = eg_config.get_resolved_config_items(
                None,
                command_line_examples_dir,
                command_line_custom_dir,
                None,
                debug=False
            )
            assert_equal(actual.examples_dir, command_line_examples_dir)
            assert_equal(actual.custom_dir, command_line_custom_dir)


def test_get_config_tuple_from_egrc_all_none_when_not_present():
    """
    We should return None for all values and an empty color_config if there is
    no data in the egrc.
    """
    actual = eg_config.get_config_tuple_from_egrc('test/assets/egrc_nodata')

    empty_color_config = eg_config.get_empty_color_config()

    target = eg_config.Config(
        examples_dir=None,
        custom_dir=None,
        color_config=empty_color_config
    )
    assert_equal(actual, target)


def test_get_config_tuple_from_egrc_when_present():
    """Make sure we extract values correctly from the egrc."""
    # These are the values hardcoded into the files.
    examples_dir = 'test/example/dir/in/egrc_withdata'
    custom_dir = 'test/custom/dir/in/egrc_withdata'
    color_config_from_file = _get_color_config_from_egrc_withdata()

    def return_expanded_path(*args, **kwargs):
        if args[0] == examples_dir:
            return examples_dir
        elif args[0] == custom_dir:
            return custom_dir
        else:
            raise TypeError(
                args[0] +
                ' was an unexpected path--should be ' +
                examples_dir +
                ' or ' +
                custom_dir
            )

    with patch(
        'eg.eg_config.get_expanded_path',
        side_effect=return_expanded_path
    ) as mock_expand:

        actual = eg_config.get_config_tuple_from_egrc(
            'test/assets/egrc_withdata'
        )

        target = eg_config.Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir,
            color_config=color_config_from_file
        )
        assert_equal(actual, target)

        mock_expand.assert_any_call(examples_dir)
        mock_expand.assert_any_call(custom_dir)


def _get_color_config_from_egrc_withdata():
    """Get the color_config that is defined in the egrc_withdata test file."""
    test_color_config = eg_config.ColorConfig(
        pound=r'\x1b[32m',
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
