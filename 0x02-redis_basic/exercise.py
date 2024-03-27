#!/usr/bin/env python3
""" store an instance of the Redis client as a private variable"""


import redis
import uuid
from typing import Callable, Union
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ Stores history of inputs and outputs for a particular function
    """
    qualified_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Add call_history params to one list in Redis
            and store its ouput in anoter list
        """
        self._redis.rpush(qualified_name + ':inputs', str(args))
        self._redis.rpush(
            qualified_name + ':outputs',
            method(self, *args, **kwargs)
        )
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """case class"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, bytes]:
        return self.get(key, fn=int)

    def count_calls(method: Callable) -> Callable:
    """ Counts how many times methods of Cache class are called
    """
    method_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increment method call number
        """
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)

    return wrapper
