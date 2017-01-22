import enum

DEFAULT_MARKDONW_FILE = 'qiita.md'


class ExitCode(enum.IntEnum):
    success = 0
    unknown = -1
