import json
from typing import Optional, Tuple

from geonames.application.ports.cache_port import CachePort, CacheContext
from geonames.infrastructure.cache.cache_serializer import _GeonamesEncoder
from geonames.infrastructure.persistence.repositories.queries.cached_geoname_query_repository import (
    CachedGeonameQueryRepository,
)
from geonames.infrastructure.persistence.repositories.queries.orm_city_query_repository import (
    OrmCityQueryRepository,
)


class CachedCityQueryRepository(CachedGeonameQueryRepository):

    _cache_prefix = "cities"

    def __init__(self, orm_repo: OrmCityQueryRepository, cache: CachePort, ttl: int = 3600, context: Optional[CacheContext] = None):
        super().__init__(orm_repo, cache, ttl, context)

    def avg_population(self, filters: Optional[dict] = None) -> Tuple[Optional[float], int]:
        filters = filters or {}
        key = self._make_key("avg_population", filters)

        cached = self._cache.get(key)
        if cached:
            self._mark(True)
            d = json.loads(cached)
            return d["avg"], d["count"]

        self._mark(False)
        avg, count = self._orm.avg_population(filters)
        self._cache.set(
            key,
            json.dumps({"avg": avg, "count": count}, cls=_GeonamesEncoder),
            ttl=self._ttl,
        )
        return avg, count
