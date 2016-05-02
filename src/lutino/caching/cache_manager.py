# -*- coding: utf-8 -*-
import uuid
import time
from datetime import datetime
from lutino.caching import CacheTimeoutError, serialize, deserialize
from lutino.caching.exceptions import CacheError, KeyInProgressError
__author__ = 'vahid'

IN_PROGRESS = '#&PROGRESS&#'


_manager = None


def init(redis_engine):
    global _manager
    _manager = CacheManager(redis_engine)


def manager():
    if _manager is None:
        raise CacheError('Caching is not initialized.')
    return _manager


class CacheManager(object):

    def __init__(self, redis_engine, max_wait=0, reset_on_timeout=True):
        self.redis = redis_engine
        self.max_wait = max_wait
        self.reset_on_timeout = reset_on_timeout

    def get_item(self, key, recover=None, ttl=None, arguments=([], {})):
        item_key = self.redis.get(key)

        start_wait_time = datetime.now()
        while item_key == IN_PROGRESS:
            # waiting a while:
            # FIXME: redis clean-up to clean IN_PROGRESS items on startup
            if 0 < self.max_wait < (datetime.now() - start_wait_time).total_seconds():
                if not self.reset_on_timeout:
                    raise CacheTimeoutError()
                else:
                    item_key = None
                    break
            time.sleep(.2)
            item_key = self.redis.get(key)

        value = self.redis.get(item_key) if item_key else None

        if value is None:
            if recover is None:
                return None
            else:
                # Trying to recover the value
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
            # setting it's value to in progress to prevent the other instances
            # to trying to set it simultaneously.
            self.redis.set(key, IN_PROGRESS, ex=5)

        guid = uuid.uuid1()
        item_key = '%s:%s' % (key, guid)

        v = value() if callable(value) else value

        self.redis.set(
            item_key,
            serialize(v),
            ex=ttl)

        self.redis.set(key, item_key, ex=ttl)
        self.redis.delete(old_item_key)
        return v

    def get_list(self, key, recover=None, ttl=None):
        # First, get the keys list
        pass

    def set_list(self, key, value, ttl=None):
        value = self.redis.get(key)

        if value == IN_PROGRESS:
            raise KeyInProgressError(key)

        # this is a new item
        # setting it's value to in progress to prevent the other instances
        # to trying to set it simultaneously.
        self.redis.set(key, IN_PROGRESS, ex=5)

        guid = uuid.uuid1()
        item_key = '%s:%s' % (key, guid)

        v = value() if callable(value) else value

        self.redis.set(
            item_key,
            serialize(v),
            ex=ttl)

        self.redis.set(key, item_key, ex=ttl)
        self.redis.delete(old_item_key)
        return v