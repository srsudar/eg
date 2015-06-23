from eg import core
from mock import patch
from nose.tools import assert_equal


def _helper_assert_about_invocation(
    argv,
    num_print_help_calls,
    num_show_list_calls,
    num_show_version_calls,
    num_handle_program_calls,
    num_handle_insufficient_args_calls,
    resolved_config,
    handle_program_args,
    egrc_path,
    examples_dir,
    custom_dir,
    use_color,
    pager_cmd,
    squeeze
):
    """
    Helper method for calling core.run_eg() and making assertions as if it were
    called from the command line.

    argv: an array to be interpreted as argv
    num_print_help_calls: the number of calls to print_help
    num_show_list_calls: the number of calls to _show_list_message. Called with
        resolved_config as a paramter.
    num_show_version_calls: the number of calls to _show_version
    num_handle_program_calls: the number of calls to handle_program
    resolved_config: the resolved config object
    handle_program_args: an array of arguments that will be exploded and passed
        individually to handle_program if num_handle_program_calls > 0
    egrc_path: the path we should parse from the command line
    examples_dir: the examples dir we should parse from the command line
    custom_dir: the custom dir we should parse from the command line
    use_color: the use_color value we should parse from the command line
    pager_cmd: the pager_cmd we should parse from the command line
    squeeze: the squeeze command we should parse from the command line
    """
    with patch('sys.argv', argv):
        with patch('argparse.ArgumentParser.print_help') as mock_help:
            with patch('eg.core._show_list_message') as mock_show_list:
                with patch('eg.core._show_version') as mock_version:
                    with patch('eg.util.handle_program') as mock_handle:
                        with patch(
                            'eg.config.get_resolved_config_items',
                            return_value=resolved_config
                        ) as mock_resolve_config:
                            with patch(
                                'eg.core._handle_insufficient_args'
                            ) as mock_bad_args:
                                core.run_eg()

                                assert_equal(
                                    mock_help.call_count,
                                    num_print_help_calls
                                )
                                assert_equal(
                                    mock_version.call_count,
                                    num_show_version_calls
                                )
                                assert_equal(
                                    mock_bad_args.call_count,
                                    num_handle_insufficient_args_calls
                                )

                                should_resolve_config = False

                                if num_show_version_calls > 0:
                                    should_resolve_config = True

                                if num_show_list_calls > 0:
                                    should_resolve_config = True
                                    mock_show_list.assert_called_once_with(
                                        resolved_config
                                    )
                                else:
                                    assert_equal(mock_show_list.call_count, 0)

                                if num_handle_program_calls > 0:
                                    should_resolve_config = True
                                    mock_handle.assert_called_once_with(
                                        *handle_program_args
                                    )
                                else:
                                    assert_equal(mock_handle.call_count, 0)

                                if should_resolve_config:
                                    mock_resolve_config.assert_called_once_with(
                                        egrc_path=egrc_path,
                                        examples_dir=examples_dir,
                                        custom_dir=custom_dir,
                                        use_color=use_color,
                                        pager_cmd=pager_cmd,
                                        squeeze=squeeze
                                    )
                                else:
                                    assert_equal(
                                        mock_resolve_config.call_count,
                                        0
                                    )


def test_fewer_than_two_args_fails():
    """
    You always need at least two arguments in argv: eg and a command.
    """
    with patch('sys.argv', ['eg']):
        with patch('argparse.ArgumentParser.print_help') as mock_help:
            core.run_eg()
            mock_help.assert_called_once_with()
    _helper_assert_about_invocation(
        argv=['eg'],
        num_print_help_calls=1,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=0,
        num_handle_insufficient_args_calls=0,
        resolved_config='config',
        handle_program_args='not applicable',
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_shows_version_if_long_version():
    """The version of eg should be shown if --version is true."""
    _helper_assert_about_invocation(
        argv=['eg', '--version'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=1,
        num_handle_program_calls=0,
        num_handle_insufficient_args_calls=0,
        resolved_config='config',
        handle_program_args='not applicable',
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_shows_version_if_short_version():
    """The version of eg should be shown if -v is true."""
    _helper_assert_about_invocation(
        argv=['eg', '-v'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=1,
        num_handle_program_calls=0,
        num_handle_insufficient_args_calls=0,
        resolved_config='config',
        handle_program_args='not applicable',
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_and_passes_args_correctly_if_only_program():
    """
    Should parse to the command-line defaults and pass to handle_program if only
    the command is given without any options.
    """
    config_obj = 'config obj'
    _helper_assert_about_invocation(
        argv=['eg', 'find'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['find', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_long_list_correctly():
    """
    Args has list == True if passed with --list.
    """
    _helper_assert_about_invocation(
        argv=['eg', '--list'],
        num_print_help_calls=0,
        num_show_list_calls=1,
        num_show_version_calls=0,
        num_handle_program_calls=0,
        num_handle_insufficient_args_calls=0,
        resolved_config='config',
        handle_program_args='not applicable',
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_short_list_correctly():
    """
    Args has list == True if passed with -l.
    """
    _helper_assert_about_invocation(
        argv=['eg', '-l'],
        num_print_help_calls=0,
        num_show_list_calls=1,
        num_show_version_calls=0,
        num_handle_program_calls=0,
        num_handle_insufficient_args_calls=0,
        resolved_config='config',
        handle_program_args='not applicable',
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_long_config_file_correctly():
    """
    Parses the config file path if passed with --config-file.
    """
    config_obj = 'a fancy config'
    _helper_assert_about_invocation(
        argv=['eg', '--config-file=path/to/config/file', 'cat'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['cat', config_obj],
        egrc_path='path/to/config/file',
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_short_config_file_correctly():
    """
    Parses the config file path if passed with -f.
    """
    config_obj = 'a fancy config'
    _helper_assert_about_invocation(
        argv=['eg', '-f=path/to/config/file', 'cat'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['cat', config_obj],
        egrc_path='path/to/config/file',
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_long_examples_dir_correctly():
    """
    Parses the examples directory if passed with --examples-dir.
    """
    config_obj = 'examples dir config obj'
    _helper_assert_about_invocation(
        argv=['eg', '--examples-dir', 'path/to/examples', 'cat'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['cat', config_obj],
        egrc_path=None,
        examples_dir='path/to/examples',
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_short_examples_dir_correctly():
    """
    Parses the examples directory if passed with -e.
    """
    config_obj = 'examples dir config obj'
    _helper_assert_about_invocation(
        argv=['eg', '-e', 'path/to/examples', 'cat'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['cat', config_obj],
        egrc_path=None,
        examples_dir='path/to/examples',
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_long_custom_dir_correctly():
    """
    Parses the custom directory if passed with --custom-dir.
    """
    config_obj = 'custom dir config obj'
    _helper_assert_about_invocation(
        argv=['eg', '--custom-dir', 'path/to/custom', 'file'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['file', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir='path/to/custom',
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_short_custom_dir_correctly():
    """
    Parses the custom directory if passed with -c.
    """
    config_obj = 'custom dir config obj'
    _helper_assert_about_invocation(
        argv=['eg', '-c', 'path/to/custom', 'file'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['file', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir='path/to/custom',
        use_color=None,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_long_squeeze_dir_correctly():
    """
    Parses squeeze if passed with --squeeze.
    """
    config_obj = 'squeeze config obj'
    _helper_assert_about_invocation(
        argv=['eg', '--squeeze', 'ls'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['ls', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=True
    )


def test_parses_short_squeeze_dir_correctly():
    """
    Parses squeeze is passed with -s.
    """
    config_obj = 'squeeze config obj'
    _helper_assert_about_invocation(
        argv=['eg', '-s', 'ls'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['ls', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd=None,
        squeeze=True
    )


def test_parses_long_pager_cmd_correctly():
    """
    Parses pager_cmd if passed with --pager-cmd.
    """
    config_obj = 'pager cmd config obj'
    _helper_assert_about_invocation(
        argv=['eg', '--pager-cmd', 'less -R', 'echo'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['echo', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd='less -R',
        squeeze=None
    )


def test_parses_short_pager_cmd_correctly():
    """
    Parses pager_cmd if passed with -p.
    """
    config_obj = 'pager cmd config obj'
    _helper_assert_about_invocation(
        argv=['eg', '-p', 'less -R', 'echo'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['echo', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=None,
        pager_cmd='less -R',
        squeeze=None
    )


def test_parses_color():
    """
    Parses --color.
    """
    config_obj = 'color config obj'
    _helper_assert_about_invocation(
        argv=['eg', '--color', 'whereis'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['whereis', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=True,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_no_color():
    """
    Parses --no-color.
    """
    config_obj = 'no color config obj'
    _helper_assert_about_invocation(
        argv=['eg', '--no-color', 'free'],
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['free', config_obj],
        egrc_path=None,
        examples_dir=None,
        custom_dir=None,
        use_color=False,
        pager_cmd=None,
        squeeze=None
    )


def test_parses_all_valid_options_simultaneously():
    """
    Parses a large number of valid options at the same time.
    """
    config_obj = 'all valid options config object'
    argv = [
        'eg',
        '--config-file=path/to/config/file',
        '--examples-dir',
        'path/to/examples',
        '-c',
        'path/to/custom',
        '--squeeze',
        '--no-color',
        '--pager-cmd',
        'less -R',
        'du'
    ]
    _helper_assert_about_invocation(
        argv=argv,
        num_print_help_calls=0,
        num_show_list_calls=0,
        num_show_version_calls=0,
        num_handle_program_calls=1,
        num_handle_insufficient_args_calls=0,
        resolved_config=config_obj,
        handle_program_args=['du', config_obj],
        egrc_path='path/to/config/file',
        examples_dir='path/to/examples',
        custom_dir='path/to/custom',
        use_color=False,
        pager_cmd='less -R',
        squeeze=True
    )
