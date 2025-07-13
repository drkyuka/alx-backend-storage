#!/usr/bin/env python3
"""
Main file
"""

import redis

Cache = __import__("exercise").Cache
replay = __import__("exercise").replay

cache = Cache()

print(f"{'*' * 20} Task 1 {'*' * 20}\n")
data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

cache.flush()

print(f"\n{'*' * 20} Task 2 {'*' * 20}\n")
TEST_CASES = {b"foo": None, 123: int, "bar": lambda d: d.decode("utf-8")}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    result = cache.get(key, fn=fn)
    print(f"Input: {value}, Output: {result} with key as {key}")
    assert result == value
    print(f"stringify: {cache.get_str(key, fn)}")
    print(f"Intensify: {cache.get_int(key, fn)}\n")


cache.flush()

print(f"\n{'*' * 20} Task 3 {'*' * 20}\n")

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))


cache.flush()

print(f"\n{'*' * 20} Task 4 {'*' * 20}\n")

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))


cache.flush()

print(f"\n{'*' * 20} Task 5 {'*' * 20}\n")

cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
