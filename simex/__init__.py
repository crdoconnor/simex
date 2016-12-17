import re as regex


class KeyNotFound(Exception):
    pass


class Simex(object):
    """
    Simple Simex containing no specified default regexes.
    """
    DEFAULTS = {}

    def __init__(
        self,
        regexes=None,
        open_delimeter="{{",
        close_delimeter="}}",
        exact=False,
        flexible_whitespace=False,
    ):
        """
        Initialize simex.

        regexes: A dict of keys and values. Will override self.DEFAULTS if specified.
        open_delimeter: what specifies the beginning of a key (default '}}')
        close_delimeter: what specifies the end of a key (default '}}')
        exact: whether to match an exact string (i.e. start with ^ and end with $).
        flexible_whitespace: match multiple whitespace characters.
        """
        if regexes is None:
            self._regexes = self.DEFAULTS
        else:
            self._regexes = dict([r for r in self.DEFAULTS.items()] + [r for r in regexes.items()])
        self._open_delimeter = open_delimeter
        self._close_delimeter = close_delimeter
        self._exact = exact
        self._flexible_whitespace = flexible_whitespace

    def compile(self, code):
        """
        Compile a simex code (e.g. <a href="{{ url }}">{{ anything }}</a>) to regex.

        Returns regex.
        """
        is_plain_text = True
        compiled_regex = r""
        for chunk in self.delimiter_regex().split(code):
            if is_plain_text:
                compiled_regex = compiled_regex + regex.escape(chunk)
            else:
                stripped_chunk = chunk.strip()
                if stripped_chunk in self._regexes.keys():
                    compiled_regex = u"{0}{1}".format(
                        compiled_regex,
                        self._regexes[stripped_chunk]
                    )
                else:
                    raise KeyNotFound("'{0}' not found in keys")
            is_plain_text = not is_plain_text
        if self._exact:
            compiled_regex = "^" + compiled_regex + "$"
        if self._flexible_whitespace:
            compiled_regex = regex.sub("\s+", " ", compiled_regex).replace(" ", "\s+")
        return regex.compile(compiled_regex)

    def delimiter_regex(self):
        return regex.compile(
            regex.escape(self._open_delimeter) + r'(.*?)' + regex.escape(self._close_delimeter)
        )


class DefaultSimex(Simex):
    """
    Simple Simex containing five default regexes.

    To see the regexes, see DEFAULTS class variable.
    """
    DEFAULTS = {
        "url": r"(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?",
        "email": r".*?\@.*?",
        "integer": r"[-+]?\d+",
        "number": r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?",
        "anything": r".*?",
    }
