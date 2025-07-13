#!/usr/bin/env python3
"""
Main file
"""

import redis

Cache = __import__("exercise").Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

TEST_CASES = {b"foo": None, 123: int, "bar": lambda d: d.decode("utf-8")}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    result = cache.get(key, fn=fn)
    print(f"Input: {value}, Output: {result} with key as {key}")
    assert result == value
    print(f"stringify: {cache.get_str(key, fn)}")
    print(f"Intensify: {cache.get_int(key, fn)}\n")


cache.flush()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))
