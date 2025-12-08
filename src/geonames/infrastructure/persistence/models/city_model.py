from sqlalchemy import Index

from geonames.infrastructure.persistence.models.geoname_base_model import GeonameBaseModel


class CityModel(GeonameBaseModel):

    __tablename__ = "cities"

    __table_args__ = (
        Index("idx_city_geonames_country_code", "country_code"),
        Index("idx_city_geonames_feature_class_code", "feature_class", "feature_code"),
        Index("idx_city_geonames_admin1", "country_code", "admin1_code"),
        Index("idx_city_geonames_admin2", "country_code", "admin2_code"),
        Index("idx_city_geonames_population", "population"),
        Index("idx_city_geonames_name", "name"),
        Index("idx_city_geonames_asciiname", "asciiname"),
        Index("idx_city_geonames_lat_lon", "latitude", "longitude"),
    )