from sqlalchemy.orm import declarative_base
from sqlalchemy import Engine


GeonamesBase = declarative_base()


def init_schema(engine: Engine):

    import geonames.infrastructure.persistence.models

    GeonamesBase.metadata.create_all(bind=engine)
