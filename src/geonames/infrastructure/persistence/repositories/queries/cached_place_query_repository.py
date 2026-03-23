from typing import Optional
from geonames.application.ports.cache_port import CachePort, CacheContext
from .cached_geoname_query_repository import CachedGeonameQueryRepository
from .orm_place_query_repository import OrmPlaceQueryRepository


class CachedPlaceQueryRepository(CachedGeonameQueryRepository):

    _cache_prefix = "places"

    def __init__(self, orm_repo: OrmPlaceQueryRepository, cache: CachePort, ttl: int = 3600, context: Optional[CacheContext] = None):
        super().__init__(orm_repo, cache, ttl, context)
