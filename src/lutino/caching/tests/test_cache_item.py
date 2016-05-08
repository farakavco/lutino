# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import CacheManager
__author__ = 'vahid'


# TODO; Concurrency testing
class TestCacheItem(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()
        self.redis.flushdb()

    def test_cache_item(self):
        cache = CacheManager(self.redis)

        d = {'1': 2, '3': 4}
        cache.set_item('key1', d)
        cache.set_item('key1', d)  # setting twice
        d2 = cache.get_item('key1')
        self.assertDictEqual(d, d2)

        cache.invalidate_item('key1')

        d2 = cache.get_item('key1', recover=lambda: d)
        self.assertDictEqual(d, d2)

if __name__ == '__main__':
    unittest.main()



