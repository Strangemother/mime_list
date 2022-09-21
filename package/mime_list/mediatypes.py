"""
Discover the content type for your media type

    >>> from mime_list import mediatypes
    >>> mediatypes.get('png')
    'image/png'


    >>> from mime_list import mediatypes
    >>> mediatypes.get('png')
    'image/png'

If the extension is unknown the package will raise a UnknownMediaType

    >>> mediatypes.get('x-ng')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/package/mime_list/mediatypes.py", line 32, in get
        raise UnknownMediaType(ext)
    mime_list.mediatypes.UnknownMediaType: x-ng

Provide a default to squash the error

    >>> mediatypes.get('x-ng', None)
    >>> mediatypes.get('x-ng', "plain/text")
    "plain/text"

The `filter` function can find multiple types for a query:

    >>> mediatypes.filter('png')
    ('image/png', 'image/x-png', 'image/x-citrix-png')

    >>> mediatypes.filter('x-png')
    ('image/png',)

Defaults are not required for the iterable response. Empty results return an empty tuple:

    >>> mediatypes.filter('x-ng')
    ()

Some examples:

    >>> mediatypes.get('jpg')
    'image/jpeg'
    >>> mediatypes.get('jpeg')
    'image/jpeg'
    >>> mediatypes.get('png')
    'image/png'
    >>> mediatypes.get('gif')
    'image/gif'
    >>> mediatypes.get('mp3')
    'audio/mpeg'
    >>> mediatypes.get('wav')
    'audio/x-wav'
    >>> mediatypes.get('pdf')
    'application/pdf'
    >>> mediatypes.get('html')
    'text/html'
    >>> mediatypes.get('txt')
    'text/plain'
    >>> mediatypes.get('yaml')
    'text/yaml'
    >>> mediatypes.get('json')
    'application/json'
    >>> mediatypes.get('js')
    'application/javascript'
"""
QUERY = ('SELECT "register_mediatype"."template" '
        'FROM "register_mediatype" '
        'WHERE "register_mediatype"."name" = "{ext}"')

from pathlib import Path

HERE = Path(__file__).parent

PATH = HERE / 'TYPES'

UNDEFINED = {}

import sqlite3

def get_cursor():
    # open sqlite
    con = sqlite3.connect(PATH)
    return con.cursor()


def standard_execute(ext):
    q = QUERY.format(ext=ext)
    cur = get_cursor()
    return cur.execute(q)


class UnknownMediaType(Exception):
    pass


def get(ext, default=UNDEFINED):
    res = standard_execute(ext)
    r = res.fetchone()
    if r is None:
        if default is UNDEFINED:
            raise UnknownMediaType(ext)
        return default
    return r[0]


def filter(ext):
    res = standard_execute(ext)
    return tuple(set(x[0] for x in res.fetchall()))





