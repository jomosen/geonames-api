from shared.application.ports.logger_port import LoggerPort
from shared.application.ports.file_downloader_port import FileDownloaderPort
from geonames.infrastructure.file_importer.mappers.base_file_row_mapper import BaseFileRowMapper
from geonames.application.ports.geoname_importer_port import GeonameImporterPort
from geonames.infrastructure.file_importer.base_geoname_file_importer import BaseGeonameFileImporter
from geonames.domain.entities.geoname import Geoname


class GeonameFileImporter(BaseGeonameFileImporter, GeonameImporterPort[Geoname]):

    FILE_URL = "https://download.geonames.org/export/dump/allCountries.zip"

    def __init__(self, 
                 file_downloader: FileDownloaderPort, 
                 mapper: BaseFileRowMapper[Geoname], 
                 logger: LoggerPort | None = None):
        
        super().__init__(download_url=self.FILE_URL, 
                         file_downloader=file_downloader, 
                         mapper=mapper, 
                         logger=logger)