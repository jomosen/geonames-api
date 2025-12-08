import os

from geonames.application.services.country_query_service import CountryQueryService
from geonames.application.services.admin_division_query_service import AdminDivisionQueryService
from geonames.application.services.city_query_service import CityQueryService
from geonames.infrastructure.persistence.repositories.queries.orm_city_query_repository import OrmCityQueryRepository
from geonames.infrastructure.persistence.repositories.queries.orm_country_query_repository import OrmCountryQueryRepository
from geonames.infrastructure.persistence.repositories.queries.orm_admin_division_query_repository import OrmAdminDivisionQueryRepository
from shared.infrastructure.persistence.database.database_connection_factory import DatabaseConnectionFactory


db_url = os.getenv("DATABASE_URL")
db_connector = DatabaseConnectionFactory(db_url)


def get_country_query_service() -> CountryQueryService:
    return CountryQueryService(country_query_repo=OrmCountryQueryRepository(db_connector.get_session()))

def get_admin_division_query_service() -> AdminDivisionQueryService:
    return AdminDivisionQueryService(admin_division_query_repo=OrmAdminDivisionQueryRepository(db_connector.get_session()))

def get_city_query_service() -> CityQueryService:
    return CityQueryService(city_query_repo=OrmCityQueryRepository(db_connector.get_session()))