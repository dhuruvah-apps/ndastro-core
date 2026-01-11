# Ayanamsa Calculations

Ayanamsa (also spelled Ayanamsha) represents the precession of the equinoxes - the difference between tropical and sidereal zodiac positions. This is crucial for Vedic astrology calculations.

## What is Ayanamsa?

In Vedic astrology, planetary positions are calculated using the sidereal zodiac, which is based on fixed stars. The tropical zodiac (used in Western astrology) is based on the seasons. Due to the precession of Earth's axis, these two systems drift apart by about 50 seconds of arc per year.

The ayanamsa value represents the angular offset between these two systems at any given time.

## Available Ayanamsa Systems

ndastro-engine supports 16 different ayanamsa calculation methods:

### Popular Systems

#### Lahiri Ayanamsa
The most widely used ayanamsa in Indian astrology, officially adopted by the Indian government.

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_lahiri_ayanamsa(date)
print(f"Lahiri: {ayanamsa:.6f}°")
# Output: Lahiri: 24.260000°
```

#### Krishnamurti (KP) Systems
Two variants used in the Krishnamurti Paddhati system.

```python
from ndastro_engine.ayanamsa import (
    get_krishnamurti_new_ayanamsa,
    get_krishnamurti_old_ayanamsa
)

date = datetime(2026, 1, 11, 12, 0, 0)
kp_new = get_krishnamurti_new_ayanamsa(date)
kp_old = get_krishnamurti_old_ayanamsa(date)

print(f"KP New: {kp_new:.6f}°")
print(f"KP Old: {kp_old:.6f}°")
```

#### Raman Ayanamsa
Used by B.V. Raman and his followers.

```python
from ndastro_engine.ayanamsa import get_raman_ayanamsa

ayanamsa = get_raman_ayanamsa(datetime(2026, 1, 11, 12, 0, 0))
print(f"Raman: {ayanamsa:.6f}°")
```

#### Fagan-Bradley Ayanamsa
Western sidereal astrology system.

```python
from ndastro_engine.ayanamsa import get_fagan_bradley_ayanamsa

ayanamsa = get_fagan_bradley_ayanamsa(datetime(2026, 1, 11, 12, 0, 0))
print(f"Fagan-Bradley: {ayanamsa:.6f}°")
```

### Traditional Systems

```python
from ndastro_engine import ayanamsa
from datetime import datetime

date = datetime(2026, 1, 11, 12, 0, 0)

# Traditional Indian systems
kali = ayanamsa.get_kali_ayanamsa(date)
janma = ayanamsa.get_janma_ayanamsa(date)
yukteshwar = ayanamsa.get_yukteshwar_ayanamsa(date)
suryasiddhanta = ayanamsa.get_suryasiddhanta_ayanamsa(date)
aryabhatta = ayanamsa.get_aryabhatta_ayanamsa(date)

print(f"Kali: {kali:.6f}°")
print(f"Janma: {janma:.6f}°")
print(f"Yukteshwar: {yukteshwar:.6f}°")
```

### Star-Based Systems

```python
from ndastro_engine import ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Star-based calculations
true_citra = ayanamsa.get_true_citra_ayanamsa(date)
true_revati = ayanamsa.get_true_revati_ayanamsa(date)
true_pusya = ayanamsa.get_true_pusya_ayanamsa(date)

print(f"True Citra: {true_citra:.6f}°")
print(f"True Revati: {true_revati:.6f}°")
print(f"True Pusya: {true_pusya:.6f}°")
```

### Other Systems

```python
from ndastro_engine import ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Additional systems
true = ayanamsa.get_true_ayanamsa(date)
madhava = ayanamsa.get_madhava_ayanamsa(date)
vishnu = ayanamsa.get_vishnu_ayanamsa(date)
ushashasi = ayanamsa.get_ushashasi_ayanamsa(date)
```

## Complete List of Functions

| Function | Description |
|----------|-------------|
| `get_lahiri_ayanamsa()` | Lahiri (Chitrapaksha) ayanamsa |
| `get_krishnamurti_new_ayanamsa()` | KP New (0°0'0" at 291 CE) |
| `get_krishnamurti_old_ayanamsa()` | KP Old (15" less than KP New) |
| `get_raman_ayanamsa()` | B.V. Raman's ayanamsa |
| `get_fagan_bradley_ayanamsa()` | Fagan-Bradley (Western sidereal) |
| `get_kali_ayanamsa()` | Kali (0° at Kali Yuga start) |
| `get_janma_ayanamsa()` | Janma system |
| `get_yukteshwar_ayanamsa()` | Sri Yukteshwar's system |
| `get_suryasiddhanta_ayanamsa()` | Surya Siddhanta |
| `get_aryabhatta_ayanamsa()` | Aryabhatta system |
| `get_true_citra_ayanamsa()` | Based on Citra (Spica) star |
| `get_true_revati_ayanamsa()` | Based on Revati (ζ Piscium) star |
| `get_true_pusya_ayanamsa()` | Based on Pusya nakshatra |
| `get_true_ayanamsa()` | True ayanamsa |
| `get_madhava_ayanamsa()` | Madhava system |
| `get_vishnu_ayanamsa()` | Vishnu system |
| `get_ushashasi_ayanamsa()` | Ushashasi system |

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
from ndastro_engine import ayanamsa

date = datetime(2026, 1, 11, 12, 0, 0)

# Compare popular systems
systems = {
    "Lahiri": ayanamsa.get_lahiri_ayanamsa(date),
    "KP New": ayanamsa.get_krishnamurti_new_ayanamsa(date),
    "Raman": ayanamsa.get_raman_ayanamsa(date),
    "Fagan-Bradley": ayanamsa.get_fagan_bradley_ayanamsa(date),
}

for name, value in systems.items():
    print(f"{name:15s}: {value:8.4f}°")
```

## Historical Values

The ayanamsa value changes over time due to precession:

```python
from datetime import datetime
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa

# Historical dates
dates = [
    datetime(1900, 1, 1, 12, 0, 0),
    datetime(1950, 1, 1, 12, 0, 0),
    datetime(2000, 1, 1, 12, 0, 0),
    datetime(2026, 1, 1, 12, 0, 0),
    datetime(2050, 1, 1, 12, 0, 0),
]

for date in dates:
    ayanamsa = get_lahiri_ayanamsa(date)
    print(f"{date.year}: {ayanamsa:.4f}°")
```

## See Also

- [API Reference: Ayanamsa](../api/ayanamsa.md)
- [Quick Start Guide](../getting-started/quick-start.md)
