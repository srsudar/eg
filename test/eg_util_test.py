import os
import subprocess

from eg import eg_util
from mock import Mock
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
            'eg.eg_util.get_config_tuple_from_egrc',
            return_value=egrc_config
        ):
            actual = eg_util.get_resolved_config_items(
                None,
                examples_dir,
                custom_dir
            )
            assert_equal(actual.examples_dir, examples_dir)
            assert_equal(actual.custom_dir, custom_dir)


def test_get_config_tuple_from_egrc_all_none_when_not_present():
    actual = eg_util.get_config_tuple_from_egrc('test/assets/egrc_nodata')
    target = eg_util.Config(examples_dir=None, custom_dir=None)
    assert_equal(actual, target)


def test_get_config_tuple_from_egrc_when_present():
    # These are the values hardcoded into the files.
    examples_dir = 'test/example/dir/in/egrc_withdata'
    custom_dir = 'test/custom/dir/in/egrc_withdata'

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
        'eg.eg_util.get_expanded_path',
        side_effect=return_expanded_path
    ) as mock_expand:

        actual = eg_util.get_config_tuple_from_egrc('test/assets/egrc_withdata')

        target = eg_util.Config(
            examples_dir=examples_dir,
            custom_dir=custom_dir
        )
        assert_equal(actual, target)

        mock_expand.assert_any_call(examples_dir)
        mock_expand.assert_any_call(custom_dir)


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
        assert_equal(eg_util.get_pager(), eg_util.DEFAULT_PAGER)


def test_get_file_path_for_program_correct():
    program = 'cp'
    examples_dir = '/Users/tyrion/test/eg_dir'
    program_file = program + eg_util.EXAMPLE_FILE_SUFFIX
    target = os.path.join(examples_dir, program_file)

    actual = eg_util.get_file_path_for_program(program, examples_dir)

    assert_equal(actual, target)


def test_has_default_entry_for_program_no_examples_dir():
    config = eg_util.Config(examples_dir=None, custom_dir='customdir')
    program = 'cp'

    has_entry = eg_util.has_default_entry_for_program(program, config)

    assert_equal(False, has_entry)


def test_has_custom_entry_for_program_no_custom_dir():
    config = eg_util.Config(examples_dir='examplesdir', custom_dir=None)
    program = 'find'

    has_entry = eg_util.has_custom_entry_for_program(program, config)

    assert_equal(False, has_entry)


def test_has_default_entry_when_present():
    config = eg_util.Config(examples_dir='examplesdir', custom_dir=None)
    program = 'mv'

    path = '/Users/tyrion/examplesdir/mv.md'

    _helper_assert_path_isfile_not_present(
        config,
        program,
        path,
        'default',
        True,
        True
    )


def test_has_default_entry_when_not_present():
    config = eg_util.Config(examples_dir='examplesdir', custom_dir=None)
    program = 'cp'

    path = '/Users/tyrion/examplesdir/cp.md'

    _helper_assert_path_isfile_not_present(
        config,
        program,
        path,
        'default',
        False,
        False,
    )


def test_has_custom_entry_when_present():
    config = eg_util.Config(examples_dir=None, custom_dir='customdir')
    program = 'find'

    path = '/Users/tyrion/customdir/find.md'

    _helper_assert_path_isfile_not_present(
        config,
        program,
        path,
        'custom',
        True,
        True
    )


def test_has_custom_entry_when_not_present():
    config = eg_util.Config(examples_dir=None, custom_dir='customdir')
    program = 'locate'

    path = '/Users/tyrion/customdir/locate.md'

    _helper_assert_path_isfile_not_present(
        config,
        program,
        path,
        'custom',
        False,
        False,
    )


def _helper_assert_path_isfile_not_present(
        config,
        program,
        file_path_for_program,
        defaultOrCustom,
        isfile,
        has_entry):
    """
    Helper for asserting whether or not a default file is present. Pass in the
    parameters defining the program and directories and say whether or not that
    file should be found.
    """
    if defaultOrCustom != 'default' and defaultOrCustom != 'custom':
        raise TypeError(
            'defaultOrCustom must be default or custom, not ' + defaultOrCustom
        )
    with patch(
        'eg.eg_util.get_file_path_for_program',
        return_value=file_path_for_program
    ) as mock_get_path:
        with patch('os.path.isfile', return_value=isfile) as mock_isfile:

            actual = None
            correct_dir = None

            if (defaultOrCustom == 'default'):
                correct_dir = config.examples_dir
                actual = eg_util.has_default_entry_for_program(program, config)
            else:
                correct_dir = config.custom_dir
                actual = eg_util.has_custom_entry_for_program(program, config)

            mock_get_path.assert_called_once_with(program, correct_dir)
            mock_isfile.assert_called_once_with(file_path_for_program)

            assert_equal(actual, has_entry)


def test_handle_program_no_entries():
    program = 'cp'
    config = eg_util.Config(examples_dir=None, custom_dir=None)

    with patch(
        'eg.eg_util.has_default_entry_for_program',
        return_value=False
    ) as mock_has_default:
        with patch(
            'eg.eg_util.has_custom_entry_for_program',
            return_value=False
        ) as mock_has_custom:
            with patch(
                'eg.eg_util.open_pager_for_file'
            ) as mock_open_pager:
                eg_util.handle_program(program, config)

                mock_has_default.assert_called_once_with(program, config)
                mock_has_custom.assert_called_once_with(program, config)

                assert_equal(mock_open_pager.call_count, 0)


def test_handle_program_finds_paths_and_calls_open_pager():
    program = 'mv'
    pager = 'more'

    examples_dir = 'test-eg-dir'
    custom_dir = 'test-custom-dir'

    config = eg_util.Config(
        examples_dir=examples_dir,
        custom_dir=custom_dir
    )

    default_path = 'test-eg-dir/mv.md'
    custom_path = 'test-custom-dir/mv.md'

    def return_correct_path(*args, **kwargs):
        program_param = args[0]
        dir_param = args[1]
        if program_param != program:
            raise NameError('expected ' + program + ', got ' + program_param)
        if dir_param == examples_dir:
            return default_path
        elif dir_param == custom_dir:
            return custom_path
        else:
            raise NameError(
                'got ' +
                dir_param +
                ', expected ' +
                examples_dir +
                ' or ' +
                custom_dir)

    with patch(
        'eg.eg_util.has_default_entry_for_program',
        return_value=True
    ) as mock_has_default:
        with patch(
            'eg.eg_util.has_custom_entry_for_program',
            return_value=True
        ) as mock_has_custom:
            with patch(
                'eg.eg_util.open_pager_for_file'
            ) as mock_open_pager:
                with patch(
                    'eg.eg_util.get_file_path_for_program',
                    side_effect=return_correct_path
                ) as mock_get_file:
                    with patch('eg.eg_util.get_pager', return_value=pager):
                        eg_util.handle_program(program, config)

                        mock_has_default.assert_called_once_with(
                            program,
                            config
                        )
                        mock_has_custom.assert_called_once_with(
                            program,
                            config
                        )

                        mock_get_file.assert_any_call(
                            program,
                            examples_dir
                        )
                        mock_get_file.assert_any_call(
                            program,
                            custom_dir
                        )

                        mock_open_pager.assert_called_once_with(
                            pager,
                            default_file_path=default_path,
                            custom_file_path=custom_path
                        )


def test_open_pager_for_file_only_default():
    pager = 'more'
    default_path = 'test/default/path'
    with patch('subprocess.call') as mock_call:
        eg_util.open_pager_for_file(pager, default_path, None)

        mock_call.assert_called_once_with([pager, default_path])


def test_open_pager_for_file_only_custom():
    pager = 'more'
    custom_path = 'test/custom/path'
    with patch('subprocess.call') as mock_call:
        eg_util.open_pager_for_file(pager, None, custom_path)

        mock_call.assert_called_once_with([pager, custom_path])


def test_open_pager_for_both_file_types():
    # This is kind of a messy function, as we do a lot of messing around with
    # subprocess.Popen. We're not going to test that absolutely everything is
    # plugged in correctly, just that things are more or less right
    pager = 'less'
    default_path = 'test/default/path'
    custom_path = 'test/custom/path'
    cat = Mock(autospec=True)
    with patch('subprocess.Popen', return_value=cat) as mock_popen:
        with patch('subprocess.call') as mock_call:
            eg_util.open_pager_for_file(pager, default_path, custom_path)

            mock_popen.assert_called_once_with(
                ('cat', custom_path, default_path),
                stdout=subprocess.PIPE
            )

            mock_call.assert_called_once_with((pager), stdin=cat.stdout)


def test_list_supported_programs_only_default():
    example_dir = 'example/dir'
    custom_dir = 'custom/dir'

    config = eg_util.Config(examples_dir=example_dir, custom_dir=custom_dir)

    def give_list(*args, **kwargs):
        if args[0] == example_dir:
            return ['cp.md', 'find.md', 'xargs.md']
        else:
            return []

    with patch('os.path.isdir', return_value=True):
        with patch('os.listdir', side_effect=give_list):
            actual = eg_util.get_list_of_all_supported_commands(config)
            target = ['cp', 'find', 'xargs']

            assert_equal(actual, target)


def test_list_supported_programs_only_custom():
    example_dir = 'example/dir'
    custom_dir = 'custom/dir'

    config = eg_util.Config(examples_dir=example_dir, custom_dir=custom_dir)

    def give_list(*args, **kwargs):
        if args[0] == custom_dir:
            return ['awk.md', 'bar.md', 'xor.md']
        else:
            return []

    with patch('os.path.isdir', return_value=True):
        with patch('os.listdir', side_effect=give_list):
            actual = eg_util.get_list_of_all_supported_commands(config)
            target = ['awk +', 'bar +', 'xor +']

            assert_equal(actual, target)


def test_list_supported_programs_both():
    examples_dir = 'example/dir'
    custom_dir = 'custom/dir'

    config = eg_util.Config(examples_dir=examples_dir, custom_dir=custom_dir)

    def give_list(*args, **kwargs):
        if args[0] == examples_dir:
            return ['alpha', 'bar.md', 'both.md', 'examples']
        else:
            # custom_dir
            return ['azy.md', 'both.md', 'examples', 'zeta']

    with patch('os.path.isdir', return_value=True):
        with patch('os.listdir', side_effect=give_list):
            actual = eg_util.get_list_of_all_supported_commands(config)

            target = [
                'alpha',
                'azy +',
                'bar',
                'both *',
                'examples *',
                'zeta +'
            ]

            assert_equal(actual, target)


def test_list_supported_programs_fails_gracefully_if_no_dirs():
    config = eg_util.Config(None, None)

    actual = eg_util.get_list_of_all_supported_commands(config)
    target = []

    assert_equal(actual, target)
