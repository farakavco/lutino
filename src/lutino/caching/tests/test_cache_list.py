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
        key_extractor = lambda o: dict(id=o['id'])

        list_key = create_cache_key('test', {'1': 2, '3': 4})

        cache.set_list(list_key, self.sample_data, key_extractor=key_extractor)
        result = cache.get_list(list_key)
        self.assertEqual(len(self.sample_data), len(list(result)))

        cache.invalidate_list(list_key)

        result = cache.get_list(list_key, recover=lambda: self.sample_data, key_extractor=key_extractor)
        self.assertEqual(len(self.sample_data), len(list(result)))
        self.assertEqual(cache.get_item('test:id=1'), self.sample_data[0])
        self.assertEqual(cache.get_item('test:id=2'), self.sample_data[1])
        self.assertEqual(cache.get_item('test:id=3'), self.sample_data[2])

if __name__ == '__main__':
    unittest.main()



