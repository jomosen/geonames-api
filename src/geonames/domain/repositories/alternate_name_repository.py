from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from geonames.domain.entities.alternate_name import AlternateName


class AlternateNameRepository(ABC):

    @abstractmethod
    def find_by_id(self, alternate_name_id: int) -> Optional[AlternateName]:
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict] = None) -> List[AlternateName]:
        pass

    @abstractmethod
    def save(self, entity: AlternateName) -> None:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def bulk_insert(self, entities: List[AlternateName]) -> None:
        pass

    @abstractmethod
    def truncate(self) -> None: 
        pass
