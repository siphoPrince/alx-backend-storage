#!/usr/bin/env python3
""" store an instance of the Redis client as a private variable"""


import redis
import uuid

class Cache:
   def __init__(self, host="localhost", port=6379):
       self._redis = redis.Redis(host=host, port=port)
       self._redis.flushdb()  # Flush the Redis database

   def store(self, data: Union[str, bytes, int, float]) -> str:
       """Stores data in the cache and returns a random key.

       Args:
           data: The data to store, can be a str, bytes, int, or float.

       Returns:
           The randomly generated key used to store the data.
       """

       key = str(uuid.uuid4())  # Generate a random UUID key
       self._redis.set(key, data)  # Store the data in Redis
       return key
