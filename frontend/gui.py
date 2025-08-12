import tkinter as tk
from tkinter import messagebox
from backend.weather_api import get_weather_for_place
from backend.data_processing import parse_current
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os

IMAGE_URL = "https://images.pexels.com/photos/186980/pexels-photo-186980.jpeg?cs=srgb&dl=pexels-tahir-shaw-50609-186980.jpg&fm=jpg"
IMAGE_PATH = "background.jpg"

def download_image():
    if not os.path.exists(IMAGE_PATH):
        try:
            response = requests.get(IMAGE_URL)
            response.raise_for_status()
            with open(IMAGE_PATH, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download image: {e}")

def search_weather():
    city = city_entry.get()
    if not city.strip():
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return
    try:
        raw_data = get_weather_for_place(city)
        parsed = parse_current(raw_data["raw"])
        city_label.config(text=f"{raw_data['place']['name']}, {raw_data['place']['country']}")
        temp_label.config(text=f"Temperature: {parsed.get('temperature_c', 'N/A')} °C")
        cond_label.config(text=f"Condition: {parsed.get('weather_text', 'N/A')}")
        feels_label.config(text=f"Feels Like: {parsed.get('feels_like_c', 'N/A')} °C")
        humidity_label.config(text=f"Humidity: {parsed.get('humidity_percent', 'N/A')} %")
        uv = parsed.get("uv_index_max")
        uv_label.config(text=f"UV Index Max: {uv if uv is not None else 'N/A'}")
        sunrise = parsed.get("sunrise")
        sunset = parsed.get("sunset")
        sunrise_label.config(text=f"Sunrise: {sunrise if sunrise else 'N/A'}")
        sunset_label.config(text=f"Sunset: {sunset if sunset else 'N/A'}")
        wind_label.config(text=f"Wind Speed: {parsed.get('wind_speed_kmh', 'N/A')} km/h")
    except Exception as e:
        messagebox.showerror("Error", str(e))

download_image()

root = tk.Tk()
root.title("Weather App")
root.geometry("400x550")
root.resizable(False, False)

# Load and resize image
img = Image.open(IMAGE_PATH)
img = img.resize((400, 150))
photo = ImageTk.PhotoImage(img)

# Create a canvas to hold the image and widgets on top
canvas = tk.Canvas(root, width=400, height=150)
canvas.pack()

# Add the image to the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Place input box and button ON TOP of the image using .place()
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.place(x=20, y=50, width=250)  # Adjust x,y to position it nicely

search_btn = tk.Button(root, text="Search", command=search_weather)
search_btn.place(x=280, y=48, width=80)

# Weather info labels below
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
