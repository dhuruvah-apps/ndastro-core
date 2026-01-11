# ndastro-engine

A modern Vedic astrology calculation engine for Python, providing accurate astronomical calculations for birth charts, planetary positions, and ayanamsa systems.

## Features

✨ **Comprehensive Ayanamsa Systems**
- 16 different ayanamsa calculation methods including Lahiri, Krishnamurti (New & Old), Raman, and more
- Accurate J2000.0 epoch-based calculations

🌍 **Planetary Calculations**
- Real-time planetary positions (tropical and sidereal)
- Retrograde motion detection with period tracking
- Support for all major planets including Rahu and Ketu

🌅 **Astronomical Events**
- Sunrise and sunset calculations for any location
- WGS84 coordinate system support
- Timezone-aware datetime handling

🎯 **Developer Friendly**
- Type-annotated for better IDE support
- Comprehensive test coverage (>90%)
- Clean, intuitive API design

## Quick Example

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

# Calculate Lahiri Ayanamsa for today
date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_lahiri_ayanamsa(date)
print(f"Lahiri Ayanamsa: {ayanamsa:.6f}°")

# Get Sun's position
sun_position = get_planet_position(
    Planets.SUN, 
    latitude=28.6139,  # New Delhi
    longitude=77.2090,
    date=date
)
print(f"Sun's longitude: {sun_position:.6f}°")
```

## Installation

Install from PyPI:

```bash
pip install ndastro-engine
```

## Documentation

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quick-start.md)
- [API Reference](api/core.md)
- [Changelog](changelog.md)

## Requirements

- Python 3.10 or higher
- skyfield >= 1.53
- pytz >= 2025.2

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jaganathanb/ndastro-core/blob/main/LICENSE) file for details.

## Contributing

Contributions are welcome! Please see our [Contributing Guide](contributing.md) for details.

## Links

- [GitHub Repository](https://github.com/jaganathanb/ndastro-core)
- [PyPI Package](https://pypi.org/project/ndastro-engine/)
- [Issue Tracker](https://github.com/jaganathanb/ndastro-core/issues)
