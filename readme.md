# MIME List


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


A comprehesive list of all the content types I've generally found, to provide 'mime' extension types for file suffix's

+ https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
+ https://www.iana.org/assignments/media-types/media-types.xhtml
