import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Weather App", page_icon="⛅", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>⛅ Weather App</h1>", unsafe_allow_html=True)

# Input field
city = st.text_input("Enter a city name:")

# OpenWeatherMap API
api_key = "6dcaaf81b52e225138f3932dc30c0af3"
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Weather emojis
weather_emojis = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌁"
}

# Fetch and display weather
if city:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_main = data["weather"][0]["main"]
        weather_desc = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        emoji = weather_emojis.get(weather_main, "🌈")

        # Display result in columns
        st.image(icon_url)
        st.subheader(f"{emoji} {weather_desc}")
        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{temp}°C")
        col2.metric("Feels Like", f"{feels_like}°C")
        col1.metric("Humidity", f"{humidity}%")
        col2.metric("Wind Speed", f"{wind_speed} m/s")

    else:
        st.error("City not found. Please enter a valid city name.")

