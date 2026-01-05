"""Pytest configuration and fixtures for ndastro_engine tests."""

import pytest


@pytest.fixture
def sample_coordinates() -> dict[str, tuple[float, float]]:
    """Provide sample geographic coordinates for testing.

    Returns
    -------
        dict: Dictionary of location names to (latitude, longitude) tuples.

    """
    return {
        "new_york": (40.7128, -74.0060),
        "london": (51.5074, -0.1278),
        "tokyo": (35.6762, 139.6503),
        "sydney": (-33.8688, 151.2093),
        "mumbai": (19.0760, 72.8777),
    }


@pytest.fixture
def sample_dates() -> list[str]:
    """Provide sample dates for testing.

    Returns
    -------
        list: List of date strings in YYYY-MM-DD format.

    """
    return [
        "2026-01-05",  # Current date
        "2026-03-20",  # Spring equinox
        "2026-06-21",  # Summer solstice
        "2026-09-23",  # Autumn equinox
        "2026-12-21",  # Winter solstice
    ]
