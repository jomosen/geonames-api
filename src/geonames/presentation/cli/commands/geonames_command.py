import typer
import os

from dotenv import load_dotenv
from typing import Any, Type

from geonames.infrastructure.persistence.database.init_schema import init_schema
from geonames.infrastructure.persistence.unit_of_work.orm_geonames_unit_of_work import OrmGeonamesUnitOfWorkFactory
from geonames.application.use_cases.import_geonames_use_case import ImportGeonamesUseCase
from geonames.presentation.cli.commands.build_geonames_import_tasks import build_geonames_import_tasks
from shared.infrastructure.adapters.application_logger import ApplicationLogger
from shared.infrastructure.adapters.tqdm_progress_bar import TqdmProgressBar
from shared.infrastructure.persistence.database.database_connection_factory import DatabaseConnectionFactory

load_dotenv()
    
app = typer.Typer()
geonames_import_cli = typer.Typer()


@geonames_import_cli.command("import")
def import_geonames():

    logger = ApplicationLogger()
    logger.info("Import process started")

    db_url = os.getenv("DATABASE_URL")
    db_connector = DatabaseConnectionFactory(db_url)

    init_schema(db_connector.engine)

    uow_factory = OrmGeonamesUnitOfWorkFactory(db_connector)
    import_tasks = build_geonames_import_tasks(logger)
    
    with uow_factory() as uow:

        for task in import_tasks:
            
            _run_import(
                getattr(uow, task["repository_attr"]),
                task["importer_cls"],
                task["description"],
                logger,
            )

    logger.info("Import process finished")

def _run_import(repository: Any, importer: Any, description: str, logger: ApplicationLogger | None = None):

    use_case = ImportGeonamesUseCase(repository, importer, logger)

    try:
        total, insert_generator = use_case.execute()
        if not total:
            if logger:
                logger.info(f"No need to import {description}")
            return

        with TqdmProgressBar(total=total, desc=description, unit="records", colour="green") as progress:
            progress.run(insert_generator)
    
    except Exception as e:
        if logger:
            logger.error(f"Error during {description}: {e}")
        return

    
