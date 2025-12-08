from typing import TypeVar, List

from geonames.application.dtos.geoname_dto import GeonameDTO
from geonames.infrastructure.persistence.models.geoname_model import GeonameModel

T = TypeVar("T")

class GeonameOutputMapper:

    @staticmethod
    def from_model(model: GeonameModel) -> GeonameDTO:

        return GeonameDTO(
            geoname_id=model.geoname_id,
            name=model.name,
            asciiname=getattr(model, "asciiname", None),
            alternatenames=getattr(model, "alternatenames", None),
            latitude=model.latitude,
            longitude=model.longitude,
            feature_class=model.feature_class,
            feature_code=model.feature_code,
            country_code=model.country_code,
            cc2=getattr(model, "cc2", None),
            admin1_code=getattr(model, "admin1_code", None),
            admin2_code=getattr(model, "admin2_code", None),
            admin3_code=getattr(model, "admin3_code", None),
            admin4_code=getattr(model, "admin4_code", None),
            population=getattr(model, "population", 0),
            elevation=getattr(model, "elevation", None),
            dem=getattr(model, "dem", None),
            timezone=getattr(model, "timezone", None),
            modification_date=getattr(model, "modification_date", None),
            admin1_name=getattr(model, "admin1_name", None),
            country_name=getattr(model, "country_name", None),
            postal_code_regex=getattr(model, "postal_code_regex", None),
        )

    @staticmethod
    def from_models(models: List[GeonameModel]) -> List[GeonameDTO]:
        return [GeonameOutputMapper.from_model(model) for model in models]