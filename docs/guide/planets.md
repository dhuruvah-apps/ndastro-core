# Planet Positions

Calculate planetary positions for any date, time, and location using NDAstro engine.

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

Each planet has two code properties:

### Short Codes

The `code` property returns a short 2-letter code:

```python
from ndastro_engine.enums import Planets

print(Planets.SUN.code)        # "SU"
print(Planets.MOON.code)       # "MO"
print(Planets.MERCURY.code)    # "ME"
print(Planets.JUPITER.code)    # "JU"
print(Planets.RAHU.code)       # "RA"
print(Planets.KETHU.code)      # "KE"
```

### Astronomical Codes

The `astronomical_code` property returns the full Skyfield-compatible name:

```python
from ndastro_engine.enums import Planets

print(Planets.SUN.astronomical_code)        # "sun"
print(Planets.MOON.astronomical_code)       # "moon"
print(Planets.MERCURY.astronomical_code)    # "mercury"
print(Planets.JUPITER.astronomical_code)    # "jupiter barycenter"
print(Planets.RAHU.astronomical_code)       # "rahu"
print(Planets.KETHU.astronomical_code)      # "kethu"
```

!!! note
    Use `astronomical_code` when calling combustion and retrograde functions, as they require the full astronomical name.

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
from ndastro_engine.ayanamsa import get_ayanamsa
from ndastro_engine.enums.planet_enum import Planets

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get tropical position
tropical = get_planet_position(Planets.JUPITER, latitude, longitude, date)

# Get ayanamsa
ayanamsa = get_ayanamsa(date, "lahiri")

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
from ndastro_engine.ayanamsa import get_ayanamsa
from ndastro_engine.enums.planet_enum import Planets
from ndastro_engine.enums.rasi_enum import Rasi

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get sidereal position
tropical = get_planet_position(Planets.MOON, latitude, longitude, date)
ayanamsa = get_ayanamsa(date, "lahiri")
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
from ndastro_engine.ayanamsa import get_ayanamsa
from ndastro_engine.enums.planet_enum import Planets
from ndastro_engine.enums.nakshatra_enum import Nakshatra

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get sidereal position
tropical = get_planet_position(Planets.MOON, latitude, longitude, date)
ayanamsa = get_ayanamsa(date, "lahiri")
sidereal = (tropical - ayanamsa) % 360

# Each nakshatra is 13°20' (13.333...)
nakshatra_number = int(sidereal / 13.333333333)
position_in_nakshatra = sidereal % 13.333333333

# Get nakshatra enum
nakshatra = Nakshatra.from_index(nakshatra_number)

print(f"Moon is in {nakshatra.name} at {position_in_nakshatra:.4f}°")
```

## Pada (Quarter) Calculation

Determine which pada (quarter, 1-4) within a nakshatra a planet is in:

```python
from datetime import datetime
from ndastro_engine.core import get_planet_position
from ndastro_engine.ayanamsa import get_ayanamsa
from ndastro_engine.enums.planet_enum import Planets
from ndastro_engine.enums.nakshatra_enum import Nakshatras

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, 12, 0, 0)

# Get sidereal position
tropical = get_planet_position(Planets.MOON, latitude, longitude, date)
ayanamsa = get_ayanamsa(date, "lahiri")
sidereal = (tropical - ayanamsa) % 360

# Get current pada (1-4)
pada = Nakshatras.current_pada(sidereal)

print(f"Moon is in pada {pada}")
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

## Accuracy Comparison

The following comparison was run against two widely-used Vedic astrology reference tools for **2026-01-01 00:00 IST (geocentric, Lahiri ayanamsa)**.

### vs JHora (true node)

All sidereal longitudes are within **0.011°** (~0.7 arcminutes) of JHora. The residual is from the Lahiri ayanamsa approximation formula, not the planetary calculation.

| Planet   | NDAstro engine | JHora    | Diff     |
|----------|----------------|----------|----------|
| Sun      | 256.1155°      | 256.119° | −0.004°  |
| Moon     | 39.0656°       | 39.066°  | −0.000°  |
| Mars     | 258.2929°      | 258.302° | −0.009°  |
| Mercury  | 244.0826°      | 244.093° | −0.010°  |
| Jupiter  | 87.1679°       | 87.163°  | +0.005°  |
| Venus    | 254.6985°      | 254.709° | −0.011°  |
| Saturn   | 331.9343°      | 331.935° | −0.001°  |
| Rahu     | 316.7617°      | 316.770° | −0.008°  |
| Ketu     | 136.7617°      | 136.770° | −0.008°  |

### vs AstroSage (mean node)

AstroSage uses the **mean node** for Rahu/Ketu by default. With `node_type="mean"`, all planets — including Rahu and Ketu — match to within **0.008°** (~0.5 arcminutes).

| Planet   | NDAstro engine | AstroSage (DMS)  | AstroSage (dec) | Diff    |
|----------|----------------|------------------|-----------------|---------|
| Sun      | 256.1155°      | 16° Sag 06′ 32″  | 256.1089°       | +0.007° |
| Moon     | 39.0656°       | 09° Tau 04′ 14″  | 39.0706°        | −0.005° |
| Mars     | 258.2929°      | 18° Sag 17′ 10″  | 258.2861°       | +0.007° |
| Mercury  | 244.0826°      | 04° Sag 04′ 35″  | 244.0764°       | +0.006° |
| Jupiter  | 87.1679°       | 27° Gem 09′ 37″  | 87.1603°        | +0.008° |
| Venus    | 254.6985°      | 14° Sag 41′ 31″  | 254.6919°       | +0.007° |
| Saturn   | 331.9343°      | 01° Pis 55′ 37″  | 331.9269°       | +0.007° |
| Rahu     | 317.9617°      | 17° Aqu 57′ 15″  | 317.9542°       | +0.008° |
| Ketu     | 137.9617°      | 17° Leo 57′ 15″  | 137.9542°       | +0.008° |

!!! note "True vs mean node"
    True and mean nodes can differ by up to **~1.5°**. JHora defaults to true node; AstroSage defaults to mean node. Configure `node_type` accordingly — see [Configuration](configuration.md#lunar-node-type).

```python
from ndastro_engine.config import configure, EngineSettingsOverride

configure(EngineSettingsOverride(node_type="true"))   # matches JHora
configure(EngineSettingsOverride(node_type="mean"))   # matches AstroSage
```

## See Also

- [Configuration](configuration.md)
- [Retrograde Periods](retrograde.md)
- [Ayanamsa Calculations](ayanamsa.md)
- [API Reference: Core](../api/core.md)
