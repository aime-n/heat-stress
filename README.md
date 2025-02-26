# WBGT Heat Stress Monitoring App

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A real-time Wet Bulb Globe Temperature (WBGT) monitoring app for Brazil, designed to assess heat stress risks using weather data from Visual Crossing API.

---

## Features
- **Real-Time WBGT Calculation**:  
  Uses temperature, humidity, wind speed, and solar radiation data.
- **Heat Stress Risk Levels**:  
  Categorizes risk from Safe to Extreme Danger.
- **Interactive Visualization**:  
  Displays WBGT risk zones with current conditions.
- **Data Transparency**:  
  Shows the number of weather stations used for accuracy.
- **City Selection**:  
  Supports multiple Brazilian cities with coordinates.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aime-n/heat-stress.git
   cd wbgt-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file:
   ```env
   VISUALCROSSING_API_KEY=your_api_key_here
   ```

---

## Usage

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. Select a Brazilian city from the dropdown.

3. View real-time:
   - WBGT calculation
   - Heat stress risk level
   - Weather station data
   - Interactive risk zone graph

---

## Project Structure
```
wbgt-app/
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── cities.csv              # Brazilian cities data
└── src/
    └── wbgt_app/           # Main application package
        ├── __init__.py     # Package initialization
        ├── app.py          # Streamlit app entry point
        ├── api_client.py   # Weather data fetching
        ├── calculations.py # WBGT formulas
        ├── data_loader.py  # Cities data loading
        ├── visualizations.py # Plotly graphs
        └── sidebar/        # Sidebar content
            ├── __init__.py
            ├── faq.py      # FAQ content
            ├── accuracy_notes.py # Accuracy info
            ├── about.py    # About the app
            └── contact.py  # Contact info
```

---

## API Key
This app uses the [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api).  
Get a free API key and add it to your `.env` file.

---

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contact
For questions or feedback, contact:  
📧 [aime.nobrega@gmail.com](mailto:aime.nobrega@gmail.com)  
