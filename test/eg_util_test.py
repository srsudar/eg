from eg import eg_util
from mock import patch


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


def test_get_file_path_for_program_valid():
    actual = eg_util.get_file_path_for_program('find')
    target = 'examples/find.txt'
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
    path = 'examples/' + program + '.txt'
    with patch('eg.eg_util.get_file_path_for_program', return_value=path):
        with patch('os.path.isfile', return_value=should_find) as mock_method:
            actual = eg_util.has_entry_for_program(program)
            if should_find:
                assert actual
            else:
                assert not actual
            mock_method.assert_called_once_with(path)


def test_get_line_number_of_subsection_returns_no_examples():
    assert True is False


def test_get_line_number_of_subsection_returns_no_subsection():
    assert True is False


def test_get_line_number_of_subsection_finds_correct_line():
    assert True is False


def open_pager_to_line_number_invokes_correctly_for_less():
    assert True is False
