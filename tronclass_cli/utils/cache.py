import shelve
from datetime import datetime


class CachedItem:
    def __init__(self, value, expire_time):
        self.value = value
        self.expire_time = expire_time


class Cache:
    def __init__(self, cache_file, force_update=False):
        self._shelve = shelve.open(str(cache_file))
        self._force_update = force_update

    def get(self, key, default=None):
        if self._force_update:
            return default
        item = self._shelve.get(key)
        if not item:
            return default
        if item.expire_time is None or item.expire_time >= datetime.now():
            return item.value
        return default

    def set(self, key, value, lifetime=None):
        self._shelve[key] = CachedItem(value, datetime.now() + lifetime if lifetime else None)

    def close(self):
        self._shelve.close()
