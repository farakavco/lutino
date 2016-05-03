# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import cache, init as init_cache
from datetime import datetime
import threading
__author__ = 'vahid'
call_count = 0


# TODO; Concurrency testing
class TestCacheDecorator(unittest.TestCase):

    def setUp(self):
        self.request_count_per_thread = 1000
        self.thread_count = 4
        self.redis = redis.Redis()
        self.sample_data_items = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }
        init_cache(self.redis)

    @cache('test')
    def get_single_item(self, key=None):
        global call_count
        call_count += 1
        return self.sample_data_items[key]

    def item_worker(self):
        for i in range(self.request_count_per_thread):
            self.assertEqual(self.get_single_item(key='a'), 1)
            self.assertEqual(self.get_single_item(key='b'), 2)
            self.assertEqual(self.get_single_item(key='c'), 3)
            self.assertEqual(self.get_single_item(key='d'), 4)

    def test_decorator_cache_item(self):
        global call_count
        call_count = 0
        start_time = datetime.now()
        threads = []
        for i in range(4):
            t = threading.Thread(target=self.item_worker(), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        seconds = (datetime.now() - start_time).total_seconds()
        self.assertEqual(call_count, 4)
        print('Total time: %s Avg: %s' % (seconds,  seconds / (self.request_count_per_thread * self.thread_count)))


if __name__ == '__main__':
    unittest.main()


