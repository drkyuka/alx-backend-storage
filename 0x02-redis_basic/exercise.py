#!/usr/bin/env python3
"""
Writing strings to Redis
"""

from uuid import uuid4
import redis


class Cache:
    """Cache class to handle Redis operations"""

    def __init__(self):
        """Initialize the Cache with a Redis connection"""
        self._redis = redis.Redis()

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
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieve a string from Redis"""
        data = self._redis.get(key)
        if data is None:
            return ""
        return str(data.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis"""
        data = self._redis.get(key)
        if data is None:
            return 0
        return int(data.decode("utf-8"))
