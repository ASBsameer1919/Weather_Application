# backend/cache_manager.py
import json
import time
from typing import Optional, Any

class CacheManager:
    """
    Very small JSON-file based cache.
    Stores a dict of { key: { ts: <unix>, value: <obj> } }
    TTL is in seconds.
    """
    def __init__(self, filename: str = "cache.json", ttl_seconds: int = 1800):
        self.filename = filename
        self.ttl = ttl_seconds
        # try load existing
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self._store = json.load(f)
        except Exception:
            self._store = {}

    def _save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self._store, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        ts = item.get("ts", 0)
        if time.time() - ts > self.ttl:
            # expired
            self._store.pop(key, None)
            self._save()
            return None
        return item.get("value")

    def set(self, key: str, value: Any):
        self._store[key] = {"ts": time.time(), "value": value}
        self._save()

    def clear(self):
        self._store = {}
        self._save()
