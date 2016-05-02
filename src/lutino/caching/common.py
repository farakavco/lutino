# -*- coding: utf-8 -*-
import collections
from urllib.parse import urlencode, quote
__author__ = 'vahid'


def create_cache_key(namespace, k):
    if isinstance(k, dict):
        hashable = urlencode(k)
    elif isinstance(k, collections.Iterable):
        hashable = tuple([quote(i) for i in k])
    else:
        hashable = k
    return '%s:%s' % (namespace, hash(hashable))
