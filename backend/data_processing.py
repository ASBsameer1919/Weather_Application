from typing import Dict, Any
from datetime import datetime
from dateutil.parser import parse as parse_dt

WMO_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail"
}

def parse_current(raw: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    out["fetched_at_utc"] = datetime.utcnow().isoformat() + "Z"

    cw = raw.get("current_weather")
    if cw:
        out["temperature_c"] = cw.get("temperature")
        out["wind_speed_kmh"] = cw.get("windspeed")
        out["wind_direction_deg"] = cw.get("winddirection")
        code = cw.get("weathercode")
        out["weather_code"] = code
        out["weather_text"] = WMO_CODE_MAP.get(code, "Unknown")
    else:
        out["error"] = "No current_weather in response"

    humidity = None
    hourly = raw.get("hourly", {})
    humidity_list = hourly.get("relativehumidity_2m", [])
    time_list = hourly.get("time", [])
    if humidity_list and time_list:
        now = datetime.utcnow()
        closest_idx = 0
        min_diff = float("inf")
        for i, t in enumerate(time_list):
            t_dt = parse_dt(t)
            diff = abs((t_dt - now).total_seconds())
            if diff < min_diff:
                min_diff = diff
                closest_idx = i
        humidity = humidity_list[closest_idx]
    out["humidity_percent"] = humidity

    uv_index_list = raw.get("daily", {}).get("uv_index_max", [])
    out["uv_index_max"] = uv_index_list[0] if uv_index_list else None

    sunrise_list = raw.get("daily", {}).get("sunrise", [])
    sunset_list = raw.get("daily", {}).get("sunset", [])
    out["sunrise"] = sunrise_list[0] if sunrise_list else None
    out["sunset"] = sunset_list[0] if sunset_list else None

    temp = out.get("temperature_c")
    wind = out.get("wind_speed_kmh")
    if temp is not None and wind is not None:
        if temp <= 10 and wind > 4.8:
            wc = 13.12 + 0.6215 * temp - 11.37 * (wind ** 0.16) + 0.3965 * temp * (wind ** 0.16)
            out["feels_like_c"] = round(wc, 1)
        else:
            out["feels_like_c"] = temp
    else:
        out["feels_like_c"] = None

    return out
