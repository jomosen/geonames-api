from typing import List

from geonames.application.dtos.geoname_dto import GeonameDTO
from geonames.application.dtos.city_stats_dto import CityStatsDTO
from geonames.application.mappers.geoname_output_mapper import GeonameOutputMapper
from geonames.application.ports.query_repository_port import QueryRepositoryPort


class CityQueryService:

    def __init__(self, city_query_repo: QueryRepositoryPort):
        self.city_query_repo = city_query_repo

    def list_cities(self, filters: dict) -> List[GeonameDTO]:
        models = self.city_query_repo.find_all(filters)
        dtos = GeonameOutputMapper.from_models(models)
        return dtos

    def get_avg_population(self, filters: dict) -> CityStatsDTO:
        avg, count = self.city_query_repo.avg_population(filters)
        return CityStatsDTO(
            avg_population=float(avg) if avg is not None else None,
            city_count=count,
        )