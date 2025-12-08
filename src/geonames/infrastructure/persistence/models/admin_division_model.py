from sqlalchemy import Index

from geonames.infrastructure.persistence.models.geoname_base_model import GeonameBaseModel


class AdminDivisionModel(GeonameBaseModel):

    __tablename__ = "admin_divisions"

    __table_args__ = (
        Index("idx_admin_geonames_country_code", "country_code"),
        Index("idx_admin_geonames_feature_class_code", "feature_class", "feature_code"),
        Index("idx_admin_geonames_admin1", "country_code", "admin1_code"),
        Index("idx_admin_geonames_admin2", "country_code", "admin2_code"),
        Index("idx_admin_geonames_population", "population"),
        Index("idx_admin_geonames_name", "name"),
        Index("idx_admin_geonames_asciiname", "asciiname"),
        Index("idx_admin_geonames_lat_lon", "latitude", "longitude"),
    )