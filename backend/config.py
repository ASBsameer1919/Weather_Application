# backend/config.py

# Open-Meteo endpoints
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Defaults
DEFAULT_TIMEOUT = 10            # seconds for HTTP requests
DEFAULT_GEOCODE_COUNT = 1      # return 1 geocode result (best match)
DEFAULT_CACHE_FILE = "cache.json"
CACHE_TTL_SECONDS = 60 * 30     # 30 minutes cache TTL

