from abc import ABC, abstractmethod
from typing import Iterable, Callable, Any


class ProgressBarPort(ABC):

    def __init__(self, *args, **kwargs) -> None: ...

    @abstractmethod
    def __enter__(self) -> "ProgressBarPort":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    @abstractmethod
    def update(self, step: int = 1):
        raise NotImplementedError

    @abstractmethod
    def write(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def run(self, iterable: Iterable[Any], process: Callable[[Any], int | None] | None = None):
        """
        Iterate through an iterable, updating progress automatically.

        Args:
            iterable: Any iterable or generator.
            process: Optional callable executed on each element,
                     returning how much to advance the bar.
        """
        raise NotImplementedError
