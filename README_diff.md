# 🌧️ Experiment 1: Short-term Rainfall Forecasting & Alert System

> Smart Water Lab Series | Week 5 Session A | Duration: 2 hours

An interactive real-time rainfall monitoring system that integrates external weather APIs, implements threshold-based alerting logic, and displays results through a Streamlit web dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-0077B6?style=for-the-badge&logo=openweathermap&logoColor=white)

---

## 📋 Overview

This experiment focuses on building a real-time rainfall monitoring system for urban flood management. The system:

- **Fetches** current weather data from OpenWeatherMap API
- **Implements** threshold-based alerting (Green/Yellow/Red levels)
- **Displays** results through an interactive Streamlit dashboard
- **Logs** critical alerts to file with timestamps
- **Provides** optional extensions for enhanced functionality

### Rainfall Intensity Categories

| Category | Intensity (mm/h) | Color Code | Alert Level |
|----------|------------------|------------|-------------|
| Light | < 2.5 | Green | Normal |
| Moderate | 2.5 - 8 | Blue | Normal |
| Heavy | 8 - 16 | Yellow | Moderate |
| Violent | ≥ 16 | Red | ALERT |

**Alert Thresholds Used in This Experiment:**
- 🟢 **Green**: Rainfall < 10 mm/h (Normal)
- 🟡 **Yellow**: 10 ≤ Rainfall < 20 mm/h (Moderate)
- 🔴 **Red**: Rainfall ≥ 20 mm/h (Heavy - ALERT)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org))
- OpenCode Cloud environment or local Python installation

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /workspace
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key (optional):**
   ```bash
   export OPENWEATHERMAP_API_KEY="your_api_key_here"
   ```
   Or enter it directly in the Streamlit sidebar when running.

### Running the Application

```bash
streamlit run weather_monitor.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
/workspace/
│
├── weather_monitor.py      # Main application code (API, alerts, dashboard)
├── test_weather_monitor.py # Comprehensive test suite (24 tests)
├── alert_log.txt           # Auto-generated log of Red alerts
├── prompt_log.md           # Documentation of AI interactions
├── requirements.txt        # Python dependencies
├── README.md               # This file - project documentation
└── __pycache__/            # Python bytecode cache
```

---

## 🎯 Features

### Core Features (Required)

| Feature | Description |
|---------|-------------|
| **API Integration** | Fetches real-time weather data from OpenWeatherMap API |
| **Error Handling** | Graceful handling of API errors, timeouts, and missing data |
| **Threshold Alerting** | Three-level alert system (Green/Yellow/Red) based on rainfall intensity |
| **Alert Logging** | Automatic logging of Red alerts to `alert_log.txt` with timestamps |
| **Interactive Dashboard** | Real-time display with color-coded status indicators |
| **Auto-refresh** | Manual refresh button for updating data |

### Optional Extensions (Implemented)

| Extension | Description |
|-----------|-------------|
| **🌍 Multi-City Monitoring** | Monitor multiple cities simultaneously with side-by-side comparison |
| **📱 Simulated Notifications** | Toast notifications for Red alerts (simulates Email/SMS) |
| **📈 Rainfall Prediction** | Linear trend prediction for next hour's rainfall |
| **🗺️ Interactive Map** | Folium-based world map with color-coded city markers |

---

## 🔧 Configuration

### Sidebar Options

- **API Key Input**: Enter your OpenWeatherMap API key securely (password field)
- **City Selection**: Choose from predefined cities (Beijing, Shanghai, Guangzhou, Shenzhen, London, New York)
- **Refresh Button**: Manually trigger data refresh

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHERMAP_API_KEY` | Your OpenWeatherMap API key | Placeholder |

---

## 🧪 Testing

Run the comprehensive test suite to verify all functionality:

```bash
python -m unittest test_weather_monitor -v
```

### Test Coverage

- **Alert Logic Tests**: Verify correct threshold boundaries (8 tests)
- **Rainfall Extraction Tests**: Validate API response parsing (4 tests)
- **Logging Tests**: Ensure proper file creation and format (3 tests)
- **Historical Simulation Tests**: Check data generation (3 tests)
- **Prediction Tests**: Validate trend forecasting (3 tests)
- **Notification Tests**: Confirm alert-triggered notifications (1 test)
- **Threshold Constants Tests**: Verify configuration values (2 tests)

**Total: 24 tests** - All passing ✅

---

## 📊 Dashboard Components

1. **Title Header**: "🌧️ Rainfall Monitor - Smart Water Lab"
2. **City Cards**: One card per selected city showing:
   - Current rainfall (large metric)
   - Color-coded status indicator
   - Historical trend chart
   - Next-hour prediction
   - Raw API data (expandable)
3. **Interactive Map**: World map with color-coded markers for each city
4. **Data Table**: Detailed view of all monitored cities
5. **Footer**: Experiment info and log file location

---

## 📝 Deliverables Checklist

| File | Status | Description |
|------|--------|-------------|
| `weather_monitor.py` | ✅ Complete | Main application with all features |
| `alert_log.txt` | ✅ Generated | Log of triggered Red alerts |
| `prompt_log.md` | ✅ Complete | AI interaction documentation |
| `test_weather_monitor.py` | ✅ Complete | Comprehensive test suite |
| `README.md` | ✅ Complete | This documentation file |
| Dashboard Screenshot | 📸 | Run app and capture manually |

---

## 🔍 Validation Results

### Physical Reasonableness
- Rainfall values from API are in realistic range (0-100 mm/h)
- Zero rainfall correctly indicates no precipitation
- Alert thresholds align with China Meteorological Administration standards

### Alert Logic Verification
| Test Input | Expected | Result |
|------------|----------|--------|
| 5.0 mm/h | Green | ✅ Pass |
| 10.0 mm/h | Yellow | ✅ Pass |
| 15.5 mm/h | Yellow | ✅ Pass |
| 19.99 mm/h | Yellow | ✅ Pass |
| 20.0 mm/h | Red | ✅ Pass |
| 50.0 mm/h | Red | ✅ Pass |

### Logging Verification
- Timestamps follow `[YYYY-MM-DD HH:MM:SS]` format
- Entries include city name, alert level, and rainfall value
- Multiple alerts append correctly without overwriting

---

## 🛠️ Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing dependencies | Run `pip install -r requirements.txt` |
| API returns 401 | Invalid/Missing API key | Enter valid key in sidebar |
| Rainfall always 0.0 | No rain at location | Expected behavior; test with different city |
| Map not displaying | Missing coordinates | Ensure city is in predefined list |
| Streamlit won't start | Port in use | Use `streamlit run weather_monitor.py --server.port 8502` |

### API Rate Limits
- Free OpenWeatherMap tier: 60 calls/minute
- Dashboard refreshes on demand to stay within limits
- Consider caching for production deployments

---

## 📚 Learning Objectives Achieved

- ✅ Integrated external weather APIs using AI assistance
- ✅ Implemented threshold-based alerting logic
- ✅ Built a real-time monitoring dashboard with Streamlit
- ✅ Applied domain knowledge to validate results
- ✅ Documented AI interactions in the Prompt Log
- ✅ Created comprehensive test suite for validation
- ✅ Implemented all four optional extensions

---

## 👥 Student Information

- **Course**: Software Development
- **Experiment**: Short-term Rainfall Forecasting & Alert System
- **Institution**: Smart Water Lab Series
- **Date**: [Insert Submission Date]

---

## 📄 License

This project was created for educational purposes as a university assignment.

© 2025 Smart Water Lab - Experiment 1. All rights reserved.
