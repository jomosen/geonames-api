import hashlib
import json
from typing import List, Optional

from geonames.application.ports.cache_port import CachePort, CacheContext
from geonames.infrastructure.cache.cache_serializer import rows_to_json, json_to_namespaces


class CachedGeonameQueryRepository:
    """
    Base decorator for geoname query repositories that adds Redis caching.
    Wraps an ORM repository and caches find_all results transparently.
    """

    _cache_prefix: str = "geonames"

    def __init__(self, orm_repo, cache: CachePort, ttl: int = 3600, context: Optional[CacheContext] = None):
        self._orm = orm_repo
        self._cache = cache
        self._ttl = ttl
        self._context = context

    def _make_key(self, method: str, filters: dict) -> str:
        raw = json.dumps(filters, sort_keys=True, default=str)
        h = hashlib.md5(raw.encode()).hexdigest()
        return f"{self._cache_prefix}:{method}:{h}"

    def _mark(self, hit: bool) -> None:
        if self._context is not None:
            self._context.hit = hit

    def find_all(self, filters: Optional[dict] = None) -> list:
        filters = filters or {}
        key = self._make_key("find_all", filters)

        cached = self._cache.get(key)
        if cached:
            self._mark(True)
            return json_to_namespaces(cached)

        self._mark(False)
        rows = self._orm.find_all(filters)
        self._cache.set(key, rows_to_json(rows), ttl=self._ttl)
        return rows
