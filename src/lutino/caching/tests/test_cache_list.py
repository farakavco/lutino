# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import CacheManager, create_cache_key
__author__ = 'vahid'


# TODO; Concurrency testing
class TestCacheItem(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()
        self.sample_data = [
            {'name': 'vahid'},
            {'name': 'taghi'},
            {'name': 'naghi'},
        ]

    def test_cache_item(self):
        cache = CacheManager(self.redis)

        key = create_cache_key('test', {'1': 2, '3': 4})

        cache.set_list(key, self.sample_data)
        result = cache.get_list(key)
        self.assertEqual(len(self.sample_data), len(result))


if __name__ == '__main__':
    unittest.main()



