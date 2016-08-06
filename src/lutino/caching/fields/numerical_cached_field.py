from lutino.caching.fields.cached_field import CachedField


class NumericalCachedField(CachedField):

    def __init__(self, redis_engine, model_name, model_identity, field_name):
        self.redis = redis_engine
        self.model_name = model_name
        self.model_identity = model_identity
        self.field_name = field_name

    @property
    def key(self):
        return '%s_%s_%s' % (self.model_name, self.model_identity, self.field_name)

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
                raise ValueError()

        self.redis.set(self.key, value, ex=ttl)
        return value

    def increment(self):
        value = self.redis.incr(self.key)
        return int(value)

    def decrement(self):
        value = self.redis.decr(self.key)
        return int(value)

    def fetch(self):
        raise NotImplementedError()

    @classmethod
    def cached_field(cls, redis, model_name, model_identity, ttl=None):
        def decorator(func):

            def wrapper(*args, **kwargs):
                obj = cls(redis, model_name, model_identity)
                return obj.get(ttl=ttl)

            return wrapper

        return decorator
