from typing import List

from geonames.application.dtos.geoname_dto import GeonameDTO
from geonames.application.mappers.geoname_output_mapper import GeonameOutputMapper
from geonames.application.ports.query_repository_port import QueryRepositoryPort


class AdminDivisionQueryService:

    def __init__(self, admin_division_query_repo: QueryRepositoryPort):
        self.admin_division_query_repo = admin_division_query_repo
        
    def list_admin_divisions(self, filters: dict) -> List[GeonameDTO]:
        models = self.admin_division_query_repo.find_all(filters)
        dtos = GeonameOutputMapper.from_models(models)
        return dtos