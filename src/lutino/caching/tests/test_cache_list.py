# -*- coding: utf-8 -*-
import unittest
from lutino.caching import create_cache_key
from lutino.caching.tests.base import CachingTestCase
__author__ = 'vahid'


class TestCacheList(CachingTestCase):

    @classmethod
    def setUpClass(cls):
        cls.sample_data = [
            {'id': 1, 'name': 'vahid'},
            {'id': 2, 'name': 'taghi'},
            {'id': 3, 'name': 'naghi'},
        ]

    def test_cache_list(self):

        def key_extractor(o):
            return dict(id=o['id'])

        list_key = create_cache_key('test', {'1': 2, '3': 4})

        self.cache_manager.set_list(
            list_key,
            (len(self.sample_data), self.sample_data),
            key_extractor=key_extractor)

        results_count, result = self.cache_manager.get_list(list_key)
        self.assertEqual(len(self.sample_data), results_count)
        self.assertEqual(len(self.sample_data), len(list(result)))

        self.cache_manager.invalidate_list(list_key)

        results_count, result = self.cache_manager.get_list(
            list_key,
            recover=lambda: (len(self.sample_data), self.sample_data),
            key_extractor=key_extractor)
        self.assertEqual(len(self.sample_data), results_count)
        self.assertEqual(len(self.sample_data), len(list(result)))
        self.assertEqual(self.cache_manager.get_item('test:id=1'), self.sample_data[0])
        self.assertEqual(self.cache_manager.get_item('test:id=2'), self.sample_data[1])
        self.assertEqual(self.cache_manager.get_item('test:id=3'), self.sample_data[2])

if __name__ == '__main__':
    unittest.main()
