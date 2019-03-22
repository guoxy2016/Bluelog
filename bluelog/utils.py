import re
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for
from unidecode import unidecode

_prev_re = re.compile(r'[ \t`~!@#$%^&*()+={}:"<>?\\\[\]\';/.,]')


def is_self_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='post.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_self_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def slugify(text, sep='-'):
    result = []
    for word in _prev_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    return sep.join(result)
