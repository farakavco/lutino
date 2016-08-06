from lutino.caching.fields.base import CachedField, MemoryCacheMixin


class NumericalCachedField(CachedField):
    __provider__ = MemoryCacheMixin()

    def __init__(self, model_name, model_identity, field_name):
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

        self.__provider__.set_cache(self.key, value)
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
    def decorate(cls):
        raise NotImplementedError()
