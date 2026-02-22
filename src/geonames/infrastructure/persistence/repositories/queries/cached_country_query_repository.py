import hashlib
import json
from typing import Optional

from geonames.application.ports.cache_port import CachePort, CacheContext
from geonames.infrastructure.cache.cache_serializer import models_to_json, json_to_namespaces
from geonames.infrastructure.persistence.repositories.queries.orm_country_query_repository import (
    OrmCountryQueryRepository,
)


class CachedCountryQueryRepository:
    """
    Cached decorator for OrmCountryQueryRepository.
    Uses a separate base from CachedGeonameQueryRepository because
    OrmCountryQueryRepository returns full ORM model instances, not Row objects.
    """

    _cache_prefix = "countries"

    def __init__(self, orm_repo: OrmCountryQueryRepository, cache: CachePort, ttl: int = 3600, context: Optional[CacheContext] = None):
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
        models = self._orm.find_all(filters)
        self._cache.set(key, models_to_json(models), ttl=self._ttl)
        return models
