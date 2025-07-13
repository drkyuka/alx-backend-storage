#! /usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
from typing import Callable


from time import sleep, time
import threading
from requests import get
import redis


r = redis.Redis()


def web_tracker(method: callable) -> callable:
    """Decorator to track web requests and cache responses."""

    @wraps(method)
    def wrapper(url: str):
        """Wrapper function to track web requests."""

        # Increment the request count for the URL
        r.incr(f"count:{url}")

        # If not cached, make the request and cache the response
        if not r.get(f"{url}"):
            r.setex(f"{url}", 10, method(url))

        # Return the cached response
        return r.get(f"{url}").decode("utf-8")

    return wrapper


@web_tracker
def get_page(url: str) -> str:
    return get(url).text


def request_during_sleep(url: str, delay: int):
    """
    Function to make requests during sleep time in a separate thread.
    """

    print(f"Thread started: Making requests every 2 seconds for {delay} seconds...")

    start_time = time()
    while time() - start_time < delay:
        try:
            print(f"[Thread] Requesting URL at {time():.2f}...")
            result = get_page(url)
            print(f"[Thread] Response length: {len(result)} chars")
            print(f"[Thread] Call count: {r.get(f'count:{url}').decode('utf-8')}")
            sleep(2)  # Wait 2 seconds between requests
        except Exception as e:
            print(f"[Thread] Error: {e}")
            break

    print("Thread finished.")


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    DELAY = 10

    # Initial requests
    for _ in range(2):
        get_page(url)

    print(f"web data => {r.get(f'{url}')}")
    print(f"call count => {r.get(f'count:{url}')}")
    print(f"\nSleeping for {DELAY} seconds...")
    print(f"Waiting for cache to expire...\n")

    # Start a thread to make requests during sleep
    thread = threading.Thread(target=request_during_sleep, args=(url, DELAY))
    thread.daemon = True
    thread.start()

    sleep(DELAY)  # Wait for the cache to expire

    # Wait for thread to complete
    thread.join()

    print(f"After {DELAY} seconds:\n")
    print(f"web data => {r.get(f'{url}')}")
    print(f"call count => {r.get(f'count:{url}')}")

    r.flushall()  # Clear the Redis database for cleanup
    print("Cache flushed.")
