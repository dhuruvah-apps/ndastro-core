"""Astronomical calculations for ndastro engine.

This module provides functions to calculate astronomical events for ndastro engine,
for a given location and date using the Skyfield library.
"""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, cast

from skyfield.almanac import find_discrete, sunrise_sunset
from skyfield.toposlib import wgs84

from ndastro_engine.config import eph, ts

if TYPE_CHECKING:
    from skyfield.timelib import Time


def get_sunrise_sunset(lat: float, lon: float, given_time: datetime, elevation: float = 914) -> tuple[datetime, datetime]:
    """Calculate the sunrise and sunset times for a given location and date.

    Args:
        lat (float): The latitude of the location in decimal degrees.
        lon (float): The longitude of the location in decimal degrees.
        given_time (datetime): The date and time for which to calculate the sunrise and sunset times.
        elevation (float, optional): The elevation of the location in meters. Defaults to 914 meters (approximately 3000 feet).

    Returns:
        tuple[datetime, datetime]: A tuple containing the sunrise and sunset times as datetime objects.

    """
    # Define location
    location = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon, elevation_m=elevation)

    # Define time range for the search (e.g., one day)
    t_start = ts.utc(given_time.date())  # Start of the day
    t_end = ts.utc(given_time.date() + timedelta(days=1))  # End of the day

    # Find sunrise time
    f = sunrise_sunset(eph, location)
    times, events = find_discrete(t_start, t_end, f)

    sunrise, sunset = cast("list[Time]", [time for time, _ in zip(times, events, strict=False)])

    return cast("tuple[datetime, datetime]", (sunrise.utc_datetime(), sunset.utc_datetime()))
