import ujson


def serialize(o):
    return ujson.dumps(o)


def deserialize(s):
    return ujson.loads(s.decode())
