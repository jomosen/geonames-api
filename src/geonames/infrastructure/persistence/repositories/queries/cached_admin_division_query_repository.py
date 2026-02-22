from typing import Optional

from geonames.application.ports.cache_port import CachePort, CacheContext
from geonames.infrastructure.persistence.repositories.queries.cached_geoname_query_repository import (
    CachedGeonameQueryRepository,
)
from geonames.infrastructure.persistence.repositories.queries.orm_admin_division_query_repository import (
    OrmAdminDivisionQueryRepository,
)


class CachedAdminDivisionQueryRepository(CachedGeonameQueryRepository):

    _cache_prefix = "admin_divisions"

    def __init__(self, orm_repo: OrmAdminDivisionQueryRepository, cache: CachePort, ttl: int = 3600, context: Optional[CacheContext] = None):
        super().__init__(orm_repo, cache, ttl, context)
