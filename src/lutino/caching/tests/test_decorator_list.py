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
        self.maxDiff = None
        self.request_count_per_thread = 1000
        self.thread_count = 4
        self.redis = redis.Redis()
        self.sample_lists = {
            'a': [
                {'mid': 1, 'type': 'a', 'name': 'vahid'},
                {'mid': 2, 'type': 'a', 'name': 'baghali'},
                {'mid': 3, 'type': 'a', 'name': 'taghi'},
                {'mid': 4, 'type': 'a', 'name': 'yadollah'},
            ],
            'b': [
                {'mid': 11, 'type': 'b', 'name': 'vahid'},
                {'mid': 22, 'type': 'b', 'name': 'baghali'},
                {'mid': 33, 'type': 'b', 'name': 'taghi'},
                {'mid': 44, 'type': 'b', 'name': 'yadollah'},
            ]
        }
        init_cache(self.redis)

    @cache('test', list_=True, key_extractor=lambda x: x['mid'])
    def get_list(self, key=None):
        global call_count
        call_count += 1
        return self.sample_lists[key]

    def list_worker(self):
        for i in range(self.request_count_per_thread):
            self.assertListEqual(self.get_list(key='a'), self.sample_lists['a'])
            self.assertListEqual(self.get_list(key='b'), self.sample_lists['b'])

    def test_decorator_cache_list(self):
        global call_count
        call_count = 0
        start_time = datetime.now()
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.list_worker(), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        seconds = (datetime.now() - start_time).total_seconds()
        self.assertEqual(call_count, 2)
        print('Total time: %s Avg: %s' % (seconds, seconds / (self.request_count_per_thread * self.thread_count)))

if __name__ == '__main__':
    unittest.main()



