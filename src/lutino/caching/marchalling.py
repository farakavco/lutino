# -*- coding: utf-8 -*-
import ujson
__author__ = 'vahid'


def serialize(o):
    return ujson.dumps(o)


def deserialize(s):
    return ujson.loads(s.decode())
