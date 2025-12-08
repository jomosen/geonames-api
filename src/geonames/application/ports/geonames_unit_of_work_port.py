from abc import abstractmethod

from geonames.domain.repositories.alternate_name_repository import AlternateNameRepository
from geonames.domain.repositories.country_repository import CountryRepository
from geonames.domain.repositories.geoname_repository import GeonameRepository
from shared.application.ports.unit_of_work_port import UnitOfWorkFactoryPort, UnitOfWorkPort


class GeonamesUnitOfWorkPort(UnitOfWorkPort):

    geoname_repo: "GeonameRepository"
    country_repo: "CountryRepository"
    alternate_name_repo: "AlternateNameRepository"
    admin_division_repo: "GeonameRepository"
    city_repo: "GeonameRepository"

class GeonamesUnitOfWorkFactoryPort(UnitOfWorkFactoryPort):

    @abstractmethod
    def __call__(self) -> "GeonamesUnitOfWorkPort":
        raise NotImplementedError
