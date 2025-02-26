import pandas as pd
import streamlit as st


# Load cities data
@st.cache_data
def load_cities():
    try:
        return pd.read_csv("cities.csv").set_index("city").to_dict(orient="index")
    except Exception as e:
        st.error(f"Error loading cities data: {e}")
        return {}
