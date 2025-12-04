from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)
class Geoname:

    geoname_id: int
    name: Optional[str] = None
    asciiname: Optional[str] = None
    alternatenames: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    feature_class: Optional[str] = None
    feature_code: Optional[str] = None
    country_code: Optional[str] = None
    cc2: Optional[str] = None
    admin1_code: Optional[str] = None
    admin2_code: Optional[str] = None
    admin3_code: Optional[str] = None
    admin4_code: Optional[str] = None
    population: Optional[int] = None
    elevation: Optional[int] = None
    dem: Optional[int] = None
    timezone: Optional[str] = None
    modification_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
