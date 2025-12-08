from typing import List

from geonames.application.dtos.geoname_dto import GeonameDTO
from geonames.application.mappers.geoname_output_mapper import GeonameOutputMapper
from geonames.application.ports.query_repository_port import QueryRepositoryPort


class GeonameQueryService:

    def __init__(self, geoname_query_repo: QueryRepositoryPort):
        self.geoname_query_repo = geoname_query_repo
        
    def list_geonames(self, filters: dict) -> List[GeonameDTO]:
        models = self.geoname_query_repo.find_all(filters)
        dtos = GeonameOutputMapper.from_models(models)
        return dtos