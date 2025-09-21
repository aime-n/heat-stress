import numpy as np


def calculate_black_globe(temp, solar_radiation, wind_speed):
    """Calculate black globe temperature (Tg) using solar radiation"""
    # Formula from ISO 7243:2017 approximation (modified for W/m² input)
    return temp + (solar_radiation / (190 + 11 * wind_speed))


def calculate_wet_bulb(temp, humidity):
    """Calculate wet bulb temperature using Stull's formula"""
    # TODO - Implement a more accurate formula
    t = temp
    rh = humidity
    tw = t * np.arctan(0.151977 * (rh + 8.313659)**0.5)
    tw += np.arctan(t + rh) - np.arctan(rh - 1.676331)
    tw += 0.00391838 * rh**1.5 * np.arctan(0.023101 * rh)
    tw -= 4.686035
    return tw


def wbt(tc, hr):
    """
    Calcule la température de thermomètre mouillé en °C à partir de :
    tc : température de l'air en °C
    hr : humidité relative en %
    
    Référence : https://journals.ametsoc.org/view/journals/apme/50/11/jamc-d-11-0143.1.xml
    """
    th = (
    tc * np.arctan(0.151977 * np.sqrt(hr + 8.313659))
    + np.arctan(tc + hr)
    - np.arctan(hr - 1.676331)
    + 0.00391838 * (hr) ** (3 / 2) * np.arctan(0.023101 * hr)
    - 4.686035
        )
    return th

def calculate_wbgt(temp, humidity, solar_radiation, wind_speed):
    """Calculate full WBGT using official formula"""
    tw = calculate_wet_bulb(temp, humidity)
    tg = calculate_black_globe(temp, solar_radiation, wind_speed)
    return 0.7 * tw + 0.2 * tg + 0.1 * temp

def get_heat_category(wbgt):
    """Classifica o risco de calor com base nos limites de WBGT e dá diretrizes de atividades"""
    if wbgt < 27.8:
        #return "✅ Tranquilo", "Pode seguir as atividades externas, sem limitações."
        return "Seguro", "Pode seguir as atividades externas, sem limitações."
    elif 27.8 <= wbgt < 29.4:
        #return "⚠️ Fique esperto", "Aumente a hidratação e evite longos períodos sob o sol."
        return "Cuidado", "Aumente a hidratação e evite longos períodos sob o sol."
    elif 29.4 <= wbgt < 31.0:
        #return "🚨 Cuidado Extremo", "Limite as atividades externas. Evite exposição prolongada ao sol."
        return "Cuidado Extremo", "Limite as atividades externas. Evite exposição prolongada ao sol."
    elif 31.0 <= wbgt < 32.1:
        #return "🔥 Perigo", "Cancele atividades externas não essenciais. Descanse em ambientes frescos."
        return "Perigo", "Cancele atividades externas não essenciais. Descanse em ambientes frescos."
    else:
        #return "💀 Perigo Extremo", "Evite sair de casa. Se necessário, use proteção intensa contra o sol."
        return "Perigo Extremo", "Evite sair de casa. Se necessário, use proteção intensa contra o sol."
