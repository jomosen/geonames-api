
from sqlalchemy import Engine

from geonames.infrastructure.persistence.database.base import GeonamesBase


def init_schema(engine: Engine):

    import geonames.infrastructure.persistence.models

    GeonamesBase.metadata.create_all(bind=engine)
