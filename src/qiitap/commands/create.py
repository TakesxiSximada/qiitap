import sys
import argparse

from .. import (
    articles,
    clients,
    constants,
)

initail_markdown_template = """<!---
<%namespace name="qiitap" module="qiitap"/>
<%doc>
title: "{title}"
item_id: {item_id}
private: {private}
tags:
{tags_text}
</%doc>
--->

{body}
"""


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs='?', default=constants.DEFAULT_MARKDONW_FILE)
    parser.add_argument('-t', '--title', default='[WIP] NO TITLE')
    parser.add_argument('-p', '--public', default=False, action='store_true')
    parser.add_argument('--body', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--no-body', default=False, action='store_true')
    parser.add_argument('--tweet', default=False, action='store_true')
    parser.add_argument('--gist', default=False, action='store_true')
    parser.add_argument('--tags', default='Qiita')

    args = parser.parse_args(argv)
    tags = args.tags.split(',')

    if args.no_body:
        body = 'Writting...'
    else:
        body = args.body.read()
    title = args.title
    private = not args.public
    tweet = args.tweet

    article = articles.Article(
        args.filepath,
        payload={
            'title': title,
            'body': body,
            'coediting': False,
            'private': private,
            'tweet': tweet,
            'tags': [{'name': tag} for tag in tags],
        },
        attrs={
            'title': title,
            'item_id': None,
        }
    )
    client = clients.get_client()
    article = client.create(article)
    tags_text = ''.join('    - name: {}\n'.format(tag) for tag in tags)
    with open(args.filepath, 'w+', encoding='utf8') as fp:
        fp.write(initail_markdown_template.format(
            title=title,
            body=body,
            item_id=article.item_id,
            tags_text=tags_text,
            private=private,
        ))
    print('Output: {} (URL={})'.format(args.filepath, article.url))

if __name__ == '__main__':
    sys.exit(main())
