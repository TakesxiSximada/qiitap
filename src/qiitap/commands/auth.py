import sys
import argparse

import getpass
import webbrowser

import six

from ..environs import build_environ


APPLICATIONS_URL = 'https://qiita.com/settings/applications'


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-browser', default=False, action='store_true')
    args = parser.parse_args(argv)  # noqa

    if not args.no_browser:
        webbrowser.open(APPLICATIONS_URL)

    access_token = getpass.getpass('ACCESS_TOKEN(Need qiita_read, qiita_write): ')
    default_tags = six.moves.input('Detault Tags(comma separated): ')
    environ = build_environ(access_token, default_tags)
    print('Created environment files: {}'.format(environ.environment_path))


if __name__ == '__main__':
    sys.exit(main())
