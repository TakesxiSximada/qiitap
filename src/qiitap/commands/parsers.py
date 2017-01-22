
def get_attributes(body):
    lexer = MarkdownLexer(body)
    tmpl = lexer.parse()
    for node in tmpl.nodes:
        if isinstance(node, mako.parsetree.Comment):
            return yaml.safe_load(node.text)
    return {}


def parse(filepath, encoding='utf8'):
    with open(filepath, 'rt', encoding=encoding) as fp:
        buf = fp.read()
        attrs = get_attributes(buf)
