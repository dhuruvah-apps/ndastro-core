"""Provides functions to determine if a planet is in retrograde motion."""

from datetime import datetime, timedelta
from typing import cast

from skyfield.searchlib import find_discrete
from skyfield.timelib import Time

from ndastro_engine.config import ts
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums import Planets


class RetrogradeFunction:
    """A class to determine if a planet is in retrograde motion from a given location on Earth.

    Attributes:
        planet_name (str): The name of the planet to observe.
        latitude (float): The latitude of the observer's location.
        longitude (float): The longitude of the observer's location.
        step_days (int): The number of days to step back for comparison (default is 7).

    Methods:
        __call__(t: Time) -> bool:
            Determines if the planet is in retrograde motion at the given time `t`.
            Returns True if the planet is in retrograde motion, otherwise False.

    """

    def __init__(self, planet_name: str, latitude: float, longitude: float) -> None:
        """Initialize a new instance of the retrograde class.

        Args:
            planet_name (str): The name of the planet.
            latitude (float): The latitude coordinate.
            longitude (float): The longitude coordinate.

        """
        self.planet_name = planet_name
        self.latitude = latitude
        self.longitude = longitude
        self.step_days = 7

    def __call__(self, t: Time) -> bool:
        """Determine if the planet is in retrograde motion at a given time.

        This method calculates the ecliptic longitude of the planet at the given time `t`
        and compares it with the ecliptic longitude of the planet at the previous time `t-1`.
        If the longitude decreases, the planet is in retrograde motion.

        Args:
            t (Time): The time at which to check for retrograde motion.

        Returns:
            bool: True if the planet is in retrograde motion, False otherwise.

        """
        lon_now = get_planet_position(Planets.from_code(self.planet_name), self.latitude, self.longitude, cast("datetime", t.utc_datetime()))
        lon_prev = get_planet_position(Planets.from_code(self.planet_name), self.latitude, self.longitude, cast("datetime", (t - 1).utc_datetime()))

        return cast("float", lon_now.longitude) < cast(
            "float",
            lon_prev.longitude,
        )  # Retrograde if longitude decreases


def __get_retrograde_function(
    planet_name: str,
    latitude: float,
    longitude: float,
) -> RetrogradeFunction:
    """Create a RetrogradeFunction instance for a given planet and location.

    Args:
        planet_name (str): The name of the planet.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        RetrogradeFunction: An instance of RetrogradeFunction for the specified planet and location.

    """
    return RetrogradeFunction(planet_name, latitude, longitude)


def find_retrograde_periods(
    start_date: datetime,
    end_date: datetime,
    planet_name: str,
    latitude: float,
    longitude: float,
) -> list[tuple[datetime, datetime]]:
    """Calculate the retrograde periods for a given planet within a specified date range and location.

    Args:
        start_date (datetime): The start date of the period to check for retrograde motion.
        end_date (datetime): The end date of the period to check for retrograde motion.
        planet_name (str): The name of the planet to check for retrograde motion.
        latitude (float): The latitude of the observation location.
        longitude (float): The longitude of the observation location.

    Returns:
        list[tuple[datetime, datetime]]: A list of tuples, each containing the start and end datetime of a retrograde period.

    """
    # Time range for 2025
    t0 = ts.utc(start_date)
    t1 = ts.utc(end_date)

    # Find times where Venus changes direction
    times, values = find_discrete(
        t0,
        t1,
        __get_retrograde_function(planet_name, latitude, longitude),
    )
    retrograde_periods = []
    in_retrograde = False
    retro_start = None

    for t, retro in zip(times, values, strict=False):
        if retro:
            if not in_retrograde:
                retro_start = cast("Time", t).utc_datetime()
                in_retrograde = True
        elif in_retrograde:
            retrograde_periods.append((retro_start, t.utc_datetime()))
            in_retrograde = False

    if in_retrograde:
        retrograde_periods.append((retro_start, t1.utc_datetime()))

    return retrograde_periods


def is_planet_in_retrograde(
    check_date: datetime,
    planet_name: str,
    latitude: float,
    longitude: float,
) -> tuple[bool, datetime | None, datetime | None]:
    """Check if a planet is in retrograde motion on a specific date.

    Args:
        check_date (datetime): The date to check for retrograde motion.
        planet_name (str): The name of the planet to check.
        latitude (float): The latitude in decimal degrees of the observation location.
        longitude (float): The longitude in decimal degrees of the observation location.

    Returns:
        tuple[bool, datetime | None, datetime | None]: A tuple containing:
            - bool: True if the planet is in retrograde motion on the given date, otherwise False.
            - datetime | None: The start date of the retrograde period (None if not in retrograde).
            - datetime | None: The end date of the retrograde period (None if not in retrograde).

    """
    if planet_name not in [Planets.SUN.code, Planets.MOON.code, Planets.ASCENDANT.code, Planets.EMPTY.code]:
        start_date = check_date - timedelta(days=365)
        end_date = check_date + timedelta(days=365)
        retrograde_periods = find_retrograde_periods(
            start_date,
            end_date,
            planet_name,
            latitude,
            longitude,
        )

        for period_start, period_end in retrograde_periods:
            if period_start <= check_date <= period_end:
                return (True, period_start, period_end)

    return (False, None, None)
