# -*- coding: utf-8 -*-
from lutino.caching import manager, create_cache_key
__author__ = 'vahid'


def cache(namespace, list_=False, ttl=None):
    def decorator(func):
        cm = manager()
        return lambda *a, **kw: \
            (cm.get_list if list_ else cm.get_item)(
                create_cache_key(namespace, kw),
                recover=func,
                ttl=ttl,
                arguments=(a, kw))
    return decorator
