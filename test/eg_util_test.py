from mock import patch
from eg import eg_util


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


def test_has_entry_for_program_finds_file():
    assert True is False


def test_does_not_have_entry_for_file():
    assert True is False


def test_get_line_number_of_subsection_returns_no_examples():
    assert True is False


def test_get_line_number_of_subsection_returns_no_subsection():
    assert True is False


def test_get_line_number_of_subsection_finds_correct_line():
    assert True is False


def open_pager_to_line_number_invokes_correctly_for_less():
    assert True is False
