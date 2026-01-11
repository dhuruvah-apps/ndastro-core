# Quick Start Guide

This guide will help you get started with ndastro-engine quickly.

## Basic Usage

### 1. Calculate Ayanamsa

Calculate the ayanamsa (precession correction) for a given date:

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa

# Calculate Lahiri ayanamsa for a date
date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_lahiri_ayanamsa(date)
print(f"Lahiri Ayanamsa: {ayanamsa:.6f}°")
# Output: Lahiri Ayanamsa: 24.260000°
```

### 2. Get Planet Positions

Get the longitude of a planet for a specific date and location:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

# New Delhi coordinates
latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get Sun's position
sun_position = get_planet_position(Planets.SUN, latitude, longitude, date)
print(f"Sun's longitude: {sun_position:.6f}°")

# Get Moon's position
moon_position = get_planet_position(Planets.MOON, latitude, longitude, date)
print(f"Moon's longitude: {moon_position:.6f}°")
```

### 3. Calculate Sunrise and Sunset

Find sunrise and sunset times for any location:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

# New Delhi coordinates
latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)
print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")
```

### 4. Check Retrograde Motion

Determine if a planet is in retrograde motion:

```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.utils import is_planet_in_retrograde
from ndastro_engine.enums.planet_enum import Planets

check_date = datetime(2023, 12, 20, 12, 0, 0)
latitude = Angle(degrees=28.6139)
longitude = Angle(degrees=77.2090)

is_retro, start_date, end_date = is_planet_in_retrograde(
    check_date, 
    Planets.MERCURY.code, 
    latitude, 
    longitude
)

if is_retro:
    print(f"Mercury is retrograde from {start_date} to {end_date}")
else:
    print("Mercury is in direct motion")
```

## Available Ayanamsa Systems

ndastro-engine supports 16 different ayanamsa calculation methods:

```python
from datetime import datetime
from ndastro_engine import ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Popular systems
lahiri = ayanamsa.get_lahiri_ayanamsa(date)
kp_new = ayanamsa.get_krishnamurti_new_ayanamsa(date)
kp_old = ayanamsa.get_krishnamurti_old_ayanamsa(date)
raman = ayanamsa.get_raman_ayanamsa(date)
fagan_bradley = ayanamsa.get_fagan_bradley_ayanamsa(date)

# Traditional systems
kali = ayanamsa.get_kali_ayanamsa(date)
yukteshwar = ayanamsa.get_yukteshwar_ayanamsa(date)
aryabhatta = ayanamsa.get_aryabhatta_ayanamsa(date)

print(f"Lahiri: {lahiri:.6f}°")
print(f"KP New: {kp_new:.6f}°")
print(f"Raman: {raman:.6f}°")
```

## Planet Enums

All planets are available through the `Planets` enum:

```python
from ndastro_engine.enums.planet_enum import Planets

# Available planets
planets = [
    Planets.SUN,
    Planets.MOON,
    Planets.MERCURY,
    Planets.VENUS,
    Planets.MARS,
    Planets.JUPITER,
    Planets.SATURN,
    Planets.URANUS,
    Planets.NEPTUNE,
    Planets.PLUTO,
    Planets.RAHU,
    Planets.KETHU,
]

# Get planet code
print(Planets.JUPITER.code)  # Output: "jupiter"
print(Planets.RAHU.code)     # Output: "rahu"
```

## Utility Functions

### Degree Normalization

```python
from ndastro_engine.utils import normalize_degree

# Normalize degrees to 0-360 range
angle = normalize_degree(450.0)
print(angle)  # Output: 90.0

angle = normalize_degree(-30.0)
print(angle)  # Output: 330.0
```

### DMS Conversion

```python
from ndastro_engine.utils import dd2dms, dms2dd, dd2dmsstr

# Decimal degrees to DMS
degrees, minutes, seconds, sign = dd2dms(45.5)
print(f"{degrees}° {minutes}' {seconds:.2f}\"")  # Output: 45° 30' 0.00"

# DMS to decimal degrees
decimal = dms2dd(45, 30, 0)
print(decimal)  # Output: 45.5

# Formatted string
dms_str = dd2dmsstr(45.5)
print(dms_str)  # Output: 45° 30' 0.00"
```

## Next Steps

- Learn more about [Ayanamsa calculations](../guide/ayanamsa.md)
- Explore [Planet positions](../guide/planets.md)
- Check the [API Reference](../api/core.md)
- Read about [Retrograde periods](../guide/retrograde.md)
