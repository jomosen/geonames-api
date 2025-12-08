from typing import Optional
from decimal import Decimal
from geonames.domain.entities.country import Country
from geonames.infrastructure.persistence.models.country_model import CountryModel


class CountryPersistenceMapper:
    
    @staticmethod
    def to_entity(model: Optional[CountryModel]) -> Optional[Country]:
        
        if model is None:
            return None

        return Country(
            iso_alpha2=model.iso_alpha2,
            iso_alpha3=model.iso_alpha3,
            iso_numeric=model.iso_numeric,
            fips_code=model.fips_code,
            country_name=model.country_name,
            capital=model.capital,
            area_sqkm=model.area_sqkm,
            population=model.population,
            continent=model.continent,
            tld=model.tld,
            currency_code=model.currency_code,
            currency_name=model.currency_name,
            phone=model.phone,
            postal_code_format=model.postal_code_format,
            postal_code_regex=model.postal_code_regex,
            languages=model.languages,
            geoname_id=model.geoname_id,
            neighbours=model.neighbours,
            equivalent_fips_code=model.equivalent_fips_code,
        )

    @staticmethod
    def to_model(entity: Country) -> CountryModel:

        return CountryModel(
            iso_alpha2=entity.iso_alpha2,
            iso_alpha3=entity.iso_alpha3,
            iso_numeric=entity.iso_numeric,
            fips_code=entity.fips_code,
            country_name=entity.country_name,
            capital=entity.capital,
            area_sqkm=entity.area_sqkm,
            population=entity.population,
            continent=entity.continent,
            tld=entity.tld,
            currency_code=entity.currency_code,
            currency_name=entity.currency_name,
            phone=entity.phone,
            postal_code_format=entity.postal_code_format,
            postal_code_regex=entity.postal_code_regex,
            languages=entity.languages,
            geoname_id=entity.geoname_id,
            neighbours=entity.neighbours,
            equivalent_fips_code=entity.equivalent_fips_code,
        )
