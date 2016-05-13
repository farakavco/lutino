# -*- coding: utf-8 -*-
import unittest
from lutino.caching import create_cache_key
from lutino.caching.tests.base import CachingTestCase
from datetime import datetime
import threading
__author__ = 'vahid'


def th():
    return threading.current_thread().name


class TestCacheDecoratorList(CachingTestCase):

    @classmethod
    def setUpClass(cls):
        cls.request_count_per_thread = 100
        cls.thread_count = 4
        cls.invalidated = False
        cls.call_count = 0
        cls.sample_lists = {
            'a': [
                {'id': 1, 'type': 'a', 'name': 'vahid'},
                {'id': 2, 'type': 'a', 'name': 'baghali'},
                {'id': 3, 'type': 'a', 'name': 'taghi'},
                {'id': 4, 'type': 'a', 'name': 'yadollah'},
            ],
            'b': [
                {'id': 11, 'type': 'b', 'name': 'vahid'},
                {'id': 22, 'type': 'b', 'name': 'baghali'},
                {'id': 33, 'type': 'b', 'name': 'taghi'},
                {'id': 44, 'type': 'b', 'name': 'yadollah'},
            ]
        }

    def list_worker(self):

        @self.cache_manager.decorate('test', list_=True, key_extractor=lambda x: dict(id=x['id']))
        def get_list(key=None):
            self.call_count += 1
            print("## get_list, call_count: %s" % self.call_count)
            return self.sample_lists[key]

        for i in range(self.request_count_per_thread):
            if not self.invalidated and i == (self.request_count_per_thread // 2) and th() == 'th 01':
                self.invalidated = True
                print('Invalidating')
                self.cache_manager.invalidate_list(create_cache_key('test', dict(key='a')))
                self.cache_manager.invalidate_list(create_cache_key('test', dict(key='b')))

            self.assertListEqual(get_list(key='a'), self.sample_lists['a'])
            self.assertListEqual(get_list(key='b'), self.sample_lists['b'])

    def test_decorator_cache_list(self):
        start_time = datetime.now()
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.list_worker, daemon=True, name='th %02d' % (i+1))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        seconds = (datetime.now() - start_time).total_seconds()
        self.assertEqual(self.call_count, 4)
        print('Total time: %s Avg: %s' % (seconds, seconds / (self.request_count_per_thread * self.thread_count)))

if __name__ == '__main__':
    unittest.main()
