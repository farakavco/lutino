# -*- coding: utf-8 -*-
from .exceptions import CacheError, CacheTimeoutError
from .common import create_cache_key
from .marchalling import deserialize, serialize
from .cache_manager import CacheManager, manager, init
from .decorator import cache
__author__ = 'vahid'
