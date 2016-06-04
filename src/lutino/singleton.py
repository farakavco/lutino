class SingletonMeta(type):
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


if __name__ == '__main__':

    class A(object):
        pass


    class B(object):
        pass


    class MyClass(A, B, metaclass=SingletonMeta):
        pass


    c1 = MyClass()
    c2 = MyClass()
    c3 = MyClass()
    c4 = MyClass()
    assert c1 is c2
    assert c1 is c3
    assert c1 is c4
