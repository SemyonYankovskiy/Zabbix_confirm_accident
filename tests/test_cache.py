import time
from unittest import TestCase

from app.cache import InMemoryCache


class TestCache(TestCase):

    def test_cache(self):
        cache = InMemoryCache()
        execute_count = 0

        def increment(argument: int):
            nonlocal execute_count
            execute_count += argument
            return execute_count

        cache.get_or_cache(1, increment, argument=1)
        self.assertEqual(execute_count, 1)

        cache.get_or_cache(1, increment, argument=1)
        self.assertEqual(execute_count, 1)

        time.sleep(1.1)
        cache.get_or_cache(1, increment, argument=1)
        self.assertEqual(execute_count, 2)
