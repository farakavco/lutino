# -*- coding: utf-8 -*-
import collections
from urllib.parse import urlencode, quote
from .exceptions import CacheTimeoutError
from .marchalling import deserialize, serialize
from .list_ import get_list
from .item import get_item, set_item
__author__ = 'vahid'

IN_PROGRESS = '#&PROGRESS&#'


def create_cache_key(namespace, k):
    if isinstance(k, dict):
        hashable = urlencode(k)
    elif isinstance(k, collections.Iterable):
        hashable = tuple([quote(i) for i in k])
    else:
        hashable = k
    return '%s:%s' % (namespace, hash(hashable))


