 

# 🌤 Weather Application

A Python-based weather application that lets you check **real-time weather conditions** for any location, either through a **simple Command Line Interface (CLI)** or a **user-friendly Graphical User Interface (GUI)**.
It also displays **scenic images** of the searched location using the **Pexels API**.

---

## ✨ Features

* **Two Modes**

  * **CLI Mode** – Get weather updates right from your terminal.
  * **GUI Mode** – Search weather in a beautiful Tkinter interface with images.
* **Live Weather Data** – Fetches current weather conditions using the **Open-Meteo API**.
* **Rich Weather Details**:

  * 🌡 Temperature & Feels Like
  * 🌦 Weather Condition
  * 💧 Humidity
  * ☀️ UV Index
  * 🌅 Sunrise & Sunset
  * 🌬 Wind Speed
* **Location Images** – Automatically fetches background images of the location from **Pexels API**.
* **Caching** – Reduces API calls by storing recent results.
* **Cross-Platform** – Runs on Windows, macOS, and Linux.

---

## 📂 Project Structure

```
Weather_Application/
│
├── backend/                # Core weather data handling
│   ├── cache_manager.py     # Cache system for API responses
│   ├── config.py            # Configurations & constants
│   ├── data_processing.py   # Parsing raw weather data
│   ├── utils.py             # Helper utilities
│   ├── weather_api.py       # Open-Meteo API interaction
│   └── __init__.py
│
├── frontend/                # GUI interface
│   ├── gui.py               # Tkinter-based weather GUI
│   └── __init__.py
│
├── tests/                   # Unit tests
│   ├── test_data_processing.py
│   ├── test_weather_api.py
│   └── __init__.py
│
├── background.jpg           # Default background image
├── cache.json               # Local cache file
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

---

## ⚙️ Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/weather-application.git
   cd weather-application
   ```

2. **Create a Virtual Environment** *(optional but recommended)*

   ```bash
   python -m venv venv
   # Activate the environment
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set API Key**

   * Get a free API key from [Pexels](https://www.pexels.com/api/).
   * Open `frontend/gui.py` and replace `PEXELS_API_KEY` with your key.

---

## 🚀 Usage

### Run in **CLI Mode**

```bash
python main.py
```

When prompted, enter **anything other than `gui`** to use CLI.

Example:

<img width="468" height="681" alt="image" src="https://github.com/user-attachments/assets/ba83c046-ab8f-4e8e-b8da-bdaa44d9e8f0" />


```
Enter 'gui' to launch GUI or anything else for CLI: cli
Enter city/place name: Hyderabad

--- Location ---
Hyderbad (lat=51.5072, lon=-0.1276)
Timezone: ISD

--- Current Weather ---
Temperature: 19.2 °C
Condition: Cloudy
Feels Like: 18.9 °C
Humidity: 70 %
UV Index Max: 3.5
Sunrise: 2025-08-13T05:45
Sunset: 2025-08-13T20:15
Wind Speed: 12.3 km/h
```

---

### Run in **GUI Mode**

```bash
python main.py
```

When prompted, type:

```
gui
```

You’ll see a **Tkinter window** where you can:

* Enter a city name
* View current weather details
* See a background image of that location

---

## 🖼 Screenshots

**Hyderabad Example**
![Hyderabad Weather]

<img width="472" height="655" alt="image" src="https://github.com/user-attachments/assets/d5309c71-93cf-4ca4-bdbb-f631ec3d40bc" />


**Thailand Example**
![Thailand Weather]

<img width="474" height="641" alt="image" src="https://github.com/user-attachments/assets/2fdb979f-b225-48c8-a5ab-2574db1e55b9" />


---

## 🛠 Tech Stack

* **Python 3.12+**
* **Tkinter** – GUI framework
* **Pillow** – Image processing
* **Requests** – HTTP requests
* **Open-Meteo API** – Weather data
* **Pexels API** – Location images
* **Pytest** – Unit testing

---

## 🧪 Run Tests

```bash
pytest tests/
```

---

## 📜 License

This project is licensed under the **MIT License**.
You’re free to use, modify, and distribute it.

---

## 🙌 Acknowledgments

* [Open-Meteo API](https://open-meteo.com/) for free weather data.
* [Pexels](https://www.pexels.com/) for high-quality background images.

---






