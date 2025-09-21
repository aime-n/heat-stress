import numpy as np
from .calculations import calculate_black_globe, calculate_wet_bulb
import plotly.graph_objects as go
import plotly.express as px
from src.config import color_scale, BRAZIL_GEOJSON
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import scipy

def create_wbgt_graph(current_temp, current_humidity, solar_radiation, wind_speed, wbgt):
    """Create interactive WBGT risk zone plot with current conditions"""
    # Generate temperature and humidity grid
    temp_range = np.linspace(20, 50, 100)
    humidity_range = np.linspace(0, 100, 100)
    temp_grid, humidity_grid = np.meshgrid(temp_range, humidity_range)
    
    # Calculate WBGT components for grid (rename Tw to wet_bulb_temp)
    wet_bulb_temp = calculate_wet_bulb(temp_grid, humidity_grid)
    black_globe_temp = calculate_black_globe(temp_grid, solar_radiation, wind_speed)
    wbgt_grid = 0.7 * wet_bulb_temp + 0.2 * black_globe_temp + 0.1 * temp_grid
    
    # Create risk zones with numeric values to avoid dtype conflict
    risk_levels = np.select(
        condlist=[
            wbgt_grid < 27.8,
            (wbgt_grid >= 27.8) & (wbgt_grid < 29.4),
            (wbgt_grid >= 29.4) & (wbgt_grid < 31.0),
            (wbgt_grid >= 31.0) & (wbgt_grid < 32.1),
            wbgt_grid >= 32.1
        ],
        choicelist=[0, 1, 2, 3, 4],  # Use numeric values
        default=4  # Ensure common dtype
    )
    
    # Create plot
    fig = go.Figure()

    # Add risk zones with proper color mapping
    fig.add_trace(go.Contour(
        x=temp_range,
        y=humidity_range,
        z=risk_levels,
        colorscale=[
            [0.0, color_scale['Seguro']],   # Safe (0)
            [0.2, color_scale['Cuidado']],   # Caution (1)
            [0.4, color_scale['Cuidado Extremo']],   # Extreme Caution (2)
            [0.6, color_scale['Perigo']],   # Danger (3)
            [1.0, color_scale['Perigo Extremo']]    # Extreme Danger (4)
        ],
        colorbar=dict(
            title='Risk Level',
            tickvals=[0.4, 1.2, 2.0, 2.8, 3.6],
            ticktext=[
                'Safe (<27.8)',
                'Caution (27.8-29.3)',
                'Extreme Caution (29.4-31.0)',
                'Danger (31.0-32.1)',
                'Extreme Danger (≥32.1)'
            ]
        ),
        line_width=0,
        opacity=0.7,
        name='Risk Zones',
        showscale=False
    ))
    
    # Add current conditions marker
    fig.add_trace(go.Scatter(
        x=[current_temp],
        y=[current_humidity],
        mode='markers',
        marker=dict(
            color='blue',
            size=14,
            line=dict(color='white', width=2)
        ),
        name='Current Conditions',
        hovertemplate=(
            f"Temp: {current_temp}°C<br>"
            f"Humidity: {current_humidity}%<br>"
            f"Solar: {solar_radiation}W/m²<br>"
            f"Wind: {wind_speed}m/s<br>" 
            f"WBGT: {wbgt:.1f}°C"   
        )
    ))
    
    # Update layout
    fig.update_layout(
        title=f"WBGT Risk Map (Current Conditions: {current_temp}°C, {current_humidity}% RH)",
        xaxis_title="Temperature (°C)",
        yaxis_title="Relative Humidity (%)",
        width=800,
        height=600,
        hovermode="closest"
    )
    
    return fig


# Função para criar o mapa
def create_brazil_heatmap(cities_data):
    
    # Criar mapa coroplético
    fig = px.choropleth(
        cities_data,
        geojson=BRAZIL_GEOJSON,
        featureidkey="properties.name",
        locations="Estado",
        color="Categoria WBGT",
        color_discrete_map=color_scale,
        scope="south america",
        hover_name="Estado",
        hover_data={"WBGT Médio": ":.1f°C"},
        labels={'WBGT': 'Temperatura de Bulbo Úmido Globais (°C)'},
        height=600
    )
    
    # Ajustar layout do mapa
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def highlight_row(row):
    # For each cell in the row, return a style with the background color from 'color_column'
    return [f'background-color: {row["color_column"]}' for _ in row]


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import streamlit as st
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

def plot_wbgt_contour(df):
    """
    Plots a contour map of WBGT values from a DataFrame using Cartopy.
    
    The DataFrame should have the following columns:
      - 'lat'  : Latitude (in degrees).
      - 'lon'  : Longitude (in degrees).
      - 'WBGT' : WBGT measurement.

    Returns:
        fig (matplotlib.figure.Figure): The figure object for further rendering.

    Usage:
        fig = plot_wbgt_contour(df)
        st.pyplot(fig)  # In Streamlit
    """
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide())

    # Extract WBGT data
    lons = df['lon'].values
    lats = df['lat'].values
    wbgt = df['WBGT'].values

    # Create a grid for contour plotting
    lon_grid, lat_grid = np.meshgrid(
        np.linspace(lons.min(), lons.max(), 100),
        np.linspace(lats.min(), lats.max(), 100)
    )
    
    # Interpolate data onto the grid
    from scipy.interpolate import griddata
    wbgt_grid = griddata((lons, lats), wbgt, (lon_grid, lat_grid), method='cubic')

    # Plot contour map
    contour = ax.contourf(lon_grid, lat_grid, wbgt_grid,
                          transform=ccrs.PlateCarree(),
                          cmap='nipy_spectral')

    # Add geographic features
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.set_global()

    # Add colorbar
    cbar = fig.colorbar(contour, orientation='horizontal', pad=0.05)
    cbar.set_label("WBGT Index")

    return fig


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from scipy.interpolate import griddata

def plot_wbgt_contour_brazil(df):
    """
    Plots a contour map of WBGT values over Brazil using Cartopy.

    The DataFrame should have the following columns:
      - 'lat'  : Latitude (in degrees).
      - 'lon'  : Longitude (in degrees).
      - 'WBGT' : WBGT measurement.

    Returns:
        fig (matplotlib.figure.Figure): The figure object for further rendering.

    Usage:
        fig = plot_wbgt_contour_brazil(df)
        st.pyplot(fig)  # In Streamlit
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Brazil boundaries
    ax.set_extent([-74, -34, -35, 5], crs=ccrs.PlateCarree())

    # Extract WBGT data
    lons = df['lon'].values
    lats = df['lat'].values
    wbgt = df['WBGT'].values

    # Create a grid for contour plotting
    lon_grid, lat_grid = np.meshgrid(
        np.linspace(lons.min(), lons.max(), 100),
        np.linspace(lats.min(), lats.max(), 100)
    )
    
    # Interpolate data onto the grid
    wbgt_grid = griddata((lons, lats), wbgt, (lon_grid, lat_grid), method='cubic')

    # Plot contour map
    contour = ax.contourf(lon_grid, lat_grid, wbgt_grid,
                          transform=ccrs.PlateCarree(),
                          cmap='nipy_spectral')

    # Add geographic features
    ax.coastlines(resolution='10m', linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.5)
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue', alpha=0.3)

    # Add colorbar
    cbar = fig.colorbar(contour, orientation='horizontal', pad=0.05)
    cbar.set_label("WBGT Index")

    return fig
