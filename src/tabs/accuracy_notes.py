def show_accuracy_notes():
    return """
## WBGT Calculation Accuracy Notes
    
### Data Sources & Accuracy
| **Parameter**       | **Accuracy**                          | **Source**                          |
|----------------------|---------------------------------------|--------------------------------------|
| Temperature          | ±1°C (stations) / ±2°C (model)       | Ground stations & satellite models  |
| Humidity             | ±5% RH (station) / ±10% RH (model)   | Direct measurements & interpolation |
| Wind Speed           | ±2 m/s (stations) / ±3 m/s (model)   | Affected by local topography         |
| Solar Radiation      | ±15% (clear sky) / ±25% (cloudy)     | GOES-R satellite estimates           |

### Critical WBGT Considerations
1. **Black Globe Temperature Estimation**  
   `Tg = Tair + (SolarRadiation/(200 + 10*WindSpeed))`  
   - Potential error: ±2°C vs actual globe thermometer

2. **Update Frequency**  
   - Data refreshes every 15-60 minutes

3. **Spatial Resolution**  
   - Represents ~10km grid averages

4. **Nighttime Limitations**  
   - Doesn't account for artificial heat sources

### Error Ranges by WBGT Level
| WBGT Range | Potential Error |
|------------|-----------------|
| <27°C      | ±1°C            |
| 27-32°C    | ±1.5°C          |
| >32°C      | ±2°C            |

### When to Trust/Doubt the Data
**High Confidence**  
✓ Clear sky daylight hours  
✓ Multiple weather stations reporting  
✓ Stable weather conditions  

**Low Confidence**  
✗ Within 2 hours of sunrise/sunset  
✗ Rapidly changing weather  
✗ Mountainous/forested terrain  

### Recommendations
- Add ±2°C error margin for safety decisions
- Check `stations` array length in API response
- Flag data older than 30 minutes
- Not for medical/occupational compliance use

*Note: These estimates are for general heat risk awareness only. Always verify with on-site measurements for critical applications.*


**Key Limitations:**
- 🕒 15-60 minute update delay
- 🌆 Urban heat islands not captured
- 🌙 Nighttime artificial heat not included
    """