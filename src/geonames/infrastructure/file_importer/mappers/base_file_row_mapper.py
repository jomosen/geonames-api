from abc import ABC, abstractmethod
from typing import Generic, List, Any, TypeVar

T = TypeVar("T")


class BaseFileRowMapper(ABC, Generic[T]):

    @abstractmethod
    def to_entity(self, row: List[Any]) -> T:
        pass