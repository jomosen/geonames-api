from abc import ABC, abstractmethod

from shared.application.ports.progress_bar_port import ProgressBarPort


class LoggerPort(ABC):

    @abstractmethod
    def set_progress_bar(self, progress_bar: ProgressBarPort) -> None:
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass