--- test_weather_monitor.py (原始)


+++ test_weather_monitor.py (修改后)
"""
Test suite for Experiment 1: Rainfall Alert System
Tests API integration, alert logic, logging, and optional extensions.
"""

import unittest
from datetime import datetime
import os
import sys

# Import functions from weather_monitor
from weather_monitor import (
    extract_rainfall,
    determine_alert_level,
    log_alert,
    simulate_historical_data,
    predict_next_hour,
    send_notification,
    THRESHOLDS,
    LOG_FILE
)


class TestAlertLogic(unittest.TestCase):
    """Test threshold-based alerting logic."""

    def test_green_alert_low_rainfall(self):
        """Rainfall < 10 mm/h should return Green."""
        level, color = determine_alert_level(5.0)
        self.assertEqual(level, "Green")
        self.assertEqual(color, "#28a745")

    def test_green_alert_zero_rainfall(self):
        """Zero rainfall should return Green."""
        level, color = determine_alert_level(0.0)
        self.assertEqual(level, "Green")

    def test_yellow_alert_boundary_low(self):
        """Rainfall exactly 10 mm/h should return Yellow."""
        level, color = determine_alert_level(10.0)
        self.assertEqual(level, "Yellow")
        self.assertEqual(color, "#ffc107")

    def test_yellow_alert_middle(self):
        """Rainfall between 10-20 mm/h should return Yellow."""
        level, color = determine_alert_level(15.5)
        self.assertEqual(level, "Yellow")

    def test_yellow_alert_boundary_high(self):
        """Rainfall just below 20 mm/h should return Yellow."""
        level, color = determine_alert_level(19.99)
        self.assertEqual(level, "Yellow")

    def test_red_alert_boundary(self):
        """Rainfall exactly 20 mm/h should return Red."""
        level, color = determine_alert_level(20.0)
        self.assertEqual(level, "Red")
        self.assertEqual(color, "#dc3545")

    def test_red_alert_heavy(self):
        """Rainfall > 20 mm/h should return Red."""
        level, color = determine_alert_level(50.0)
        self.assertEqual(level, "Red")

    def test_red_alert_extreme(self):
        """Extreme rainfall should still return Red."""
        level, color = determine_alert_level(100.0)
        self.assertEqual(level, "Red")


class TestRainfallExtraction(unittest.TestCase):
    """Test rainfall extraction from API responses."""

    def test_extract_rain_1h(self):
        """Extract rainfall from 1h data."""
        data = {'rain': {'1h': 5.5}}
        rainfall = extract_rainfall(data)
        self.assertEqual(rainfall, 5.5)

    def test_extract_rain_3h(self):
        """Extract rainfall from 3h data (should divide by 3)."""
        data = {'rain': {'3h': 9.0}}
        rainfall = extract_rainfall(data)
        self.assertEqual(rainfall, 3.0)

    def test_extract_no_rain(self):
        """No rain key should return 0.0."""
        data = {'weather': [{'main': 'Clouds'}]}
        rainfall = extract_rainfall(data)
        self.assertEqual(rainfall, 0.0)

    def test_extract_empty_rain(self):
        """Empty rain object should return 0.0."""
        data = {'rain': {}}
        rainfall = extract_rainfall(data)
        self.assertEqual(rainfall, 0.0)


class TestLogging(unittest.TestCase):
    """Test alert logging functionality."""

    def setUp(self):
        """Create a test log file."""
        self.test_log = "test_alert_log.txt"
        # Temporarily change LOG_FILE for testing
        import weather_monitor
        self.original_log = weather_monitor.LOG_FILE
        weather_monitor.LOG_FILE = self.test_log

    def tearDown(self):
        """Clean up test log file."""
        import weather_monitor
        weather_monitor.LOG_FILE = self.original_log
        if os.path.exists(self.test_log):
            os.remove(self.test_log)

    def test_log_alert_creates_file(self):
        """Logging should create file if it doesn't exist."""
        log_alert("TestCity", 25.0, "Red")
        self.assertTrue(os.path.exists(self.test_log))

    def test_log_alert_format(self):
        """Log entry should have correct format with timestamp."""
        log_alert("Beijing", 30.5, "Red")
        with open(self.test_log, 'r') as f:
            content = f.read()

        # Check timestamp format [YYYY-MM-DD HH:MM:SS]
        self.assertIn("[20", content)
        self.assertIn("ALERT: Beijing", content)
        self.assertIn("Level: Red", content)
        self.assertIn("Rainfall: 30.50 mm/h", content)

    def test_log_alert_appends(self):
        """Multiple logs should append, not overwrite."""
        log_alert("City1", 21.0, "Red")
        log_alert("City2", 22.0, "Red")
        with open(self.test_log, 'r') as f:
            lines = f.readlines()
        self.assertGreaterEqual(len(lines), 2)


class TestHistoricalSimulation(unittest.TestCase):
    """Test historical data simulation for charts."""

    def test_simulate_returns_dataframe(self):
        """Should return a pandas DataFrame."""
        df = simulate_historical_data(10.0, hours=5)
        self.assertEqual(len(df), 5)
        self.assertIn('Time', df.columns)
        self.assertIn('Rainfall (mm/h)', df.columns)

    def test_simulate_custom_hours(self):
        """Should generate specified number of hours."""
        df = simulate_historical_data(5.0, hours=10)
        self.assertEqual(len(df), 10)

    def test_simulate_non_negative(self):
        """Simulated values should be non-negative."""
        df = simulate_historical_data(0.5, hours=20)
        self.assertTrue(all(df['Rainfall (mm/h)'] >= 0))


class TestPrediction(unittest.TestCase):
    """Test rainfall prediction using historical trends."""

    def test_predict_with_history(self):
        """Prediction should work with sufficient history."""
        import pandas as pd
        from datetime import datetime

        history = pd.DataFrame({
            'Time': pd.date_range(end=datetime.now(), periods=5, freq='H'),
            'Rainfall (mm/h)': [5, 8, 12, 15, 18]  # Increasing trend
        })

        prediction = predict_next_hour(18.0, history)
        # Should predict higher than current due to upward trend
        self.assertGreater(prediction, 18.0)

    def test_predict_insufficient_history(self):
        """Should return current value if history too short."""
        import pandas as pd
        history = pd.DataFrame({'Time': [datetime.now()], 'Rainfall (mm/h)': [10.0]})
        prediction = predict_next_hour(10.0, history)
        self.assertEqual(prediction, 10.0)

    def test_predict_non_negative(self):
        """Prediction should never be negative."""
        import pandas as pd
        history = pd.DataFrame({
            'Time': pd.date_range(end=datetime.now(), periods=3, freq='H'),
            'Rainfall (mm/h)': [10, 5, 1]  # Decreasing trend
        })
        prediction = predict_next_hour(1.0, history)
        self.assertGreaterEqual(prediction, 0.0)


class TestNotifications(unittest.TestCase):
    """Test notification system for alerts."""

    def test_notification_only_on_red(self):
        """Notifications should only trigger on Red alerts."""
        # This test mainly verifies the logic path
        # Actual st.toast calls are tested manually in dashboard
        result_green = send_notification("City", "Green", 5.0)
        result_yellow = send_notification("City", "Yellow", 15.0)
        result_red = send_notification("City", "Red", 25.0)

        self.assertIsNone(result_green)
        self.assertIsNone(result_yellow)
        self.assertIsNotNone(result_red)
        self.assertIn("CRITICAL ALERT", result_red)


class TestThresholdConstants(unittest.TestCase):
    """Test threshold configuration."""

    def test_thresholds_defined(self):
        """Thresholds should be properly defined."""
        self.assertIn('Green', THRESHOLDS)
        self.assertIn('Yellow', THRESHOLDS)
        self.assertIn('Red', THRESHOLDS)

    def test_threshold_values(self):
        """Threshold values should match requirements."""
        self.assertEqual(THRESHOLDS['Green'], 10)
        self.assertEqual(THRESHOLDS['Yellow'], 20)


if __name__ == '__main__':
    print("=" * 60)
    print("Running Experiment 1: Rainfall Alert System Tests")
    print("=" * 60)
    unittest.main(verbosity=2)