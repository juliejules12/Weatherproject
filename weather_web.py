import streamlit as st
import requests
import datetime
import geocoder
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

API_KEY = "6dcaaf81b52e225138f3932dc30c0af3"

st.set_page_config(page_title="JulesJulie Weather App", page_icon="⛅")
st.markdown("<h1 style='text-align: center;'>🌤️ Weather App by <span style='color:#6c63ff;'>JulesJulie</span></h1>", unsafe_allow_html=True)

# 📍 Auto-detect location
if st.button("📍 Use My Location"):
    g = geocoder.ip('me')
    if g.ok:
        st.session_state.city = g.city
    else:
        st.error("Couldn't detect location.")

city = st.text_input("Enter a city name:", st.session_state.get("city", ""))

if city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()

        weather = data["weather"][0]["description"].title()
        icon = data["weather"][0]["icon"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=100)
        st.markdown(f"## 🌤️ {weather}")
        st.markdown(f"**Temperature:** {temp}°C")
        st.markdown(f"**Feels Like:** {feels_like}°C")
        st.markdown(f"**Humidity:** {humidity}%")
        st.markdown(f"**Wind Speed:** {wind_speed} m/s")

        # 🗺️ City map preview
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        st.markdown("### 🗺️ City Map")
        city_map = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup=city).add_to(city_map)
        st_folium(city_map, width=700)

        # 📉 Weekly forecast
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_res = requests.get(forecast_url)
        if forecast_res.status_code == 200:
            forecast_data = forecast_res.json()
            dates = []
            temps = []

            for i in range(0, 40, 8):  # 5-day, every 24 hours
                day = forecast_data["list"][i]
                date = datetime.datetime.strptime(day["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
                dates.append(str(date))
                temps.append(day["main"]["temp"])

            st.markdown("### 📉 Weekly Forecast")
            fig, ax = plt.subplots()
            ax.plot(dates, temps, marker="o")
            ax.set_xlabel("Date")
            ax.set_ylabel("Temp (°C)")
            ax.set_title(f"Weekly Forecast for {city}")
            st.pyplot(fig)
    else:
        st.error("City not found 😞")

