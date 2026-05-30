--- weather_monitor.py (原始)


+++ weather_monitor.py (修改后)
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
from typing import Dict, List, Optional, Tuple
import folium
from streamlit_folium import st_folium
import random

# Configuration
DEFAULT_CITIES = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'London', 'New York']
API_KEY_PLACEHOLDER = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual key or set via env var
LOG_FILE = "alert_log.txt"

# Rainfall Thresholds (mm/h) as per experiment requirements
# Green: < 10 mm/h (Normal)
# Yellow: 10 ≤ Rainfall < 20 mm/h (Moderate)
# Red: Rainfall ≥ 20 mm/h (Heavy - ALERT)
THRESHOLDS = {
    'Green': 10,
    'Yellow': 20,
    'Red': float('inf')
}

def get_api_key() -> str:
    """Retrieve API key from environment variable or use placeholder."""
    return os.getenv("OPENWEATHERMAP_API_KEY", API_KEY_PLACEHOLDER)

def fetch_weather_data(city: str, api_key: str) -> Optional[Dict]:
    """
    Fetch current weather data for a given city from OpenWeatherMap API.

    Args:
        city: Name of the city
        api_key: OpenWeatherMap API key

    Returns:
        Dictionary containing weather data or None if error occurs
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use metric units
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for {city}: {e}")
        return None

def extract_rainfall(data: Dict) -> float:
    """
    Extract rainfall intensity (mm/h) from API response.
    Note: OpenWeatherMap 'rain' field often shows rain volume for the last hour.
    We treat this as mm/h for the purpose of this experiment.

    Args:
        data: JSON response from API

    Returns:
        Rainfall intensity in mm/h, 0.0 if no rain data available
    """
    if 'rain' in data:
        # API returns rain volume for last 1h (or 3h), we assume mm/h
        rain_data = data['rain']
        if '1h' in rain_data:
            return float(rain_data['1h'])
        elif '3h' in rain_data:
            # Approximate hourly rate from 3h data
            return float(rain_data['3h']) / 3.0
    return 0.0

def determine_alert_level(rainfall: float) -> Tuple[str, str]:
    """
    Determine alert level and color based on rainfall intensity.

    Args:
        rainfall: Rainfall intensity in mm/h

    Returns:
        Tuple of (level_name, color_code)
    """
    if rainfall < THRESHOLDS['Green']:
        return "Green", "#28a745"  # Normal
    elif rainfall < THRESHOLDS['Yellow']:
        return "Yellow", "#ffc107"  # Moderate
    else:
        return "Red", "#dc3545"   # Heavy - ALERT

def log_alert(city: str, rainfall: float, level: str):
    """
    Log alert events to a file with timestamp.

    Args:
        city: City name
        rainfall: Rainfall intensity
        level: Alert level
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ALERT: {city} - Level: {level}, Rainfall: {rainfall:.2f} mm/h\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def simulate_historical_data(current_rain: float, hours: int = 5) -> pd.DataFrame:
    """
    Generate simulated historical data for demonstration/charting.
    In a real system, this would come from a database or past API calls.

    Args:
        current_rain: Current rainfall value
        hours: Number of hours of history to simulate

    Returns:
        DataFrame with historical timestamps and simulated rainfall
    """
    dates = pd.date_range(end=datetime.now(), periods=hours, freq='H')
    # Simulate some variation around current value
    values = [max(0, current_rain + random.uniform(-2, 2)) for _ in range(hours)]
    return pd.DataFrame({'Time': dates, 'Rainfall (mm/h)': values})

def send_notification(city: str, level: str, rainfall: float):
    """
    Optional Extension: Simulate Email/SMS notifications for alerts.
    In a production system, this would integrate with SMTP or Twilio API.
    """
    if level == "Red":
        msg = f"🚨 CRITICAL ALERT: Heavy rainfall detected in {city}! ({rainfall:.2f} mm/h)"
        st.toast(msg, icon="📱")
        return msg
    return None

def predict_next_hour(current_rain: float, history: pd.DataFrame) -> float:
    """
    Simple linear trend prediction for next hour.
    Optional Extension: Rainfall prediction using historical trends.

    Args:
        current_rain: Current rainfall
        history: Historical data dataframe

    Returns:
        Predicted rainfall for next hour
    """
    if len(history) < 2:
        return current_rain

    # Simple linear regression slope calculation
    x = list(range(len(history)))
    y = history['Rainfall (mm/h)'].values

    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_xx = sum(x[i] ** 2 for i in range(n))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2) if (n * sum_xx - sum_x ** 2) != 0 else 0

    # Predict next value
    prediction = y[-1] + slope
    return max(0.0, prediction)

# --- Streamlit Dashboard ---

def main():
    st.set_page_config(page_title="Smart Water Lab - Rainfall Monitor", layout="wide")

    st.title("🌧️ Rainfall Monitor - Smart Water Lab")
    st.markdown("---")

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    # API Key Input
    api_key = st.sidebar.text_input("OpenWeatherMap API Key", type="password", value=get_api_key())
    if api_key == API_KEY_PLACEHOLDER:
        st.sidebar.warning("Please enter your API Key in the sidebar or set OPENWEATHERMAP_API_KEY env var.")

    # Optional Extension: Multiple City Monitoring
    st.sidebar.subheader("Monitor Cities")
    selected_cities = st.sidebar.multiselect(
        "Select cities to monitor:",
        DEFAULT_CITIES,
        default=['Beijing']
    )

    if not selected_cities:
        st.info("Select at least one city from the sidebar to start monitoring.")
        st.stop()

    # Refresh Button (Simulating auto-refresh)
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    # Main Display Area
    # Create columns for multiple cities
    cols = st.columns(len(selected_cities))

    all_alerts_triggered = False

    for i, city in enumerate(selected_cities):
        with cols[i]:
            st.subheader(f"📍 {city}")

            if api_key == API_KEY_PLACEHOLDER:
                st.error("API Key missing")
                continue

            # Fetch Data
            with st.spinner(f"Fetching data for {city}..."):
                data = fetch_weather_data(city, api_key)

            if data:
                rainfall = extract_rainfall(data)
                level, color = determine_alert_level(rainfall)

                # Display Metric
                st.metric(label="Current Rainfall", value=f"{rainfall:.2f} mm/h")

                # Alert Status Indicator
                st.markdown(
                    f"""
                    <div style="padding: 10px; border-radius: 5px; background-color: {color}; color: white; text-align: center; font-weight: bold;">
                        STATUS: {level.upper()}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Trigger Alert Logic
                if level == "Red":
                    st.error("⚠️ HEAVY RAINFALL ALERT TRIGGERED!")
                    log_alert(city, rainfall, level)
                    send_notification(city, level, rainfall)  # Extension: Notification
                    all_alerts_triggered = True

                # Optional Extension: Prediction
                st.markdown("##### 📈 Trend & Prediction")
                hist_data = simulate_historical_data(rainfall)
                predicted_val = predict_next_hour(rainfall, hist_data)
                st.line_chart(hist_data.set_index('Time'))
                st.caption(f"Predicted next hour: {predicted_val:.2f} mm/h")

                # Raw Data Toggle
                with st.expander("View Raw API Data"):
                    st.json(data)
            else:
                st.error("Failed to retrieve data.")

    # Optional Extension: Map Visualization with Folium
    st.markdown("---")
    st.subheader("🗺️ Interactive City Monitoring Map")

    # Geocoding simple list for demo (In real app, use geocoder or API)
    city_coords = {
        'Beijing': (39.9042, 116.4074),
        'Shanghai': (31.2304, 121.4737),
        'Guangzhou': (23.1291, 113.2644),
        'Shenzhen': (22.5431, 114.0579),
        'London': (51.5074, -0.1278),
        'New York': (40.7128, -74.0060)
    }

    map_data = []
    for city in selected_cities:
        if city in city_coords:
            lat, lon = city_coords[city]
            # Fetch again to get current status for map tooltip
            if api_key != API_KEY_PLACEHOLDER:
                d = fetch_weather_data(city, api_key)
                r = extract_rainfall(d) if d else 0
                lvl, _ = determine_alert_level(r)
            else:
                r = 0
                lvl = "Green"

            map_data.append({
                'lat': lat,
                'lon': lon,
                'city': city,
                'rain': r,
                'level': lvl
            })

    if map_data:
        df_map = pd.DataFrame(map_data)

        # Create Folium Map
        m = folium.Map(location=[20, 0], zoom_start=2)

        for _, row in df_map.iterrows():
            # Color code markers based on alert level
            if row['level'] == 'Red':
                color = '#dc3545'
            elif row['level'] == 'Yellow':
                color = '#ffc107'
            else:
                color = '#28a745'

            popup_html = f"""
            <div style="font-family: Arial; min-width: 150px;">
                <h4>{row['city']}</h4>
                <p>Rainfall: <b>{row['rain']:.2f} mm/h</b></p>
                <p>Status: <b style="color:{color}">{row['level']}</b></p>
            </div>
            """

            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=12,
                popup=folium.Popup(popup_html, max_width=300),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                weight=2
            ).add_to(m)

        st_folium(m, width=700, height=400)

        # Detailed map table
        st.dataframe(df_map)
    else:
        st.info("No map data available for selected cities.")

    # Footer
    st.markdown("---")
    st.caption("Experiment 1: Short-term Rainfall Forecasting & Alert System | Smart Water Lab Series")
    st.caption(f"Logs are being saved to `{LOG_FILE}`")

if __name__ == "__main__":
    main()