import re

from mako import (
    exceptions,
    lexer,
    parsetree,
)


class MarkdownLexer(lexer.Lexer):
    def match_control_line(self):
        # <MATCH_CONTROL_RE>
        match = self.match(
            r"(?<=^)[\t ]*(%(?!%))[\t ]*((?:(?:\\r?\n)|[^\r\n])*)"
            r"(?:\r?\n|\Z)", re.M)
        # </MATCH_CONTROL_RE>

        if match:
            operator = match.group(1)
            text = match.group(2)
            if operator == '%':
                m2 = re.match(r'(end)?(\w+)\s*(.*)', text)
                if not m2:
                    raise exceptions.SyntaxException(
                        "Invalid control line: '%s'" %
                        text,
                        **self.exception_kwargs)
                isend, keyword = m2.group(1, 2)
                isend = (isend is not None)

                if isend:
                    if not len(self.control_line):
                        raise exceptions.SyntaxException(
                            "No starting keyword '%s' for '%s'" %
                            (keyword, text),
                            **self.exception_kwargs)
                    elif self.control_line[-1].keyword != keyword:
                        raise exceptions.SyntaxException(
                            "Keyword '%s' doesn't match keyword '%s'" %
                            (text, self.control_line[-1].keyword),
                            **self.exception_kwargs)
                self.append_node(parsetree.ControlLine, keyword, isend, text)
            else:
                self.append_node(parsetree.Comment, text)
            return True
        else:
            return False
