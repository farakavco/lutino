import unittest
import redis

from lutino.caching import CacheManager


class RedisTestCase(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()
        self.redis.flushdb()


class CachingTestCase(RedisTestCase):

    def setUp(self):
        super(CachingTestCase, self).setUp()
        self.cache_manager = CacheManager(self.redis)
