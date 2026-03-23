from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response

from geonames.application.dtos.city_stats_dto import CityStatsDTO
from geonames.application.dtos.country_dto import CountryDTO
from geonames.application.dtos.geoname_dto import GeonameDTO
from geonames.application.ports.cache_port import CacheContext
from geonames.application.services.city_query_service import CityQueryService
from geonames.application.services.admin_division_query_service import AdminDivisionQueryService
from geonames.application.services.country_query_service import CountryQueryService
from geonames.application.services.place_query_service import PlaceQueryService

from ..dependencies import (
    get_country_query_service,
    get_admin_division_query_service,
    get_city_query_service,
    get_place_query_service,
    get_cache_context,
)


router = APIRouter()


def _set_cache_header(response: Response, context: CacheContext) -> None:
    response.headers["X-Cache"] = "HIT" if context.hit else "MISS"


@router.get("/countries", tags=["countries"], response_model=List[CountryDTO])
def get_countries(
    response: Response,
    country_query_service: CountryQueryService = Depends(get_country_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    iso_alpha2: Optional[str] = Query(None, min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    continent: Optional[str] = Query(None, min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    min_population: Optional[int] = Query(None, ge=0),
    max_population: Optional[int] = Query(None, ge=0),
    currency_code: Optional[str] = Query(None, min_length=3, max_length=3, regex="^(?i)[A-Z]{3}$"),
):
    filters = {
        "iso_alpha2": iso_alpha2.upper() if iso_alpha2 else None,
        "continent": continent.upper() if continent else None,
        "min_population": min_population,
        "max_population": max_population,
        "currency_code": currency_code.upper() if currency_code else None,
    }

    dtos = country_query_service.list_countries(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}", tags=["countries"], response_model=CountryDTO)
def get_country(
    response: Response,
    country_query_service: CountryQueryService = Depends(get_country_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
):
    filters = {"iso_alpha2": country_code.upper()}

    dtos = country_query_service.list_countries(filters)
    _set_cache_header(response, cache_context)
    if not dtos:
        raise HTTPException(status_code=404, detail="Country not found")
    return dtos[0]


@router.get("/countries/{country_code}/admin-divisions", tags=["admin-divisions"], response_model=List[GeonameDTO])
def get_admin_divisions_by_country(
    response: Response,
    admin_division_query_service: AdminDivisionQueryService = Depends(get_admin_division_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    feature_code: Optional[str] = Query(None, min_length=4, max_length=4, regex="^(?i)ADM[1-4]$"),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "feature_code": feature_code,
        "admin1_code": admin1_code,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = admin_division_query_service.list_admin_divisions(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/admin-divisions/{level}", tags=["admin-divisions"], response_model=List[GeonameDTO])
def get_admin_divisions_by_country_and_level(
    response: Response,
    admin_division_query_service: AdminDivisionQueryService = Depends(get_admin_division_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    level: int = Path(..., ge=1, le=4),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=20),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "feature_code": f"ADM{level}",
        "name": name,
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = admin_division_query_service.list_admin_divisions(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/cities/stats", tags=["cities"], response_model=CityStatsDTO)
def get_cities_stats_by_country(
    response: Response,
    city_query_service: CityQueryService = Depends(get_city_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=10),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=10),
    min_population: Optional[int] = Query(None, ge=0),
):
    filters = {
        "country_code": country_code.upper(),
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "min_population": min_population,
    }

    dto = city_query_service.get_avg_population(filters)
    _set_cache_header(response, cache_context)
    return dto


@router.get("/countries/{country_code}/cities", tags=["cities"], response_model=List[GeonameDTO])
def get_cities_by_country(
    response: Response,
    city_query_service: CityQueryService = Depends(get_city_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=10),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=10),
    min_population: Optional[int] = Query(None, ge=0),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "min_population": min_population,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = city_query_service.list_cities(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/places", tags=["places"], response_model=List[GeonameDTO])
def get_places_by_country(
    response: Response,
    place_query_service: PlaceQueryService = Depends(get_place_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    feature_class: Optional[str] = Query(None, min_length=1, max_length=1, regex="^(?i)[A-Z]$"),
    feature_code: Optional[str] = Query(None, min_length=2, max_length=10),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin3_code: Optional[str] = Query(None, min_length=1, max_length=20),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "feature_class": feature_class.upper() if feature_class else None,
        "feature_code": feature_code.upper() if feature_code else None,
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "admin3_code": admin3_code,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = place_query_service.list_places(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/places/mountains", tags=["places"], response_model=List[GeonameDTO])
def get_mountains_by_country(
    response: Response,
    place_query_service: PlaceQueryService = Depends(get_place_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin3_code: Optional[str] = Query(None, min_length=1, max_length=20),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "feature_codes": ["MT", "MTS", "PK", "PKS", "MTPASS", "HLL", "HLLS", "VLC", "RDGE", "BUTE"],
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "admin3_code": admin3_code,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = place_query_service.list_places(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/places/beaches", tags=["places"], response_model=List[GeonameDTO])
def get_beaches_by_country(
    response: Response,
    place_query_service: PlaceQueryService = Depends(get_place_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin3_code: Optional[str] = Query(None, min_length=1, max_length=20),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "feature_codes": ["BCH", "BCHS"],
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "admin3_code": admin3_code,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = place_query_service.list_places(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/places/lakes", tags=["places"], response_model=List[GeonameDTO])
def get_lakes_by_country(
    response: Response,
    place_query_service: PlaceQueryService = Depends(get_place_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin3_code: Optional[str] = Query(None, min_length=1, max_length=20),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "feature_codes": ["LK", "LKS", "LKN", "LKNI", "LKOI", "LKC", "LKI", "LKO", "LKX"],
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "admin3_code": admin3_code,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = place_query_service.list_places(filters)
    _set_cache_header(response, cache_context)
    return dtos


@router.get("/countries/{country_code}/places/ports", tags=["places"], response_model=List[GeonameDTO])
def get_ports_by_country(
    response: Response,
    place_query_service: PlaceQueryService = Depends(get_place_query_service),
    cache_context: CacheContext = Depends(get_cache_context),
    country_code: str = Path(..., min_length=2, max_length=2, regex="^(?i)[A-Z]{2}$"),
    name: Optional[str] = Query(None, min_length=1, max_length=200),
    admin1_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin2_code: Optional[str] = Query(None, min_length=1, max_length=20),
    admin3_code: Optional[str] = Query(None, min_length=1, max_length=20),
    language: Optional[str] = Query(None, min_length=2, max_length=7, regex="^(?i)[a-z]{2}(-[A-Z]{2})?$"),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    expand: Optional[str] = Query(None),
):
    filters = {
        "country_code": country_code.upper(),
        "name": name,
        "feature_codes": ["PRT", "PRTQ", "PRTHQS"],
        "admin1_code": admin1_code,
        "admin2_code": admin2_code,
        "admin3_code": admin3_code,
        "language": language.lower() if language else None,
        "limit": limit,
        "offset": offset,
        "expand": expand.split(",") if expand else None,
    }

    dtos = place_query_service.list_places(filters)
    _set_cache_header(response, cache_context)
    return dtos
