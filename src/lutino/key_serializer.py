# -*- coding: utf-8 -*-
__author__ = 'vahid'


class BaseKeySerializer(object):

    def dumps(self, v):
        raise NotImplementedError()

    def loads(self, v):
        raise NotImplementedError()


class XorKeySerializer(BaseKeySerializer):

    def __init__(self, secret):
        self.secret = int(secret)

    def dumps(self, v):
        assert isinstance(v, int)
        return hex(v ^ self.secret)[2:]

    def loads(self, v):
        return int(v, 16) ^ self.secret


if __name__ == '__main__':
    s = XorKeySerializer(34523534)

    for i in range(2 ** 16):
        d = s.dumps(i)
        if i % 1000000:
            print(i, d)
        assert i == s.loads(d)
