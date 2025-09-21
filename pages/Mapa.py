import streamlit as st
import pandas as pd
from src.data_loader import load_cities
from src.visualization import create_brazil_heatmap, highlight_row, plot_wbgt_contour, plot_wbgt_contour_brazil
from data_processing import get_multiple_cities_data, group_by_state


BRAZIL_CITIES = load_cities()

cities_wbgt = get_multiple_cities_data(BRAZIL_CITIES)

df = pd.DataFrame(cities_wbgt)

top10 = df.sort_values('WBGT', ascending=False).head(10)

st.subheader("Top 10 Cidades com maior índice de calor WBGT")
st.dataframe(
    top10[['Cidade', 'Estado', 'WBGT', 'Categoria WBGT']],
    use_container_width=True
)

state_df = group_by_state(df)

st.title("Mapa de Risco de Calor no Brasil - Por Estado")

st.subheader("Mapa de Risco de Calor no Brasil")

# Criar e exibir o mapa
fig = create_brazil_heatmap(state_df)
# Adicione tooltips interativos
fig.update_traces(
    hovertemplate="<b>%{location}</b><br>WBGT: %{z}°C<extra></extra>",
    marker_line_width=0.5,
    marker_opacity=0.8
)

st.plotly_chart(fig, use_container_width=True)

# Adicionar pontos no mapa para cidades específicas
#st.map(df[['lat', 'lon', 'WBGT', 'color_column']],
#        color='color_column',  # Crie uma coluna com cores baseadas na categoria
#        size='WBGT',  # Opcional: tamanho do ponto baseado no WBGT
#        zoom=3)

# Legenda interativa

st.markdown("""
**Legenda do Mapa:**
- <span style='color:#a8e6cf;'>■</span> Seguro (<27.8°C)
- <span style='color:#ffd3b6;'>■</span> Cuidado (27.8-29.3°C)
- <span style='color:#ffaaa5;'>■</span> Cuidado Extremo (29.4-31.0°C)
- <span style='color:#ff8b94;'>■</span> Perigo (31.0-32.1°C)
- <span style='color:#ff0000;'>■</span> Perigo Extremo (≥32.1°C)
""", unsafe_allow_html=True)

fig = plot_wbgt_contour_brazil(df)

# Display in Streamlit
st.pyplot(fig)


if st.button('Atualizar Dados do Mapa'):
    st.cache_data.clear()
    df = get_multiple_cities_data(BRAZIL_CITIES)
    state_df = group_by_state(df)
    fig = create_brazil_heatmap(state_df)
    st.plotly_chart(fig, use_container_width=True)

    fig = plot_wbgt_contour_brazil(df)

    # Display in Streamlit
    st.pyplot(fig)