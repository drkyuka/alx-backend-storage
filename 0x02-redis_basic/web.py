#! /usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
from time import sleep
from urllib import response
from requests import get
import redis


r = redis.Redis()


def web_tracker(method):
    @wraps(method)
    def wrapper(url: str):
        """Wrapper function to track web requests."""

        # Increment the request count for the URL
        r.incr(f"count:{url}")

        # Check if the response is cached
        if r.get(f"response:{url}"):
            return r.get(f"response:{url}").decode("utf-8")

        # If not cached, make the request and cache the response
        response = method(url)
        r.setex(f"response:{url}", 10, response)

        # Return the response
        return response

    return wrapper


@web_tracker
def get_page(url: str) -> str:
    return get(url).text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    DELAY = 10
    for _ in range(2):
        get_page(url)
    print(f"web data => {r.get(f'response:{url}')}")
    print(f"call count => {r.get(f'count:{url}')}")
    print(f"\nSleeping for {DELAY} seconds...")
    print(f"Waiting for cache to expire...\n")

    sleep(DELAY)  # Wait for the cache to expire

    print(f"After {DELAY} seconds:\n")
    print(f"web data => {r.get(f'response:{url}')}")
    print(f"call count => {r.get(f'count:{url}')}")

    r.flushall()  # Clear the Redis database for cleanup
    print("Cache flushed.")
