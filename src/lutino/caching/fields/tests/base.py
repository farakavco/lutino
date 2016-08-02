from lutino.caching.tests.base import RedisTestCase
from lutino.caching.fields.numerical_cached_field import VideoVisitCachedFieldBase


class VideoVisitCachedTestCase(RedisTestCase):

    def setUp(self):
        super(VideoVisitCachedTestCase, self).setUp()
        self.model_identity = 'AB'
        self.video_visit_cached_field = VideoVisitCachedFieldBase(self.redis, self.model_identity)
