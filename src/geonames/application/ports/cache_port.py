from typing import Optional, Protocol


class CachePort(Protocol):
    def get(self, key: str) -> Optional[str]: ...
    def set(self, key: str, value: str, ttl: int) -> None: ...
    def delete(self, key: str) -> None: ...


class CacheContext:
    """Mutable per-request object that tracks whether the last query was a cache hit."""
    def __init__(self) -> None:
        self.hit: bool = False
