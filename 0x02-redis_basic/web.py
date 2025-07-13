#! /usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
from time import sleep
from requests import get
import redis


r = redis.Redis()


def web_tracker(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        """Wrapper function to track web requests."""
        key = f"count:{args[0]}"
        r.incr(key)
        result = method(*args, **kwargs)
        r.set(f"cache:{args[0]}", result, ex=10)
        return result

    return wrapper


@web_tracker
def get_page(url: str) -> str:
    response = get(url)
    if response.status_code == 200:
        return response.text
    return "Error fetching page"


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    DELAY = 10
    for _ in range(2):
        get_page(url)
    print(f"web data => {r.get(f'cache:{url}')}")
    print(f"call count => {r.get(f'count:{url}')}")
    print(f"\nSleeping for {DELAY} seconds...")
    print(f"Waiting for cache to expire...\n")

    sleep(DELAY)  # Wait for the cache to expire

    print(f"After {DELAY} seconds:\n")
    print(f"web data => {r.get(f'cache:{url}')}")
    print(f"call count => {r.get(f'count:{url}')}")

    r.flushall()  # Clear the Redis database for cleanup
    print("Cache flushed.")
