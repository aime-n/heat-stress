import streamlit as st


def show_faq():
    return """
    ### Perguntas Frequentes
    
    **P: O que é o WBGT?**  
    R: O Wet Bulb Globe Temperature (WBGT) é uma medida de como o calor é percebido sob luz solar direta.
    Ele combina:
    - Temperatura 🌡️
    - Umidade 💧
    - Vento 🌬️
    - Radiação solar ☀️
    O WBGT é utilizado para avaliar o estresse térmico e determinar níveis seguros de exposição a altas temperaturas.

    **P: Com que frequência os dados são atualizados?**  
    R: A cada 15-60 minutos a partir das estações meteorológicas

    **P: Posso usar isso para segurança no local de trabalho?**  
    R: Use apenas como orientação - sempre verifique com medições no local

    **P: Quem usa o WBGT?**  
    R: Higienistas industriais, atletas, eventos esportivos, militares, alguns ambientes de trabalho e, aparentemente, você.

    **P: Como o WBGT se compara ao índice de calor?**  
    R:
    - O WBGT é usado para medir o estresse térmico sob luz solar direta, enquanto o índice de calor é usado para medir o estresse térmico em áreas sombreadas
    - O WBGT leva em consideração mais fatores do que o índice de calor
    """


st.markdown(show_faq())
