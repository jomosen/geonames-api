from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AlternateName:
    
    alternate_name_id: int
    geoname_id: int
    alternate_name: str
    iso_language: Optional[str] = None
    is_preferred_name: bool = False
    is_short_name: bool = False
    is_colloquial: bool = False
    is_historic: bool = False
