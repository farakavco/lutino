# -*- coding: utf-8 -*-
import collections
import uuid
import time
from lutino.caching import serialize, deserialize
from lutino.caching.common import create_cache_key
from redlock import Redlock
__author__ = 'vahid'


class CacheManager(object):

    def __init__(self, redis_engine, lock_ttl=1000):
        self.redis = redis_engine
        self.redlock = Redlock([redis_engine])
        self.lock_ttl = lock_ttl

    @staticmethod
    def get_lock_key(key):
        return '%s:lock' % key

    def lock(self, key, nowait=False):
        lock_key = self.get_lock_key(key)
        l = False
        while not l:
            l = self.redlock.lock(lock_key, self.lock_ttl)
            if l or nowait:
                return l
            time.sleep(.3)

    def unlock(self, lock):
        self.redlock.unlock(lock)

    def get_item(self, key, recover=None, ttl=None, arguments=([], {}), **kw):
        item_key = self.redis.get(key)

        value = self.redis.get(item_key) if item_key else None

        # return None if cannot recover the value
        if value is None and recover is None:
            return None

        # Trying to recover the value
        if value is None:
            return self.set_item(
                key,
                lambda: recover(*arguments[0], **arguments[1]),
                ttl=ttl)
        else:
            return deserialize(value)

    def set_item(self, key, value, ttl=None):
        old_item_key = self.redis.get(key)

        if old_item_key is None:
            # this is a new item
            # locking it to prevent concurrency violation
            lock = self.lock(key, nowait=True)
            if not lock:
                # it seems this item is loading in another thread
                # so, waiting for that:
                # wait & make sure the object is reloaded, the release the lock
                self.unlock(self.lock(key))
                return self.get_item(key)

            # check if item loaded
            v = self.get_item(key, None)
            if v:
                self.unlock(lock)
                return v

        else:
            lock = None

        try:
            guid = uuid.uuid1()
            item_key = '%s:%s' % (key, guid)
            value = value() if callable(value) else value

            self.redis.set(
                item_key,
                serialize(value),
                ex=ttl)

            self.redis.set(key, item_key, ex=ttl)
            if old_item_key:
                self.redis.delete(old_item_key)
            return value
        finally:
            if lock:
                self.unlock(lock)

    def get_list(self, key, recover=None, ttl=None, arguments=([], {}), key_extractor=None):
        # First, get the keys list
        value = self.redis.get(key)
        if value is None and recover is None:
            return None

        # Trying to recover the value
        if value is None:
            return self.set_list(
                    key,
                    lambda: recover(*arguments[0], **arguments[1]),
                    ttl=ttl,
                    key_extractor=key_extractor)
        else:
            item_keys = deserialize(value)
            return [self.get_item(item_key) for item_key in item_keys]

    def set_list(self, key, value, ttl=None, key_extractor=None):
        # locking it to prevent concurrency violation
        lock = self.lock(key)

        # check if item loaded
        v = self.get_list(key)
        if v:
            self.unlock(lock)
            return v

        if key_extractor is None:
            def key_extractor(x):
                return x['id']

        try:
            value = value() if callable(value) else value
            item_keys = []
            assert isinstance(value, collections.Iterable), "Value must be iterable"

            for item_value in value:
                item_key = create_cache_key(key.split(':')[0], key_extractor(item_value))
                item_keys.append(item_key)
                self.set_item(
                    item_key,
                    item_value,
                    ttl=ttl)

            self.redis.set(
                key,
                serialize(item_keys),
                ex=ttl)

            return value
        finally:
            if lock:
                self.unlock(lock)

    def invalidate_item(self, key):
        item_key = self.redis.get(key)
        self.redis.delete(key)
        if item_key:
            self.redis.delete(item_key)

    def invalidate_list(self, key):
        self.redis.delete(key)

    def decorate(self, namespace, list_=False, ttl=None, key_extractor=None):

        def decorator(func):

            def wrapper(*args, **kwargs):
                cache_key = create_cache_key(namespace, kwargs)
                cache_params = dict(
                    ttl=ttl,
                    recover=func,
                    arguments=(args, kwargs),
                )
                if list_:
                    cache_method = self.get_list
                    cache_params['key_extractor'] = key_extractor
                else:
                    cache_method = self.get_item
                return cache_method(cache_key, **cache_params)

            return wrapper

        return decorator
