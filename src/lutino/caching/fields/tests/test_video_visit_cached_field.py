import unittest

from lutino.caching.fields.tests.base import VideoVisitCachedTestCase


class TestVideoVisitCachedField(VideoVisitCachedTestCase):

    def test_numerical_cached_field(self):

        default_visit = 10
        self.video_visit_cached_field.set(default_visit)
        stored_visit = self.video_visit_cached_field.get()
        self.assertEqual(default_visit, stored_visit)

        self.video_visit_cached_field.increment()
        incremented_visit = self.video_visit_cached_field.get()
        self.assertEqual(stored_visit + 1, incremented_visit)


if __name__ == '__main__':
    unittest.main()
