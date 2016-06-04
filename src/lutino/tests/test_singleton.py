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

        self.assertIs(MyClass(), MyClass())
        self.assertEqual(init_called, 2)


if __name__ == '__main__':
    unittest.main()
