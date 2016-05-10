# -*- coding: utf-8 -*-
import time
import threading
from redlock import Redlock
from redis import StrictRedis
__author__ = 'vahid'

threads_count = 4
lock_ttl = 1000


redis = StrictRedis()
redlock = Redlock([redis])
request_count_per_thread = 10


def log(*s):
    print('%s:' % threading.current_thread().name, *s, flush=True)


def lock(key):
    l = False
    while not l:
        l = redlock.lock(key, lock_ttl)
        if l:
            log('Locking, key:', key)
            return l
        log('Waiting for key:', key)
        time.sleep(.3)


def unlock(lock):
    log('Unlocking:', lock.resource)
    redlock.unlock(lock)


def worker():
    for r in range(request_count_per_thread):
        l = lock('akey')
        time.sleep(.1)
        redis.set('a', 'something')

        unlock(l)

        l = lock('akey')
        time.sleep(.1)
        redis.set('b', 'something')
        unlock(l)


if __name__ == '__main__':
    threads = []
    for i in range(threads_count):
        threads.append(threading.Thread(target=worker, name='th-%s' % i))
        threads[-1].start()

    for t in threads:
        t.join()
