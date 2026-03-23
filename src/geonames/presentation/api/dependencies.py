import os
from typing import Generator

from sqlalchemy.orm import Session
from fastapi import Depends

from geonames.application.services.country_query_service import CountryQueryService
from geonames.application.services.admin_division_query_service import AdminDivisionQueryService
from geonames.application.services.city_query_service import CityQueryService
from geonames.application.services.place_query_service import PlaceQueryService
from geonames.infrastructure.persistence.repositories.queries.orm_city_query_repository import OrmCityQueryRepository
from geonames.infrastructure.persistence.repositories.queries.orm_country_query_repository import OrmCountryQueryRepository
from geonames.infrastructure.persistence.repositories.queries.orm_admin_division_query_repository import OrmAdminDivisionQueryRepository
from geonames.infrastructure.persistence.repositories.queries.orm_place_query_repository import OrmPlaceQueryRepository
from geonames.infrastructure.persistence.repositories.queries.cached_city_query_repository import CachedCityQueryRepository
from geonames.infrastructure.persistence.repositories.queries.cached_admin_division_query_repository import CachedAdminDivisionQueryRepository
from geonames.infrastructure.persistence.repositories.queries.cached_country_query_repository import CachedCountryQueryRepository
from geonames.infrastructure.persistence.repositories.queries.cached_place_query_repository import CachedPlaceQueryRepository
from geonames.application.ports.cache_port import CacheContext
from geonames.infrastructure.cache.redis_cache import RedisCache
from shared.infrastructure.persistence.database.database_connection_factory import DatabaseConnectionFactory
from shared.infrastructure.cache.redis_connector import RedisConnector


db_url = os.getenv("DATABASE_URL")
db_connector = DatabaseConnectionFactory(db_url)

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_ttl = int(os.getenv("REDIS_TTL", "3600"))
redis_connector = RedisConnector(redis_url)


def get_db_session() -> Generator[Session, None, None]:
    session = db_connector.get_session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_redis_cache() -> RedisCache:
    return RedisCache(redis_connector.get_client())


def get_cache_context() -> CacheContext:
    return CacheContext()


def get_country_query_service(
    session: Session = Depends(get_db_session),
    cache: RedisCache = Depends(get_redis_cache),
    context: CacheContext = Depends(get_cache_context),
) -> CountryQueryService:
    return CountryQueryService(
        country_query_repo=CachedCountryQueryRepository(
            orm_repo=OrmCountryQueryRepository(session),
            cache=cache,
            ttl=redis_ttl,
            context=context,
        )
    )

def get_admin_division_query_service(
    session: Session = Depends(get_db_session),
    cache: RedisCache = Depends(get_redis_cache),
    context: CacheContext = Depends(get_cache_context),
) -> AdminDivisionQueryService:
    return AdminDivisionQueryService(
        admin_division_query_repo=CachedAdminDivisionQueryRepository(
            orm_repo=OrmAdminDivisionQueryRepository(session),
            cache=cache,
            ttl=redis_ttl,
            context=context,
        )
    )

def get_city_query_service(
    session: Session = Depends(get_db_session),
    cache: RedisCache = Depends(get_redis_cache),
    context: CacheContext = Depends(get_cache_context),
) -> CityQueryService:
    return CityQueryService(
        city_query_repo=CachedCityQueryRepository(
            orm_repo=OrmCityQueryRepository(session),
            cache=cache,
            ttl=redis_ttl,
            context=context,
        )
    )

def get_place_query_service(
    session: Session = Depends(get_db_session),
    cache: RedisCache = Depends(get_redis_cache),
    context: CacheContext = Depends(get_cache_context),
) -> PlaceQueryService:
    return PlaceQueryService(
        place_query_repo=CachedPlaceQueryRepository(
            orm_repo=OrmPlaceQueryRepository(session),
            cache=cache,
            ttl=redis_ttl,
            context=context,
        )
    )
