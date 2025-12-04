from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from geonames.domain.entities.geoname import Geoname


class GeoNameRepository(ABC):

    @abstractmethod
    def find_by_id(self, geoname_id: int) -> Optional[Geoname]:
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict] = None) -> List[Geoname]:
        pass

    @abstractmethod
    def save(self, entity: Geoname) -> None:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def bulk_insert(self, entities: List[Geoname]) -> None:
        pass

    @abstractmethod
    def truncate(self) -> None:
        pass
