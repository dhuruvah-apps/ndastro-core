# Ayanamsa Calculations

Ayanamsa (also spelled Ayanamsha) represents the precession of the equinoxes - the difference between tropical and sidereal zodiac positions. This is crucial for Vedic astrology calculations.

## What is Ayanamsa?

In Vedic astrology, planetary positions are calculated using the sidereal zodiac, which is based on fixed stars. The tropical zodiac (used in Western astrology) is based on the seasons. Due to the precession of Earth's axis, these two systems drift apart by about 50 seconds of arc per year.

The ayanamsa value represents the angular offset between these two systems at any given time.

## Basic Usage

Use the type-safe `get_ayanamsa()` function with a date and system name:

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa, AyanamsaSystem
from typing import cast

date = datetime(2026, 1, 11, 12, 0, 0)

# Calculate Lahiri ayanamsa
lahiri = get_ayanamsa(date, cast(AyanamsaSystem, "lahiri"))
print(f"Lahiri: {lahiri:.6f}°")
# Output: Lahiri: 24.260000°

# Or use without cast if your IDE supports it:
raman = get_ayanamsa(date, "raman")  # type: AyanamsaSystem
kp_new = get_ayanamsa(date, "krishnamurti_new")
fagan = get_ayanamsa(date, "fagan_bradley")

print(f"Raman: {raman:.6f}°")
print(f"KP New: {kp_new:.6f}°")
print(f"Fagan-Bradley: {fagan:.6f}°")
```

**Type-Safety:** The `AyanamsaSystem` type ensures autocomplete support in your IDE and catches invalid system names at development time.

## Available Ayanamsa Systems

NDAstro engine supports 17 different ayanamsa calculation methods:

### Popular Systems

#### Lahiri Ayanamsa
The most widely used ayanamsa in Indian astrology, officially adopted by the Indian government.
Uses the modern Swiss Ephemeris ``SIDM_LAHIRI`` constants with NASA JPL DE440T — the most
accurate available implementation.

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_ayanamsa(date, "lahiri")
print(f"Lahiri: {ayanamsa:.6f}°")
```

#### True Lahiri / Chitrapaksha (`true_lahiri`)

A compatibility mode that replicates the ayanamsa used by JHora, DrikPanchang, and AstroSage.
These platforms share two systematic deviations from the modern `"lahiri"` mode:

1. **IAU-1940 constants (SE ``SIDM_LAHIRI_1940``):** They use the original Lahiri epoch
   constants published in the 1940s (epoch = J1900, ayan₀ = 22.4458°, rate = 50.2798"/yr)
   rather than the refined modern values.
2. **Double Delta-T application:** Their Swiss Ephemeris wrapper pre-converts birth UT to TT
   manually, then passes TT to ``swe.calc_ut()`` which adds Delta-T a second time, advancing
   the effective Moon computation time by ~69 seconds (in 2025).

When used with `DasaContext`, dasa start dates match JHora/DrikPanchang/AstroSage within
approximately **4 hours** for a 6-year Mahadasa. Proportionally larger offsets apply to
longer dasas (up to ~13 hours for a 20-year Venus Mahadasa).

> **This mode exists for cross-platform compatibility only.**
> Use `"lahiri"` for astronomically accurate results based on NASA JPL DE440T.

```python
from datetime import datetime
import pytz
from ndastro_engine.dasa import DasaContext, get_dasa_timeline

# Reproduces JHora 'Traditional Lahiri' dasa dates
context = DasaContext(
    birth_datetime=datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.timezone("Asia/Kolkata").localize(
        datetime(2026, 1, 1)).tzinfo),
    lat=12.9833,
    lon=77.5833,
    ayanamsa_system="true_lahiri",
)
timeline = get_dasa_timeline(context)
```

> **Note:** The `true_lahiri` ayanamsa value returned by `get_ayanamsa()` uses the
> IAU-1940 constants only (no time shift). The double-Delta-T Moon shift is applied
> automatically inside `get_dasa_birth_info()` and `get_dasa_timeline()`.

#### Krishnamurti (KP) Systems
Two variants used in the Krishnamurti Paddhati system.

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)
kp_new = get_ayanamsa(date, "krishnamurti_new")
kp_old = get_ayanamsa(date, "krishnamurti_old")

print(f"KP New: {kp_new:.6f}°")
print(f"KP Old: {kp_old:.6f}°")
```

#### Raman Ayanamsa
Used by B.V. Raman and his followers.

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_ayanamsa(date, "raman")
```

## Parsing ISO Datetime Strings

When working with datetime strings from external sources, use `parse_iso_datetime()` to safely parse ISO format strings with automatic UTC default for missing timezone information:

```python
from ndastro_engine.utils import parse_iso_datetime
from ndastro_engine.ayanamsa import get_ayanamsa

# Parse ISO datetime strings
# If no timezone is present, UTC is assumed
date1 = parse_iso_datetime("2026-01-11T12:00:00")
date2 = parse_iso_datetime("2026-01-11T12:00:00Z")
date3 = parse_iso_datetime("2026-01-11T12:00:00+05:30")

# All parsed datetimes are timezone-aware
print(f"Date1 timezone: {date1.tzinfo}")
print(f"Date2 timezone: {date2.tzinfo}")
print(f"Date3 timezone: {date3.tzinfo}")

# Use with ayanamsa calculations
lahiri = get_ayanamsa(date1, "lahiri")
print(f"Lahiri ayanamsa: {lahiri:.6f}°")
print(f"Raman: {ayanamsa:.6f}°")
```

#### Fagan-Bradley Ayanamsa
Western sidereal astrology system.

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_ayanamsa(date, "fagan_bradley")
print(f"Fagan-Bradley: {ayanamsa:.6f}°")
```

### Traditional Systems

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Traditional Indian systems
kali = get_ayanamsa(date, "kali")
janma = get_ayanamsa(date, "janma")
yukteshwar = get_ayanamsa(date, "yukteshwar")
suryasiddhanta = get_ayanamsa(date, "suryasiddhanta")
aryabhatta = get_ayanamsa(date, "aryabhatta")

print(f"Kali: {kali:.6f}°")
print(f"Janma: {janma:.6f}°")
print(f"Yukteshwar: {yukteshwar:.6f}°")
```

### Star-Based Systems

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Star-based calculations
true_citra = get_ayanamsa(date, "true_citra")
true_revati = get_ayanamsa(date, "true_revati")
true_pusya = get_ayanamsa(date, "true_pusya")

print(f"True Citra: {true_citra:.6f}°")
print(f"True Revati: {true_revati:.6f}°")
print(f"True Pusya: {true_pusya:.6f}°")
```

### Other Systems

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Additional systems
true = get_ayanamsa(date, "true")
madhava = get_ayanamsa(date, "madhava")
vishnu = get_ayanamsa(date, "vishnu")
ushashasi = get_ayanamsa(date, "ushashasi")
```

## Complete List of System Names

| System Name | Description |
|-------------|-------------|
| `lahiri` | Lahiri (Chitrapaksha) — modern SE SIDM_LAHIRI constants, NASA JPL DE440T |
| `true_lahiri` | True Lahiri / Chitrapaksha (IAU-1940 / SE SIDM_LAHIRI_1940) — matches JHora/DrikPanchang |
| `krishnamurti_new` | KP New (0°0'0" at 291 CE) |
| `krishnamurti_old` | KP Old (15" less than KP New) |
| `raman` | B.V. Raman's ayanamsa |
| `fagan_bradley` | Fagan-Bradley (Western sidereal) |
| `kali` | Kali (0° at Kali Yuga start) |
| `janma` | Janma system |
| `yukteshwar` | Sri Yukteshwar's system |
| `suryasiddhanta` | Surya Siddhanta |
| `aryabhatta` | Aryabhatta system |
| `true_citra` | Based on Citra (Spica) star |
| `true_revati` | Based on Revati (ζ Piscium) star |
| `true_pusya` | Based on Pusya nakshatra |
| `true` | True ayanamsa |
| `madhava` | Madhava system |
| `vishnu` | Vishnu system |
| `ushashasi` | Ushashasi system |

## Understanding the Calculations

All ayanamsa calculations use a quadratic formula based on Julian centuries from J2000.0 epoch:

```
ayanamsa = c0 + c1 × b6 + c2 × b6²
```

Where:
- `c0`: Constant term (ayanamsa at reference epoch)
- `c1`: Linear term (degrees per Julian century)
- `c2`: Quadratic term (degrees per square Julian century)
- `b6`: Time parameter in Julian centuries from J2000.0

## Comparing Different Systems

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Compare popular systems
systems = ["lahiri", "krishnamurti_new", "raman", "fagan_bradley"]

for system in systems:
    value = get_ayanamsa(date, system)
    print(f"{system:20s}: {value:8.4f}°")
```

## Historical Values

The ayanamsa value changes over time due to precession:

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_ayanamsa

# Historical dates
dates = [
    datetime(1900, 1, 1, 12, 0, 0),
    datetime(1950, 1, 1, 12, 0, 0),
    datetime(2000, 1, 1, 12, 0, 0),
    datetime(2026, 1, 1, 12, 0, 0),
    datetime(2050, 1, 1, 12, 0, 0),
]

for date in dates:
    ayanamsa = get_ayanamsa(date, "lahiri")
    print(f"{date.year}: {ayanamsa:.4f}°")
```

## See Also

- [API Reference: Ayanamsa](../api/ayanamsa.md)
- [Quick Start Guide](../getting-started/quick-start.md)
