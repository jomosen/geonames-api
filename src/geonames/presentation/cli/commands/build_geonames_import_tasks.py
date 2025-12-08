from shared.infrastructure.adapters.tqdm_progress_bar import TqdmProgressBar
from shared.infrastructure.adapters.file_downloader import FileDownloader
from geonames.infrastructure.file_importer.mappers.country_file_row_mapper import CountryFileRowMapper
from geonames.infrastructure.file_importer.mappers.geoname_file_row_importer import GeonameFileRowMapper
from geonames.infrastructure.file_importer.mappers.alternate_name_file_row_mapper import AlternateNameFileRowMapper
from geonames.infrastructure.file_importer.geoname_file_importer import GeonameFileImporter
from geonames.infrastructure.file_importer.countries_file_importer import CountriesFileImporter
from geonames.infrastructure.file_importer.admin_file_importer import AdminDivisionFileImporter
from geonames.infrastructure.file_importer.city_file_importer import CityFileImporter
from geonames.infrastructure.file_importer.alternate_name_file_importer import AlternateNameFileImporter


def build_geonames_import_tasks(logger):
    """Factory that builds the import configuration with injected dependencies."""
    return [
        {
            "description": "Importing Countries",
            "importer_cls": CountriesFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=CountryFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "country_repo",
        },
        {
            "description": "Importing Admin Divisions",
            "importer_cls": AdminDivisionFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=GeonameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "admin_division_repo",
        },
        {
            "description": "Importing Cities",
            "importer_cls": CityFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=GeonameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "city_repo",
        },
        {
            "description": "Importing Alternate Names",
            "importer_cls": AlternateNameFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=AlternateNameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "geoname_alternatename_repo",
        },
        {
            "description": "Importing GeoNames",
            "importer_cls": GeonameFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=GeonameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "geoname_repo",
        },
    ]
