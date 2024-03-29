#!/usr/bin/env python3
""" store an instance of the Redis client as a private variable"""


import redis
import uuid
from typing import Unioni, Callable

class Cache:
    """main class"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @functools.wraps
    def count_calls(method: Callable):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data):
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

     def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, bytes, None]:
        return self.get(key, fn=int)
