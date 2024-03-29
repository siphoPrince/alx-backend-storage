#!/usr/bin/env python3
"""get page"""


import requests
import redis
import functools


def track_url_access_count(method):
    """track url"""
    @functools.wraps(method)
    def wrapper(url, *args, **kwargs):
        """Initialize Redis client"""
        redis_client = redis.Redis()

        """ Track URL access count"""
        count_key = f"count:{url}"
        access_count = redis_client.incr(count_key)

        return method(url, *args, **kwargs)
    return wrapper

def cache_content(method):
    """main cahce"""
    @functools.wraps(method)
    def wrapper(url, *args, **kwargs):
        """ Initialize Redis client"""
        redis_client = redis.Redis()

        """ If URL content is cached, return it"""
        cache_key = f"content:{url}"
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")

        """ Retrieve HTML content from URL"""
        content = method(url, *args, **kwargs)

        """Cache HTML content with expiration time of 10 seconds"""
        redis_client.setex(cache_key, 10, content)

        return content
    return wrapper

@track_url_access_count
@cache_content
def get_page(url: str) -> str:
    """get page"""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
