import streamlit as st


def show_about():
    return """
    ## Sobre Este App
    
    **Objetivo:**  
    Fornecer monitoramento em tempo real de estresse térmico para o Brasil usando:
    - Dados acessíveis via API de clima gratuita 🌐
    - Diretrizes de segurança médica 🩺
    - 2 neurônios em hiperfoco

    **Versão:** 1.0.0  
    **Última atualização:** Fevereiro de 2025
    **Desenvolvedora:** Aimê Nobrega
    """
st.markdown(show_about())
