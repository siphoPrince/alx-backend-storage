#!/usr/bin/env python3
""" store an instance of the Redis client as a private variable"""


import redis
import uuid
from typing import Union

class Cache:
    """main class"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
