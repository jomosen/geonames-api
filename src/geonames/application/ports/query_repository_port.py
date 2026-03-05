from typing import Optional, Protocol, Tuple


class QueryRepositoryPort(Protocol):
    def find_all(self, filters: dict, expand: list[str] | None, limit: int, offset: int):
        ...

    def avg_population(self, filters: dict) -> Tuple[Optional[float], int]:
        ...
