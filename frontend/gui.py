import tkinter as tk
from tkinter import messagebox
from backend.weather_api import get_weather_for_place
from backend.data_processing import parse_current
from PIL import Image, ImageTk
import requests
import os

# Pexels API key (replace with your key)
PEXELS_API_KEY = "59cis2gua9WjWrfVxYusx20At9ZkhzExTAunyIFkqhvxvlRHeFOdBWva"

# Default background image
IMAGE_PATH = "background.jpg"
DEFAULT_IMAGE_URL = "https://images.pexels.com/photos/186980/pexels-photo-186980.jpeg"

def download_image(url, path):
    """Download an image from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download image: {e}")
        return False

def get_city_image(city_name):
    """Fetch an image URL for the given city using Pexels API."""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": city_name, "per_page": 1}
    try:
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["large"]
    except Exception as e:
        print(f"Image fetch error: {e}")
    return DEFAULT_IMAGE_URL

def calculate_feels_like(temp_c, humidity, wind_kmh):
    feels_like = temp_c
    if humidity and humidity > 50:
        feels_like += (humidity - 50) * 0.05
    if wind_kmh and wind_kmh > 10:
        feels_like -= (wind_kmh - 10) * 0.02
    return round(feels_like, 1)

def update_background(image_path):
    """Update background image in the app."""
    img = Image.open(image_path).resize((400, 150))
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo  # Keep reference to avoid garbage collection

def search_weather():
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return
    if city.isdigit():
        messagebox.showwarning("Input Error", "City name cannot be only numbers!")
        return
    
    try:
        # Weather
        raw_data = get_weather_for_place(city)
        parsed = parse_current(raw_data["raw"])
        
        temperature = parsed.get('temperature_c')
        humidity = parsed.get('humidity_percent')
        wind_speed = parsed.get('wind_speed_kmh')
        
        feels_like_value = calculate_feels_like(temperature, humidity, wind_speed)
        
        city_label.config(text=f"{raw_data['place']['name']}, {raw_data['place']['country']}")
        temp_label.config(text=f"Temperature: {temperature if temperature is not None else 'N/A'} °C")
        cond_label.config(text=f"Condition: {parsed.get('weather_text', 'N/A')}")
        feels_label.config(text=f"Feels Like: {feels_like_value} °C")
        humidity_label.config(text=f"Humidity: {humidity if humidity is not None else 'N/A'} %")
        uv = parsed.get("uv_index_max")
        uv_label.config(text=f"UV Index Max: {uv if uv is not None else 'N/A'}")
        sunrise_label.config(text=f"Sunrise: {parsed.get('sunrise', 'N/A')}")
        sunset_label.config(text=f"Sunset: {parsed.get('sunset', 'N/A')}")
        wind_label.config(text=f"Wind Speed: {wind_speed if wind_speed is not None else 'N/A'} km/h")
        
        # Image for city
        image_url = get_city_image(city)
        if download_image(image_url, IMAGE_PATH):
            update_background(IMAGE_PATH)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setup window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x550")
root.resizable(False, False)

# Canvas for background image
canvas = tk.Canvas(root, width=400, height=150)
canvas.pack()

# Default background
download_image(DEFAULT_IMAGE_URL, IMAGE_PATH)
update_background(IMAGE_PATH)

# Entry + Button frame
input_frame = tk.Frame(root)
input_frame.pack(pady=(10, 5))

city_entry = tk.Entry(input_frame, font=("Arial", 14), width=28)
city_entry.pack(pady=(0, 5))

search_btn = tk.Button(input_frame, text="Search", command=search_weather, font=("Arial", 12))
search_btn.pack()

# Weather info labels
city_label = tk.Label(root, text="", font=("Arial", 16, "bold"))
city_label.pack(pady=(10, 5))

temp_label = tk.Label(root, text="", font=("Arial", 14))
temp_label.pack()

cond_label = tk.Label(root, text="", font=("Arial", 14))
cond_label.pack()

feels_label = tk.Label(root, text="", font=("Arial", 14))
feels_label.pack()

humidity_label = tk.Label(root, text="", font=("Arial", 14))
humidity_label.pack()

uv_label = tk.Label(root, text="", font=("Arial", 14))
uv_label.pack()

sunrise_label = tk.Label(root, text="", font=("Arial", 14))
sunrise_label.pack()

sunset_label = tk.Label(root, text="", font=("Arial", 14))
sunset_label.pack()

wind_label = tk.Label(root, text="", font=("Arial", 14))
wind_label.pack()

if __name__ == "__main__":
    root.mainloop()
