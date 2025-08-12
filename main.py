# main.py
from backend import weather_api, data_processing

def cli():
    print("Simple Weather Backend CLI (Open-Meteo)")
    place = input("Enter city/place name: ").strip()
    if not place:
        print("Please enter a place name.")
        return
    try:
        res = weather_api.get_weather_for_place(place)
    except Exception as e:
        print("Error:", e)
        return

    place_info = res["place"]
    raw = res["raw"]
    parsed = data_processing.parse_current(raw)

    print("\n--- Location ---")
    print(f"{place_info.get('name')}, {place_info.get('country')} (lat={place_info.get('latitude')}, lon={place_info.get('longitude')})")
    print("Timezone:", place_info.get("timezone"))

    print("\n--- Current Weather ---")
    for k, v in parsed.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    mode = input("Enter 'gui' to launch GUI or anything else for CLI: ").strip().lower()
    if mode == "gui":
        from frontend import gui
        gui.root.mainloop()
    else:
        cli()
