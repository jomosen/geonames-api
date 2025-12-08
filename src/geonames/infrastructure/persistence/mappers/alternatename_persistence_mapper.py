from typing import Optional
from geonames.domain.entities.alternate_name import AlternateName
from geonames.infrastructure.persistence.models.alternate_name_model import AlternateNameModel


class AlternateNamePersistenceMapper:

    @staticmethod
    def to_entity(model: Optional[AlternateNameModel]) -> Optional[AlternateName]:

        if model is None:
            return None
        
        return AlternateName(
            alternate_name_id=model.alternate_name_id,
            geoname_id=model.geoname_id,
            alternate_name=model.alternate_name,
            iso_language=model.iso_language,
            is_preferred_name=model.is_preferred_name,
            is_short_name=model.is_short_name,
            is_colloquial=model.is_colloquial,
            is_historic=model.is_historic,
        )

    @staticmethod
    def to_model(entity: AlternateName) -> AlternateNameModel:
        return AlternateNameModel(
            alternate_name_id=entity.alternate_name_id,
            geoname_id=entity.geoname_id,
            alternate_name=entity.alternate_name,
            iso_language=entity.iso_language,
            is_preferred_name=entity.is_preferred_name,
            is_short_name=entity.is_short_name,
            is_colloquial=entity.is_colloquial,
            is_historic=entity.is_historic,
        )
