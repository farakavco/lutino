import unittest

from lutino.caching.fields.numerical_cached_field import NumericalCachedField
from lutino.caching.tests.base import RedisTestCase


class TestVideoVisitCachedField(RedisTestCase):

    def setUp(self):
        super().setUp()
        self.model_identity = 'AB'
        self.numerical_cached_field = NumericalCachedField(self.redis, 'videos', self.model_identity, 'visits')

    def test_numerical_cached_field(self):

        default_visit = 10
        self.numerical_cached_field.set(default_visit)
        stored_visit = self.numerical_cached_field.get()
        self.assertEqual(default_visit, stored_visit)

        self.numerical_cached_field.increment()
        incremented_visit = self.numerical_cached_field.get()
        self.assertEqual(stored_visit + 1, incremented_visit)

        self.numerical_cached_field.decrement()
        decremented_visit = self.numerical_cached_field.get()
        self.assertEqual(stored_visit, decremented_visit)


if __name__ == '__main__':
    unittest.main()
