from lutino.caching.fields.cached_field import CachedField


class NumericalCachedField(CachedField):

    def __init__(self, redis_engine, model_name, model_identity):
        self.redis = redis_engine
        self.model_name = model_name
        self.model_identity = model_identity

    @property
    def key(self):
        return '%s_%s_visits' % (self.model_name, self.model_identity)

    def get(self, ttl=None):
        value = self.redis.get(self.key)

        if value is None:
            return self.set(self.key, ttl)
        else:
            return int(value)

    def set(self, value=None, ttl=None):
        if value is None:
            value = self.fetch()

            if value is None:
                raise ValueError

        self.redis.set(self.key, value, ex=ttl)
        return value

    def increment(self):
        value = self.redis.incr(self.key)
        return int(value)

    def fetch(self):
        raise NotImplementedError()


# noinspection PyAbstractClass
class VideoVisitCachedFieldBase(NumericalCachedField):
    def __init__(self, redis_engine, model_identity):
        super(VideoVisitCachedFieldBase, self).__init__(redis_engine, 'videos', model_identity)
