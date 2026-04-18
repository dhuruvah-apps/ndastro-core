# API Reference: Retrograde Module

## Overview

This module provides functions to detect and track planetary retrograde motion from any location on Earth.

## Functions

::: ndastro_engine.retrograde
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## RetrogradeFunction Class

::: ndastro_engine.retrograde.RetrogradeFunction
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Examples

### Check if a Planet is Retrograde

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums import Planets

# Location: Chennai, India
latitude = Angle(degrees=13.0827)
longitude = Angle(degrees=80.2707)

# Check Mercury retrograde on a specific date
check_date = datetime(2023, 12, 20, 12, 0, 0)
is_retro, start_date, end_date = is_planet_in_retrograde(
    check_date,
    Planets.MERCURY.astronomical_code,
    latitude,
    longitude
)

if is_retro:
    print(f"Mercury is retrograde from {start_date} to {end_date}")
else:
    print("Mercury is in direct motion")
```

### Get Retrograde Period for Multiple Planets

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums import Planets

latitude = Angle(degrees=28.6139)  # New Delhi
longitude = Angle(degrees=77.2090)
check_date = datetime(2026, 4, 18, 12, 0, 0)

planets_to_check = [
    Planets.MERCURY,
    Planets.VENUS,
    Planets.MARS,
    Planets.JUPITER,
    Planets.SATURN
]

for planet in planets_to_check:
    is_retro, start, end = is_planet_in_retrograde(
        check_date,
        planet.astronomical_code,
        latitude,
        longitude
    )
    status = "Retrograde" if is_retro else "Direct"
    print(f"{planet.name}: {status}")
    if is_retro and start and end:
        print(f"  Period: {start.date()} to {end.date()}")
```

## See Also

- [Retrograde Periods Guide](../guide/retrograde.md) - Detailed guide on retrograde motion
- [Core Module](core.md) - Core astronomical calculations
- [Planets Enum](enums.md) - Planet definitions and codes
