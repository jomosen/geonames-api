from typing import Optional, Tuple, Type
from sqlalchemy import func
from sqlalchemy.orm import Session
from geonames.infrastructure.persistence.models.city_model import CityModel
from .orm_geoname_query_repository import OrmGeonameQueryRepository


class OrmCityQueryRepository(OrmGeonameQueryRepository):

    def __init__(self,
                 session: Session,
                 model_class: Type[CityModel] = CityModel):

        self.session = session
        self.model_class = model_class

    def avg_population(self, filters: Optional[dict] = None) -> Tuple[Optional[float], int]:
        filters = filters or {}

        query = self.session.query(
            func.avg(self.model_class.population),
            func.count(self.model_class.geoname_id),
        )

        query = self._apply_basic_filters(filters, query)

        avg, count = query.one()
        return avg, count