import tkinter as tk
from tkinter import scrolledtext
import requests
import datetime
import os

# Your OpenWeather API key
API_KEY = "6dcaaf81b52e225138f3932dc30c0af3"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# 📍 Get user location based on IP
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("city", "")
    except:
        return ""

# 🌦️ Emoji for weather
def get_emoji(condition):
    condition = condition.lower()
    if "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "clear" in condition:
        return "☀️"
    elif "snow" in condition:
        return "❄️"
    elif "storm" in condition:
        return "⛈️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    else:
        return "🌡️"

# 🌤️ Get weather function
def on_get_weather():
    city = city_entry.get().strip()
    if not city:
        output_box.insert(tk.END, "❗ Please enter a city name.\n")
        return

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            output = f"❌ Error: {data.get('message', 'City not found.')}\n"
        else:
            weather = data["weather"][0]
            main = data["main"]
            wind = data["wind"]
            name = data["name"]
            local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emoji = get_emoji(weather['description'])

            output = (
                f"📍 City: {name}\n"
                f"🌡️ Temperature: {main['temp']}\u00b0C (feels like {main['feels_like']}\u00b0C)\n"
                f"🔻 Min: {main['temp_min']}\u00b0C | 🔹 Max: {main['temp_max']}\u00b0C\n"
                f"🌤️ Condition: {weather['description'].capitalize()} {emoji}\n"
                f"💧 Humidity: {main['humidity']}%\n"
                f"🌬️ Wind Speed: {wind['speed']} m/s\n"
                f"🕒 Local Time: {local_time}\n"
                f"🌍 Map: https://www.google.com/maps/search/{name}\n"
            )

            # 🔔 Simple alerts
            if main["temp"] < 5:
                output += "🔔 Cold alert!\n"
            elif main["temp"] > 30:
                output += "🔔 Heat alert!\n"
            if "rain" in weather["description"].lower():
                output += "🔔 Rain alert!\n"

            # Save to log file
            with open("weather_log.txt", "a", encoding="utf-8") as file:
                file.write((output + "\n\n").encode("utf-8", errors="replace").decode("utf-8"))

            # Save to history
            with open("history.txt", "a", encoding="utf-8") as file:
                file.write(name + "\n")

        output_box.insert(tk.END, output + "\n")
        output_box.see(tk.END)

    except Exception as e:
        output_box.insert(tk.END, f"❌ Error: {e}\n")

# 📜 View search history
def show_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r", encoding="utf-8") as file:
            history = file.read().strip().split("\n")
        if history:
            output_box.insert(tk.END, "\n📖 Search History:\n")
            for city in history[-5:]:
                output_box.insert(tk.END, f"🔹 {city}\n")
    else:
        output_box.insert(tk.END, "\n📬 No history found.\n")

# 🪟 Setup GUI
root = tk.Tk()
root.title("🌦️ Weather App")
root.geometry("620x530")

# 🔳 App icon (must be .ico)
try:
    root.iconbitmap("icon.ico")
except:
    pass  # silently fail if icon not found

# 🌍 Auto-fill user location
auto_city = get_user_location()

# 🖊️ Entry field
city_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
city_entry.pack(pady=10)
city_entry.insert(0, auto_city or "Enter city name")

# 🔘 Buttons
get_button = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=on_get_weather)
get_button.pack(pady=5)

history_button = tk.Button(root, text="Show Search History", font=("Helvetica", 10), command=show_history)
history_button.pack(pady=3)

# 📬 Output display
output_box = scrolledtext.ScrolledText(root, height=18, width=70, font=("Courier", 10))
output_box.pack(pady=10)

# 🔀 Start GUI loop
root.mainloop()

