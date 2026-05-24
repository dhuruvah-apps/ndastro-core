# Dasa Calculations

Dasa systems are fundamental time periods used in Vedic astrology to predict life events and timings. The NDAstro engine provides a complete, production-ready implementation of Dasa calculations with support for multiple systems and custom extensions.

## Overview

A Dasa (also spelled Dasha) is a planetary period that divides a person's life into specific timeframes ruled by different planets (lords). The engine supports:

- **4 hierarchical levels**: Mahadasa (major period), Antardasa (sub-period), Pratyantardasa (sub-sub-period), and Sookshmadasa (sub-sub-sub-period)
- **Built-in Vimshottari system**: The most widely used 120-year dasa cycle
- **Custom dasa registration**: Define your own dasa systems at runtime

## Core Concepts

### Birth Information
When calculating dasas, the engine first determines:
- **Sidereal Moon longitude** at birth (converted using the selected ayanamsa system)
- **Janma Nakshatra** (birth lunar mansion)
- **Start lord**: The planet that rules the dasa cycle at birth
- **Fractions**: How far into the starting dasa period the birth occurs

### Dasa Periods
Each dasa period is represented by:
- **Level**: 1 (Mahadasa) to 4 (Sookshmadasa)
- **Lord**: The ruling planet for that period
- **Start/End timestamps**: Exact UTC datetime of period boundaries
- **Children**: Nested periods at the next level

### Timeline Generation
Timelines are generated from birth with configurable:
- **Levels**: How many levels deep to calculate (1-4)
- **Years**: Optional time horizon (defaults to full cycle from birth)

## Getting Started

### Basic Usage

```python
from datetime import datetime
import pytz
from ndastro_engine.dasa import DasaContext, DasaQuery, get_dasa_timeline

# Define birth context
context = DasaContext(
    birth_datetime=datetime(1985, 10, 24, 6, 30, 0, tzinfo=pytz.UTC),
    lat=13.08,           # Chennai latitude
    lon=80.27,           # Chennai longitude
    ayanamsa_system="lahiri",  # Sidereal zodiac
    dasa_type="vimshottari"    # Default dasa system
)

# Generate timeline for 40 years with 4 levels
query = DasaQuery(levels=4, years=40)
timeline = get_dasa_timeline(context, query)

# Inspect periods
for period in timeline[:3]:  # First 3 mahadasas
    print(f"{period.lord}: {period.start_utc.date()} → {period.end_utc.date()}")
```

### Get Birth Information

```python
from ndastro_engine.dasa import get_dasa_birth_info

birth_info = get_dasa_birth_info(context)
print(f"Sidereal Moon: {birth_info.sidereal_moon_longitude:.2f}°")
print(f"Janma Nakshatra: {birth_info.janma_nakshatra.name}")
print(f"Start Lord: {birth_info.start_lord}")
print(f"Progress in Nakshatra: {birth_info.nakshatra_progress_fraction:.1%}")
```

### Find Running Dasa

```python
from datetime import datetime, timedelta
from ndastro_engine.dasa import get_running_dasa

# Query date 40 years after birth
query_date = context.birth_datetime + timedelta(days=365*40)

running = get_running_dasa(query_date, context)

print(f"Mahadasa: {running.maha.lord} ({running.maha.start_utc.date()} → {running.maha.end_utc.date()})")
print(f"Antardasa: {running.antara.lord} ({running.antara.start_utc.date()} → {running.antara.end_utc.date()})")
print(f"Pratyantara: {running.pratyantara.lord}")
print(f"Sookshma: {running.sookshma.lord}")
```

## Vimshottari Dasa

Vimshottari is the most commonly used dasa system in Vedic astrology, featuring a 120-year cycle divided among 9 planets:

| Planet | Years |
|--------|-------|
| Ketu   | 7     |
| Venus  | 20    |
| Sun    | 6     |
| Moon   | 10    |
| Mars   | 7     |
| Rahu   | 18    |
| Jupiter| 16    |
| Saturn | 19    |
| Mercury| 17    |

The start lord is determined by the **Janma Nakshatra** (birth lunar mansion), using the nakshatra owner in sidereal calculations.

```python
from ndastro_engine.dasa import DasaContext, get_supported_dasa_types

# Vimshottari is the default
context = DasaContext(
    birth_datetime=...,
    lat=...,
    lon=...,
    dasa_type="vimshottari"
)

print(f"Supported systems: {get_supported_dasa_types()}")
```

## Custom Dasa Systems

You can define and register your own dasa systems at runtime using the registration API:

```python
from ndastro_engine.dasa import DasaDefinition, register_dasa_type
from ndastro_engine.enums import Planets

# Define a 3-planet custom system: Sun (6yr), Moon (8yr), Mars (5yr) = 19-year cycle
custom_lords = (Planets.SUN.name, Planets.MOON.name, Planets.MARS.name)
custom_years = {
    Planets.SUN.name: 6.0,
    Planets.MOON.name: 8.0,
    Planets.MARS.name: 5.0,
}

definition = DasaDefinition(
    lords=custom_lords,
    years_by_lord=custom_years,
    cycle_years=19.0,
    start_lord_resolver=lambda nakshatra: Planets.SUN.name  # Always start with Sun
)

register_dasa_type("custom_19_year", definition)

# Now use it in DasaContext
context = DasaContext(
    birth_datetime=...,
    lat=...,
    lon=...,
    dasa_type="custom_19_year"
)
```

### Custom Start Lord Resolvers

The `start_lord_resolver` function determines which planet's dasa is active at birth based on the Janma Nakshatra. Common patterns:

**Explicit Mapping** (e.g., Ashtottari):
```python
NAKSHATRA_LORDS = {
    Nakshatras.ASWINNI: Planets.RAHU.name,
    Nakshatras.BHARANI: Planets.RAHU.name,
    # ... map all 27 nakshatras
}

def resolver(nakshatra: Nakshatras) -> str:
    return NAKSHATRA_LORDS[nakshatra]
```

**Cyclic Pattern** (e.g., Yogini):
```python
YOGINI_LORDS = (
    "MANGALA", "PINGALA", "DHANYA", "BHRAMARI",
    "BHADRIKA", "ULKA", "SIDDHA", "SANKATA"
)

def resolver(nakshatra: Nakshatras) -> str:
    return YOGINI_LORDS[(nakshatra.value - 1) % len(YOGINI_LORDS)]
```

**Nakshatra Owner** (e.g., Vimshottari):
```python
def resolver(nakshatra: Nakshatras) -> str:
    return nakshatra.owner.name  # Use the planet that owns this nakshatra
```

## API Functions

### get_supported_dasa_types()

Returns all available dasa system names (built-in + custom registered).

```python
supported = get_supported_dasa_types()
# ('vimshottari',) — or more if custom types registered
```

### get_dasa_birth_info(context)

Extracts birth-time dasa information: sidereal moon position, nakshatra, start lord, and progress fractions.

```python
birth_info = get_dasa_birth_info(context)
# Returns: DasaBirthInfo with all birth-time dasa data
```

### get_dasa_timeline(context, query=None)

Generates a list of mahadasa periods (level 1) with optional nested children at levels 2, 3, 4.

```python
timeline = get_dasa_timeline(context, DasaQuery(levels=3, years=60))
# Returns: list[DasaPeriod] with up to 3 levels of nesting
```

### get_running_dasa(query_datetime, context, query=None)

Finds the currently running dasa at all 4 levels for a given timestamp.

```python
running = get_running_dasa(datetime(2026, 4, 18, 12, 0, 0, tzinfo=pytz.UTC), context)
# Returns: RunningDasa with maha, antara, pratyantara, sookshma DasaPeriod or None
```

### register_dasa_type(name, definition)

Registers a new custom dasa system for use in `DasaContext`.

```python
register_dasa_type("my_system", DasaDefinition(...))

# Raises ValueError if:
# - name is empty or contains whitespace
# - name conflicts with built-in type
```

## Practical Examples

### Predict Event Timing

```python
from datetime import datetime
import pytz
from ndastro_engine.dasa import DasaContext, DasaQuery, get_dasa_timeline

context = DasaContext(
    birth_datetime=datetime(1985, 10, 24, 6, 30, 0, tzinfo=pytz.UTC),
    lat=13.08,
    lon=80.27,
    ayanamsa_system="lahiri"
)

# Get 60-year timeline with all 4 levels
timeline = get_dasa_timeline(context, DasaQuery(levels=4, years=60))

# Find Saturn mahadasa periods
for period in timeline:
    if period.lord == "SATURN":
        print(f"Saturn Mahadasa: {period.start_utc.date()} → {period.end_utc.date()}")
        print(f"  Antara periods:")
        for antara in period.children:
            print(f"    {antara.lord}: {antara.start_utc.date()} → {antara.end_utc.date()}")
```

### Compare Different Ayanamsa Systems

```python
from ndastro_engine.dasa import DasaContext, get_dasa_birth_info

for ayanamsa in ["lahiri", "raman", "krishnamurti"]:
    context = DasaContext(
        birth_datetime=...,
        lat=...,
        lon=...,
        ayanamsa_system=ayanamsa
    )
    info = get_dasa_birth_info(context)
    print(f"{ayanamsa}: Start Lord = {info.start_lord}")
```

## Best Practices

1. **Always specify ayanamsa**: Different ayanamsa systems produce different nakshatra positions and thus different start lords. Lahiri is most common in Indian astrology.

2. **Use UTC timestamps**: All dasa calculations work internally in UTC. Convert local times to UTC before querying.

3. **Validate custom systems**: When registering a custom dasa, ensure:
   - All lords in the sequence have corresponding year entries
   - Years are positive values
   - Cycle years equals the sum of all lord years

4. **Cache timelines**: If you need multiple queries on the same birth, generate the full timeline once rather than calling repeatedly.

5. **Handle None levels**: When requesting 4 levels, some query dates may only have 1-3 populated levels (near boundaries), so check for None values.

## Precision & Compatibility

### Why NDAstro is more accurate than traditional platforms

NDAstro uses **NASA JPL DE440T** via Skyfield for all planetary positions, the most accurate
publicly available modern ephemeris.  Traditional platforms (JHora, DrikPanchang, AstroSage)
use an older computation stack that contains two systematic deviations:

#### Deviation 1 — IAU-1940 Lahiri constants

These platforms use the *Traditional Lahiri* label in their UI, which maps to Swiss Ephemeris
``SIDM_LAHIRI_1940`` (mode 43). This uses epoch constants from the 1940 IAU publication:

| Constant | SIDM_LAHIRI_1940 (traditional platforms) | SIDM_LAHIRI (NDAstro `"lahiri"`) |
|---|---|---|
| Epoch | J1900 (JD 2415021.0) | JD 2415020.9132 |
| Ayanamsa at epoch | 22.44578° | 22.46084° |
| Rate | 50.2798"/yr | 50.2388"/yr |

This produces an ayanamsa approximately **53 arcsec lower** than the modern value,
shifting the computed sidereal Moon forward by the same amount.

#### Deviation 2 — Double Delta-T application (software bug)

JHora and platforms derived from it pre-convert the birth UT to TT manually, then pass
the result to ``swe.calc_ut()`` which adds Delta-T a **second time**.  In 2025, Delta-T
≈ 69 seconds, so the Moon position is computed as if birth occurred ~69 seconds later
than it actually did.  The Moon moves at ~13°/day, so this advances the Moon by
approximately **43 arcsec**.

### Combined effect on dasa start dates

Both deviations advance the sidereal Moon by a total of ~96 arcsec, which propagates
through the nakshatra-fraction calculation into the Mahadasa elapsed-days calculation:

| Dasa Lord | Period | Offset from NDAstro (approx.) |
|---|---|---|
| Sun | 6 years | ~3.9 days |
| Mars / Ketu | 7 years | ~4.6 days |
| Moon | 10 years | ~6.5 days |
| Jupiter | 16 years | ~10.5 days |
| Rahu | 18 years | ~11.8 days |
| Saturn | 19 years | ~12.4 days |
| Venus | 20 years | ~13.1 days |

**NDAstro `"lahiri"` output is correct.** The traditional platforms’ dates are systematically
shifted because of the older epoch constants and the double-DeltaT bug.

### `true_lahiri` mode — compatibility output

When you need dasa dates that match JHora/DrikPanchang/AstroSage for client comparison or
cross-validation, use `ayanamsa_system="true_lahiri"` in `DasaContext`:

```python
from ndastro_engine.dasa import DasaContext, get_dasa_timeline

context = DasaContext(
    birth_datetime=...,
    lat=...,
    lon=...,
    ayanamsa_system="true_lahiri",  # JHora-compatible output
)
timeline = get_dasa_timeline(context)
```

This replicates both deviations (IAU-1940 constants + double-DeltaT shift) and produces
dasa start dates within approximately **4 hours** of JHora Traditional Lahiri for a
6-year Sun Mahadasa (and proportionally for other lords).

> The `true_lahiri` mode uses only Skyfield for all computations. Delta-T is read
> from Skyfield's built-in IERS table (`t.tt - t.ut1`); the SIDM_LAHIRI_1940 ayanamsa
> uses IAU-1940 precession constants plus the IAU 2000B nutation in longitude (Δψ) from
> `skyfield.nutationlib.iau2000b`, matching SE to within 0.001 arcsec. No additional
> dependencies are required.

## See Also

- [API Reference](../api/dasa.md) - Complete function signatures and type definitions
- [Planetary Positions](planets.md) - Related planetary calculation guide
- [Ayanamsa Systems](ayanamsa.md) - Learn about sidereal zodiac systems
