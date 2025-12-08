
from shared.application.ports.logger_port import LoggerPort
from shared.application.ports.file_downloader_port import FileDownloaderPort
from geonames.application.ports.geoname_importer_port import GeonameImporterPort
from geonames.infrastructure.file_importer.mappers.base_file_row_mapper import BaseFileRowMapper
from geonames.infrastructure.file_importer.base_geoname_file_importer import BaseGeonameFileImporter
from geonames.domain.entities.country import Country


class CountriesFileImporter(BaseGeonameFileImporter, GeonameImporterPort[Country]):

    FILE_URL = "https://download.geonames.org/export/dump/countryInfo.txt"

    def __init__(self, file_downloader: FileDownloaderPort, mapper: BaseFileRowMapper[Country], logger: LoggerPort | None = None):
        super().__init__(download_url=self.FILE_URL, file_downloader=file_downloader, mapper=mapper, logger=logger)