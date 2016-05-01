# -*- coding: utf-8 -*-
from redis import StrictRedis
import uuid
import time
from datetime import datetime
from lutino.caching import IN_PROGRESS, CacheTimeoutError, serialize, deserialize
__author__ = 'vahid'

redis = StrictRedis(host='localhost', port=6379, db=0)


def get_item(key, recover=None, ttl=None, arguments=([], {}), max_wait=0, reset_on_timeout=True):
    item_key = redis.get(key)

    start_wait_time = datetime.now()
    while item_key == IN_PROGRESS:
        # waiting a while:
        # FIXME: redis clean-up to clean IN_PROGRESSes on startup
        if 0 < max_wait < (datetime.now() - start_wait_time).total_seconds():
            if reset_on_timeout:
                raise CacheTimeoutError()
            else:
                item_key = None
                break
        time.sleep(.2)
        item_key = redis.get(key)

    value = redis.get(item_key) if item_key else None

    if value is None:
        set_item(
            key,
            lambda: recover(*arguments[0], **arguments[1]),
            ttl=ttl)

    return deserialize(value)


def set_item(key, value, ttl=None):
    old_item_key = redis.get(key)

    if old_item_key is None:
        # this is a new item
        # setting it's value to in progress to prevent the other instances
        # to trying to set it simultaneously.
        redis.set(key, IN_PROGRESS, ex=5)

    guid = uuid.uuid1()
    item_key = '%s:%s' % (key, guid)

    redis.set(
        item_key,
        serialize(value() if callable(value) else value),
        ex=ttl)

    redis.set(key, item_key, ex=ttl)
    redis.delete(old_item_key)
