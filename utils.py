from urlparse import urlparse, urlunparse, parse_qsl, ParseResult
from urllib import urlencode

import collections
import os.path
import time

POST, GET = 'POST', 'GET'

NOT_A_PAGE_CONTENT_TYPES = frozenset([
    'text/plain',
    'text/x-python',
    'image/gif',
    'image/jpeg',
    'image/png',
    'image/svg+xml',
])

INPUT_TYPE_DICT = {
    "text": "abcdefgh",
    "email": "ex@amp.le",
    "password": "abcd1234",
    "checkbox": "true",
    "radio": "1",
    "datetime": "1990-12-31T23:59:60Z",
    "datetime-local":
    "1985-04-12T23:20:50.52",
    "date": "1996-12-19",
    "month": "1996-12",
    "time": "13:37:00",
    "week": "1996-W16",
    "number": "123456",
    "range": "1.23",
    "url": "http://localhost/",
    "search": "query",
    "tel": "012345678",
    "color": "#FFFFFF",
    "hidden": "Secret.",
    "submit": ""
}

SCRIPTABLE_ATTRS = (
    'onblur',
    'onchange',
    'onclick',
    'ondblclick',
    'onfocus',
    'onkeydown',
    'onkeypress',
    'onkeyup',
    'onload',
    'onmousedown',
    'onmousemove',
    'onmouseout',
    'onmouseover',
    'onmouseup',
    'onreset',
    'onselect',
    'onsubmit',
    'onunload'
)

def get_url_host(url):
    return urlparse(url).netloc

def get_url_path(url):
    return urlparse(url).path

def get_url_query(url):
    return dict(parse_qsl(get_url_parts(url)[4]))

def get_url_parts(url):
    if isinstance(url, ParseResult):
        return list(url)
    else:
        return list(urlparse(url))

def update_url_params(url, params):
    url_parts = get_url_parts(url)
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)

def replace_url_params(url, replace):
    url_parts = get_url_parts(url)
    query = {k: replace for k in dict(parse_qsl(url_parts[4]))}
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)

def remove_url_params(url):
    url_parts = get_url_parts(url)
    url_parts[4] = ''
    return urlunparse(url_parts)

def modify_parameter(parameters, key, value):
    res = parameters.copy()
    res[key] = value
    return res

def get_all_path_links(url):
    url_parts = get_url_parts(url)
    url_parts[4] = ''
    path = url_parts[2]

    while os.path.dirname(path) != '/':
        path = os.path.dirname(path)
        if not path:
            break

        url_parts[2] = path + '/'
        yield urlunparse(url_parts)


def is_ascii(s):
     return not all(ord(char) < 128 for char in s)

def compare(x, y):
    return collections.Counter(x) == collections.Counter(y)

def validate_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = parsed_url._replace(**{"scheme": "http"})
    return parsed_url.geturl().replace('///', '//')

def contains_url(tag):
    return any(k in ('src',) and not v is None for k, v in tag.attrs.iteritems())