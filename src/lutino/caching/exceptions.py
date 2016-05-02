# -*- coding: utf-8 -*-
__author__ = 'vahid'


class CacheError(Exception):
    pass


class CacheTimeoutError(CacheError):
    pass
