# -*- coding: utf-8 -*-
import unittest
import redis
from lutino.caching import cache, init as init_cache, manager, create_cache_key
from datetime import datetime
import threading
__author__ = 'vahid'
call_count = 0


def th():
    return threading.current_thread().name


class TestCacheDecoratorItem(unittest.TestCase):

    def setUp(self):
        self.request_count_per_thread = 20
        self.thread_count = 3
        self.redis = redis.Redis()
        self.redis.flushdb()
        self.sample_data_items = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }
        init_cache(self.redis)
        self.invalidated = False

    @cache('test')
    def get_single_item(self, key=None):
        global call_count
        call_count += 1
        print('%s: key=%s Calling backend' % (th(), key))
        return self.sample_data_items[key]

    def item_worker(self):
        for i in range(self.request_count_per_thread):
            if not self.invalidated and i == (self.request_count_per_thread // 2) and th() == 'th 01':
                self.invalidated = True
                manager().set_item(create_cache_key('test', dict(key='a')), 11)
                manager().set_item(create_cache_key('test', dict(key='b')), 22)
                manager().set_item(create_cache_key('test', dict(key='c')), 33)
                manager().set_item(create_cache_key('test', dict(key='d')), 44)

            self.assertIsNotNone(self.get_single_item(key='a'))
            self.assertIsNotNone(self.get_single_item(key='b'))
            self.assertIsNotNone(self.get_single_item(key='c'))
            self.assertIsNotNone(self.get_single_item(key='d'))

    def test_decorator_cache_item(self):
        global call_count
        call_count = 0
        start_time = datetime.now()
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.item_worker, daemon=True, name='th %02d' % (i+1))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        seconds = (datetime.now() - start_time).total_seconds()
        self.assertTrue(4 <= call_count <= 8)
        print('Total time: %s Avg: %s' % (seconds,  seconds / (self.request_count_per_thread * self.thread_count)))


if __name__ == '__main__':
    unittest.main()



