#!/usr/bin/env python3
"""
Writing strings to Redis
"""

from uuid import uuid4
from functools import wraps
import redis


def count_calls(method):
    """Decorator to count calls to a function."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to increment call count."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method):
    """Decorator to store the history of calls to a method."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to store call history."""
        key = method.__qualname__
        self._redis.rpush(f"{key}:inputs", str(args))

        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{key}:outputs", result)
        return result

    return wrapper


class Cache:
    """Cache class to handle Redis operations"""

    def __init__(self):
        """Initialize the Cache with a Redis connection"""
        self._redis = redis.Redis()

    @call_history
    @count_calls
    def store(self, data: bytes) -> str:
        """Store data in Redis and return the key"""
        key = uuid4().__str__()
        self._redis.set(key, data)
        return key

    def flush(self):
        """Flush the Redis instance"""
        self._redis.flushdb()

    def get(self, key: str, fn=None):
        """Retrieve data from Redis and apply a function if provided"""
        # print(f"Retrieving key: {key}")
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str, fn=None) -> str:
        """Retrieve a string from Redis using get with decode."""
        result = self.get(key, fn)
        if result is None:
            return ""
        if isinstance(result, bytes):
            return result.decode("utf-8")
        if isinstance(result, str):
            return result

    def get_int(self, key: str, fn=None) -> int:
        """Retrieve an integer from Redis using get with int conversion."""
        result = self.get(key, fn)
        if result is not None and isinstance(result, int):
            return int(result)
        return 0
