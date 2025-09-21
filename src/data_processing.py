import streamlit as st
import pandas as pd
from src.api_client import get_weather_data_visualcrossing, get_weather_data_open_meteo
from src.calculations import calculate_wbgt, get_heat_category
from concurrent.futures import ThreadPoolExecutor
from src.config import color_scale


def get_multiple_cities_data(brazil_cities):
    # Initialize progress bar
    progress_bar = st.progress(0)
    total_cities = len(brazil_cities)

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = []
        for city, info in brazil_cities.items():
            futures.append(executor.submit(fetch_city_data, city, info))

        cities_data = []
        for i, future in enumerate(futures):
            result = future.result()
            if result:
                cities_data.append(result)
            # Update progress bar
            progress_bar.progress((i + 1) / total_cities)

    # Convert the list to a DataFrame
    df = pd.DataFrame(cities_data)
    return df


def fetch_city_data(city, info):
    data = get_weather_data_open_meteo(info['lat'], info['lon'])
    if data:
        wbgt = calculate_wbgt(data['temp'], data['humidity'], 
                            data['solar_radiation'], data['wind_speed'])
        category, _ = get_heat_category(wbgt)
        color = color_scale[category]
        return {
            'Cidade': city,
            'Estado': info['state'],  
            'lat': info['lat'],
            'lon': info['lon'],
            'WBGT': wbgt,
            'Categoria WBGT': category,
            'color_column': color
        }
    return None


# Função para agrupar por estado
def group_by_state(df):
    state_data = df.groupby('Estado', as_index=False).agg({
        'WBGT': 'mean',
        'Categoria WBGT': lambda x: x.mode()[0] if not x.mode().empty else 'Sem dados'
    })
    state_data.rename(columns={'WBGT': 'WBGT Médio'}, inplace=True)
    return state_data