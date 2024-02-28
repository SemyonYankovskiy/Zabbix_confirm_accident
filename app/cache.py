from datetime import datetime, timedelta
from typing import Any


class InMemoryCache:
    def __init__(self):
        self._cache = {}
        self._cache_size = 0

    def __len__(self) -> int:
        return self._cache_size

    def get(self, key) -> Any:
        if key in self._cache:
            return self._cache[key]["data"]
        return None

    def set(self, key, value, timeout: int) -> None:
        self._cache[key] = {"data": value, "expires": datetime.now() + timedelta(seconds=timeout)}
        self._cache_size += 1

    def delete(self, key) -> None:
        self._cache.pop(key, None)

    def get_or_cache(self, timeout: int, function, *args, **kwargs) -> Any:
        cache_data = self._cache.get(function.__name__, None)
        if cache_data is not None and cache_data["expires"] > datetime.now():
            return cache_data["data"]

        result = function(*args, **kwargs)
        self.set(function.__name__, result, timeout)
        return result


cache = InMemoryCache()
