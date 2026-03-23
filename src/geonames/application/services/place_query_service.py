from typing import List
from geonames.application.dtos.geoname_dto import GeonameDTO
from geonames.application.mappers.geoname_output_mapper import GeonameOutputMapper
from geonames.application.ports.query_repository_port import QueryRepositoryPort


class PlaceQueryService:

    def __init__(self, place_query_repo: QueryRepositoryPort):
        self.place_query_repo = place_query_repo

    def list_places(self, filters: dict) -> List[GeonameDTO]:
        models = self.place_query_repo.find_all(filters)
        return GeonameOutputMapper.from_models(models)
