# -*- coding: utf-8 -*-
import uuid
import time
from datetime import datetime
from lutino.caching import CacheTimeoutError, serialize, deserialize
__author__ = 'vahid'

IN_PROGRESS = '#&PROGRESS&#'


class CacheManager(object):

    def __init__(self, redis_engine):
        self.redis = redis_engine

    def get_item(self, key, recover=None, ttl=None, arguments=([], {}), max_wait=0, reset_on_timeout=True):
        item_key = self.redis.get(key)

        start_wait_time = datetime.now()
        while item_key == IN_PROGRESS:
            # waiting a while:
            # FIXME: redis clean-up to clean IN_PROGRESS items on startup
            if 0 < max_wait < (datetime.now() - start_wait_time).total_seconds():
                if reset_on_timeout:
                    raise CacheTimeoutError()
                else:
                    item_key = None
                    break
            time.sleep(.2)
            item_key = self.redis.get(key)

        value = self.redis.get(item_key) if item_key else None

        if value is None:
            self.set_item(
                key,
                lambda: recover(*arguments[0], **arguments[1]),
                ttl=ttl)

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

        self.redis.set(
            item_key,
            serialize(value() if callable(value) else value),
            ex=ttl)

        self.redis.set(key, item_key, ex=ttl)
        self.redis.delete(old_item_key)

    def get_list(self, key, recover=None, ttl=None):
        pass
