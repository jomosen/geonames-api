from geonames.application.ports.geonames_unit_of_work_port import GeonamesUnitOfWorkPort
from shared.application.ports.unit_of_work_port import UnitOfWorkFactoryPort
from shared.infrastructure.persistence.database.mysql_connector import MySQLConnector


class OrmGeonamesUnitOfWork(GeonamesUnitOfWorkPort):

    def __init__(self, 
                 session_factory, 
                 geoname_repo_cls, 
                 country_repo_cls, 
                 geoname_alternatename_repo_cls, 
                 admin_division_repo_cls, 
                 city_repo_cls):
        
        self._session_factory = session_factory
        self._geoname_repo_cls = geoname_repo_cls
        self._country_repo_cls = country_repo_cls
        self._geoname_alternatename_repo_cls = geoname_alternatename_repo_cls
        self._admin_division_repo_cls = admin_division_repo_cls
        self._city_repo_cls = city_repo_cls

        self.session = None
        self.geoname_repo = None
        self.country_repo = None
        self.geoname_alternatename_repo = None
        self.admin_division_repo = None
        self.city_repo = None

    def __enter__(self):
        self.session = self._session_factory()
        self.geoname_repo = self._geoname_repo_cls(self.session)
        self.country_repo = self._country_repo_cls(self.session)
        self.geoname_alternatename_repo = self._geoname_alternatename_repo_cls(self.session)
        self.admin_division_repo = self._admin_division_repo_cls(self.session)
        self.city_repo = self._city_repo_cls(self.session)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class OrmGeonamesUnitOfWorkFactory(UnitOfWorkFactoryPort):

    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def __call__(self) -> OrmGeonamesUnitOfWork:

        from geonames.infrastructure.persistence.repositories.commands.orm_geoname_repository import OrmGeonameRepository
        from geonames.infrastructure.persistence.repositories.commands.orm_alternate_name_repository import OrmAlternateNameRepository
        from geonames.infrastructure.persistence.repositories.commands.orm_country_repository import OrmCountryRepository
        from geonames.infrastructure.persistence.repositories.commands.orm_admin_division_repository import OrmAdminDivisionRepository
        from geonames.infrastructure.persistence.repositories.commands.orm_city_repository import OrmCityRepository

        return OrmGeonamesUnitOfWork(
            session_factory=self.connector.get_session,
            geoname_repo_cls=OrmGeonameRepository,
            country_repo_cls=OrmCountryRepository,
            geoname_alternatename_repo_cls=OrmAlternateNameRepository,
            admin_division_repo_cls=OrmAdminDivisionRepository,
            city_repo_cls=OrmCityRepository,
        )
