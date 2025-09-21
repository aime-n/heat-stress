import requests
import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("VISUALCROSSING_API_KEY")


def get_weather_data_open_meteo(lat, lon):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m, " 
        "shortwave_radiation",
        "timezone": "auto",
        "forecast_days": 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Get current hour's data
        current_hour = datetime.now().strftime("%Y-%m-%dT%H:00")
        hour_index = data["hourly"]["time"].index(current_hour)
        
        return {
            "temp": data["hourly"]["temperature_2m"][hour_index],
            "humidity": data["hourly"]["relative_humidity_2m"][hour_index],
            "wind_speed": data["hourly"]["wind_speed_10m"][hour_index],
            "solar_radiation": data["hourly"]["shortwave_radiation"][hour_index],
            "station_count": 0
        }
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None
    

def get_weather_data_visualcrossing(lat, lon):
    """Fetch weather data from Visual Crossing API"""
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    params = {
        "unitGroup": "metric",
        "include": "current",
        "key": API_KEY,
        "contentType": "json"
    }
    
    try:
        response = requests.get(f"{base_url}/{lat},{lon}/today", params=params)

        response.raise_for_status()
        data = response.json()
        current = data["currentConditions"]

        station_count = len(data["stations"]) if "stations" in data else 0

        return {
            "temp": current["temp"],
            "humidity": current["humidity"],
            "wind_speed": current["windspeed"],
            "solar_radiation": current["solarradiation"],
            "station_count": station_count
        }
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None