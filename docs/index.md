# NDAstro engine

A modern Vedic astrology calculation engine for Python, providing accurate astronomical calculations for birth charts, planetary positions, and ayanamsa systems.

## Features

✨ **Comprehensive Ayanamsa Systems**
- 16 different ayanamsa calculation methods including Lahiri, Krishnamurti (New & Old), Raman, and more
- Accurate J2000.0 epoch-based calculations

🌍 **Planetary Calculations**
- Real-time planetary positions (tropical and sidereal)
- Retrograde motion detection with period tracking
- Planetary combustion calculations
- Support for all major planets including Rahu and Ketu

🌅 **Astronomical Events**
- Sunrise and sunset calculations for any location
- WGS84 coordinate system support
- Timezone-aware datetime handling

⏱️ **Dasa Calculations**
- Multi-level dasa periods (Mahadasa, Antardasa, Pratyantardasa, Sookshmadasa)
- Vimshottari system built-in with full extensibility for custom systems

🎯 **Developer Friendly**
- Type-annotated for better IDE support
- Comprehensive test coverage (>90%)
- Clean, intuitive API design

## Accuracy

NDAstro engine is validated against two industry-standard Vedic astrology reference tools for **2026-01-01 00:00 IST, geocentric, Lahiri ayanamsa**.

=== "vs JHora (true node)"

    | Planet   | NDAstro engine | JHora    | Diff    |
    |----------|----------------|----------|---------|
    | Sun      | 256.1155°      | 256.119° | −0.004° |
    | Moon     | 39.0656°       | 39.066°  | −0.000° |
    | Mars     | 258.2929°      | 258.302° | −0.009° |
    | Mercury  | 244.0826°      | 244.093° | −0.010° |
    | Jupiter  | 87.1679°       | 87.163°  | +0.005° |
    | Venus    | 254.6985°      | 254.709° | −0.011° |
    | Saturn   | 331.9343°      | 331.935° | −0.001° |
    | Rahu     | 316.7617°      | 316.770° | −0.008° |
    | Ketu     | 136.7617°      | 136.770° | −0.008° |

    All planets within **0.011°** (< 1 arcminute).

=== "vs AstroSage (mean node)"

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

    All planets within **0.008°** (< 0.5 arcminutes). Configure `node_type="mean"` to match AstroSage's mean node.

See [Planet Positions → Accuracy Comparison](guide/planets.md#accuracy-comparison) for full details and how to reproduce these results.

## Quick Example

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa
from ndastro_engine.core import get_planet_position
from ndastro_engine.enums.planet_enum import Planets

# Calculate Lahiri Ayanamsa for today
date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_ayanamsa(date, "lahiri")
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
