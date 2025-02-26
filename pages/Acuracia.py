import streamlit as st

def show_accuracy_notes():
    return """
## Notas sobre a Precisão do Cálculo do WBGT
    
### Fontes de Dados & Precisão
| **Parâmetro**        | **Precisão**                          | **Fonte**                           |
|----------------------|---------------------------------------|-------------------------------------|
| Temperatura          | ±1°C (estações) / ±2°C (modelo)       | Estações terrestres & modelos de satélite |
| Umidade              | ±5% UR (estação) / ±10% UR (modelo)   | Medições diretas & interpolação     |
| Velocidade do Vento  | ±2 m/s (estações) / ±3 m/s (modelo)   | Afetado pela topografia local      |
| Radiação Solar       | ±15% (céu claro) / ±25% (nuvens)      | Estimativas do satélite GOES-R     |

### Considerações Críticas sobre o WBGT
1. **Estimativa da Temperatura do Globo Negro**  
   `Tg = Tair + (RadiaçãoSolar/(200 + 10*VelocidadeVento))`  
   - Erro potencial: ±2°C em comparação com o termômetro de globo real

2. **Frequência de Atualização**  
   - Os dados são atualizados a cada 15-60 minutos

3. **Resolução Espacial**  
   - Representa médias de grade de ~10 km

4. **Limitações Noturnas**  
   - Não leva em conta fontes de calor artificiais

### Faixas de Erro por Nível de WBGT
| Faixa de WBGT | Erro Potencial |
|---------------|----------------|
| <27°C         | ±1°C           |
| 27-32°C       | ±1.5°C         |
| >32°C         | ±2°C           |

### Quando Confiar/Duvidar dos Dados
**Alta Confiança**  
✓ Horas de dia com céu claro  
✓ Múltiplas estações meteorológicas reportando  
✓ Condições climáticas estáveis  

**Baixa Confiança**  
✗ Dentro de 2 horas do nascer/pôr do sol  
✗ Mudanças climáticas rápidas  
✗ Terreno montanhoso/florestal  

### Recomendações
- Adicionar margem de erro de ±2°C para decisões de segurança
- Verificar o comprimento do array `stations` na resposta da API
- Marcar dados com mais de 30 minutos de idade
- Não é recomendado para uso médico/ocupacional

*Nota: Estas estimativas são para conscientização geral sobre riscos térmicos. Sempre verifique com medições no local para aplicações críticas.*

**Limitações Chave:**
- 🕒 Atraso de atualização de 15-60 minutos
- 🌆 Ilhas de calor urbanas não capturadas
- 🌙 Calor artificial noturno não incluído
    """

st.markdown(show_accuracy_notes())
