# ndastro-engine

[![PyPI version](https://badge.fury.io/py/ndastro-engine.svg)](https://badge.fury.io/py/ndastro-engine)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Python library for astronomical calculations, built on top of [Skyfield](https://rhodesmill.org/skyfield/). ndastro-engine provides a clean, intuitive API for computing sunrise, sunset, and other astronomical events for any location on Earth.

## Features

- 🌅 **Sunrise & Sunset Calculations** - Accurate sunrise and sunset times for any location
- 🌍 **WGS84 Coordinates** - Support for standard latitude/longitude coordinates
- 📅 **Date-based Queries** - Calculate astronomical events for any date
- 🎯 **High Precision** - Powered by Skyfield using JPL ephemeris data (DE440t)
- 🔧 **Easy Configuration** - Automatic ephemeris data management
- 📦 **Modern Python** - Type hints, clean API, and follows best practices

## Installation

Install using pip:

```bash
pip install ndastro-engine
```

For development:

```bash
pip install ndastro-engine[dev]
```

## Quick Start

```python
from datetime import datetime
from ndastro_engine.astro_engine import get_sunrise_sunset

# Define location (New York City)
latitude = 40.7128
longitude = -74.0060

# Get sunrise and sunset for today
today = datetime.now()
sunrise, sunset = get_sunrise_sunset(latitude, longitude, today)

print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")
```

## Usage Examples

### Basic Sunrise/Sunset Calculation

```python
from datetime import datetime
from ndastro_engine.astro_engine import get_sunrise_sunset

# Location: London, UK
lat = 51.5074
lon = -0.1278

# Calculate for a specific date
date = datetime(2026, 1, 15)
sunrise, sunset = get_sunrise_sunset(lat, lon, date)

print(f"On {date.date()}, sunrise is at {sunrise.strftime('%H:%M:%S')} UTC")
print(f"On {date.date()}, sunset is at {sunset.strftime('%H:%M:%S')} UTC")
```

### Working with Different Time Zones

```python
from datetime import datetime
import pytz
from ndastro_engine.astro_engine import get_sunrise_sunset

# Location: Tokyo, Japan
lat = 35.6762
lon = 139.6503

# Get times in local timezone
date = datetime(2026, 6, 21)
sunrise_utc, sunset_utc = get_sunrise_sunset(lat, lon, date)

# Convert to Tokyo time
tokyo_tz = pytz.timezone('Asia/Tokyo')
sunrise_local = sunrise_utc.replace(tzinfo=pytz.UTC).astimezone(tokyo_tz)
sunset_local = sunset_utc.replace(tzinfo=pytz.UTC).astimezone(tokyo_tz)

print(f"Sunrise (Tokyo): {sunrise_local.strftime('%H:%M:%S %Z')}")
print(f"Sunset (Tokyo): {sunset_local.strftime('%H:%M:%S %Z')}")
```

## Configuration

The library automatically downloads and caches the required JPL ephemeris data (DE441) on first use. The data is stored in your system's application data directory:

- **Windows**: `%APPDATA%\ndastro`
- **macOS**: `~/Library/Application Support/ndastro`
- **Linux**: `~/.local/share/ndastro`

This data is approximately 3 MB and only needs to be downloaded once.

## API Reference

### `get_sunrise_sunset(lat, lon, given_time)`

Calculate sunrise and sunset times for a specific location and date.

**Parameters:**
- `lat` (Angle): Latitude of the location in degrees
- `lon` (Angle): Longitude of the location in degrees  
- `given_time` (datetime): The date for which to calculate sunrise/sunset

**Returns:**
- `tuple[datetime, datetime]`: A tuple containing (sunrise, sunset) as UTC datetime objects

**Example:**
```python
from datetime import datetime
from skyfield.units import Angle
from ndastro_engine.astro_engine import get_sunrise_sunset

lat = Angle(degrees=34.0522)  # Los Angeles
lon = Angle(degrees=-118.2437)
date = datetime(2026, 3, 20)

sunrise, sunset = get_sunrise_sunset(lat, lon, date)
```

## Requirements

- Python 3.10 or higher
- skyfield >= 1.53
- pytz >= 2025.2

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/jaganathanb/ndastro-core.git
cd ndastro-core

# Install with development dependencies
pip install -e .[dev]
```

### Running Tests

```bash
pytest
```

### Code Quality

The project uses:
- **ruff** for linting and formatting
- **mypy** for type checking
- **pytest** for testing

```bash
# Run linter
ruff check .

# Run type checker
mypy ndastro_engine

# Format code
ruff format .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on [Skyfield](https://rhodesmill.org/skyfield/) by Brandon Rhodes
- Uses JPL ephemeris data (DE440t) for high-precision calculations
- Inspired by the need for a simple, modern astronomical calculation library

## Support

- 📫 **Email**: jaganathan.eswaran at gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/jaganathanb/ndastro-core/issues)
- 📖 **Documentation**: [GitHub Repository](https://github.com/jaganathanb/ndastro-core)

## Roadmap

### Coming Soon: Vedic Astrology Features 🕉️

The library will soon include comprehensive Vedic (Hindu/Indian) astrology functionalities:

**Panchanga Calculations:**
- Tithi (Lunar day) - All 30 tithis with precise timing
- Nakshatra (Lunar mansion) - 27 nakshatras with pada divisions
- Yoga - 27 yogas based on Sun-Moon positions
- Karana - Half-tithi divisions
- Vara (Weekday) - Traditional Hindu weekday system

**Astrological Timings:**
- Rahu Kala (Inauspicious period)
- Gulika Kala
- Yamaganda Kala
- Abhijit Muhurta (Auspicious time)
- Brahma Muhurta (Pre-dawn period)
- Dur Muhurtam (Inauspicious periods)

**Planetary Calculations:**
- Graha Sphuta (Planetary positions in sidereal zodiac)
- Ayanamsa corrections (Lahiri, Raman, Krishnamurti systems)
- Bhava (House) calculations
- Dasha periods (Vimshottari, Ashtottari, Yogini)
- Planetary strengths (Shadbala, Ashtakavarga)

**Hora & Choghadiya:**
- Hourly lord calculations
- Choghadiya divisions for day/night
- Auspicious/inauspicious period identification

**Festival & Event Calculations:**
- Hindu festival dates (Diwali, Holi, Navratri, etc.)
- Ekadashi dates
- Purnima (Full moon) and Amavasya (New moon)
- Sankranti (Solar transitions)
- Vyatipata and Vaidhriti yogas

**Birth Chart Features:**
- Rashi (Moon sign) calculations
- Lagna (Ascendant) determination
- Navamsa and other divisional charts
- Compatibility matching (Guna Milan)

### Other Planned Features

- Moon phase calculations
- Solar and lunar eclipse predictions
- Planetary positions (Western tropical system)
- Twilight times (civil, nautical, astronomical)
- Constellation identification
- Custom observer elevation support

## Changelog

See [CHANGELOG.md](https://github.com/jaganathanb/ndastro-core/releases) for a list of changes.

---

Made with ❤️ by Jaganathan B
