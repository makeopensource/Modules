import re

from jinja2 import nodes
from jinja2.ext import Extension

import markdown


class MarkdownExtension(Extension):
    tags = {"mk"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(["name:endmk"], drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_markdown_support"), [], [], body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        return markdown.markdown(caller())


def linkify(title):
    return re.sub(r"\s+", "-", title).lower()

