from abc import ABC, abstractmethod


class FileDownloaderPort(ABC):

    @abstractmethod
    def download(self, url: str, dest_path: str) -> None:
        raise NotImplementedError