# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import CacheManager
__author__ = 'vahid'


class TestCacheItem(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()

    def test_cache_item(self):
        cache = CacheManager(self.redis)

        d = {'1': 2, '3': 4}
        cache.set_item('key1', d)
        d2 = cache.get_item('key1')
        self.assertDictEqual(d, d2)


if __name__ == '__main__':
    unittest.main()



