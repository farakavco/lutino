# -*- coding: utf-8 -*-
__author__ = 'vahid'


class CacheError(Exception):
    pass


class CacheTimeoutError(CacheError):
    pass


class KeyInProgressError(CacheError):

    def __init__(self, key):
        self.key = key
        super(KeyInProgressError, self).__init__('The given key is under progress: %s' % key)