# tests/test_weather_api.py
import pytest
from backend import weather_api

def test_geocode_known_place():
    res = weather_api.geocode("Bangkok")
    assert res is not None
    assert "latitude" in res and "longitude" in res

def test_get_weather_for_place():
    obj = weather_api.get_weather_for_place("Bangkok", use_cache=False)
    assert "place" in obj and "raw" in obj
    assert "current_weather" in obj["raw"] or "hourly" in obj["raw"]
