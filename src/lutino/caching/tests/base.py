# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import init as init_cache
__author__ = 'vahid'


class RedisTestCase(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()
        self.redis.flushdb()


class CachingTestCase(RedisTestCase):

    def setUp(self):
        super(CachingTestCase, self).setUp()
        init_cache(self.redis)

