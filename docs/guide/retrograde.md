# Retrograde Periods

Detect and track planetary retrograde motion - when planets appear to move backward in the sky from Earth's perspective.

## What is Retrograde Motion?

Retrograde motion is an apparent backward movement of a planet as observed from Earth. This is an optical illusion caused by the difference in orbital speeds and positions of Earth and the other planet.

In Vedic astrology, retrograde planets are considered to have special significance.

## Checking if a Planet is Retrograde

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

# Location: New Delhi
latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)

# Check date
check_date = datetime(2023, 12, 20, 12, 0, 0)

# Check Mercury retrograde
is_retro, start_date, end_date = is_planet_in_retrograde(
    check_date,
    Planets.MERCURY.code,
    latitude,
    longitude
)

if is_retro:
    print(f"Mercury is retrograde!")
    print(f"Started: {start_date}")
    print(f"Ends: {end_date}")
else:
    print("Mercury is in direct motion")
```

## Return Values

The function returns a tuple of three values:

1. **bool**: `True` if the planet is retrograde, `False` otherwise
2. **datetime | None**: Start date of the retrograde period (or `None`)
3. **datetime | None**: End date of the retrograde period (or `None`)

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)
check_date = datetime(2024, 2, 15, 12, 0, 0)

is_retro, start, end = is_planet_in_retrograde(
    check_date,
    Planets.VENUS.code,
    latitude,
    longitude
)

print(f"Retrograde: {is_retro}")
print(f"Start: {start}")
print(f"End: {end}")
```

## Finding Retrograde Periods

Find all retrograde periods in a date range:

```python
from datetime import datetime
from ndastro_engine.utils import find_retrograde_periods
from ndastro_engine.enums.planet_enum import Planets

# Date range
start_date = datetime(2024, 1, 1, 12, 0, 0)
end_date = datetime(2024, 12, 31, 12, 0, 0)

# Location
latitude = 28.6139
longitude = 77.2090

# Find Mercury retrograde periods in 2024
periods = find_retrograde_periods(
    start_date,
    end_date,
    Planets.MERCURY.code,
    latitude,
    longitude
)

print(f"Mercury retrograde periods in 2024: {len(periods)}")
for i, (start, end) in enumerate(periods, 1):
    duration = (end - start).days
    print(f"\nPeriod {i}:")
    print(f"  Start: {start.strftime('%Y-%m-%d')}")
    print(f"  End: {end.strftime('%Y-%m-%d')}")
    print(f"  Duration: {duration} days")
```

## Checking Multiple Planets

Check retrograde status for multiple planets:

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)
check_date = datetime(2024, 6, 15, 12, 0, 0)

# Planets that can go retrograde
planets = [
    Planets.MERCURY,
    Planets.VENUS,
    Planets.MARS,
    Planets.JUPITER,
    Planets.SATURN,
]

print(f"Retrograde status on {check_date.strftime('%Y-%m-%d')}:\n")

for planet in planets:
    is_retro, start, end = is_planet_in_retrograde(
        check_date,
        planet.code,
        latitude,
        longitude
    )
    
    status = "RETROGRADE" if is_retro else "Direct"
    print(f"{planet.name:10s}: {status}")
    
    if is_retro:
        print(f"             Period: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
```

## Planets That Never Go Retrograde

Sun and Moon never go retrograde from Earth's perspective:

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)
check_date = datetime(2024, 6, 15, 12, 0, 0)

# Sun never goes retrograde
is_retro, _, _ = is_planet_in_retrograde(
    check_date,
    Planets.SUN.code,
    latitude,
    longitude
)
print(f"Sun retrograde: {is_retro}")  # Always False

# Moon never goes retrograde
is_retro, _, _ = is_planet_in_retrograde(
    check_date,
    Planets.MOON.code,
    latitude,
    longitude
)
print(f"Moon retrograde: {is_retro}")  # Always False
```

## Retrograde Frequency

Different planets have different retrograde frequencies:

| Planet | Retrograde Frequency | Average Duration |
|--------|---------------------|------------------|
| Mercury | ~3 times per year | ~20 days |
| Venus | ~18 months | ~40 days |
| Mars | ~26 months | ~60-80 days |
| Jupiter | ~13 months | ~120 days |
| Saturn | ~12.5 months | ~140 days |
| Uranus | ~12 months | ~150 days |
| Neptune | ~12 months | ~160 days |
| Pluto | ~12 months | ~160 days |

## Mercury Retrograde Example

Mercury retrograde is the most frequent and well-known:

```python
from datetime import datetime
from ndastro_engine.utils import find_retrograde_periods
from ndastro_engine.enums.planet_enum import Planets

# Find Mercury retrograde for 2024
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 12, 31, 23, 59, 59)

periods = find_retrograde_periods(
    start,
    end,
    Planets.MERCURY.code,
    28.6139,
    77.2090
)

print(f"Mercury Retrograde Periods in 2024:\n")
for i, (start_date, end_date) in enumerate(periods, 1):
    duration = (end_date - start_date).days
    print(f"Period {i}:")
    print(f"  {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}")
    print(f"  Duration: {duration} days\n")
```

## Checking Retrograde at Birth Time

For natal chart analysis:

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

# Birth details
birth_datetime = datetime(1990, 5, 15, 14, 30, 0)
birth_latitude = Angle(degrees=28.6139)
birth_longitude = Angle(degrees=77.2090)

planets_to_check = [
    Planets.MERCURY,
    Planets.VENUS,
    Planets.MARS,
    Planets.JUPITER,
    Planets.SATURN,
]

print("Retrograde planets at birth:\n")
retrograde_planets = []

for planet in planets_to_check:
    is_retro, _, _ = is_planet_in_retrograde(
        birth_datetime,
        planet.code,
        birth_latitude,
        birth_longitude
    )
    
    if is_retro:
        retrograde_planets.append(planet.name)
        print(f"✓ {planet.name}")

if not retrograde_planets:
    print("No retrograde planets at birth time")
```

## Annual Retrograde Calendar

Create a retrograde calendar for the year:

```python
from datetime import datetime, timedelta
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)
year = 2024

planets = [Planets.MERCURY, Planets.VENUS, Planets.MARS]

# Check first day of each month
for month in range(1, 13):
    check_date = datetime(year, month, 1, 12, 0, 0)
    print(f"\n{check_date.strftime('%B %Y')}:")
    
    for planet in planets:
        is_retro, start, end = is_planet_in_retrograde(
            check_date,
            planet.code,
            latitude,
            longitude
        )
        
        if is_retro:
            print(f"  {planet.name}: RETROGRADE")
```

## Retrograde Direction Changes

Detect when planets station (change direction):

```python
from datetime import datetime, timedelta
from ndastro_engine.utils import find_retrograde_periods
from ndastro_engine.enums.planet_enum import Planets

# Find retrograde periods
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 12, 31, 23, 59, 59)

periods = find_retrograde_periods(
    start,
    end,
    Planets.JUPITER.code,
    28.6139,
    77.2090
)

print("Jupiter Stations in 2024:\n")
for i, (retro_start, retro_end) in enumerate(periods, 1):
    print(f"Period {i}:")
    print(f"  Station Retrograde: {retro_start.strftime('%B %d, %Y')}")
    print(f"  Station Direct: {retro_end.strftime('%B %d, %Y')}")
    print()
```

## Performance Considerations

Retrograde calculations search a 2-year window (1 year before and after):

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

# This checks from 2023-01-01 to 2025-01-01
check_date = datetime(2024, 1, 1, 12, 0, 0)
latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)

# Cached for efficiency
is_retro, start, end = is_planet_in_retrograde(
    check_date,
    Planets.SATURN.code,
    latitude,
    longitude
)
```

## See Also

- [Planet Positions](planets.md)
- [API Reference: Utils](../api/utils.md)
- [Quick Start Guide](../getting-started/quick-start.md)
