# -*- coding: utf-8 -*-
import collections
from urllib.parse import urlencode, quote
__author__ = 'vahid'


def create_cache_key(namespace, k):
    if isinstance(k, dict):
        subkey = urlencode(k)
    elif isinstance(k, collections.Iterable):
        subkey = ','.join([quote(i) for i in k])
    else:
        subkey = k
    key = '%s:%s' % (namespace, subkey)
    return key
