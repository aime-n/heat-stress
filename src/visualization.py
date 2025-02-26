import numpy as np
from .calculations import calculate_black_globe, calculate_wet_bulb
import plotly.graph_objects as go


def create_wbgt_graph(current_temp, current_humidity, solar_radiation, wind_speed):
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
            [0.0, '#a8e6cf'],   # Safe (0)
            [0.2, '#ffd3b6'],   # Caution (1)
            [0.4, '#ffaaa5'],   # Extreme Caution (2)
            [0.6, '#ff8b94'],   # Danger (3)
            [1.0, '#ff0000']    # Extreme Danger (4)
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
        name='Risk Zones'
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
            f"Wind: {wind_speed}m/s"
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