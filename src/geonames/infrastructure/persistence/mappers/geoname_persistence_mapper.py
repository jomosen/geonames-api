from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Type, TypeVar
from geonames.domain.entities.geoname import Geoname
from geonames.infrastructure.persistence.models.geoname_model import GeonameModel


class GeonamePersistenceMapper:

    @staticmethod
    def to_model(entity: Geoname, model_class: Type[GeonameModel] = GeonameModel) -> GeonameModel:

        return model_class(
            geoname_id=entity.geoname_id,
            name=entity.name,
            asciiname=entity.asciiname,
            alternatenames=entity.alternatenames,
            latitude=entity.latitude,
            longitude=entity.longitude,
            feature_class=entity.feature_class,
            feature_code=entity.feature_code,
            country_code=entity.country_code,
            cc2=entity.cc2,
            admin1_code=entity.admin1_code,
            admin2_code=entity.admin2_code,
            admin3_code=entity.admin3_code,
            admin4_code=entity.admin4_code,
            population=entity.population,
            elevation=entity.elevation,
            dem=entity.dem,
            timezone=entity.timezone,
            modification_date=entity.modification_date,
            created_at=getattr(entity, "created_at", None),
            updated_at=getattr(entity, "updated_at", None),
        )

    @staticmethod
    def to_entity(model: Optional[GeonameModel]) -> Geoname | None:

        if model is None:
            return None

        return Geoname(
            geoname_id=model.geoname_id,
            name=model.name,
            asciiname=model.asciiname,
            alternatenames=model.alternatenames,
            latitude=float(model.latitude) if isinstance(model.latitude, Decimal) else model.latitude,
            longitude=float(model.longitude) if isinstance(model.longitude, Decimal) else model.longitude,
            feature_class=model.feature_class,
            feature_code=model.feature_code,
            country_code=model.country_code,
            cc2=model.cc2,
            admin1_code=model.admin1_code,
            admin2_code=model.admin2_code,
            admin3_code=model.admin3_code,
            admin4_code=model.admin4_code,
            population=model.population,
            elevation=model.elevation,
            dem=model.dem,
            timezone=model.timezone,
            modification_date=str(model.modification_date) if isinstance(model.modification_date, date) else model.modification_date,
            created_at=model.created_at if isinstance(model.created_at, datetime) else None,
            updated_at=model.updated_at if isinstance(model.updated_at, datetime) else None,
        )
