from typing import List, Any

from geonames.infrastructure.file_importer.mappers.base_file_row_mapper import BaseFileRowMapper
from geonames.domain.entities.country import Country


class CountryFileRowMapper(BaseFileRowMapper[Country]):

    def to_entity(self, row: List[Any]) -> Country:

        return Country(
            iso_alpha2=row[0],
            iso_alpha3=row[1] or None,
            iso_numeric=int(row[2]) if row[2] else None,
            fips_code=row[3] or None,
            country_name=row[4],
            capital=row[5] or None,
            area_sqkm=float(row[6]) if row[6] else None,
            population=int(row[7]) if row[7] else None,
            continent=row[8] or None,
            tld=row[9] or None,
            currency_code=row[10] or None,
            currency_name=row[11] or None,
            phone=row[12] or None,
            postal_code_format=row[13] or None,
            postal_code_regex=row[14] or None,
            languages=row[15] or None,
            geoname_id=int(row[16]) if row[16] else None,
            neighbours=row[17] or None,
            equivalent_fips_code=row[18] or None,
        )
