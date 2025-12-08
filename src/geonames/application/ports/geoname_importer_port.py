from abc import ABC, abstractmethod
from typing import Generator, TypeVar, Generic

T = TypeVar("T")

class GeonameImporterPort(ABC, Generic[T]):

    @abstractmethod
    def ensure_data_is_available(self) -> None:
        pass

    @abstractmethod
    def load_entities(self) -> Generator[T, None, None]:
        pass

    @abstractmethod
    def count_total_records(self) -> int:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass
