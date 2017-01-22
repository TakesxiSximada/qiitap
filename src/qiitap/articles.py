import os
import json
import yaml
import mako.parsetree
from mako.template import Template
from mako.lookup import TemplateLookup

from .lexers import MarkdownLexer


def parse_attrs(body):
    lexer = MarkdownLexer(body)
    tmpl = lexer.parse()
    for node in tmpl.nodes:
        if isinstance(node, mako.parsetree.Comment):
            return yaml.safe_load(node.text)
    return {}


def build_payload(body, attrs):
    lookup = TemplateLookup(directories=[os.getcwd()])
    tmpl = Template(
        body, lookup=lookup,
        lexer_cls=MarkdownLexer,
    )
    renderd_body = tmpl.render(
        attrs=attrs,
    )

    return {
        'title': attrs['title'],
        'body': renderd_body,
        'coediting': attrs.get('coediting', False),
        'gist': attrs.get('gist', False),
        'private': attrs.get('private', False),
        'tags': attrs.get('tags', [
            {
                'name': 'Qiita',
                'versions': [
                    '0.0.1'
                ]
            },
        ]),
    }


class Article(object):
    def __init__(self, filepath, payload, attrs):
        self.filepath = filepath
        self.payload = payload
        self.attrs = attrs
        self.url = None

    @property
    def item_id(self):
        return self.attrs.get('item_id')

    @item_id.setter
    def item_id(self, code):
        self.attrs['item_id'] = code

    @property
    def payload_str(self):
        return json.dumps(self.payload)

    @property
    def body(self):
        return self.payload['body']


def build_article(filepath, encoding='utf8'):
    with open(filepath, 'rt', encoding='utf8') as fp:
        buf = fp.read()
        attrs = parse_attrs(buf)
        payload = build_payload(buf, attrs)
        return Article(filepath, payload, attrs)
