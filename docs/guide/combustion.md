# Planetary Combustion

Planetary combustion is a Vedic astrology concept where a planet loses its strength when it comes too close to the Sun. The `ndastro_engine.combustion` module provides functions to determine if a planet is in combustion and to find combustion periods.

## What is Combustion?

In Vedic astrology, when a planet is too close to the Sun (within a certain degree range called the "orb"), it is said to be "combust" or "burnt." A combust planet is considered weakened and may not fully express its qualities.

### Combustion Orbs

Different planets have different combustion orbs:

| Planet | Combustion Orb |
|--------|----------------|
| Mercury | 12° |
| Venus | 8° |
| Mars | 17° |
| Jupiter | 11° |
| Saturn | 15° |

!!! note
    The Sun, Moon, Rahu, and Kethu cannot be in combustion.

## Checking if a Planet is Combust

Use the `is_planet_in_combust()` function to check if a planet is combust on a specific date:

```python
from datetime import datetime
import pytz
from ndastro_engine.combustion import is_planet_in_combust
from ndastro_engine.enums import Planets

# Check if Mercury is combust on a specific date
check_date = datetime(2026, 2, 13, 12, 0, 0, tzinfo=pytz.UTC)
latitude = 40.7128  # New York
longitude = -74.0060

is_combust, period_start, period_end = is_planet_in_combust(
    check_date=check_date,
    planet_name=Planets.MERCURY.astronomical_code,
    latitude=latitude,
    longitude=longitude
)

if is_combust:
    print(f"Mercury is combust on {check_date.date()}")
    print(f"Combustion period: {period_start.date()} to {period_end.date()}")
else:
    print(f"Mercury is not combust on {check_date.date()}")
```

The function returns a tuple containing:
- `is_combust` (bool): Whether the planet is combust on the specified date
- `period_start` (datetime | None): The start date of the combustion period, or None if not combust
- `period_end` (datetime | None): The end date of the combustion period, or None if not combust

## Finding Combustion Periods

To find all combustion periods for a planet within a date range, use the `find_combust_periods()` function:

```python
from datetime import datetime
import pytz
from ndastro_engine.combustion import find_combust_periods
from ndastro_engine.enums import Planets

# Find all combustion periods for Venus in 2026
start_date = datetime(2026, 1, 1, tzinfo=pytz.UTC)
end_date = datetime(2026, 12, 31, tzinfo=pytz.UTC)
latitude = 19.0760  # Mumbai
longitude = 72.8777

combust_periods = find_combust_periods(
    start_date=start_date,
    end_date=end_date,
    planet_name=Planets.VENUS.astronomical_code,
    latitude=latitude,
    longitude=longitude
)

# Display the results
for period_start, period_end in combust_periods:
    duration = (period_end - period_start).days
    print(f"Venus combust from {period_start.date()} to {period_end.date()} ({duration} days)")
```

## Checking Multiple Planets

You can check combustion status for multiple planets:

```python
from datetime import datetime
import pytz
from ndastro_engine.combustion import is_planet_in_combust
from ndastro_engine.enums import Planets

check_date = datetime(2026, 3, 15, 12, 0, 0, tzinfo=pytz.UTC)
latitude = 51.5074  # London
longitude = -0.1278

# Check all planets that can be combust
planets = [
    Planets.MERCURY,
    Planets.VENUS,
    Planets.MARS,
    Planets.JUPITER,
    Planets.SATURN
]

print(f"Combustion status on {check_date.date()}:\n")
for planet in planets:
    is_combust, period_start, period_end = is_planet_in_combust(
        check_date=check_date,
        planet_name=planet.astronomical_code,
        latitude=latitude,
        longitude=longitude
    )
    if is_combust:
        print(f"{planet.name}: Combust (until {period_end.date()})")
    else:
        print(f"{planet.name}: Not combust")
```

## Understanding the Results

### Combustion Periods

The `find_combust_periods()` function returns a list of tuples, where each tuple contains:
- `period_start`: The datetime when combustion begins
- `period_end`: The datetime when combustion ends

Periods are returned in chronological order and do not overlap.

### Location Impact

While planetary combustion is primarily based on the angular separation from the Sun (which doesn't vary significantly with observer location), there can be minor differences due to:
- Parallax effects
- Atmospheric refraction calculations

For most practical purposes, the location has minimal impact on combustion calculations.

## Practical Examples

### Example 1: Find When Mercury is Not Combust

```python
from datetime import datetime, timedelta
import pytz
from ndastro_engine.combustion import find_combust_periods
from ndastro_engine.enums import Planets

# Get combustion periods for Mercury
start = datetime(2026, 6, 1, tzinfo=pytz.UTC)
end = datetime(2026, 9, 30, tzinfo=pytz.UTC)
lat, lon = 35.6762, 139.6503  # Tokyo

combust_periods = find_combust_periods(start, end, Planets.MERCURY.astronomical_code, lat, lon)

# Find non-combust periods
current = start
non_combust_periods = []

for period_start, period_end in combust_periods:
    if current < period_start:
        non_combust_periods.append((current, period_start))
    current = period_end

if current < end:
    non_combust_periods.append((current, end))

print("Mercury is NOT combust during:")
for nc_start, nc_end in non_combust_periods:
    days = (nc_end - nc_start).days
    print(f"  {nc_start.date()} to {nc_end.date()} ({days} days)")
```

### Example 2: Count Combust Days in a Year

```python
from datetime import datetime
import pytz
from ndastro_engine.combustion import find_combust_periods
from ndastro_engine.enums import Planets

start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
end = datetime(2026, 12, 31, tzinfo=pytz.UTC)
lat, lon = 40.7128, -74.0060  # New York

planets = [
    ("Mercury", Planets.MERCURY.astronomical_code),
    ("Venus", Planets.VENUS.astronomical_code),
    ("Mars", Planets.MARS.astronomical_code),
    ("Jupiter", Planets.JUPITER.astronomical_code),
    ("Saturn", Planets.SATURN.astronomical_code)
]

print("Total combust days in 2026:\n")
for planet_name, planet_code in planets:
    periods = find_combust_periods(start, end, planet_code, lat, lon)
    total_days = sum((p_end - p_start).days for p_start, p_end in periods)
    print(f"{planet_name:8} : {total_days:3} days ({len(periods)} period(s))")
```

### Example 3: Get Combustion Period Details

```python
from datetime import datetime
import pytz
from ndastro_engine.combustion import is_planet_in_combust
from ndastro_engine.enums import Planets

check_date = datetime(2026, 3, 15, 12, 0, 0, tzinfo=pytz.UTC)
lat, lon = 40.7128, -74.0060  # New York

is_combust, period_start, period_end = is_planet_in_combust(
    check_date, Planets.SATURN.astronomical_code, lat, lon
)

if is_combust:
    duration = (period_end - check_date).days
    print(f"Saturn is combust on {check_date.date()}")
    print(f"Combustion started: {period_start.date()}")
    print(f"Combustion ends: {period_end.date()}")
    print(f"Days remaining in combustion: {duration}")
else:
    print(f"Saturn is not combust on {check_date.date()}")
```

