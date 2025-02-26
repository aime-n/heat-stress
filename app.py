import streamlit as st
from src.api_client import get_weather_data_visualcrossing
from src.calculations import calculate_wbgt, get_heat_category, calculate_black_globe, calculate_wet_bulb
from src.visualization import create_wbgt_graph
from src.data_loader import load_cities

st.set_page_config(
                   page_icon=None, 
                   page_title="WBGT Heat Stress monitor",
                   layout="centered", 
                   initial_sidebar_state="collapsed", 
                   menu_items=None)

BRAZIL_CITIES = load_cities()

st.sidebar.markdown("oii")



# Streamlit UI setup
st.title("🌡️ WBGT Heat Stress Monitor")

if not BRAZIL_CITIES:
    st.error("No cities data available")
    st.stop()

selected_city = st.selectbox("Select a Brazilian City:", list(BRAZIL_CITIES.keys()))

# tab0, tab1, tab2, tab3 = st.tabs(["Monitor", "FAQ", "Accuracy", "About"])
#with tab0:
city_coords = BRAZIL_CITIES[selected_city]
weather_data = get_weather_data_visualcrossing(city_coords["lat"], city_coords["lon"])



if weather_data:
    # Full WBGT calculation
    tg = calculate_black_globe(weather_data["temp"], 
                            weather_data["solar_radiation"],
                            weather_data["wind_speed"])
    wbgt = calculate_wbgt(weather_data["temp"],
                        weather_data["humidity"],
                        weather_data["solar_radiation"],
                        weather_data["wind_speed"])
    
    # Display all metrics and visualizations
    category, advice = get_heat_category(wbgt)
    st.subheader(f"Current Conditions in {selected_city}: {category}")
    # cols = st.columns(4)
    #cols[0].metric("Temperature", f"{weather_data['temp']:.1f}°C")
    #cols[1].metric("Humidity", f"{weather_data['humidity']}%")
    #cols[2].metric("Solar Radiation", f"{weather_data['solar_radiation']} W/m²")
    #cols[3].metric("Wind Speed", f"{weather_data['wind_speed']} m/s")

    # st.subheader("WBGT Calculation")
    #cols = st.columns(4)
    #cols[0].metric("Wet Bulb Temperature", f"{calculate_wet_bulb(weather_data['temp'], weather_data['humidity']):.1f}°C")
    #cols[1].metric("Black Globe Temperature", f"{tg:.1f}°C")
    #cols[2].metric("Dry Bulb Temperature", f"{weather_data['temp']:.1f}°C")
    #cols[3].metric("**Weather Stations Used:**", f"{weather_data['station_count']}")

    # Add some vertical space
    # st.markdown("<br>", unsafe_allow_html=True)



    #col1, col2 = st.columns(2)
    #col1.markdown("### **Calculated WBGT**:  {:.1f}°C".format(wbgt))
    #col2.markdown(f"### {category}")


    # Full-width recommendation
    

    # Visualization
    # st.subheader("Heat Stress Risk Zones")
    fig = create_wbgt_graph(
        current_temp=weather_data['temp'],
        current_humidity=weather_data['humidity'],
        solar_radiation=weather_data['solar_radiation'],
        wind_speed=weather_data['wind_speed']  # This was missing
    )
    st.plotly_chart(fig)

    st.info(f"**Recommendation:** {advice}")




#with tab1:
#    st.markdown(faq.show_faq())

#with tab2:
#    st.markdown(accuracy_notes.show_accuracy_notes())

#with tab3:
#    st.markdown(about.show_about())


# Add some vertical space
st.markdown("<br>", unsafe_allow_html=True)

