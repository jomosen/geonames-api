from typing import TypeVar, List

from geonames.application.dtos.country_dto import CountryDTO
from geonames.infrastructure.persistence.models.country_model import CountryModel

T = TypeVar("T")

class CountryOutputMapper:

    @staticmethod
    def from_model(model: CountryModel) -> CountryDTO:

        return CountryDTO(
            geoname_id=model.geoname_id,
            iso_alpha2=model.iso_alpha2,
            iso_alpha3=getattr(model, "iso_alpha3", None),
            iso_numeric=getattr(model, "iso_numeric", None),
            fips_code=getattr(model, "fips_code", None),
            country_name=model.country_name,
            capital=getattr(model, "capital", None),
            area_sqkm=getattr(model, "area_sqkm", None),
            population=getattr(model, "population", None),
            continent=getattr(model, "continent", None),
            tld=getattr(model, "tld", None),
            currency_code=getattr(model, "currency_code", None),
            currency_name=getattr(model, "currency_name", None),
            phone=getattr(model, "phone", None),
            postal_code_format=getattr(model, "postal_code_format", None),
            postal_code_regex=getattr(model, "postal_code_regex", None),
            languages=getattr(model, "languages", None),
            neighbours=getattr(model, "neighbours", None),
            equivalent_fips_code=getattr(model, "equivalent_fips_code", None),
        )

    @staticmethod
    def from_models(models: List[CountryModel]) -> List[CountryDTO]:
        return [CountryOutputMapper.from_model(model) for model in models]
