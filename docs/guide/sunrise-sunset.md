# Sunrise and Sunset

Calculate sunrise and sunset times for any location and date.

## Basic Usage

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

# Location: New Delhi
latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)

print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")
```

## Output Format

The function returns two `datetime` objects in UTC timezone:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)

# Format the output
print(f"Sunrise: {sunrise.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Sunset: {sunset.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Get times in local timezone
import pytz
local_tz = pytz.timezone('Asia/Kolkata')
sunrise_local = sunrise.astimezone(local_tz)
sunset_local = sunset.astimezone(local_tz)

print(f"Sunrise (IST): {sunrise_local.strftime('%H:%M:%S')}")
print(f"Sunset (IST): {sunset_local.strftime('%H:%M:%S')}")
```

## Multiple Locations

Calculate for different cities:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

date = datetime(2026, 1, 11, tzinfo=timezone.utc)

locations = {
    "New Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
}

for city, (lat, lon) in locations.items():
    sunrise, sunset = get_sunrise_sunset(lat, lon, date)
    print(f"\n{city}:")
    print(f"  Sunrise: {sunrise.strftime('%H:%M:%S UTC')}")
    print(f"  Sunset: {sunset.strftime('%H:%M:%S UTC')}")
```

## Multiple Dates

Calculate for a range of dates:

```python
from datetime import datetime, timezone, timedelta
from ndastro_engine.core import get_sunrise_sunset

# New Delhi
latitude = 28.6139
longitude = 77.2090

# Calculate for a week
start_date = datetime(2026, 1, 11, tzinfo=timezone.utc)

for day in range(7):
    date = start_date + timedelta(days=day)
    sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)
    
    daylight = sunset - sunrise
    hours = daylight.total_seconds() / 3600
    
    print(f"{date.strftime('%Y-%m-%d')}:")
    print(f"  Sunrise: {sunrise.strftime('%H:%M')}")
    print(f"  Sunset: {sunset.strftime('%H:%M')}")
    print(f"  Daylight: {hours:.2f} hours\n")
```

---

## Planet Rise and Set

Calculate rise and set times for any physical planet — including the Moon — using `get_planet_rise_set`.

### Basic Usage

```python
from datetime import datetime, timezone
import pytz
from ndastro_engine.core import get_planet_rise_set
from ndastro_engine.enums import Planets

latitude = 12.971667   # Bangalore
longitude = 77.593611
date = datetime(2026, 5, 24, tzinfo=timezone.utc)

moonrise, moonset = get_planet_rise_set(Planets.MOON, latitude, longitude, date)

ist = pytz.timezone('Asia/Kolkata')
print(f"Moonrise: {moonrise.astimezone(ist).strftime('%H:%M')} IST")
print(f"Moonset:  {moonset.astimezone(ist).strftime('%H:%M')} IST")
```

### All Physical Planets

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_planet_rise_set
from ndastro_engine.enums import Planets

latitude = 28.6139   # New Delhi
longitude = 77.2090
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

physical_planets = [
    Planets.SUN,
    Planets.MOON,
    Planets.MERCURY,
    Planets.VENUS,
    Planets.MARS,
    Planets.JUPITER,
    Planets.SATURN,
]

for planet in physical_planets:
    rise, set_ = get_planet_rise_set(planet, latitude, longitude, date)
    if rise and set_:
        print(f"{planet.name:10s}: rises {rise.strftime('%H:%M')} UTC, sets {set_.strftime('%H:%M')} UTC")
    else:
        print(f"{planet.name:10s}: no rise/set on this date")
```

### Unsupported Planets

`Rahu`, `Kethu`, `Ascendant`, and `Empty` are not physical bodies and always return `(None, None)`:

```python
from ndastro_engine.core import get_planet_rise_set
from ndastro_engine.enums import Planets

from datetime import datetime, timezone
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

rise, set_ = get_planet_rise_set(Planets.RAHU, 28.6139, 77.2090, date)
print(rise, set_)  # None None
```

### Optional Elevation

Like `get_sunrise_sunset`, you can pass an explicit elevation in metres:

```python
from ndastro_engine.core import get_planet_rise_set
from ndastro_engine.enums import Planets
from datetime import datetime, timezone

rise, set_ = get_planet_rise_set(
    Planets.MOON,
    28.6139, 77.2090,
    datetime(2026, 1, 11, tzinfo=timezone.utc),
    elevation=216.0,
)
```

!!! note
    Either value in the returned tuple may be `None` when a planet does not rise or set on the requested date (e.g., circumpolar bodies at high latitudes).

## Seasonal Variations

See how sunrise/sunset times change throughout the year:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset
import pytz

latitude = 28.6139
longitude = 77.2090
year = 2026

# Sample dates throughout the year
dates = [
    datetime(year, 1, 1, tzinfo=timezone.utc),   # Winter
    datetime(year, 4, 1, tzinfo=timezone.utc),   # Spring
    datetime(year, 7, 1, tzinfo=timezone.utc),   # Summer
    datetime(year, 10, 1, tzinfo=timezone.utc),  # Autumn
]

local_tz = pytz.timezone('Asia/Kolkata')

for date in dates:
    sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)
    sunrise_local = sunrise.astimezone(local_tz)
    sunset_local = sunset.astimezone(local_tz)
    
    daylight = sunset - sunrise
    hours = daylight.total_seconds() / 3600
    
    print(f"{date.strftime('%B %Y')}:")
    print(f"  Sunrise: {sunrise_local.strftime('%H:%M IST')}")
    print(f"  Sunset: {sunset_local.strftime('%H:%M IST')}")
    print(f"  Daylight: {hours:.2f} hours\n")
```

## Calculating Day Length

Get the duration of daylight:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)

# Calculate duration
duration = sunset - sunrise
hours = duration.total_seconds() / 3600
minutes = (duration.total_seconds() % 3600) / 60

print(f"Day length: {int(hours)} hours {int(minutes)} minutes")
```

## Finding the Earliest/Latest Sunrise

Find extremes throughout the year:

```python
from datetime import datetime, timezone, timedelta
from ndastro_engine.core import get_sunrise_sunset

latitude = 28.6139
longitude = 77.2090
year = 2026

earliest_sunrise = None
latest_sunrise = None
earliest_time = None
latest_time = None

# Check every day of the year
for day in range(365):
    date = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=day)
    sunrise, _ = get_sunrise_sunset(latitude, longitude, date)
    
    if earliest_time is None or sunrise < earliest_time:
        earliest_time = sunrise
        earliest_sunrise = date
    
    if latest_time is None or sunrise > latest_time:
        latest_time = sunrise
        latest_sunrise = date

print(f"Earliest sunrise: {earliest_sunrise.strftime('%Y-%m-%d')} at {earliest_time.strftime('%H:%M UTC')}")
print(f"Latest sunrise: {latest_sunrise.strftime('%Y-%m-%d')} at {latest_time.strftime('%H:%M UTC')}")
```

## Time Zone Handling

Always use timezone-aware datetime objects:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset
import pytz

latitude = 28.6139
longitude = 77.2090

# Method 1: UTC timezone
date_utc = datetime(2026, 1, 11, tzinfo=timezone.utc)
sunrise, sunset = get_sunrise_sunset(latitude, longitude, date_utc)

# Method 2: Convert from local timezone
local_tz = pytz.timezone('Asia/Kolkata')
date_local = local_tz.localize(datetime(2026, 1, 11, 12, 0, 0))
date_utc = date_local.astimezone(timezone.utc)
sunrise, sunset = get_sunrise_sunset(latitude, longitude, date_utc)

# Convert results to desired timezone
sunrise_ist = sunrise.astimezone(local_tz)
sunset_ist = sunset.astimezone(local_tz)

print(f"Sunrise (IST): {sunrise_ist}")
print(f"Sunset (IST): {sunset_ist}")
```

## Special Cases

### Polar Regions

In polar regions, there can be days with no sunrise or no sunset:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

# Northern location
latitude = 70.0  # Northern Norway
longitude = 25.0
date = datetime(2026, 6, 21, tzinfo=timezone.utc)  # Summer solstice

try:
    sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
except Exception as e:
    print(f"Special case: {e}")
```

### Equator

Near the equator, day length is nearly constant:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

# Singapore (near equator)
latitude = 1.3521
longitude = 103.8198

dates = [
    datetime(2026, 1, 1, tzinfo=timezone.utc),
    datetime(2026, 7, 1, tzinfo=timezone.utc),
]

for date in dates:
    sunrise, sunset = get_sunrise_sunset(latitude, longitude, date)
    duration = (sunset - sunrise).total_seconds() / 3600
    print(f"{date.strftime('%Y-%m-%d')}: {duration:.2f} hours")
```

## Coordinate Systems

The function uses WGS84 coordinates (same as GPS):

```python
# Valid coordinate ranges
# Latitude: -90° (South Pole) to +90° (North Pole)
# Longitude: -180° (West) to +180° (East)

from ndastro_engine.core import get_sunrise_sunset
from datetime import datetime, timezone

# Examples with different hemispheres
locations = {
    "North Pole": (90.0, 0.0),
    "South Pole": (-90.0, 0.0),
    "Prime Meridian": (51.5074, 0.0),      # London
    "International Date Line": (0.0, 180.0),
}

date = datetime(2026, 1, 11, tzinfo=timezone.utc)

for name, (lat, lon) in locations.items():
    try:
        sunrise, sunset = get_sunrise_sunset(lat, lon, date)
        print(f"{name}: Sunrise {sunrise.strftime('%H:%M')}, Sunset {sunset.strftime('%H:%M')}")
    except Exception as e:
        print(f"{name}: {e}")
```

## Elevation Handling

By default, elevation is resolved automatically from latitude and longitude using an elevation API.
If elevation lookup fails (for example, network issues), the calculation safely falls back to `0` meters.

You can also provide elevation explicitly when you want full control:

```python
from datetime import datetime, timezone
from ndastro_engine.core import get_sunrise_sunset

latitude = 28.6139
longitude = 77.2090
date = datetime(2026, 1, 11, tzinfo=timezone.utc)

# Explicit elevation in meters
sunrise, sunset = get_sunrise_sunset(latitude, longitude, date, elevation=216.0)

print(sunrise, sunset)
```

## See Also

- [Planet Positions](planets.md)
- [API Reference: Core](../api/core.md)
- [Quick Start Guide](../getting-started/quick-start.md)
