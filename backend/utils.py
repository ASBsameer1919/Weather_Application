# backend/utils.py
from datetime import datetime
from typing import Optional

def kelvin_to_celsius(k: float) -> float:
    return k - 273.15

def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9/5) + 32

def format_iso_to_local(iso_ts: str) -> str:
    """
    Basic pretty formatting for ISO timestamps returned by Open-Meteo.
    Example input: '2025-08-10 T06:12:00'
    """
    try:
        dt = datetime.fromisoformat(iso_ts)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_ts

def safe_get(d: dict, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur
