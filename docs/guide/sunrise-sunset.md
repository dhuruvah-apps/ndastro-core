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

sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)

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

sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)

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
    sunrise, sunset = get_sunrise_sunset(date, lat, lon)
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
    sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)
    
    daylight = sunset - sunrise
    hours = daylight.total_seconds() / 3600
    
    print(f"{date.strftime('%Y-%m-%d')}:")
    print(f"  Sunrise: {sunrise.strftime('%H:%M')}")
    print(f"  Sunset: {sunset.strftime('%H:%M')}")
    print(f"  Daylight: {hours:.2f} hours\n")
```

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
    sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)
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

sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)

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
    sunrise, _ = get_sunrise_sunset(date, latitude, longitude)
    
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
sunrise, sunset = get_sunrise_sunset(date_utc, latitude, longitude)

# Method 2: Convert from local timezone
local_tz = pytz.timezone('Asia/Kolkata')
date_local = local_tz.localize(datetime(2026, 1, 11, 12, 0, 0))
date_utc = date_local.astimezone(timezone.utc)
sunrise, sunset = get_sunrise_sunset(date_utc, latitude, longitude)

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
    sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)
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
    sunrise, sunset = get_sunrise_sunset(date, latitude, longitude)
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
        sunrise, sunset = get_sunrise_sunset(date, lat, lon)
        print(f"{name}: Sunrise {sunrise.strftime('%H:%M')}, Sunset {sunset.strftime('%H:%M')}")
    except Exception as e:
        print(f"{name}: {e}")
```

## See Also

- [Planet Positions](planets.md)
- [API Reference: Core](../api/core.md)
- [Quick Start Guide](../getting-started/quick-start.md)
