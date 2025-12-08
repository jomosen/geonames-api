
from sqlalchemy import Engine

from geonames.infrastructure.persistence.database.base import GeonamesBase


def init_schema(engine: Engine):

    import geonames.infrastructure.persistence.models.geoname_base_model
    import geonames.infrastructure.persistence.models.geoname_model
    import geonames.infrastructure.persistence.models.alternate_name_model
    import geonames.infrastructure.persistence.models.country_model
    import geonames.infrastructure.persistence.models.admin_division_model
    import geonames.infrastructure.persistence.models.city_model

    GeonamesBase.metadata.create_all(bind=engine)
