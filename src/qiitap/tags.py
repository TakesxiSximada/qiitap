import logging
from .compat import StringIO
from .exc import TruncateError


logger = logging.getLogger(__name__)


def qinclude(context, path, start_at=None, end_at=None):
    """
    start_at: None -> ファイルの先頭から
    start_at: 'TAG' -> TAGの次の行から
    end_at: None -> ファイルの最後まで
    end_at: 'TAG' -> TAGの手前の行まで

    """
    truncate_count = 0
    truncate_char = ''

    fp = StringIO()
    is_content = start_at is None

    with open(path) as source:
        for ii, line in enumerate(source):
            if not is_content and start_at in line:
                is_content = True
                if line != '' and line[0] in (' ', '\t'):
                    truncate_char = line[0]
                    truncate_count = len(line) - len(line.lstrip(truncate_char))
                continue
            elif is_content and end_at is not None and end_at in line:
                is_content = False
                break

            if is_content:
                fp.write(line)

    fp.seek(0)

    try:
        dp = StringIO()
        for line in fp:
            truncate_line = line[:truncate_count] if truncate_char else line
            writable_line = line[truncate_count:]
            if truncate_char:
                if line.strip() == '':
                    writable_line = '\n'
                elif len(truncate_line) != truncate_line.count(truncate_char):
                    raise TruncateError('Truncate failed: {}'.format(repr(truncate_line)))
            dp.write(writable_line)
    except TruncateError as err:
        logger.warning('Cannnot truncate: %s', err)
        fp.seek(0)
        dp = StringIO()
        dp.write(fp.read())

    dp.seek(0)
    context.write(dp.read())
    return ''
