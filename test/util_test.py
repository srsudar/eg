import json
import os
import pytest

from eg import config
from eg import substitute
from eg import util
from mock import Mock
from mock import patch

PATH_UNSQUEEZED_FILE = os.path.join(
    'test',
    'assets',
    'pwd_unsqueezed.md'
)
PATH_SQUEEZED_FILE = os.path.join(
    'test',
    'assets',
    'pwd_squeezed.md'
)


def _create_config(
    examples_dir=None,
    custom_dir=None,
    color_config=None,
    use_color=True,
    pager_cmd=None,
    editor_cmd=None,
    squeeze=False,
    subs=None
):
    """
    Create a config.Config object with default values for expediency in
    testing.
    """
    return config.Config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        color_config=color_config,
        use_color=use_color,
        pager_cmd=pager_cmd,
        editor_cmd=editor_cmd,
        squeeze=squeeze,
        subs=subs
    )


@patch('os.walk')
def test_get_file_paths_for_program_with_single(mock_walk):
    program = 'cp'
    examples_dir = '/Users/tyrion'
    program_file = program + util.EXAMPLE_FILE_SUFFIX
    expected = ['/Users/tyrion/cp.md']

    mock_walk.return_value = [
        [examples_dir, [], [program_file, 'cp.txt', 'other_file.md']],
    ]

    actual = util.get_file_paths_for_program(program, examples_dir)
    assert actual == expected
    mock_walk.assert_called_once_with(examples_dir)


@patch('os.walk')
def test_get_file_paths_for_program_with_nested(mock_walk):
    program = 'cp'
    examples_dir = '/Users/tyrion'
    program_file = 'cp.md'

    mock_walk.return_value = [
        [
            examples_dir,
            ['dirA', 'dirB'],
            [program_file, 'cp.txt', 'other_file.md'],
        ],
        [
            examples_dir + '/dirA',
            ['dirA-child'],
            [program_file, 'bad.md'],
        ],
        [
            examples_dir + '/dirA/dirA-child',
            [],
            ['bad.md', program_file, 'wtf.md'],
        ],
        [
            examples_dir + '/dirB',
            [],
            ['foo.md', program_file],
        ],
    ]

    expected = [
        '/Users/tyrion/cp.md',
        '/Users/tyrion/dirA/cp.md',
        '/Users/tyrion/dirA/dirA-child/cp.md',
        '/Users/tyrion/dirB/cp.md',
    ]

    actual = util.get_file_paths_for_program(program, examples_dir)
    assert actual == expected
    mock_walk.assert_called_once_with(examples_dir)


@patch('os.walk')
def test_get_file_paths_for_program_with_none(mock_walk):
    expected = []
    mock_walk.return_value = []

    actual = util.get_file_paths_for_program('cp', '/Users/tyrion')
    assert actual == expected
    mock_walk.assert_called_once_with('/Users/tyrion')


@patch('os.walk')
def test_get_file_paths_for_program_throws_if_missing_dir(mock_walk):
    with pytest.raises(TypeError):
        util.get_file_paths_for_program('cp')


def test_has_default_entry_for_program_no_examples_dir():
    test_config = _create_config(
        examples_dir=None,
        custom_dir='customdir',
    )

    program = 'cp'

    has_entry = util.has_default_entry_for_program(program, test_config)
    assert has_entry == False


def test_has_custom_entry_for_program_no_custom_dir():
    test_config = _create_config(
        examples_dir='examplesdir',
        custom_dir=None,
    )

    program = 'find'

    has_entry = util.has_custom_entry_for_program(program, test_config)
    assert has_entry == False


def test_has_default_entry_when_present():
    test_config = _create_config(
        examples_dir='examplesdir',
    )
    program = 'mv'

    path = '/Users/tyrion/examplesdir/mv.md'

    _helper_assert_path_isfile_not_present(
        test_config,
        program,
        path,
        'default',
        True,
        True
    )


def test_has_default_entry_when_not_present():
    test_config = _create_config(
        examples_dir='examplesdir',
    )
    program = 'cp'

    path = '/Users/tyrion/examplesdir/cp.md'

    _helper_assert_path_isfile_not_present(
        test_config,
        program,
        path,
        'default',
        False,
        False,
    )


def test_has_custom_entry_when_present():
    test_config = _create_config(
        examples_dir=None,
        custom_dir='customdir',
        color_config=None,
        use_color=False,
        pager_cmd=None,
        squeeze=False,
        subs=None
    )
    program = 'find'

    path = '/Users/tyrion/customdir/find.md'

    _helper_assert_path_isfile_not_present(
        test_config,
        program,
        path,
        'custom',
        True,
        True
    )


def test_has_custom_entry_when_not_present():
    test_config = _create_config(
        custom_dir='customdir',
        color_config=None,
        use_color=False,
        pager_cmd=None,
        squeeze=False,
        subs=None
    )

    program = 'locate'

    path = '/Users/tyrion/customdir/locate.md'

    _helper_assert_path_isfile_not_present(
        test_config,
        program,
        path,
        'custom',
        False,
        False,
    )


@patch('eg.util.get_file_paths_for_program')
def _helper_assert_path_isfile_not_present(
    config,
    program,
    file_path_for_program,
    defaultOrCustom,
    is_file,
    has_entry,
    mock_get_paths,
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

    if is_file:
        mock_get_paths.return_value = [file_path_for_program]
    else:
        mock_get_paths.return_value = []

    actual = None
    correct_dir = None

    if (defaultOrCustom == 'default'):
        correct_dir = config.examples_dir
        actual = util.has_default_entry_for_program(program, config)
    else:
        correct_dir = config.custom_dir
        actual = util.has_custom_entry_for_program(program, config)

    mock_get_paths.assert_called_once_with(program, correct_dir)

    assert actual == has_entry


@patch('eg.util.page_string')
@patch('eg.util.get_formatted_contents')
@patch('eg.util.get_contents_from_files')
@patch('eg.util.has_custom_entry_for_program')
@patch('eg.util.has_default_entry_for_program')
@patch('eg.util.get_resolved_program')
def test_handle_program_no_entries(
    mock_resolve_program,
    mock_has_default,
    mock_has_custom,
    mock_get_contents,
    mock_format,
    mock_page_string,
):
    """
    We should do the right thing if there are no entries for a given program.
    """
    program = 'cp'
    test_config = _create_config()

    mock_resolve_program.return_value = program
    mock_has_default.return_value = False
    mock_has_custom.return_value = False

    util.handle_program(program, test_config)

    mock_resolve_program.assert_called_once_with(
        program,
        test_config
    )

    mock_has_default.assert_called_once_with(
        program,
        test_config
    )

    mock_has_custom.assert_called_once_with(
        program,
        test_config
    )

    # We should have aborted and not called any of the
    # other methods.
    assert mock_get_contents.call_count == 0
    assert mock_format.call_count == 0
    assert mock_page_string.call_count == 0


@patch('eg.util.get_resolved_program')
@patch('eg.util.has_default_entry_for_program', return_value=True)
@patch('eg.util.has_custom_entry_for_program', return_value=True)
@patch('eg.util.get_contents_from_files')
@patch('eg.util.get_file_paths_for_program')
@patch('eg.util.get_formatted_contents')
@patch('eg.util.page_string')
def test_handle_program_finds_paths_and_calls_open_pager_no_alias(
    mock_page,
    mock_format,
    mock_get_paths,
    mock_get_contents,
    mock_has_custom,
    mock_has_default,
    mock_resolve,
):
    """
    If there are entries for the program, handle_program needs to get the
    paths, get the contents, format the contents, and page the resulting
    string.
    """
    program = 'mv'

    examples_dir = 'test-eg-dir'
    custom_dir = 'test-custom-dir'
    color_config = None
    use_color = False
    pager_cmd = 'foo bar'
    squeeze = False
    subs = ['foo', 'bar']

    file_contents = 'I am the contents of mv.md.'
    formatted_contents = 'and I am the formatted contents of mv.md.'

    test_config = _create_config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        color_config=color_config,
        use_color=use_color,
        pager_cmd=pager_cmd,
        squeeze=squeeze,
        subs=subs
    )

    default_paths = ['test-eg-dir/mv.md']
    custom_paths = ['test-custom-dir/mv.md']

    def return_correct_path(*args, **kwargs):
        program_param = args[0]
        dir_param = args[1]
        if program_param != program:
            raise NameError('expected ' + program + ', got ' + program_param)
        if dir_param == examples_dir:
            return default_paths
        elif dir_param == custom_dir:
            return custom_paths
        else:
            raise NameError(
                'got ' +
                dir_param +
                ', expected ' +
                examples_dir +
                ' or ' +
                custom_dir)

    mock_format.return_value = formatted_contents
    mock_get_paths.side_effect=return_correct_path
    mock_get_contents.return_value = file_contents
    mock_resolve.return_value = program

    util.handle_program(program, test_config)

    mock_resolve.assert_called_once_with(
        program,
        test_config
    )

    mock_has_default.assert_called_once_with(
        program,
        test_config
    )
    mock_has_custom.assert_called_once_with(
        program,
        test_config
    )

    mock_get_paths.assert_any_call(
        program,
        examples_dir
    )
    mock_get_paths.assert_any_call(
        program,
        custom_dir,
    )

    mock_get_contents.assert_called_once_with(
        default_paths,
        custom_paths
    )

    mock_format.assert_called_once_with(
        file_contents,
        use_color=test_config.use_color,
        color_config=test_config.color_config,
        squeeze=test_config.squeeze,
        subs=test_config.subs
    )

    mock_page.assert_called_once_with(
        formatted_contents,
        test_config.pager_cmd
    )


@patch('eg.util.get_resolved_program')
@patch('eg.util.has_default_entry_for_program', return_value=True)
@patch('eg.util.has_custom_entry_for_program', return_value=True)
@patch('eg.util.get_contents_from_files')
@patch('eg.util.get_file_paths_for_program')
@patch('eg.util.get_formatted_contents')
@patch('eg.util.page_string')
def test_handle_program_finds_paths_and_calls_open_pager_with_alias(
    mock_page,
    mock_format,
    mock_get_paths,
    mock_get_contents,
    mock_has_custom,
    mock_has_default,
    mock_resolve,
):
    """
    If there are entries for the program, handle_program needs to get the
    paths, get the contents, format the contents, and page the resulting
    string.
    """
    alias_for_program = 'link'
    resolved_program = 'ln'

    examples_dir = 'test-eg-dir'
    custom_dir = 'test-custom-dir'
    color_config = None
    use_color = False
    pager_cmd = 'foo bar'
    squeeze = False
    subs = ['foo', 'bar']

    file_contents = 'I am the contents of ln.md.'
    formatted_contents = 'and I am the formatted contents of ln.md.'

    test_config = _create_config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
        color_config=color_config,
        use_color=use_color,
        pager_cmd=pager_cmd,
        squeeze=squeeze,
        subs=subs
    )

    default_paths = ['test-eg-dir/ln.md']
    custom_paths = ['test-custom-dir/ln.md']

    def return_correct_path(*args, **kwargs):
        program_param = args[0]
        dir_param = args[1]
        if program_param != resolved_program:
            raise NameError(
                'expected ' +
                resolved_program +
                ', got ' +
                program_param
            )
        if dir_param == examples_dir:
            return default_paths
        elif dir_param == custom_dir:
            return custom_paths
        else:
            raise NameError(
                'got ' +
                dir_param +
                ', expected ' +
                examples_dir +
                ' or ' +
                custom_dir)

    mock_format.return_value = formatted_contents
    mock_get_paths.side_effect = return_correct_path
    mock_get_contents.return_value = file_contents
    mock_resolve.return_value = resolved_program

    util.handle_program(
        alias_for_program,
        test_config
    )

    mock_resolve.assert_called_once_with(
        alias_for_program,
        test_config
    )

    mock_has_default.assert_called_once_with(
        resolved_program,
        test_config
    )
    mock_has_custom.assert_called_once_with(
        resolved_program,
        test_config
    )

    mock_get_paths.assert_any_call(
        resolved_program,
        examples_dir
    )
    mock_get_paths.assert_any_call(
        resolved_program,
        custom_dir,
    )

    mock_get_contents.assert_called_once_with(
        default_paths,
        custom_paths
    )

    mock_format.assert_called_once_with(
        file_contents,
        use_color=test_config.use_color,
        color_config=test_config.color_config,
        squeeze=test_config.squeeze,
        subs=test_config.subs
    )

    mock_page.assert_called_once_with(
        formatted_contents,
        test_config.pager_cmd
    )


@patch('os.path.isdir', return_value=True)
@patch('os.listdir')
@patch('eg.util.get_alias_dict')
def _helper_assert_list_supported_programs(
    config_obj,
    default_list,
    custom_list,
    alias_dict,
    target_list,
    get_dict_mock,
    listdir_mock,
    isdir_mock,
):
    """
    config_obj: Config object to be passed to get_list function
    default_list: the list of default programs
    custom_list: the list of programs with custom programs
    alias_dict: dict of aliases
    target_list: list of string that should be returned
    """
    def give_list(*args, **kwargs):
        dir_name = args[0]
        if dir_name == config_obj.custom_dir:
            return custom_list
        elif dir_name == config_obj.examples_dir:
            return default_list
        else:
            raise NameError('Not the default or custom dir: ' + dir_name)

    get_dict_mock.return_value = alias_dict
    listdir_mock.side_effect = give_list

    actual = util.get_list_of_all_supported_commands(config_obj)
    assert actual == target_list


def test_list_supported_programs_only_default():
    example_dir = 'example/dir'
    custom_dir = 'custom/dir'

    test_config = _create_config(
        examples_dir=example_dir,
        custom_dir=custom_dir,
    )

    examples_list = ['aliases', 'cp.md', 'find.md', 'xargs.md']
    custom_list = []
    target = ['cp', 'find', 'xargs']
    _helper_assert_list_supported_programs(
        test_config,
        examples_list,
        custom_list,
        {},
        target
    )


def test_list_supported_programs_only_custom():
    example_dir = 'example/dir'
    custom_dir = 'custom/dir'

    test_config = _create_config(
        examples_dir=example_dir,
        custom_dir=custom_dir,
    )
    target = ['awk +', 'bar +', 'xor +']
    _helper_assert_list_supported_programs(
        test_config,
        [],
        ['awk.md', 'bar.md', 'xor.md'],
        {},
        target
    )


def test_list_supported_programs_both():
    examples_dir = 'example/dir'
    custom_dir = 'custom/dir'

    test_config = _create_config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
    )
    examples_list = ['alpha.md', 'bar.md', 'both.md', 'examples.md']
    custom_list = ['azy.md', 'both.md', 'examples.md', 'zeta.md']
    target = [
        'alpha',
        'azy +',
        'bar',
        'both *',
        'examples *',
        'zeta +'
    ]
    _helper_assert_list_supported_programs(
        test_config,
        examples_list,
        custom_list,
        {},
        target
    )


def test_list_supported_commands_includes_aliases():
    examples_dir = 'examples/dir/for/aliases'
    custom_dir = 'custom/dir/for/aliases'

    test_config = _create_config(
        examples_dir=examples_dir,
        custom_dir=custom_dir,
    )
    # Things we want to cover:
    #   normal alias
    #   alias that shadows a custom-only declaration
    #   alias that points to a * or + program

    examples_list = [
        'alpha.md',
        'bar.md',
        'both.md',
        'default-only.md',
        'examples.md',
        'z-hidden-by-alias.md'
    ]
    custom_list = [
        'aaa.md',
        'azy.md',
        'both.md',
        'examples.md',
        'zeta.md'
    ]
    alias_dict = {
        'aaa': 'alpha',
        'y-alias-for-both': 'both',
        'alias-for-azy': 'azy',
        'z-hidden-by-alias': 'azy'
    }

    target = [
        'aaa -> alpha',  # shadow the custom file
        'alias-for-azy -> azy +',
        'alpha',
        'azy +',
        'bar',
        'both *',
        'default-only',
        'examples *',
        'y-alias-for-both -> both *',
        'z-hidden-by-alias -> azy +',
        'zeta +'
    ]
    _helper_assert_list_supported_programs(
        test_config,
        examples_list,
        custom_list,
        alias_dict,
        target
    )


def test_list_supported_programs_fails_gracefully_if_no_dirs():
    test_config = _create_config()

    actual = util.get_list_of_all_supported_commands(test_config)
    target = []

    assert actual == target


def test_calls_pipepager_if_not_less():
    """
    We're special casing less a bit, as it is the default value, so if a custom
    command has been set that is NOT less, we should call pipepager straight
    away.
    """
    _helper_assert_about_pager('page me plz', 'cat', False)


def test_calls_fallback_pager_if_none():
    """
    If pager_cmd is None, we should just use the fallback pager.
    """
    _helper_assert_about_pager('page me plz', None, True)


def test_calls_pipepager_if_less():
    """
    We should call pipepager if we ask to use less and less is installed on the
    machine.
    """
    _helper_assert_about_pager('a fancy value to page', 'less -R', False)


def test_calls_fallback_if_cmd_is_flag_string():
    """
    We are using a flag string to indicate if we should use the fallback pager.
    """
    _helper_assert_about_pager(
        'page via fallback',
        util.FLAG_FALLBACK,
        True
    )


@patch('pydoc.pager')
@patch('pydoc.pipepager')
def _helper_assert_about_pager(
    str_to_page,
    pager_cmd,
    use_fallback,
    pipepager,
    default_pager,
):
    """
    Help with asserting about pager.

    str_to_page: what you're paging
    pager_cmd: the string you're passing to pipepager (or None)
    use_default: false if we should actually use pydoc.pipepager, true if we
        instead are going to fallback to pydoc.pager
    """
    util.page_string(str_to_page, pager_cmd)

    if use_fallback:
        default_pager.assert_called_once_with(str_to_page)
        assert pipepager.call_count == 0
    else:
        assert default_pager.call_count == 0
        pipepager.assert_called_once_with(
            str_to_page,
            cmd=pager_cmd
        )


@patch('eg.util._get_contents_of_file')
def _helper_assert_file_contents(
    default_path,
    default_contents,
    custom_path,
    custom_contents,
    target_contents,
    get_contents_mock,
):
    """
    Helper method to assert things about the get_contents_from_files method.
    Does not actually hit the disk.

    default_path: the path of a default file
    default_contents: the contents of the default file
    custom_path: the path to a custom file
    custom_contents: the contents of the custom file
    target_contents: the final combined contents that should be returned by the
        get_contents_from_files method.
    """

    # This method will be used by the mock framework to return the right file
    # contents based on the file name.
    def return_file_contents(*args, **kwargs):
        if args[0] == default_path:
            return default_contents
        elif args[0] == custom_path:
            return custom_contents
        else:
            raise TypeError(
                args[0] +
                ' was an unexpected path--should be ' +
                default_path +
                ' or ' +
                custom_path
            )

    get_contents_mock.side_effect = return_file_contents

    actual = util.get_contents_from_files(default_path, custom_path)
    assert actual == target_contents


@patch('eg.util.pydoc.pipepager', side_effect=KeyboardInterrupt)
def test_page_string_excepts_keyboard_interrupt_if_not_less(pipepager_mock):
    """
    Do not fail when user hits ctrl-c while in pager.
    """
    try:
        util.page_string('page me plz', 'cat')
    except KeyboardInterrupt:
        raise AssertionError('Should not have got this far')
    pipepager_mock.assert_called_once_with('page me plz', cmd='cat')


@patch('eg.util.pydoc.pager', side_effect=KeyboardInterrupt)
def test_page_string_excepts_keyboard_interrupt_if_none(pager_mock):
    """
    Do not fail when user hits ctrl-c while in pipepager.
    """
    try:
        util.page_string('page me plz', None)
    except KeyboardInterrupt:
        raise AssertionError('Should not have got this far')
    pager_mock.assert_called_once_with('page me plz')


def test_get_contents_from_files_only_default():
    """
    Retrieve the correct file contents when only a default file is present.
    """
    default_path = 'test/default/path'
    default_contents = 'contents of the default file'
    _helper_assert_file_contents(
        default_path,
        default_contents,
        None,
        None,
        default_contents
    )


def test_get_contents_from_files_only_custom():
    """
    Retrieve only the custom file contents when we only have a custom file
    path.
    """
    custom_path = 'test/custom/path'
    custom_contents = 'contents of the custom file'
    _helper_assert_file_contents(
        None,
        None,
        custom_path,
        custom_contents,
        custom_contents
    )


def test_get_contents_from_file_both_default_and_custom():
    default_path = 'test/default/path'
    default_contents = 'contents of the default file'
    custom_path = 'test/custom/path'
    custom_contents = 'contents of the custom file'
    combined_contents = custom_contents + default_contents
    _helper_assert_file_contents(
        default_path,
        default_contents,
        custom_path,
        custom_contents,
        combined_contents
    )

@patch('eg.util.get_colorized_contents')
@patch('eg.util.get_squeezed_contents')
@patch('eg.util.get_substituted_contents')
def _helper_assert_formatted_contents(
    starting_contents,
    use_color,
    color_config,
    squeeze,
    subs,
    colorized_contents,
    squeezed_contents,
    subbed_contents,
    formatted_result,
    sub_method,
    squeeze_method,
    color_method,
):
    """
    Helper method to assist in asserting things about the
    get_formatted_contents method.

    starting_contents: the starting string that we are working with
    use_color: True if we should use color
    color_config: the color config to be passed to get_colorized_contents
    squeeze: True if we should squeeze
    subs: the list of Substitutions that we should pass to
        get_substituted_contents
    colored_contents: the result of get_colorized_contents
    squeezed_contents: the result of get_squeezed_contents
    subbed_contents: the result of subbed_contents
    formatted_result: the final, formatted string that should be returned
    """
    sub_method.return_value = subbed_contents
    squeeze_method.return_value = squeezed_contents
    color_method.return_value = colorized_contents

    actual = util.get_formatted_contents(
        starting_contents,
        use_color,
        color_config,
        squeeze,
        subs
    )

    # We'll update the contents as they get formatted to make sure
    # we pass the right thing to the various methods.
    contents_thus_far = starting_contents

    if use_color:
        color_method.assert_called_once_with(
            contents_thus_far,
            color_config
        )
        contents_thus_far = colorized_contents
    else:
        assert color_method.call_count == 0

    if squeeze:
        squeeze_method.assert_called_once_with(contents_thus_far)
        contents_thus_far = squeezed_contents
    else:
        assert squeeze_method.call_count == 0

    if subs:
        sub_method.assert_called_once_with(
            contents_thus_far,
            subs
        )
        contents_thus_far = subbed_contents
    else:
        assert sub_method.call_count == 0

    assert actual == formatted_result


def test_get_formatted_contents_does_not_format_methods_if_all_falsey():
    """
    We should invoke none of the formatter methods if the flags are false and
    subs is not truthy.
    """
    starting_contents = 'this is where we start'
    _helper_assert_formatted_contents(
        starting_contents,
        False,
        'some color config',
        False,
        None,
        'this was colored',
        'this was squeezed',
        'these contents were subbed',
        starting_contents
    )


def test_get_formatted_contents_calls_colorize_if_use_color():
    """
    Colorize the contents if use_color = True.
    """
    starting_contents = 'this is where we start'
    colorized_contents = 'COLORIZED: this is where we start'
    _helper_assert_formatted_contents(
        starting_contents,
        True,
        'some color config',
        False,
        None,
        colorized_contents,
        'this was squeezed',
        'these contents were subbed',
        colorized_contents
    )


def test_get_formatted_contents_squeezes():
    """If squeeze, we need to squeeze."""
    starting_contents = 'this is where we start'
    squeezed_contents = 'this is the result of a squeezing'
    _helper_assert_formatted_contents(
        starting_contents,
        False,
        'some color config',
        True,
        None,
        'this was colored',
        squeezed_contents,
        'these contents were subbed',
        squeezed_contents
    )


def test_get_formatted_contents_subsitutes():
    """If subs is truthy, get_substituted contents should be called."""
    starting_contents = 'this is where we start'
    subbed_contents = 'substituted like a teacher'
    _helper_assert_formatted_contents(
        starting_contents,
        False,
        'some color config',
        False,
        ['truthy', 'list'],
        'this was colored',
        'this was squeezed',
        subbed_contents,
        subbed_contents
    )


def test_perform_all_formatting():
    """
    When use_color, squeeze, and subs are all truthy, all the formatting
    should be applied in that order.
    """
    starting_contents = 'the starting point for grand formatting'
    subbed_contents = 'subbed is the last thing called so should be the result'
    _helper_assert_formatted_contents(
        starting_contents,
        True,
        'some color config',
        True,
        ['truthy', 'list'],
        'this was colored',
        'this was squeezed',
        subbed_contents,
        subbed_contents
    )


def _get_file_as_string(path):
    """Get the contents of the file as a string."""
    with open(path, 'r') as f:
        data = f.read()
    return data


def test_get_squeezed_contents_correctly_squeezes():
    """
    Our squeeze method should follow our convention, which is to remove the
    blank line between a description and an example, to keep two blank lines
    between sections, and otherwise have only single blank lines.
    """
    unsqueezed = _get_file_as_string(PATH_UNSQUEEZED_FILE)
    # the target squeezed output is a reference implementation in
    # pwd_squeezed.md.
    target = _get_file_as_string(PATH_SQUEEZED_FILE)
    actual = util.get_squeezed_contents(unsqueezed)

    assert actual == target


def test_get_substituted_contents_handles_empty_subs():
    """Nothing should be formatted if there are no substitutions."""
    raw_contents = 'this should not be subbed'
    actual = util.get_substituted_contents(raw_contents, [])
    assert actual == raw_contents


def test_get_substituted_contents_substitutes_calls_correct_methods():
    """
    The get_substituted_contents method calls things in the correct order.
    """
    sub_one = Mock(auto_spec=substitute.Substitution)
    sub_one_result = 'result of sub one'
    sub_one.apply_and_get_result.return_value = sub_one_result

    sub_two = Mock(auto_spec=substitute.Substitution)
    sub_two_result = 'result of sub two'
    sub_two.apply_and_get_result.return_value = sub_two_result

    starting_contents = 'the string we should be substituting into'
    target = sub_two_result
    subs = [sub_one, sub_two]

    actual = util.get_substituted_contents(starting_contents, subs)

    sub_one.apply_and_get_result.assert_called_once_with(starting_contents)
    sub_two.apply_and_get_result.assert_called_once_with(sub_one_result)

    assert actual == target


def test_get_substituted_contents_substitutes_correctly():
    """
    Basic test to make sure Substitutions can get applied correctly.
    """
    sub_one = substitute.Substitution('foo', 'bar', False)
    sub_two = substitute.Substitution('bar\n\n', 'baz\n', True)

    start = 'foo\n\n something else\n\n    bar\n\n'
    target = 'baz\n something else\n\n    baz\n'

    subs = [sub_one, sub_two]
    actual = util.get_substituted_contents(start, subs)

    assert actual == target


@patch('eg.color.EgColorizer')
def test_get_colorized_contents_calls_methods(patched_colorizer_class):
    """
    We should call the correct methods on the EgColorizer objects when we color
    a file.
    """
    raw_contents = 'these are uncolored contents'
    colored_contents = 'COLORED: ' + raw_contents
    color_config = 'some color config'

    # The actual instance created by these calls is stored at return_value.
    colorizer_instance = patched_colorizer_class.return_value
    colorizer_instance.colorize_text.return_value = colored_contents

    actual = util.get_colorized_contents(raw_contents, color_config)

    assert actual == colored_contents
    colorizer_instance.colorize_text.assert_called_once_with(raw_contents)


@patch('eg.util.get_alias_dict')
def _helper_assert_get_resolved_program(
    program,
    resolved_program,
    config_obj,
    alias_dict,
    mock_dict,
):
    """
    program: the program to resolved for as an alias
    resolved_program: the result of the resolution.
    config_obj: the config_obj to use toe resolve the alias path
    alias_dict: the dict of aliases to be returned
    """
    mock_dict.return_value = alias_dict

    actual = util.get_resolved_program(program, config_obj)
    assert actual == resolved_program
    mock_dict.assert_called_once_with(config_obj)


def test_get_resolved_program_no_alias():
    """
    A program that is not an alias should return itself.
    """
    alias_dict = {
        'link': 'ln',
        'nc': 'netcat'
    }
    config_obj = 'a config'
    _helper_assert_get_resolved_program('link', 'ln', config_obj, alias_dict)


def test_get_resolved_program_is_alias():
    """
    A program that is an alias should return the resolved value.
    """
    alias_dict = {
        'link': 'ln',
        'nc': 'netcat'
    }
    config_obj = 'some new config'
    _helper_assert_get_resolved_program('cp', 'cp', config_obj, alias_dict)


def test_get_alias_dict_returns_contents_of_correct_file():
    """
    get_alias_dict should read data from the file at the default path.
    """
    alias_dict = {
        'link': 'ln',
        'nc': 'netcat'
    }
    config_obj = _create_config(
        examples_dir='path/to/examples/dir',
    )

    alias_file_path = 'path/to/alias/file'
    alias_dict_str = json.dumps(alias_dict)
    _helper_assert_get_alias_dict(
        alias_dict_str,
        alias_dict,
        config_obj,
        alias_file_path,
        True
    )


def test_get_alias_dict_fails_gracefully_if_not_file():
    """
    Since users can specify a directory for examples that might not contain the
    aliases file, we want to fail gracefully if the file doesn't exist.
    """
    contents_of_alias_dict_file = 'should never be reached'
    config_obj = _create_config(
        examples_dir='path/to/examples/dir',
    )
    alias_file_path = 'path/to/the/alias/file'
    _helper_assert_get_alias_dict(
        contents_of_alias_dict_file,
        {},
        config_obj,
        alias_file_path,
        False
    )


@patch('eg.util._get_contents_of_file')
@patch('eg.util._get_alias_file_path')
@patch('os.path.isfile')
def _helper_assert_get_alias_dict(
    contents_of_alias_dict_file,
    target_alias_dict,
    config_obj,
    alias_file_path,
    alias_file_path_is_file,
    mock_is_file,
    mock_get_alias_file_path,
    mock_get_contents,
):
    """
    contents_of_alias_dict_file: the string contents of the file storing the
        dictionary of aliases
    target_alias_dict: the target result of get_alias_dict
    config_obj: the Config object
    alias_file_path: the path to be returned by _get_alias_file_path
    alias_file_path_is_file: True if the alias path is a file, else False
    """
    mock_is_file.return_value = alias_file_path_is_file
    mock_get_alias_file_path.return_value = alias_file_path
    mock_get_contents.return_value = contents_of_alias_dict_file

    actual = util.get_alias_dict(config_obj)

    assert actual == target_alias_dict

    mock_get_alias_file_path.assert_called_once_with(config_obj)
    mock_is_file.assert_called_once_with(alias_file_path)

    if alias_file_path_is_file:
        mock_get_contents.assert_called_once_with(alias_file_path)
    else:
        assert mock_get_contents.call_count == 0


@patch('os.path.join')
def test_get_alias_file_path(mock_join):
    """
    _get_alias_file_path should just join the example dir and the alias file
    name, to make sure we look in the right place for the file.
    """
    config_obj = _create_config(
        examples_dir='handy/dandy/examples/dir',
    )

    join_result = 'joined path'
    mock_join.return_value = join_result

    actual = util._get_alias_file_path(config_obj)
    assert actual == join_result
    mock_join.assert_called_once_with(
        config_obj.examples_dir,
        util.ALIAS_FILE_NAME
    )


def test_is_example_file_true_if_has_suffix():
    """
    Should be true if ends in EXAMPLE_FILE_SUFFIX.
    """
    file_name = 'find.md'
    actual = util._is_example_file(file_name)
    assert actual == True


def test_is_example_file_true_if_not_suffix():
    """
    Should be false if the file does not end in EXAMPLE_FILE_SUFFIX.
    """
    file_name = 'aliases.json'
    actual = util._is_example_file(file_name)
    assert actual == False


def test_can_parse_alias_file():
    """
    Make sure aliases.json file can be parsed.

    This is to make sure an edit doesn't accidentally corrupt it.
    """
    # We'll have to hardcode this.
    alias_file_path = os.path.join(
        config.DEFAULT_EXAMPLES_DIR,
        util.ALIAS_FILE_NAME
    )
    alias_file_contents = util._get_contents_of_file(alias_file_path)
    alias_dict = json.loads(alias_file_contents)
    # We'll check that link goes to ln, as we know that one will be present.
    assert alias_dict['link'] == 'ln'


@patch('os.path.exists')
@patch('eg.util._inform_cannot_edit_no_custom_dir')
@patch('eg.util.get_resolved_program')
@patch('eg.util.get_file_paths_for_program')
@patch('subprocess.call')
def test_edit_custom_examples_correct_with_custom_dir(
    mock_call,
    mock_get_paths,
    mock_get_program,
    mock_inform,
    mock_exists,
):
    """
    We should resolve aliases, get the custom file path, and call subprocess.
    """
    program = 'du'
    resolved_program = 'alias for du'
    config = _create_config(custom_dir='path/to/custom', editor_cmd='nano')
    paths = ['path/to/custom/du.md']

    mock_get_program.return_value = resolved_program
    mock_get_paths.return_value = paths
    mock_exists.return_value = True

    util.edit_custom_examples(program, config)

    mock_get_program.assert_called_once_with(program, config)
    mock_get_paths.assert_called_once_with(resolved_program, config.custom_dir)
    mock_call.assert_called_once_with([config.editor_cmd, paths])
    assert mock_inform.call_count == 0


@patch('os.path.exists')
@patch('eg.util._inform_cannot_edit_no_custom_dir')
@patch('eg.util.get_resolved_program')
@patch('eg.util.get_file_paths_for_program')
@patch('subprocess.call')
def test_edit_custom_examples_informs_if_no_custom_dir(
    mock_call,
    mock_get_paths,
    mock_get_program,
    mock_inform,
    mock_exists,
):
    """
    We should inform the user if they are trying to edit with no custom dir.

    This should be true if it is not set and if the path does not exist.
    """
    program = 'awk'

    # First with no custom dir set.
    config = _create_config(editor_cmd='vi -e')
    mock_exists.return_value = True
    util.edit_custom_examples(program, config)
    assert mock_inform.call_count == 1

    # And now with it set but a nonexistent path.
    config = _create_config(custom_dir='/path/to/custom', editor_cmd='vi -e')
    mock_exists.return_value = False
    util.edit_custom_examples(program, config)
    assert mock_inform.call_count == 2

    assert mock_call.call_count == 0
    assert mock_get_paths.call_count == 0
    assert mock_get_program.call_count == 0
