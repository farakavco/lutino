import unittest
from lutino.singleton import SingletonMeta


class TestSingletonMeta(unittest.TestCase):

    def test_singleton_meta(self):
        init_called = 0

        class A(object):
            pass

        class B(object):
            pass

        class MyClass(A, B, metaclass=SingletonMeta):
            def __init__(self):
                nonlocal init_called
                init_called += 1
                self.value1 = 'value1'

        self.assertIs(MyClass(), MyClass())
        self.assertEqual(init_called, 2)
        self.assertEqual(MyClass().value1, MyClass().value1)
        c1 = MyClass()
        c2 = MyClass()
        c1.value1 = 123
        self.assertEqual(c1.value1, 123)
        self.assertEqual(c2.value1, 123)

    def test_singleton_meta_inheritance(self):

        class B(object, metaclass=SingletonMeta):
            pass

        class MyClass(B):
            pass

        class AnotherClass(metaclass=SingletonMeta):
            pass

        self.assertIsNot(MyClass(), B())
        self.assertIs(MyClass(), MyClass())
        self.assertIs(AnotherClass(), AnotherClass())
        self.assertIsNot(MyClass(), AnotherClass())


if __name__ == '__main__':
    unittest.main()
