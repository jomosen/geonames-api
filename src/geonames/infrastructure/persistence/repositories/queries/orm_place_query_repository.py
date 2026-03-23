from typing import Type
from sqlalchemy.orm import Session
from geonames.infrastructure.persistence.models.geoname_model import GeonameModel
from .orm_geoname_query_repository import OrmGeonameQueryRepository


class OrmPlaceQueryRepository(OrmGeonameQueryRepository):

    def __init__(self, session: Session, model_class: Type[GeonameModel] = GeonameModel):
        self.session = session
        self.model_class = model_class
