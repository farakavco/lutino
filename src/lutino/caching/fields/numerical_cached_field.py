from lutino.caching.fields.cached_field import CachedField


class NumericalCachedField(CachedField):

    def __init__(self, redis_engine, model_name, model_identity):
        self.redis = redis_engine
        self.model_name = model_name
        self.model_identity = model_identity

    @property
    def key(self):
        return '%s_%s_visits' % (self.model_name, self.model_identity)

    def get(self, key, ttl):
        value = self.redis.get(key)

        if value is None:
            return self.set(key, ttl)
        else:
            return value

    def set(self, key, ttl):
        value = self.fetch()
        self.redis.set(key, value, ex=ttl)
        return value

    def increment(self, key):
        value = self.redis.incr(key)
        return value

    def fetch(self):
        raise NotImplementedError()


# noinspection PyAbstractClass
class VideoVisitCachedFieldBase(NumericalCachedField):
    def __init__(self, redis_engine, model_identity):
        super(VideoVisitCachedFieldBase, self).__init__(redis_engine, 'videos', model_identity)
