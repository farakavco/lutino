# -*- coding: utf-8 -*-
import collections
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

    def get_item(self, key, recover=None, ttl=None, arguments=([], {})):
        item_key = self.redis.get(key)

        value = self.redis.get(item_key) if item_key else None

        # return None if cannot recover the value
        if value is None and recover is None:
            return None

        # Trying to recover the value
        if value is None:
            try:
                return self.set_item(
                    key,
                    lambda: recover(*arguments[0], **arguments[1]),
                    ttl=ttl,
                    no_wait=True)
            except KeyInProgressError:
                # Nice!, it seems this item is recovering in another pipe,
                # so just waiting for the item to be loaded
                self.wait_for_lock(key)
                value = self.redis.get(item_key)

        return deserialize(value)

    def set_item(self, key, value, ttl=None, no_wait=False):
        old_item_key = self.redis.get(key)

        if old_item_key is None:
            # this is a new item
            # locking it to prevent concurrency violation
            self.lock(key, no_wait=no_wait)

        try:
            guid = uuid.uuid1()
            item_key = '%s:%s' % (key, guid)
            value = value() if callable(value) else value

            self.redis.set(
                item_key,
                serialize(value),
                ex=ttl)

            self.redis.set(key, item_key, ex=ttl)
            self.redis.delete(old_item_key)
            return value
        finally:
            if self.is_locked(key):
                self.unlock(key)

    @staticmethod
    def create_lock_key(key):
        return '%s:lock' % key

    def is_locked(self, key):
        lock_key = self.create_lock_key(key)
        return self.redis.get(lock_key) is not None

    def wait_for_lock(self, key):
        lock_key = self.create_lock_key(key)
        start_wait_time = datetime.now()
        while self.redis.get(lock_key) is not None:
            if 0 < self.max_wait < (datetime.now() - start_wait_time).total_seconds():
                raise KeyInProgressError(key)
            time.sleep(.2)

    def lock(self, key, no_wait=False):
        lock_key = self.create_lock_key(key)
        start_wait_time = datetime.now()
        while self.redis.get(lock_key) == 'yes':
            if no_wait or 0 < self.max_wait < (datetime.now() - start_wait_time).total_seconds():
                raise KeyInProgressError(key)
            time.sleep(.2)
        self.redis.set(lock_key, 'yes', ex=1)

    def unlock(self, key):
        lock_key = self.create_lock_key(key)
        self.redis.delete(lock_key)

    def get_list(self, key, recover=None, ttl=None, arguments=([], {}), key_extractor=None):
        # First, get the keys list
        value = self.redis.get(key)
        if value is None and recover is None:
            return None

        # Trying to recover the value
        if value is None:
            try:
                return self.set_list(
                    key,
                    lambda: recover(*arguments[0], **arguments[1]),
                    ttl=ttl,
                    no_wait=True,
                    key_extractor=key_extractor
                )
            except KeyInProgressError:
                # Nice!, it seems this item is recovering in another pipe,
                # so just waiting for the item to be loaded
                self.wait_for_lock(key)
                value = self.redis.get(key)

        item_keys = deserialize(value)
        for item_key in item_keys:
            yield self.get_item(item_key)

    def set_list(self, key, value, ttl=None, key_extractor=None, no_wait=False):
        self.lock(key, no_wait=no_wait)

        if key_extractor is None:
            key_extractor = lambda x: x['id']

        try:
            value = value() if callable(value) else value
            item_keys = []
            assert isinstance(value, collections.Iterable), "Value must be iterable"

            for item_value in value:
                item_key = key_extractor(item_value)
                item_keys.append(item_key)
                self.set_item(
                    item_key,
                    item_value,
                    ttl=ttl,
                    no_wait=no_wait)

            self.redis.set(
                key,
                serialize(item_keys),
                ex=ttl)

            return value
        finally:
            self.unlock(key)
