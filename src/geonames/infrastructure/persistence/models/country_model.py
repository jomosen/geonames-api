from sqlalchemy import Column, String,Integer, BigInteger, CHAR, Float

from geonames.infrastructure.persistence.database.base import GeonamesBase as Base


class CountryModel(Base):

    __tablename__ = "countries"

    geoname_id = Column(Integer, primary_key=True)
    iso_alpha2 = Column(CHAR(2), unique=True)
    iso_alpha3 = Column(CHAR(3))
    iso_numeric = Column(Integer)
    fips_code = Column(CHAR(2))
    country_name = Column(String(100), nullable=False)
    capital = Column(String(100))
    area_sqkm = Column(Float)                       
    population = Column(BigInteger)
    continent = Column(CHAR(2))                     
    tld = Column(String(10))                        
    currency_code = Column(CHAR(3))
    currency_name = Column(String(50))
    phone = Column(String(20))
    postal_code_format = Column(String(50))
    postal_code_regex = Column(String(200))
    languages = Column(String(200))
    neighbours = Column(String(100))
    equivalent_fips_code = Column(String(10))
