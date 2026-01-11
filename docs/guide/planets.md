# Planet Positions

Calculate planetary positions for any date, time, and location using ndastro-engine.

## Basic Usage

Get the longitude of any planet:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

# Location: New Delhi
latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get Sun's position
sun_position = get_planet_position(Planets.SUN, latitude, longitude, date)
print(f"Sun's longitude: {sun_position:.6f}°")
```

## Available Planets

```python
from ndastro_engine.enums.planet_enum import Planets

# All available planets
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
    Planets.RAHU,      # North Node
    Planets.KETHU,     # South Node
]

# Get positions for all planets
for planet in planets:
    position = get_planet_position(planet, latitude, longitude, date)
    print(f"{planet.name:10s}: {position:8.4f}°")
```

## Planet Codes

Each planet has a code used internally:

```python
from ndastro_engine.enums.planet_enum import Planets

print(Planets.SUN.code)        # "sun"
print(Planets.MOON.code)       # "moon"
print(Planets.JUPITER.code)    # "jupiter barycenter"
print(Planets.RAHU.code)       # "rahu"
print(Planets.KETHU.code)      # "kethu"
```

## Calculating Multiple Positions

Get positions for multiple planets at once:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

latitude = 28.6139  # New Delhi
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Calculate positions for inner planets
inner_planets = [Planets.SUN, Planets.MOON, Planets.MERCURY, Planets.VENUS, Planets.MARS]
positions = {}

for planet in inner_planets:
    positions[planet.name] = get_planet_position(planet, latitude, longitude, date)

# Display results
for planet, position in positions.items():
    print(f"{planet:10s}: {position:8.4f}°")
```

## Sidereal vs Tropical

By default, positions are calculated in the tropical zodiac. For sidereal positions (used in Vedic astrology), subtract the ayanamsa:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa
from ndastro_engine.enums.planet_enum import Planets

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get tropical position
tropical = get_planet_position(Planets.JUPITER, latitude, longitude, date)

# Get ayanamsa
ayanamsa = get_lahiri_ayanamsa(date)

# Calculate sidereal position
sidereal = tropical - ayanamsa

print(f"Tropical: {tropical:.4f}°")
print(f"Ayanamsa: {ayanamsa:.4f}°")
print(f"Sidereal: {sidereal:.4f}°")
```

## Rashi (Sign) Calculation

Determine which rashi (zodiac sign) a planet is in:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa
from ndastro_engine.enums.planet_enum import Planets
from ndastro_engine.enums.rasi_enum import Rasi

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get sidereal position
tropical = get_planet_position(Planets.MOON, latitude, longitude, date)
ayanamsa = get_lahiri_ayanamsa(date)
sidereal = (tropical - ayanamsa) % 360

# Get rashi (each rashi is 30°)
rashi_number = int(sidereal / 30)
position_in_rashi = sidereal % 30

# Get rashi enum
rashi = Rasi.from_index(rashi_number)

print(f"Moon is in {rashi.name} at {position_in_rashi:.4f}°")
```

## Nakshatra Calculation

Determine which nakshatra a planet occupies:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa
from ndastro_engine.enums.planet_enum import Planets
from ndastro_engine.enums.nakshatra_enum import Nakshatra

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get sidereal position
tropical = get_planet_position(Planets.MOON, latitude, longitude, date)
ayanamsa = get_lahiri_ayanamsa(date)
sidereal = (tropical - ayanamsa) % 360

# Each nakshatra is 13°20' (13.333...)
nakshatra_number = int(sidereal / 13.333333333)
position_in_nakshatra = sidereal % 13.333333333

# Get nakshatra enum
nakshatra = Nakshatra.from_index(nakshatra_number)

print(f"Moon is in {nakshatra.name} at {position_in_nakshatra:.4f}°")
```

## Time-based Calculations

Calculate positions at different times:

```python
from datetime import datetime, timedelta
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

latitude = 28.6139
longitude = 77.2090
base_date = datetime(2026, 1, 11, 0, 0, 0)

# Calculate Moon's position every 6 hours
for hours in range(0, 25, 6):
    date = base_date + timedelta(hours=hours)
    position = get_planet_position(Planets.MOON, latitude, longitude, date)
    print(f"{date.strftime('%Y-%m-%d %H:%M')}: {position:.4f}°")
```

## Location-based Calculations

Positions vary slightly based on observer's location:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

date = datetime(2026, 1, 11, 12, 0, 0)

# Different locations
locations = {
    "New Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
}

for city, (lat, lon) in locations.items():
    position = get_planet_position(Planets.MOON, lat, lon, date)
    print(f"{city:15s}: {position:.4f}°")
```

## Understanding Rahu and Kethu

Rahu (North Node) and Kethu (South Node) are lunar nodes - the points where the Moon's orbit intersects the ecliptic:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

rahu = get_planet_position(Planets.RAHU, latitude, longitude, date)
kethu = get_planet_position(Planets.KETHU, latitude, longitude, date)

# Kethu is always 180° opposite to Rahu
print(f"Rahu: {rahu:.4f}°")
print(f"Kethu: {kethu:.4f}°")
print(f"Difference: {abs(rahu - kethu):.4f}° (should be ~180°)")
```

## Performance Tips

When calculating positions for multiple planets or times:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

# Efficient: Reuse date and location
latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Calculate once, use multiple times
planets = [Planets.SUN, Planets.MOON, Planets.JUPITER]
positions = {p.name: get_planet_position(p, latitude, longitude, date) for p in planets}
```

## See Also

- [Retrograde Periods](retrograde.md)
- [Ayanamsa Calculations](ayanamsa.md)
- [API Reference: Core](../api/core.md)
