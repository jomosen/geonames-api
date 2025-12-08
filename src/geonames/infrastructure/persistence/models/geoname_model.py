from sqlalchemy import Index

from .geoname_base_model import GeonameBaseModel


class GeonameModel(GeonameBaseModel):

    __tablename__ = "geonames"

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