import re as regex


class Expression(object):
    """Represents a simplematch expression."""
    BRACKET_MATCH = regex.compile(r"\{\{(.*?)\}\}")

    def __init__(self, expression, regexes=None):
        self._expression = expression
        self._regexes = regexes if regexes is not None else {}

    def regex(self):
        """
        Returns a regular expression object representing the simplematch.
        """
        is_plain_text = True
        compiled_regex = r""
        for chunk in self.BRACKET_MATCH.split(self._expression):
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
                    compiled_regex = u"{0}{1}{2}{3}".format(
                        compiled_regex,
                        u"\{\{", chunk, u"\}\}"
                    )
            is_plain_text = not is_plain_text
        return compiled_regex

    def match(self, string=None, flags=0):
        return regex.match(self.regex(), string, flags=0)

    def search(self, string=None, flags=0):
        return regex.search(self.regex(), string, flags=0)

def simex(expression, **regexps):
    return Expression(expression, **regexps)