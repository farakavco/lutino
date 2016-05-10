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


class TestCacheDecoratorList(unittest.TestCase):

    def setUp(self):
        global call_count
        call_count = 0
        self.maxDiff = None
        self.request_count_per_thread = 100
        self.thread_count = 4
        self.redis = redis.Redis()
        self.redis.flushdb()
        self.invalidated = False
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
        print("## get_list, call_count: %s" % call_count)
        return self.sample_lists[key]

    def list_worker(self):
        for i in range(self.request_count_per_thread):
            if not self.invalidated and i == (self.request_count_per_thread // 2) and th() == 'th 01':
                self.invalidated = True
                print('Invalidating')
                manager().invalidate_list(create_cache_key('test', dict(key='a')))
                manager().invalidate_list(create_cache_key('test', dict(key='b')))

            self.assertListEqual(self.get_list(key='a'), self.sample_lists['a'])
            self.assertListEqual(self.get_list(key='b'), self.sample_lists['b'])

    def test_decorator_cache_list(self):
        global call_count
        call_count = 0
        start_time = datetime.now()
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.list_worker, daemon=True, name='th %02d' % (i+1))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        seconds = (datetime.now() - start_time).total_seconds()
        self.assertEqual(call_count, 4)
        print('Total time: %s Avg: %s' % (seconds, seconds / (self.request_count_per_thread * self.thread_count)))

if __name__ == '__main__':
    unittest.main()



