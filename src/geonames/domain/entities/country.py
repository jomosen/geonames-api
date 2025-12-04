from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Country:

    iso_alpha2: str
    country_name: str
    geoname_id: int
    iso_alpha3: Optional[str] = None
    iso_numeric: Optional[int] = None
    fips_code: Optional[str] = None
    capital: Optional[str] = None
    area_sqkm: Optional[float] = None
    population: Optional[int] = None
    continent: Optional[str] = None
    tld: Optional[str] = None
    currency_code: Optional[str] = None
    currency_name: Optional[str] = None
    phone: Optional[str] = None
    postal_code_format: Optional[str] = None
    postal_code_regex: Optional[str] = None
    languages: Optional[str] = None
    neighbours: Optional[str] = None
    equivalent_fips_code: Optional[str] = None