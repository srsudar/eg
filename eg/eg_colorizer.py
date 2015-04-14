import re
import sys


class EgColorizer():

    def __init__(self, color_config):
        self.color_config = color_config

    def colorize_heading(self, text):
        return self._color_helper(
            text,
            '(^#+)(.*)$',
            (
                self.color_config.pound +
                r'\1' +
                self.color_config.pound_reset +
                self.color_config.heading +
                r'\2' +
                self.color_config.heading_reset
            )
        )

    def colorize_block_indent(self, text):
        return self._color_helper(
            text,
            '^    (\$?)(.*)$',
            (
                '    ' +
                self.color_config.prompt +
                r'\1' +
                self.color_config.prompt_reset +
                self.color_config.code +
                r'\2' +
                self.color_config.code_reset
            )
        )

    def colorize_backticks(self, text):
        """untested"""
        return self._color_helper(
            text,
            '`([^`]+)`',
            (
                '`' +
                self.color_config.backticks +
                r'\1' +
                self.color_config.backticks_reset +
                '`'
            )
        )

    def colorize_text(self, text):
        """Colorize the text."""
        result = text
        result = self.colorize_heading(result)
        result = self.colorize_block_indent(result)
        result = self.colorize_backticks(result)
        return result

    def _color_helper(self, text, pattern, repl):
        # < 2.7 didn't have the flags named argument.
        if sys.version_info[1] < 7:
            compiled_pattern = re.compile(pattern, re.MULTILINE)
            return re.sub(
                compiled_pattern,
                repl,
                text
            )
        else:
            return re.sub(
                pattern,
                repl,
                text,
                flags=re.MULTILINE
            )
