# -*- coding: utf-8 -*-
import unittest
from lutino.caching.tests.base import CachingTestCase
__author__ = 'vahid'


# TODO; Concurrency testing
class TestCacheItem(CachingTestCase):

    def test_cache_item(self):

        d = {'1': 2, '3': 4}
        self.cache_manager.set_item('key1', d)
        self.cache_manager.set_item('key1', d)  # setting twice
        d2 = self.cache_manager.get_item('key1')
        self.assertDictEqual(d, d2)

        self.cache_manager.invalidate_item('key1')

        d2 = self.cache_manager.get_item('key1', recover=lambda: d)
        self.assertDictEqual(d, d2)

if __name__ == '__main__':
    unittest.main()



