# tests/test_data_processing.py
from backend import data_processing

def test_wmo_map():
    # check known mapping exists
    assert data_processing.WMO_CODE_MAP.get(0) == "Clear sky"

def test_parse_current_handles_empty():
    out = data_processing.parse_current({})
    assert "fetched_at_utc" in out
    assert ("error" in out) or ("temperature_c" in out)
