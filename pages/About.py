import streamlit as st


def show_about():
    return """
    ## Sobre Este App
    
    **Objetivo:**  
    Fornecer monitoramento em tempo real de estresse térmico para o Brasil usando:
    - Dados de código aberto 🌐
    - Diretrizes de segurança médica 🩺
    - Integração com API de clima ⚙️

    **Versão:** 1.0.0  
    **Última atualização:** Fevereiro de 2025
    """
st.markdown(show_about())
