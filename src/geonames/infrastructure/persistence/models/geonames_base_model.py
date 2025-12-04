from sqlalchemy import Column, Index, String,Integer, BigInteger, DECIMAL, Date, TIMESTAMP

from geonames.infrastructure.persistence.database.base import GeonamesBase as Base


class GeonamesBaseModel(Base):

    __abstract__ = True

    geoname_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(200))
    asciiname = Column(String(200))
    alternatenames = Column(String(10000))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    feature_class = Column(String(1))
    feature_code = Column(String(10))
    country_code = Column(String(2))
    cc2 = Column(String(200))
    admin1_code = Column(String(20))
    admin2_code = Column(String(80))
    admin3_code = Column(String(20))
    admin4_code = Column(String(20))
    population = Column(BigInteger)
    elevation = Column(Integer)
    dem = Column(Integer)
    timezone = Column(String(40))
    modification_date = Column(Date)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    __table_args__ = (
        Index("idx_geonames_country_code", "country_code"),
        Index("idx_geonames_feature_class_code", "feature_class", "feature_code"),
        Index("idx_geonames_admin1", "country_code", "admin1_code"),
        Index("idx_geonames_admin2", "country_code", "admin2_code"),
        Index("idx_geonames_population", "population"),
        Index("idx_geonames_name", "name"),
        Index("idx_geonames_asciiname", "asciiname"),
        Index("idx_geonames_lat_lon", "latitude", "longitude"),
    )
