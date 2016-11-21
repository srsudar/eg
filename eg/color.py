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
        # In this case we are going to go line by line, as we need to handle
        # the somewhat special case to avoid backticks in block indents.
        lines = text.split('\n')
        output = []

        for line in lines:
            if (line.startswith('    ')):
                # We are in a block indent. In this special case we do not want
                # to colorize backticks, as we are using backticks in a piece
                # of example code that should not be colorized.
                output.append(line)
            else:
                colorized = self._color_helper(
                    line,
                    '`([^`]+)`',
                    (
                        '`' +
                        self.color_config.backticks +
                        r'\1' +
                        self.color_config.backticks_reset +
                        '`'
                    )
                )
                output.append(colorized)

        return '\n'.join(output)

    def colorize_text(self, text):
        """Colorize the text."""
        # As originally implemented, this method acts upon all the contents of
        # the file as a single string using the MULTILINE option of the re
        # package. I believe this was ostensibly for performance reasons, but
        # it has a few side effects that are less than ideal. It's non-trivial
        # to avoid some substitutions based on other matches using this
        # technique, for example. In the case of block indents, e.g., backticks
        # that occur in the example ($ pwd is `pwd`) should not be escaped.
        # With the MULTILINE flag that is not simple. colorize_backticks() is
        # currently operating on a line by line basis and special casing for
        # this scenario. If these special cases proliferate, the line breaking
        # should occur here in order to minimize the number of iterations.

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
