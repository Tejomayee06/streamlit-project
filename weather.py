import streamlit as st
import requests
from datetime import datetime
st.set_page_config(page_title="Welcome App",page_icon="🌞")
WMO_CODES={
    0:"Clear sky",
    1:"Mainly clear",
    2:"Partly cloudly",
    3:"Overcast",
    45:"Fog",
    48:"Depositing rime fog",
    51:"Light derizzle",
    53:"Moderate drizzle",
    55:"Dense drizzle",
    56:"Light freezing drizzle",
    57:"Dense freezing drizzle",
    61:"Slight rain",
    63:"Moderate drizzle",
    65:"Heavy rain",
    66:"Light freezing rain",
    67:"Heavy freezing rain",
    71:"Slight snow fall",
    73:"Moderate snow fall",
    75:"Heavy snow fall",
    77:"Snow grains",
    80:"Slight rain showers",
    81:"Moderate rain showers",
    82:"Violent rain showers",
    85:"Slight snow showers",
    86:"Heavy snow showers",
    95:"Thunderstrome",
    96:"Thunderstrome with slight hail",
    99:"Thunderstrom with heavy hail"
}
def get_wmo(code):
    return WMO_CODES.get(code, "Unknown weather condition")
def wind_direction(degree):
    directions=["N","NE","E","SE","S","SW","W","NW"]
    idx=int((degree/45)%8)
    return directions[idx]
'''
geocode api:to get the latitude and longitude of the city
open meteo api:to get the weather on the latitude and longitude
'''
def geocode(city):
    r=requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name":city,"count":5, "language":"en","format":"json"}, timeout=8,
    )
    r.raise_for_status()
    return r.json().get("results", [])
def fetch_weather(lat,lon):
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
         params={
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,weather_code,uv_index",
        "hourly": "temperature_2m,precipitation_probability",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 7,
    },
        timeout=8,       # FIX 1: added timeout
        verify=False,    # FIX 2: fixes SSLEOFError
)
    r.raise_for_status()
    return r.json()
st.title(":sunny: Weather App Dashboard")
st.caption("Get the current weather and 7-day forecast for any city"
           "in the world.")
city_input = st.text_input("Enter a city name",
                           placeholder="e.g. London, Paris,New York")
unit=st.radio("Select temperature unit", ("Celsius", "Fahrenheit"),
              horizontal=True)
if not city_input:
    st.info("Please enter a city name to get the weather information:")
    st.stop()

with st.spinner("Fetching location data...."):
    try:
        locations = geocode(city_input)
    except Exception as e:
        st.error(f"Geocode Failed: {e}")
        st.stop()
options = [f"{r['name']}, {r.get('admin1', '')}, {r['country']}" for r in locations]
chosen_ind = st.selectbox("Select the current location", range(len(options)), format_func= lambda x: options[x])
loc = locations[chosen_ind]

with st.spinner("fetch weather data..."):
    try:
        data = fetch_weather(loc["latitude"], loc["longitude"])
    except Exception as e :
        st.error(f"Weather Fetch Failed: {e}")
        st.stop()
    
    cur = data["current"]
    daily = data["daily"]
    hourly = data["hourly"]

    def fmt(c):
        return round(c*9/5 + 32,1) if unit == "Fahrenheit" else c
    
st.divider()
desc= get_wmo(cur["weather_code"])   # FIX 3: was "weathercode"
st.subheader("current weather")
st.metric("Tempreature", f"{fmt(cur['temperature_2m'])}° {unit}", f"Feels like {fmt(cur['apparent_temperature'])}° {unit}")  # FIX 4: key name typos + extra ) removed

col1, col2, col3, col4 = st.columns(4)
col1.metric(":cloudy: Humidity", f"{cur['relative_humidity_2m']}%")
col2.metric(":wind_blowing_face: Wind Speed", f"{cur['wind_speed_10m']}{wind_direction(cur['wind_direction_10m'])}")
col3.metric(":droplet: Precipittion", f"{cur['precipitation']} mm")
col4.metric(":sun_with_face: UV Index", f"{cur['uv_index']}")
st.caption(f"Condition: {desc}")