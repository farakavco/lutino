
class CachedField(object):
    pass


class AbstractCacheProvider(object):

    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def increment(self, key):
        raise NotImplementedError

    def decrement(self, key):
        raise NotImplementedError


class RedisCacheProvider(AbstractCacheProvider):

    def __init__(self, redis):
        self.redis = redis


class MemoryCacheProvider(AbstractCacheProvider):
    pass

