# -*- coding: utf-8 -*-
from lutino.caching import manager, create_cache_key
__author__ = 'vahid'


def cache(namespace, list_=False, ttl=None, key_extractor=None):
    def decorator(func):
        return lambda *a, **kw: \
            (manager().get_list if list_ else manager().get_item)(
                create_cache_key(namespace, kw),
                recover=func,
                ttl=ttl,
                arguments=(a, kw),
                key_extractor=key_extractor)
    return decorator
