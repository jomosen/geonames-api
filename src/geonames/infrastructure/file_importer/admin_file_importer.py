import os
import mmap
from typing import Generator
from shared.application.ports.logger_port import LoggerPort
from shared.application.ports.file_downloader_port import FileDownloaderPort
from geonames.infrastructure.file_importer.mappers.base_file_row_mapper import BaseFileRowMapper
from geonames.application.ports.geoname_importer_port import GeonameImporterPort
from geonames.infrastructure.file_importer.base_geoname_file_importer import BaseGeonameFileImporter
from geonames.domain.entities.geoname import Geoname


class AdminDivisionFileImporter(BaseGeonameFileImporter, GeonameImporterPort[Geoname]):

    FILE_URL = "https://download.geonames.org/export/dump/allCountries.zip"

    def __init__(self, file_downloader: FileDownloaderPort, mapper: BaseFileRowMapper[Geoname], logger: LoggerPort | None = None):
        super().__init__(download_url=self.FILE_URL, file_downloader=file_downloader, mapper=mapper, logger=logger)

    def count_total_records(self) -> int:

        file_path = self.read_target_path

        if not file_path.exists() or os.path.getsize(file_path) == 0:
            return 0

        valid_codes = {b"ADM1", b"ADM2", b"ADM3", b"ADM4"}

        try:
            with open(file_path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    count = 0
                    for line in iter(mm.readline, b""):
                        # feature code is in column 7 (index 6 or 7 depending on tab-split)
                        parts = line.split(b"\t")
                        if len(parts) > 7 and parts[7] in valid_codes:
                            count += 1
                    return count

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading file with mmap: {e}. Returning 0 records.")
            return 0


    def load_entities(self) -> Generator[Geoname, None, None]:
        for raw_row in self.read_raw_data():
            try:
                if raw_row[7] not in ('ADM1', 'ADM2', 'ADM3', 'ADM4'):
                    raise ValueError(
                        f"Unsupported GeoName for mapping. Filtering: "
                        f"Feature Code '{raw_row[7]}' must be one of ('ADM1', 'ADM2', 'ADM3', 'ADM4')."
                    )
                yield self.mapper.to_entity(raw_row)
            except ValueError:
                continue
            except Exception as e:
                print(f"Error processing row {raw_row}: {e}")