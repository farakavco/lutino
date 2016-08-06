


class CachedField(object):
    pass


class AbstractCacheProvider(object):

    def set(self, key, value):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def increment(self, key):
        raise NotImplementedError()

    def decrement(self, key):
        raise NotImplementedError()


class RedisCacheProvider(AbstractCacheProvider):

    def __init__(self, redis):
        self.redis = redis

memo = {}


class MemoryCacheProvider(AbstractCacheProvider):

    def set(self, key, value):
        memo[key] = value
        return memo[key]

    def get(self, key):
        return memo[key] if key in memo else None

    def increment(self, key):
        memo[key] += 1

    def decrement(self, key):
        memo[key] -= 1
