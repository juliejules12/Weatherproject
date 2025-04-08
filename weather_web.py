import streamlit as st
import requests

def main():
    st.title("🌤️ Weather App")
    
    city = st.text_input("Enter a city name:")
    if city:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.write(f"**Weather in {city}**")
            st.write(f"Temperature: {data['main']['temp']}°C")
            st.write(f"Description: {data['weather'][0]['description']}")
        else:
            st.error("City not found.")

if __name__ == "__main__":
    main()
