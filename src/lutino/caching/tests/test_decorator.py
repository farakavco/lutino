# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import cache, init as init_cache
__author__ = 'vahid'
call_count = 0


# TODO; Concurrency testing
class TestCacheDecorator(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis()
        self.sample_data = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }
        init_cache(self.redis)

    def test_cache_item(self):

        @cache('test')
        def get_objects(key=None):
            global call_count
            call_count += 1
            return self.sample_data[key]

        for i in range(100):
            self.assertEqual(get_objects(key='a'), 1)
            self.assertEqual(get_objects(key='b'), 2)
            self.assertEqual(get_objects(key='c'), 3)
            self.assertEqual(get_objects(key='d'), 4)

        self.assertEqual(call_count, 4)


if __name__ == '__main__':
    unittest.main()



