from typing import List, Any

from geonames.infrastructure.file_importer.mappers.base_file_row_mapper import BaseFileRowMapper
from geonames.domain.entities.geoname import Geoname 


class GeonameFileRowMapper(BaseFileRowMapper[Geoname]):

    def to_entity(self, row: List[Any]) -> Geoname:

        return Geoname(
            geoname_id=int(row[0]),
            name=row[1],
            asciiname=row[2],
            alternatenames=row[3],
            latitude=float(row[4]),
            longitude=float(row[5]),
            feature_class=row[6],
            feature_code=row[7],
            country_code=row[8],
            cc2=row[9],
            admin1_code=row[10],
            admin2_code=row[11],
            admin3_code=row[12],
            admin4_code=row[13],
            population=int(row[14]) if row[14] else 0,
            elevation=int(row[15]) if row[15] else None,
            dem=int(row[16]) if row[16] else None,
            timezone=row[17],
            modification_date=row[18],
        )