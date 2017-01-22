import os

from .exc import NoTokenError

DEFAULT_ENVIRONMENT_PATH = os.path.join(os.path.expanduser('~'), '.qiita')


class QiitapEnviron(object):
    @property
    def host(self):
        return os.environ.get('QIITA_HOST', 'https://qiita.com')

    @property
    def environment_path(self):
        return os.environ.get('QIITA_ENVIRONMENT_PATH', DEFAULT_ENVIRONMENT_PATH)

    @property
    def token_path(self):
        return os.path.join(self.environment_path, 'token')

    @property
    def default_tags_path(self):
        return os.path.join(self.environment_path, 'default_tags')

    @property
    def token(self):
        token = os.environ.get('QIITA_TOKEN')
        if not token:
            with open(self.token_path) as fp:
                token = fp.readline().strip()
        if not token:
            raise NoTokenError()
        return token

    @property
    def default_tags(self):
        with open(self.default_tags_path) as fp:
            default_tags = fp.readline().strip()
        return default_tags


def build_environ(token, tags_str):
    environ = QiitapEnviron()
    os.makedirs(environ.environment_path, exist_ok=True)
    os.chmod(environ.environment_path, 0o700)

    token = token.strip()
    if token:
        with open(environ.token_path, 'w+b') as fp:
            fp.write(token.strip().encode())
        os.chmod(environ.token_path, 0o600)

    clean_tags_str = ','.join(tag.strip() for tag in tags_str.split(','))
    if clean_tags_str:
        with open(environ.default_tags_path, 'w+b') as fp:
            fp.write(clean_tags_str.encode())
        os.chmod(environ.default_tags_path, 0o600)

    return environ
