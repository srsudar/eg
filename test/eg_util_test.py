from eg import eg_util
from mock import patch
from nose.tools import assert_equal


def test_pager_set_returns_true():
    with patch('os.getenv', return_value='less'):
        actual = eg_util.pager_env_is_set()
        assert actual is True


def test_pager_not_set_returns_false():
    # os.getenv returns None if a variable is not set
    with patch('os.getenv', return_value=None):
        actual = eg_util.pager_env_is_set()
        print actual
        assert actual is False


def test_config_returns_defaults_if_all_none_and_no_egrc():
    with patch('os.path.isfile', return_value=False):
        config = eg_util.get_resolved_config_items(None, None, None)
        assert config.examples_dir == eg_util.DEFAULT_EXAMPLES_DIR
        assert config.custom_dir is None


def test_config_returns_egrc_values_if_present():
    with patch('os.path.isfile', return_value=True):
        examples_dir = 'test_eg_dir_from_egrc'
        custom_dir = 'test_custom_dir_from_egrc'
        def_config = eg_util.Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir
        )
        with patch(
            'eg.eg_util.get_config_tuple_from_egrc',
            return_value=def_config
        ):
            config = eg_util.get_resolved_config_items(None, None, None)
            assert_equal(config.examples_dir, examples_dir)
            assert_equal(config.custom_dir, custom_dir)


def test_config_uses_custom_egrc_path():
    """Make sure we use the passed in egrc path rather than the default."""
    with patch('os.path.isfile', return_value=True):
        def_config = eg_util.Config(
            examples_dir='eg_dir',
            custom_dir='custom_dir'
        )
        egrc_path = 'test/path/to/egrc'
        with patch(
            'eg.eg_util.get_config_tuple_from_egrc',
            return_value=def_config
        ) as mocked_method:
            eg_util.get_resolved_config_items(egrc_path, None, None)
            mocked_method.assert_called_once_with(egrc_path)


def test_config_returns_passed_in_values_for_dirs():
    with patch('os.path.isfile', return_value=True):
        examples_dir = 'test_eg_dir_user_defined'
        custom_dir = 'test_custom_dir_user_defined'
        egrc_examples_dir = 'egrc_examples_dir'
        egrc_custom_dir = 'egrc_custom_dir'
        egrc_config = eg_util.Config(
            examples_dir=egrc_examples_dir,
            custom_dir=egrc_custom_dir
        )
        with patch(
            'eg.eg_util.get_config_tuple_frmo_egrc',
            return_value=egrc_config
        ):
            actual = eg_util.get_resolved_config_items(
                None,
                examples_dir,
                custom_dir
            )
            assert_equal(actual.examples_dir, examples_dir)
            assert_equal(actual.custom_dir, custom_dir)


def test_get_file_path_for_program_valid():
    actual = eg_util.get_file_path_for_program('find')
    target = './examples/find.md'
    assert actual == target


def test_has_entry_for_program_finds_file():
    _assert_has_entry_helper(True)


def test_does_not_have_entry_for_file():
    _assert_has_entry_helper(False)


def _assert_has_entry_helper(should_find):
    """
    Helps assert whether or not there is an entry for a program. Handles
    mocking out calls.

    should_find_program true if the program should exist, false if it should
    not
    """
    program = 'foo'
    path = './examples/' + program + '.txt'
    with patch('eg.eg_util.get_file_path_for_program', return_value=path):
        with patch('os.path.isfile', return_value=should_find) as mock_method:
            actual = eg_util.has_entry_for_program(program)
            if should_find:
                assert actual
            else:
                assert not actual
            mock_method.assert_called_once_with(path)


def test_open_pager_to_line_number_invokes_correctly_for_less():
    pager = 'less'
    file_path = 'examples/touch.md'
    with patch('subprocess.call') as mock_method:
        eg_util.open_pager_for_file(pager, file_path)
        mock_method.assert_called_once_with([pager, file_path])


def test_get_pager_with_custom_correct():
    custom_pager = 'more'
    with patch('eg.eg_util.pager_env_is_set', return_value=True):
        with patch('os.getenv', return_value=custom_pager):
            assert eg_util.get_pager() == custom_pager


def test_get_pager_without_custom_correct():
    with patch('eg.eg_util.pager_env_is_set', return_value=False):
        assert eg_util.get_pager() == eg_util.DEFAULT_PAGER


def test_get_path_to_rc_file():
    passed_in_value = '~/.egrc'
    target_return = '/Users/tyrion'
    with patch('os.path.expanduser', return_value=target_return) as mocked:
        result = eg_util.get_path_to_rc_file()
        assert result == target_return
        mocked.assert_called_once_with(passed_in_value)
