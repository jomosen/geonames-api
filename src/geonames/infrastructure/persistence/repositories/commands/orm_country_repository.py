from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from geonames.domain.repositories.country_repository import CountryRepository
from geonames.domain.entities.country import Country
from geonames.infrastructure.persistence.models.country_model import CountryModel
from geonames.infrastructure.persistence.mappers.country_persistence_mapper import CountryPersistenceMapper


class OrmCountryRepository(CountryRepository):

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, geoname_id: int) -> Optional[Country]:
        model = self.session.get(CountryModel, geoname_id)
        if model:
            return CountryPersistenceMapper.to_entity(model)
        return None

    def find_all(self, filters: Optional[Dict] = None) -> List[Country]:
        query = self.session.query(CountryModel)
        
        if filters:
            if 'iso' in filters:
                query = query.filter(CountryModel.iso == filters['iso'])
            if 'iso3' in filters:
                query = query.filter(CountryModel.iso3 == filters['iso3'])
        
        models = query.all()
        return [CountryPersistenceMapper.to_entity(model) for model in models]

    def count_all(self) -> int:
        return self.session.query(func.count(CountryModel.geoname_id)).scalar()

    def save(self, entity: Country) -> None:
        model = CountryPersistenceMapper.to_model(entity)
        existing = self.session.get(CountryModel, model.geoname_id)

        if existing:
            for attr, value in vars(model).items():
                if hasattr(existing, attr) and value is not None:
                    setattr(existing, attr, value)
        else:
            self.session.add(model)

        self.session.commit()
    
    def bulk_insert(self, entities: List[Country]) -> None:
        models = [
            CountryPersistenceMapper.to_model(entity) for entity in entities
        ]
        self.session.bulk_save_objects(models)
        self.session.commit()

    def truncate(self):
        table_name = CountryModel.__tablename__
        self.session.execute(text(f"TRUNCATE TABLE {table_name}"))
        self.session.commit()
