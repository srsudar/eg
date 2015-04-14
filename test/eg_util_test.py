import os
import subprocess

from eg import eg_config
from eg import eg_util
from mock import Mock
from mock import patch
from nose.tools import assert_equal


def test_get_file_path_for_program_correct():
    program = 'cp'
    examples_dir = '/Users/tyrion/test/eg_dir'
    program_file = program + eg_util.EXAMPLE_FILE_SUFFIX
    target = os.path.join(examples_dir, program_file)

    actual = eg_util.get_file_path_for_program(program, examples_dir)

    assert_equal(actual, target)


def test_has_default_entry_for_program_no_examples_dir():
    config = eg_config.Config(
        examples_dir=None,
        custom_dir='customdir',
        color_config=None,
        use_color=False
    )

    program = 'cp'

    has_entry = eg_util.has_default_entry_for_program(program, config)

    assert_equal(False, has_entry)


def test_has_custom_entry_for_program_no_custom_dir():
    config = eg_config.Config(
        examples_dir='examplesdir',
        custom_dir=None,
        color_config=None,
        use_color=False
    )

    program = 'find'

    has_entry = eg_util.has_custom_entry_for_program(program, config)

    assert_equal(False, has_entry)


def test_has_default_entry_when_present():
    config = eg_config.Config(
        examples_dir='examplesdir',
        custom_dir=None,
        color_config=None,
        use_color=False,
    )
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
    config = eg_config.Config(
        examples_dir='examplesdir',
        custom_dir=None,
        color_config=None,
        use_color=False
    )
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
    config = eg_config.Config(
        examples_dir=None,
        custom_dir='customdir',
        color_config=None,
        use_color=False
    )
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
    config = eg_config.Config(
        examples_dir=None,
        custom_dir='customdir',
        color_config=None,
        use_color=False
    )

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
        has_entry
):
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


def _helper_assert_open_pager_for_file(
    default_file_path,
    default_file_contents,
    custom_file_path,
    custom_file_contents,
    use_color,
    color_config,
    combined_contents,
    colorized_contents,
    paged_contents
):
    """
    Helper method for testing open_pager_for_file method.
    """
    # Make sure the caller is using this method correctly.
    valid_paged_contents = [colorized_contents, combined_contents]
    if paged_contents not in valid_paged_contents:
        print 'paged_contents must be either combined or colorized _contents'
        assert_equal(True, False)

    def return_file_contents(*args, **kwargs):
        if args[0] == default_file_path:
            return default_file_contents
        elif args[0] == custom_file_path:
            return custom_file_contents
        else:
            raise TypeError(
                args[0] +
                ' was an unexpected path--should be ' +
                default_file_path +
                ' or ' +
                custom_file_path
            )

    with patch(
        'eg.eg_util._get_contents_of_file',
        side_effect=return_file_contents
    ):
        with patch(
            'eg.eg_colorizer.EgColorizer',
        ) as patched_colorizer_class:
            # The actual instance created by these calls is stored at
            # return_value
            colorizer_instance = patched_colorizer_class.return_value
            colorizer_instance.colorize_text.return_value = colorized_contents
            with patch('pydoc.pager') as patched_pager:
                # Make the call then assert things happened as we expected.
                eg_util.open_pager_for_file(
                    default_file_path,
                    custom_file_path,
                    use_color,
                    color_config
                )

                if use_color:
                    # Make sure we created the colorizer with the correct config
                    # and that we called colorizing method correctly.
                    colorizer_instance.colorize_text.assert_called_once_with(
                        combined_contents
                    )
                else:
                    colorizer_instance.colorize_text.assert_no_calls()

                patched_pager.assert_called_once_with(paged_contents)


def test_handle_program_no_entries():
    program = 'cp'
    config = eg_config.Config(
        examples_dir=None,
        custom_dir=None,
        color_config=None,
        use_color=False
    )

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

    examples_dir = 'test-eg-dir'
    custom_dir = 'test-custom-dir'
    color_config = None
    use_color = False

    config = eg_config.Config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        color_config=color_config,
        use_color=use_color
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
                        custom_dir,
                    )

                    mock_open_pager.assert_called_once_with(
                        default_file_path=default_path,
                        custom_file_path=custom_path,
                        use_color=use_color,
                        color_config=color_config
                    )


def test_open_pager_for_file_only_default():
    default_path = 'test/default/path'
    default_contents = 'contents of the default file'
    combined_contents = default_contents
    colorized_contents = 'COLOR: ' + combined_contents

    _helper_assert_open_pager_for_file(
        default_path,
        default_contents,
        None,
        None,
        False,
        None,
        combined_contents,
        colorized_contents,
        combined_contents
    )


def test_open_pager_for_file_only_custom():
    custom_path = 'test/custom/path'
    custom_contents = 'contents of the custom file'
    combined_contents = custom_contents
    colored_contents = 'COLOR: ' + combined_contents

    _helper_assert_open_pager_for_file(
        None,
        None,
        custom_path,
        custom_contents,
        False,
        None,
        combined_contents,
        colored_contents,
        combined_contents
    )


def test_open_pager_for_both_file_types():
    default_path = 'test/default/path'
    default_contents = 'contents of the default file'
    custom_path = 'test/custom/path'
    custom_contents = 'contents of the custom file'
    combined_contents = custom_contents + default_contents
    colorized_contents = 'COLORIZED: ' + combined_contents

    _helper_assert_open_pager_for_file(
        default_path,
        default_contents,
        custom_path,
        custom_contents,
        True,
        None,
        combined_contents,
        colorized_contents,
        colorized_contents
    )


def test_list_supported_programs_only_default():
    example_dir = 'example/dir'
    custom_dir = 'custom/dir'

    config = eg_config.Config(
        examples_dir=example_dir,
        custom_dir=custom_dir,
        color_config=None,
        use_color=False
    )

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

    config = eg_config.Config(
        examples_dir=example_dir,
        custom_dir=custom_dir,
        color_config=None,
        use_color=False
    )

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

    config = eg_config.Config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        color_config=None,
        use_color=False
    )

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
    config = eg_config.Config(None, None, None, None)

    actual = eg_util.get_list_of_all_supported_commands(config)
    target = []

    assert_equal(actual, target)


def test_calls_colorize_is_use_color_set():
    """We should call the colorize function if use_color = True."""
    default_file = 'def_path'
    default_contents = 'def contents'
    custom_path = 'custom_path',
    custom_contents = 'custom contents'
    combined_contents = custom_contents + default_contents
    colorized_contents = 'colorized: ' + combined_contents

    _helper_assert_open_pager_for_file(
        default_file,
        default_contents,
        custom_path,
        custom_contents,
        True,
        eg_config.get_default_color_config(),
        combined_contents,
        colorized_contents,
        colorized_contents
    )


def test_does_not_call_colorize_if_use_color_false():
    """We should not call colorize if use_color = False."""
    default_file = 'def_path'
    default_contents = 'def contents'
    custom_path = 'custom_path',
    custom_contents = 'custom contents'
    combined_contents = custom_contents + default_contents
    colorized_contents = 'colorized: ' + combined_contents

    _helper_assert_open_pager_for_file(
        default_file,
        default_contents,
        custom_path,
        custom_contents,
        False,
        eg_config.get_default_color_config(),
        combined_contents,
        colorized_contents,
        combined_contents
    )
