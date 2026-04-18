# Dasa API Reference

Complete API documentation for the Dasa calculation module (`ndastro_engine.dasa`).

## Types

### DasaType

```python
DasaType: TypeAlias = Literal["vimshottari"]
```

Type alias for built-in dasa system names. Custom registered systems return `str`.

---

### DasaContext

```python
@dataclass(frozen=True)
class DasaContext:
    birth_datetime: datetime
    lat: float
    lon: float
    ayanamsa_system: AyanamsaSystem = "lahiri"
    dasa_type: str = "vimshottari"
```

Birth context required for all dasa calculations.

**Parameters:**
- `birth_datetime` (datetime) — Birth time (timezone-aware recommended; UTC if naive)
- `lat` (float) — Birth latitude (-90 to 90)
- `lon` (float) — Birth longitude (-180 to 180)
- `ayanamsa_system` (str, optional) — Sidereal zodiac system (default: `"lahiri"`)
- `dasa_type` (str, optional) — Dasa system name (default: `"vimshottari"`)

**Example:**
```python
context = DasaContext(
    birth_datetime=datetime(1990, 5, 15, 14, 30, 0, tzinfo=pytz.UTC),
    lat=28.6139,
    lon=77.2090,
    ayanamsa_system="lahiri",
    dasa_type="vimshottari"
)
```

---

### DasaQuery

```python
@dataclass(frozen=True)
class DasaQuery:
    levels: int = 4
    years: float | None = None
```

Options for timeline generation and running dasa lookups.

**Parameters:**
- `levels` (int, optional) — Number of dasa levels (1-4); default: 4
  - 1 = Mahadasa only
  - 2 = Mahadasa + Antardasa
  - 3 = Mahadasa + Antardasa + Pratyantardasa
  - 4 = All 4 levels including Sookshmadasa
- `years` (float | None, optional) — Time horizon from birth in years
  - If None: uses full dasa cycle minus elapsed time in first dasa
  - If set: generates periods for exactly `years` years

**Example:**
```python
# 3 levels, 50-year horizon
query = DasaQuery(levels=3, years=50)
```

---

### DasaBirthInfo

```python
@dataclass(frozen=True)
class DasaBirthInfo:
    sidereal_moon_longitude: float
    janma_nakshatra: Nakshatras
    nakshatra_progress_fraction: float
    nakshatra_remaining_fraction: float
    start_lord: str
```

Birth-time dasa information extracted from astrological calculations.

**Attributes:**
- `sidereal_moon_longitude` (float) — Moon's sidereal longitude at birth (0–360°)
- `janma_nakshatra` (Nakshatras) — Birth lunar mansion (27 nakshatras)
- `nakshatra_progress_fraction` (float) — Progress into the birth nakshatra (0–1)
- `nakshatra_remaining_fraction` (float) — Remaining fraction (1 - progress)
- `start_lord` (str) — Planet ruling the dasa at birth

**Example:**
```python
info = get_dasa_birth_info(context)
print(f"Janma Nakshatra: {info.janma_nakshatra.name}")
print(f"Start Lord: {info.start_lord}")
```

---

### DasaPeriod

```python
@dataclass(frozen=True)
class DasaPeriod:
    dasa_type: str
    level: int
    level_name: str
    lord: str
    start_utc: datetime
    end_utc: datetime
    children: tuple[DasaPeriod, ...] = ()
```

A single dasa period (mahadasa, antardasa, etc.) with optional nested children.

**Attributes:**
- `dasa_type` (str) — Name of the dasa system
- `level` (int) — Period level (1–4)
- `level_name` (str) — Human-readable level ("maha", "antara", "pratyantara", "sookshma")
- `lord` (str) — Ruling planet for this period
- `start_utc` (datetime) — Period start in UTC (may be before birth)
- `end_utc` (datetime) — Period end in UTC
- `children` (tuple[DasaPeriod, ...]) — Nested periods at next level (empty if at max requested level)

**Example:**
```python
for period in timeline:
    print(f"{period.level_name}: {period.lord}")
    print(f"  Duration: {(period.end_utc - period.start_utc).days} days")
    for child in period.children:
        print(f"  → {child.level_name}: {child.lord}")
```

---

### RunningDasa

```python
@dataclass(frozen=True)
class RunningDasa:
    maha: DasaPeriod | None
    antara: DasaPeriod | None
    pratyantara: DasaPeriod | None
    sookshma: DasaPeriod | None
```

Running dasa periods at all 4 levels for a specific timestamp.

**Attributes:**
- `maha` (DasaPeriod | None) — Mahadasa (level 1)
- `antara` (DasaPeriod | None) — Antardasa (level 2)
- `pratyantara` (DasaPeriod | None) — Pratyantardasa (level 3)
- `sookshma` (DasaPeriod | None) — Sookshmadasa (level 4)

Values are None if the query date falls outside the calculated timeline or if not all 4 levels were requested in the original timeline.

**Example:**
```python
running = get_running_dasa(datetime.now(pytz.UTC), context)
if running.maha:
    print(f"Current Mahadasa: {running.maha.lord}")
```

---

### DasaDefinition

```python
@dataclass(frozen=True)
class DasaDefinition:
    lords: tuple[str, ...]
    years_by_lord: dict[str, float]
    cycle_years: float
    start_lord_resolver: Callable[[Nakshatras], str]
```

Definition of a dasa system for use with `register_dasa_type()`.

**Attributes:**
- `lords` (tuple[str, ...]) — Sequence of planet names (ruling the cycle in order)
- `years_by_lord` (dict[str, float]) — Years assigned to each lord (sum should equal `cycle_years`)
- `cycle_years` (float) — Total cycle length in years
- `start_lord_resolver` (Callable) — Function that takes Janma Nakshatra and returns the start lord

**Example:**
```python
definition = DasaDefinition(
    lords=("SUN", "MOON", "MARS"),
    years_by_lord={"SUN": 6, "MOON": 8, "MARS": 5},
    cycle_years=19,
    start_lord_resolver=lambda n: "SUN"
)
```

---

## Functions

### get_supported_dasa_types()

```python
def get_supported_dasa_types() -> tuple[str, ...]
```

Returns all registered dasa system names (built-in + custom).

**Returns:**
- Tuple of dasa type names

**Raises:**
- None

**Example:**
```python
systems = get_supported_dasa_types()
print(systems)  # ('vimshottari',) or more if registered
```

---

### get_dasa_birth_info(context: DasaContext) -> DasaBirthInfo

```python
def get_dasa_birth_info(context: DasaContext) -> DasaBirthInfo
```

Computes sidereal moon position and dasa birth information from geographical/astronomical context.

**Parameters:**
- `context` (DasaContext) — Birth context

**Returns:**
- DasaBirthInfo — Birth-time dasa data

**Raises:**
- ValueError — If `dasa_type` is unsupported

**Example:**
```python
info = get_dasa_birth_info(context)
print(f"Start Lord: {info.start_lord}")
print(f"Janma Nakshatra: {info.janma_nakshatra.name}")
```

---

### get_dasa_timeline(context: DasaContext, query: DasaQuery | None = None) -> list[DasaPeriod]

```python
def get_dasa_timeline(
    context: DasaContext,
    query: DasaQuery | None = None
) -> list[DasaPeriod]
```

Generates dasa timeline from birth with up to 4 hierarchical levels.

**Parameters:**
- `context` (DasaContext) — Birth context
- `query` (DasaQuery | None, optional) — Timeline options (default: `DasaQuery()` = 4 levels, full cycle)

**Returns:**
- List of DasaPeriod (mahadasas), each with nested children at requested levels

**Raises:**
- ValueError — If `levels` ∉ [1, 4] or `years` ≤ 0 or `dasa_type` unsupported

**Example:**
```python
timeline = get_dasa_timeline(context, DasaQuery(levels=2, years=40))
for maha in timeline:
    print(f"{maha.lord}: {maha.start_utc.date()} → {maha.end_utc.date()}")
    for antara in maha.children:
        print(f"  {antara.lord}")
```

---

### get_running_dasa(query_datetime: datetime, context: DasaContext, query: DasaQuery | None = None) -> RunningDasa

```python
def get_running_dasa(
    query_datetime: datetime,
    context: DasaContext,
    query: DasaQuery | None = None
) -> RunningDasa
```

Finds the currently running dasa at all 4 levels for a given timestamp.

**Parameters:**
- `query_datetime` (datetime) — Query time (timezone-aware recommended)
- `context` (DasaContext) — Birth context
- `query` (DasaQuery | None, optional) — Query options (default: 4 levels, full cycle)

**Returns:**
- RunningDasa with `maha`, `antara`, `pratyantara`, `sookshma` (any can be None)

**Raises:**
- ValueError — If dasa_type unsupported

**Example:**
```python
now = datetime.now(pytz.UTC)
running = get_running_dasa(now, context)
print(f"Today's Mahadasa: {running.maha.lord if running.maha else 'N/A'}")
```

---

### register_dasa_type(name: str, definition: DasaDefinition) -> None

```python
def register_dasa_type(name: str, definition: DasaDefinition) -> None
```

Registers a custom dasa system for runtime use.

**Parameters:**
- `name` (str) — Unique identifier (must be non-empty, no leading/trailing whitespace)
- `definition` (DasaDefinition) — System definition

**Returns:**
- None

**Raises:**
- ValueError — If `name` is empty/whitespace or conflicts with built-in system

**Example:**
```python
register_dasa_type(
    "my_custom_dasa",
    DasaDefinition(
        lords=("SUN", "MOON", "MARS"),
        years_by_lord={"SUN": 5, "MOON": 5, "MARS": 5},
        cycle_years=15,
        start_lord_resolver=lambda n: "SUN"
    )
)

# Now use it
context = DasaContext(..., dasa_type="my_custom_dasa")
```

---

## Constants

### Built-in Dasa Systems

**Vimshottari (120-year cycle)**
- Lords: Ketu (7y), Venus (20y), Sun (6y), Moon (10y), Mars (7y), Rahu (18y), Jupiter (16y), Saturn (19y), Mercury (17y)
- Start Lord Resolver: Uses Janma Nakshatra owner (nakshatra.owner.name)
- Default system, most widely used in Vedic astrology

---

## Examples

### Example 1: Full Timeline with All Levels

```python
from datetime import datetime
import pytz
from ndastro_engine.dasa import DasaContext, DasaQuery, get_dasa_timeline

context = DasaContext(
    birth_datetime=datetime(1985, 10, 24, 6, 30, 0, tzinfo=pytz.UTC),
    lat=13.08,
    lon=80.27,
)

timeline = get_dasa_timeline(context, DasaQuery(levels=4, years=120))

# Print first mahadasa and all its sub-periods
maha = timeline[0]
print(f"Mahadasa {maha.lord}: {maha.start_utc} → {maha.end_utc}")
for antara in maha.children:
    print(f"  Antara {antara.lord}: {antara.start_utc} → {antara.end_utc}")
    for pratyantara in antara.children:
        print(f"    Pratyantara {pratyantara.lord}")
```

### Example 2: Custom Dasa Registration

```python
from ndastro_engine.dasa import DasaDefinition, register_dasa_type, DasaContext
from ndastro_engine.enums import Planets, Nakshatras

# Define Yogini dasa (36-year, 8-planet system)
yogini_lords = ("MANGALA", "PINGALA", "DHANYA", "BHRAMARI",
                "BHADRIKA", "ULKA", "SIDDHA", "SANKATA")

def yogini_resolver(nakshatra: Nakshatras) -> str:
    return yogini_lords[(nakshatra.value - 1) % len(yogini_lords)]

register_dasa_type(
    "yogini",
    DasaDefinition(
        lords=yogini_lords,
        years_by_lord={
            "MANGALA": 1, "PINGALA": 2, "DHANYA": 3, "BHRAMARI": 4,
            "BHADRIKA": 5, "ULKA": 6, "SIDDHA": 7, "SANKATA": 8
        },
        cycle_years=36,
        start_lord_resolver=yogini_resolver
    )
)

# Use it
context = DasaContext(..., dasa_type="yogini")
```

### Example 3: Running Dasa at Specific Date

```python
from datetime import datetime, timedelta
import pytz
from ndastro_engine.dasa import DasaContext, get_running_dasa

context = DasaContext(...)

# Check dasa 30 years after birth
query_date = context.birth_datetime + timedelta(days=365.25 * 30)
running = get_running_dasa(query_date, context)

if running.maha:
    days_remaining = (running.maha.end_utc - query_date).days
    print(f"In {running.maha.lord} Mahadasa")
    print(f"Ends in {days_remaining} days")
```

---

## See Also

- [Dasa Guide](../guide/dasa.md) — User guide with concepts and practical examples
- [Core API](core.md) — Planetary position calculations
- [Ayanamsa API](ayanamsa.md) — Sidereal zodiac systems
