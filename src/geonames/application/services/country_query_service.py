from typing import List

from geonames.application.dtos.country_dto import CountryDTO
from geonames.application.mappers.country_output_mapper import CountryOutputMapper
from geonames.application.ports.query_repository_port import QueryRepositoryPort


class CountryQueryService:

    def __init__(self, country_query_repo: QueryRepositoryPort):
        self.country_query_repo = country_query_repo
        
    def list_countries(self, filters: dict) -> List[CountryDTO]:
        models = self.country_query_repo.find_all(filters)
        dtos = CountryOutputMapper.from_models(models)
        return dtos