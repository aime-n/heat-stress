import streamlit as st


def show_about():
    return """
    ## About This App
    
    **Purpose:**  
    Provide real-time heat stress monitoring for Brazil using:
    - Open-source data 🌐
    - Medical safety guidelines 🩺
    - Weather API integration ⚙️

    **Version:** 1.0.0  
    **Last Updated:** February 2025
    """
st.markdown(show_about())