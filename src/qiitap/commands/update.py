import sys
import argparse

from .. import (
    articles,
    clients,
    constants,
)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs='?', default=constants.DEFAULT_MARKDONW_FILE)
    args = parser.parse_args(argv)

    filepath = args.filepath
    article = articles.build_article(filepath)

    client = clients.get_client()
    article = client.update(article)
    print('Updated: {}'.format(article.url))


if __name__ == '__main__':
    sys.exit(main())
