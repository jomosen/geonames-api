from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from geonames.domain.entities.country import Country


class CountryGeoNameRepository(ABC):

    @abstractmethod
    def find_by_id(self, geoname_id: int) -> Optional[Country]:
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict] = None) -> List[Country]:
        pass

    @abstractmethod
    def save(self, entity: Country) -> None:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def bulk_insert(self, entities: List[Country]) -> None:
        pass

    @abstractmethod
    def truncate(self) -> None:
        pass
