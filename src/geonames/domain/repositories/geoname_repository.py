from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from geonames.domain.entities.geoname import Geoname


class GeonameRepository(ABC):

    @abstractmethod
    def save(self, entity: Geoname) -> None:
        pass

    @abstractmethod
    def bulk_insert(self, entities: List[Geoname]) -> None:
        pass

    @abstractmethod
    def truncate(self) -> None:
        pass
