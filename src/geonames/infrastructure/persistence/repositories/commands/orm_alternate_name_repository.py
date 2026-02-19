from typing import List, Optional, Dict
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from geonames.domain.entities.alternate_name import AlternateName
from geonames.domain.repositories.alternate_name_repository import AlternateNameRepository
from geonames.infrastructure.persistence.models.alternate_name_model import AlternateNameModel
from geonames.infrastructure.persistence.mappers.alternatename_persistence_mapper import AlternateNamePersistenceMapper


class OrmAlternateNameRepository(AlternateNameRepository):

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, alternate_name_id: int) -> Optional[AlternateName]:
        model = self.session.get(AlternateNameModel, alternate_name_id)
        if model:
            return AlternateNamePersistenceMapper.to_entity(model)
        return None

    def find_all(self, filters: Optional[Dict] = None) -> List[AlternateName]:
        query = self.session.query(AlternateNameModel)
        
        if filters:
            if 'geoname_id' in filters:
                query = query.filter(AlternateNameModel.geoname_id == filters['geoname_id'])
            if 'iso_language' in filters:
                query = query.filter(AlternateNameModel.iso_language == filters['iso_language'])
            if 'is_preferred_name' in filters:
                query = query.filter(AlternateNameModel.is_preferred_name == filters['is_preferred_name'])
        
        models = query.all()
        return [AlternateNamePersistenceMapper.to_entity(model) for model in models]

    def count_all(self) -> int:
        return self.session.query(func.count(AlternateNameModel.alternate_name_id)).scalar()
    
    def save(self, entity: AlternateName) -> None:
        model = AlternateNamePersistenceMapper.to_model(entity)
        self.session.merge(model)
        self.session.commit()
    
    def bulk_insert(self, entities: List[AlternateName]) -> None:
        models = [
            AlternateNamePersistenceMapper.to_model(entity) for entity in entities
        ]
        self.session.bulk_save_objects(models)
        self.session.commit()

    def truncate(self):
        table_name = AlternateNameModel.__tablename__
        self.session.execute(text(f"TRUNCATE TABLE {table_name}"))
        self.session.commit()
