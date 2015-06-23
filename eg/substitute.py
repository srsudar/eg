import re


class Substitution:
    """
    A substitution to be performed on a piece of text.
    """

    def __init__(self, pattern, replacement, is_multiline):
        """
        Initialize the Substitution:
            pattern: the pattern to match as will be passed to 're.sub'.
            replacement: the argument that will be passed as the replacement to
                're.sub'. This way it can employ r'\1' style matching of
                parenthesis captures.
            is_multiline: if True, the pattern will be compiled with the
                re.MULTILINE flag.
        """
        self.pattern = pattern
        self.repl = replacement
        self.is_multiline = is_multiline

    def apply_and_get_result(self, string):
        """
        Perform the substitution represented by this object on string and return
        the result.
        """
        if self.is_multiline:
            compiled_pattern = re.compile(self.pattern, re.MULTILINE)
        else:
            compiled_pattern = re.compile(self.pattern)

        result = re.sub(compiled_pattern, self.repl, string)
        return result

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
