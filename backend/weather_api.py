# backend/weather_api.py
import requests
from typing import Optional, Dict, Any, List
from . import config
from .cache_manager import CacheManager

class WeatherAPIError(Exception):
    pass

cache = CacheManager(config.DEFAULT_CACHE_FILE, ttl_seconds=config.CACHE_TTL_SECONDS)

def geocode(place_name: str, count: int = None, timeout: int = None) -> Optional[Dict[str, Any]]:
    """
    Use Open-Meteo geocoding to resolve a place name to coordinates.
    Returns the first match dict or None.
    """
    if count is None:
        count = config.DEFAULT_GEOCODE_COUNT
    if timeout is None:
        timeout = config.DEFAULT_TIMEOUT

    params = {"name": place_name, "count": count}
    try:
        r = requests.get(config.GEOCODE_URL, params=params, timeout=timeout)
        r.raise_for_status()
        j = r.json()
    except Exception as e:
        raise WeatherAPIError(f"Geocoding request failed: {e}")

    results = j.get("results")
    if not results:
        return None
    return results[0]

def fetch_forecast_by_coords(latitude: float, longitude: float,
                             current_weather: bool = True,
                             hourly: Optional[List[str]] = None,
                             daily: Optional[List[str]] = None,
                             timezone: str = "auto",
                             timeout: int = None) -> Dict[str, Any]:
    """
    Fetch forecast/current weather using Open-Meteo.
    Returns raw JSON.
    """
    if timeout is None:
        timeout = config.DEFAULT_TIMEOUT

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
    }
    if current_weather:
        params["current_weather"] = "true"
    if hourly:
        params["hourly"] = ",".join(hourly)
    if daily:
        params["daily"] = ",".join(daily)

    try:
        r = requests.get(config.FORECAST_URL, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise WeatherAPIError(f"Forecast request failed: {e}")

def get_weather_for_place(place_name: str, use_cache: bool = True) -> Dict[str, Any]:
    """
    High-level: geocode place name, fetch forecast. Caches by place_name.
    Returns dict: { "place": {...}, "raw": {...} }
    """
    cache_key = f"weather:{place_name.lower()}"
    if use_cache:
        cached = cache.get(cache_key)
        if cached:
            return cached

    place = geocode(place_name)
    if not place:
        raise WeatherAPIError(f"Place not found: {place_name}")

    lat = place["latitude"]
    lon = place["longitude"]

    hourly = ["temperature_2m", "relativehumidity_2m", "weathercode", "windspeed_10m"]
    daily = ["sunrise", "sunset", "uv_index_max"]

    raw = fetch_forecast_by_coords(lat, lon, current_weather=True, hourly=hourly, daily=daily, timezone="auto")

    out = {"place": place, "raw": raw}
    cache.set(cache_key, out)
    return out
