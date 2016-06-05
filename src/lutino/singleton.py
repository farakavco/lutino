class SingletonMeta(type):
    """
    Usage:

        class MyClass(A, B, metaclass=SingletonMeta):
            pass

        assert MyClass() is MyClass()

    Note: the __init__ method should be called on each MyClass call, but the `self` argument is guaranteed
    to be always the singleton instance.

    """

    _singleton_instances = dict()

    # noinspection PyInitNewSignature
    def __new__(mcs, name, bases, namespace, **kwargs):
        meta_class = type.__new__(mcs, name, bases, namespace, **kwargs)

        def new(cls, *args, **kw):
            if cls in mcs._singleton_instances:
                return mcs._singleton_instances[cls]

            instance = super(meta_class, cls).__new__(cls, *args, **kw)
            if cls not in mcs._singleton_instances:
                mcs._singleton_instances[cls] = instance

            return mcs._singleton_instances[cls]

        meta_class.__new__ = new
        return meta_class
