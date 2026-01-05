"""Unit tests for ndastro_engine.astro_engine module."""

from datetime import datetime

import pytz

from ndastro_engine.core import get_sunrise_sunset


class TestGetSunriseSunset:
    """Test cases for get_sunrise_sunset function."""

    def test_get_sunrise_sunset_basic(self) -> None:
        """Test basic sunrise/sunset calculation."""
        # Setup test data
        lat = 12.97
        lon = 77.59
        test_date = datetime(2026, 1, 5, 10, 0, 0, tzinfo=pytz.timezone("UTC"))

        # Execute function
        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date)

        # Assertions
        assert sunrise.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S") == "06:43:09"
        assert sunset.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S") == "18:06:46"
