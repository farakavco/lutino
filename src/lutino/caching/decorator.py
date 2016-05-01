# -*- coding: utf-8 -*-
from lutino.caching import get_list, get_item, create_cache_key
__author__ = 'vahid'


def cache(namespace, list_=False, ttl=None):
    def decorator(func):
        return lambda a, kw: \
            (get_list if list_ else get_item)(
                create_cache_key(namespace, kw),
                recover=func,
                ttl=ttl,
                arguments=(a, kw))
    return decorator
