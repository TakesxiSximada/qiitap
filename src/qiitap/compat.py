import six

if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO  # noqa
