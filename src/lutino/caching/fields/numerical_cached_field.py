from lutino.caching.fields.base import CachedField, MemoryCacheProvider


class NumericalCachedField(CachedField):
    __provider__ = MemoryCacheProvider()

    def __init__(self, model_name, model_identity, field_name, fetcher, ttl=None, type_=int):
        self.model_name = model_name
        self.model_identity = model_identity
        self.field_name = field_name
        self.fetcher = fetcher
        self.ttl = ttl
        self.type_ = type_

    def __iadd__(self, other):
        self.set(self.value() + other)
        # self.increment()
        return self

    def __isub__(self, other):
        self.set(self.value() - other)
        # self.decrement()
        return self

    @property
    def key(self):
        return '%s_%s_%s' % (self.model_name, self.model_identity, self.field_name)

    def value(self):
        return self.type_(self.get())

    def get(self):
        value = self.__provider__.get(self.key)

        if value is None:
            value = self.__provider__.set(self.key, self.fetch())

        return value

    def set(self, value=None, ttl=None):
        if value is None:
            value = self.fetch()

            if value is None:
                raise ValueError()

        self.__provider__.set(self.key, value)
        return value

    def increment(self):
        self.__provider__.increment(self.key)

    def decrement(self):
        self.__provider__.decrement(self.key)

    def fetch(self):
        return self.fetcher()

    @classmethod
    def decorate(cls):
        raise NotImplementedError()
