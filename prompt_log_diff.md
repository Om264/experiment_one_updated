--- prompt_log.md (原始)


+++ prompt_log.md (修改后)
# Prompt Log - Experiment 1: Rainfall Alert System

## Student Information
- **Course**: Software Development
- **Experiment**: Short-term Rainfall Forecasting & Alert System
- **Date**: [Insert Date]

---

## AI Interaction Documentation

### Interaction 1: Initial Code Structure Request
**Prompt:**
> I am a water resources student building a rainfall monitoring system. Please write Python code to fetch current weather data for Beijing using the OpenWeatherMap API. The code should:
> 1. Use the requests library to make the API call
> 2. Extract rainfall intensity from the response
> 3. Handle API errors gracefully
> 4. Include comments explaining each step
> API endpoint: https://api.openweathermap.org/data/2.5/weather

**AI Response Summary:**
The AI generated a basic `fetch_weather_data` function using the `requests` library with error handling (try-except block) and timeout settings. It correctly identified the need to parse JSON response.

**Corrections/Refinements Made:**
- Added explicit timeout parameter (10s) to prevent hanging requests.
- Modified to accept `city` and `api_key` as parameters for flexibility.
- Added type hints for better code documentation.

---

### Interaction 2: Alert Logic Implementation
**Prompt:**
> Implement threshold-based alerting logic for rainfall. Requirements:
> - Green: Rainfall < 10 mm/h (Normal)
> - Yellow: 10 ≤ Rainfall < 20 mm/h (Moderate)
> - Red: Rainfall ≥ 20 mm/h (Heavy - ALERT)
> Return both the level name and a color code for UI display.

**AI Response Summary:**
Generated `determine_alert_level` function returning a tuple of (level, color). Used hex codes for web compatibility.

**Corrections/Refinements Made:**
- Verified thresholds match experiment requirements exactly.
- Ensured strict inequality checks (< vs <=) match the specification.

---

### Interaction 3: Dashboard Layout
**Prompt:**
> Create a Streamlit dashboard that displays:
> 1. Title 'Rainfall Monitor'
> 2. Current rainfall as a large metric
> 3. Color-coded alert status
> 4. Support for multiple cities
> 5. Auto-refresh capability

**AI Response Summary:**
Provided structure using `st.columns` for multi-city layout and `st.metric` for displaying values. Suggested `st.rerun()` for refresh functionality.

**Corrections/Refinements Made:**
- Implemented sidebar for configuration (API Key, City Selection).
- Added HTML injection (`unsafe_allow_html=True`) for custom colored status boxes since Streamlit's native alerts are limited to specific colors.
- Added a manual "Refresh" button to trigger updates.

---

### Interaction 4: Optional Extensions
**Prompt:**
> How can I add these optional extensions?
> 1. Multiple city monitoring
> 2. Email/SMS notifications for alerts
> 3. Rainfall prediction using historical trends
> 4. Map visualization with Folium

**AI Response Summary:**
- **Multiple Cities**: Suggested using `st.multiselect` and iterating through selected cities to create dynamic columns.
- **Notifications**: Proposed simulating email/SMS via `st.toast` for Red alerts (production would use SMTP/Twilio).
- **Prediction**: Proposed a simple linear regression approach on simulated historical data to forecast the next hour.
- **Map**: Recommended using `folium` library for interactive maps with color-coded markers based on alert levels.

**Implementation Details:**
- Created `simulate_historical_data` to generate dummy history for the chart (since real-time API only gives current data).
- Implemented `predict_next_hour` using basic slope calculation.
- Added `send_notification` function to simulate push notifications when Red alert triggers.
- Hardcoded coordinates for major cities (Beijing, Shanghai, London, New York, etc.) for the Folium map demo.
- Map markers change color (Green/Yellow/Red) based on current rainfall status.

---

## Errors Encountered & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Missing dependencies | Ran `pip install streamlit requests pandas` |
| API returns 401 Unauthorized | Invalid/Missing API Key | Added input field in sidebar for user to enter valid key |
| Rainfall always 0.0 | No rain occurring at test location | Validated logic with manual value injection; confirmed code works when API returns data |
| Map not showing | Missing 'lat'/'lon' columns | Ensured DataFrame passed to `st.map` strictly contains required column names |

---

## Validation Results

1. **API Integration**: Successfully fetches data for Beijing, Shanghai, etc.
2. **Alert Logic**:
   - Tested with mock value 5.0 -> Returns Green
   - Tested with mock value 15.0 -> Returns Yellow
   - Tested with mock value 25.0 -> Returns Red & Logs to file
3. **Logging**: `alert_log.txt` created with proper timestamps upon Red alert.
4. **Physical Reasonableness**: Values returned by API are in mm/h range (0-100 typically), which matches physical expectations for rainfall intensity.

---

## Final Code Structure
- `weather_monitor.py`: Main application containing all logic and UI.
- `alert_log.txt`: Auto-generated log file.
- `prompt_log.md`: This file.