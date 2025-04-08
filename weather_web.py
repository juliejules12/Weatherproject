import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Weather App", page_icon="🌤️")
st.markdown("<h1 style='text-align: center;'>🌤️ Weather App</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>by julesjulie 💻</h5>", unsafe_allow_html=True)
st.write(" ")

api_key = "6dcaaf81b52e225138f3932dc30c0af3"

def get_current_location():
    try:
        ipinfo = requests.get("https://ipinfo.io/json").json()
        return ipinfo.get("city", "Kingston")
    except:
        return "Kingston"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url)
    return res.json()

def get_weekly_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    return requests.get(url).json()

city = st.text_input("📍 Enter a city name:", get_current_location())

if city:
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("City not found. Please try again.")
    else:
        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        icon = data["weather"][0]["icon"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=100)
        st.markdown(f"## 🌤️ {weather}")

        sound_url = "https://www.soundjay.com/button/beep-07.wav"
        st.markdown(
            f"""
            <audio autoplay>
                <source src="{sound_url}" type="audio/wav">
                Your browser does not support the audio element.
            </audio>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temperature", f"{temp:.2f}°C")
            st.metric("Humidity", f"{humidity}%")
        with col2:
            st.metric("Feels Like", f"{feels_like:.2f}°C")
            st.metric("Wind Speed", f"{wind} m/s")

        st.markdown("### 🗺️ Map Preview")
        st.map(pd.DataFrame([[lat, lon]], columns=["lat", "lon"]))

        forecast = get_weekly_forecast(city)
        if "list" in forecast:
            dates = []
            temps = []

            for entry in forecast["list"]:
                dt = datetime.datetime.fromtimestamp(entry["dt"])
                if dt.hour == 12:
                    dates.append(dt.strftime("%a"))
                    temps.append(entry["main"]["temp"])

            if dates and temps:
                st.markdown("### 📉 Weekly Temperature Forecast")
                df_chart = pd.DataFrame({"Day": dates, "Temp (°C)": temps})
                st.line_chart(df_chart.set_index("Day"))


