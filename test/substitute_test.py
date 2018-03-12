import re

from eg import substitute
from mock import patch
from nose.tools import assert_equal
from nose.tools import assert_true


def test_equality():
    """== should work on Substitution objects."""
    alpha = substitute.Substitution('foo', 'bar', False)
    beta = substitute.Substitution('foo', 'bar', False)
    assert_true(alpha == beta)


def test_not_equal():
    """!= should work on Substitution objects."""
    alpha = substitute.Substitution('foo', 'bar', True)
    beta = substitute.Substitution('foo', 'bar', False)
    assert_true(alpha != beta)


def test_applies_multiline_substitution():
    """Correctly applies a substitution that is multiline."""
    raw = 'foo\n\n\n    bar something\n\n\n  the end'
    subbed = 'foo\n    bar something\n  the end'
    pattern = '\n\n\n'
    replacement = '\n'
    sub = substitute.Substitution(pattern, replacement, True)

    actual = sub.apply_and_get_result(raw)
    assert_equal(actual, subbed)


def test_applies_normal_mode_substitution():
    """Correctly applies a substitution that is not multiline."""
    raw = 'foo\n\n\n    bar something\n\n\n    the end'
    subbed = 'foo\n\n\nbar something\n\n\nthe end'
    pattern = '    '
    replacement = ''
    sub = substitute.Substitution(pattern, replacement, False)

    actual = sub.apply_and_get_result(raw)
    assert_equal(actual, subbed)


def test_calls_correct_re_methods_for_multiline():
    """
    Rather than test re functionality, make sure that we call the appropriate
    methods themselves on the re library when we use multiline.
    """
    _helper_assert_about_apply_and_get_result(True)


def test_calls_correct_re_methods_without_multiline():
    """
    Rather than test re functionality, make sure that we call the appropriate
    methods themselves on the re library when we don't use multiline.
    """
    _helper_assert_about_apply_and_get_result(False)


@patch('re.sub')
@patch('re.compile')
def _helper_assert_about_apply_and_get_result(
    is_multiline,
    compile_method,
    sub_method
):
    """
    Helper method to assert about the correct results of calls to
    apply_and_get_result to ensure the correct methods are called.
    """
    pattern = 'pattern whoopty'
    repl = 'replacement whoopty'
    compiled_pattern = 'whoopty compiled'
    subbed_result = 'substituted'
    starting_string = 'the start'

    compile_method.return_value = compiled_pattern
    sub_method.return_value = subbed_result

    if is_multiline:
        sub = substitute.Substitution(pattern, repl, True)
    else:
        sub = substitute.Substitution(pattern, repl, False)
    actual = sub.apply_and_get_result(starting_string)

    if is_multiline:
        compile_method.assert_called_once_with(pattern, re.MULTILINE)
    else:
        compile_method.assert_called_once_with(pattern)

    sub_method.assert_called_once_with(
        compiled_pattern,
        repl,
        starting_string
    )
    assert_equal(actual, subbed_result)
