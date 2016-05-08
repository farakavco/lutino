# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import CacheManager, create_cache_key
__author__ = 'vahid'


# TODO; Concurrency testing
class TestCacheList(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()
        self.redis.flushdb()
        self.sample_data = [
            {'id': 1, 'name': 'vahid'},
            {'id': 2, 'name': 'taghi'},
            {'id': 3, 'name': 'naghi'},
        ]

    def test_cache_list(self):
        cache = CacheManager(self.redis)

        key = create_cache_key('test', {'1': 2, '3': 4})

        cache.set_list(key, self.sample_data)
        result = cache.get_list(key)
        self.assertEqual(len(self.sample_data), len(list(result)))

        cache.invalidate_list(key)

        result = cache.get_list(key, recover=lambda: self.sample_data)
        self.assertEqual(len(self.sample_data), len(list(result)))

if __name__ == '__main__':
    unittest.main()



