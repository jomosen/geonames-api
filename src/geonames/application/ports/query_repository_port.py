from typing import Protocol


class QueryRepositoryPort(Protocol):
    def find_all(self, filters: dict, expand: list[str] | None, limit: int, offset: int):
        ...
