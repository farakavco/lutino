class SingletonMeta(type):
    """
    Usage:

        class MyClass(A, B, metaclass=SingletonMeta):
            pass

        assert MyClass() is MyClass()

    Note: the __init__ method should be called on each MyClass call, but the `self` argument is guaranteed
    to be always the singleton instance.

    """

    _singleton_instance = None

    # noinspection PyInitNewSignature
    def __new__(mcs, name, bases, namespace, **kwargs):
        class_ = type.__new__(mcs, name, bases, namespace, **kwargs)

        def new(cls, *args, **kw):
            if mcs._singleton_instance is None:
                # mcs._singleton_instance = bases[0].__new__(cls, *args, **kwargs)
                mcs._singleton_instance = super(class_, cls).__new__(cls, *args, **kw)
            return mcs._singleton_instance

        class_.__new__ = new
        return class_
