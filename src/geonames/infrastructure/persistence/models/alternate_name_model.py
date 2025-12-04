from sqlalchemy import Column, Index, Integer, String, Boolean, ForeignKey
from geonames.infrastructure.persistence.database.base import GeonamesBase as Base


class AlternateNameModel(Base):

    __tablename__ = "alternate_names"

    alternate_name_id = Column(Integer, primary_key=True, autoincrement=False)
    geoname_id = Column(Integer, index=True, nullable=False)
    alternate_name = Column(String(400), nullable=False)
    iso_language = Column(String(7), nullable=True)
    is_preferred_name = Column(Boolean, default=False)
    is_short_name = Column(Boolean, default=False)
    is_colloquial = Column(Boolean, default=False)
    is_historic = Column(Boolean, default=False)

    __table_args__ = (
        Index("idx_altname_geoname_id", "geoname_id"),
        Index("idx_altname_lang_preferred", "iso_language", "is_preferred_name"),
        Index("idx_altname_short", "is_short_name"),
        Index("idx_altname_name", "alternate_name")
    )
