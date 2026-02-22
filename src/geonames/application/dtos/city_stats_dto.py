from pydantic import BaseModel, Field
from typing import Optional


class CityStatsDTO(BaseModel):
    avg_population: Optional[float] = Field(None, description="Average population of the matched cities")
    city_count: int = Field(..., description="Number of cities matching the filters")
