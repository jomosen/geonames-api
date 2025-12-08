import os
import zipfile
import csv
import mmap

from pathlib import Path
from dotenv import load_dotenv
from typing import Generator, TypeVar

from geonames.application.ports.geoname_importer_port import GeonameImporterPort
from geonames.infrastructure.file_importer.mappers.base_file_row_mapper import BaseFileRowMapper
from shared.application.ports.logger_port import LoggerPort
from shared.application.ports.file_downloader_port import FileDownloaderPort
from shared.infrastructure.adapters.exceptions.zip_unpack_error import ZipUnpackError

T = TypeVar("T")


class BaseGeonameFileImporter(GeonameImporterPort[T]):

    def __init__(self, 
                 download_url: str, 
                 file_downloader: FileDownloaderPort,
                 mapper: BaseFileRowMapper, 
                 logger: LoggerPort | None = None):

        self.DOWNLOAD_URL = download_url
        self.file_downloader = file_downloader
        self.mapper = mapper
        self.logger = logger

        load_dotenv()

        self.FILENAME = Path(self.DOWNLOAD_URL.split('/')[-1])
        self.IS_ZIPPED = self.FILENAME.suffix.lower() == ".zip"

        self.temp_path = Path(os.getenv("TEMP_PATH", "./tmp"))
        self.temp_path.mkdir(parents=True, exist_ok=True)
        
        self.download_target_path = self.temp_path / self.FILENAME
        
        if self.IS_ZIPPED:
            self.read_target_path = self.temp_path / self.FILENAME.with_suffix(".txt")
        else:
            self.read_target_path = self.download_target_path

    def ensure_data_is_available(self) -> None:

        if self.read_target_path.exists() or self.download_target_path.exists():
            return

        self.download_file()

        if self.IS_ZIPPED:
            self.extract_file()

    def download_file(self) -> None:
        self.file_downloader.download(self.DOWNLOAD_URL, str(self.download_target_path))
    
    def extract_file(self) -> None:

        zip_path = self.download_target_path
        if not zip_path.exists():
            return

        txt_filename_in_zip = self.read_target_path.name 

        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extract(txt_filename_in_zip, self.temp_path)

        except Exception as e:
            if os.path.exists(zip_path):
                os.remove(zip_path)

            raise ZipUnpackError(f"Failed to unpack {zip_path}: {e}") from e

    def count_total_records(self) -> int:
        file_path = self.read_target_path

        if not file_path.exists() or os.path.getsize(file_path) == 0:
            return 0

        try:
            with open(file_path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    count = 0
                    for raw_line in iter(mm.readline, b""):
                        line = raw_line.decode("utf-8", errors="ignore").strip()
                        if not line or line.startswith("#"):
                            continue
                        count += 1
                    return count
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading file with mmap: {e}. Returning 0 records.")
            return 0
        
    def load_entities(self) -> Generator[T, None, None]:

        for raw_row in self.read_raw_data():
            try:
                entity = self.mapper.to_entity(raw_row)
                yield entity
            except ValueError:
                continue
            except Exception as e:
                print(f"Error processing row {raw_row}: {e}")

        self.cleanup()
            
    def read_raw_data(self) -> Generator[list[str], None, None]:

        file_path = self.read_target_path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if not row or row[0].startswith("#"):
                    continue
                yield row

    def cleanup(self) -> None:

        if self.download_target_path.exists():
            self.download_target_path.unlink()