# Configuration

NDAstro engine is configurable via environment variables or at runtime using `configure()`. All settings are collected in the `EngineSettings` dataclass and can be selectively overridden without restarting the process.

## Settings Reference

| Setting | Env variable | Default | Valid values |
|---|---|---|---|
| `position_reference` | `NDASTRO_POSITION_REFERENCE` | `geocentric` | `geocentric`, `topocentric` |
| `node_type` | `NDASTRO_NODE_TYPE` | `true` | `true`, `mean` |
| `ayanamsa_delta` | `NDASTRO_AYANAMSA_DELTA` | `0.0` | any float (degrees) |
| `dasa_year_length` | `NDASTRO_DASA_YEAR_LENGTH` | `365.25` | any float (days) |
| `apply_nutation` | `NDASTRO_APPLY_NUTATION` | `true` | `true`, `false` |
| `apply_aberration` | `NDASTRO_APPLY_ABERRATION` | `true` | `true`, `false` |
| `apply_grav_deflection` | `NDASTRO_APPLY_GRAV_DEFLECTION` | `true` | `true`, `false` |
| `sunrise_definition` | `NDASTRO_SUNRISE_DEFINITION` | `geometric` | `geometric`, `disc_centre` |

## Environment Variables

Set settings via a `.env` file or shell environment before importing the package:

```bash
# .env
NDASTRO_POSITION_REFERENCE=geocentric
NDASTRO_NODE_TYPE=true
NDASTRO_AYANAMSA_DELTA=0.0
NDASTRO_DASA_YEAR_LENGTH=365.25
NDASTRO_SUNRISE_DEFINITION=geometric
```

These are read once at import time via `EngineSettings.from_env()`.

## Runtime Configuration

Use `configure()` to change settings at runtime without restarting:

```python
from ndastro_engine.config import configure, EngineSettingsOverride

# Override specific settings — unset fields keep their env/default values
configure(EngineSettingsOverride(
    node_type="mean",
    position_reference="geocentric",
))
```

Only the fields you set in `EngineSettingsOverride` are applied; everything else stays as loaded from the environment.

### Loading a `.env` file at runtime

```python
from pathlib import Path
from ndastro_engine.config import configure

configure(env_file=Path("/path/to/my.env"))
```

You can combine both:

```python
from ndastro_engine.config import configure, EngineSettingsOverride

configure(
    EngineSettingsOverride(node_type="true"),
    env_file=Path(".env.production"),
)
```

## EngineSettings Dataclass

`EngineSettings` is a plain `dataclass` — read the active settings at any time:

```python
from ndastro_engine.config import settings

print(settings.position_reference)  # "geocentric"
print(settings.node_type)           # "true"
print(settings.ayanamsa_delta)      # 0.0
```

---

## Per-Request Overrides

`configure()` changes the **global** settings singleton and affects every subsequent call on all threads. For web servers handling concurrent requests, use `override_settings()` instead — it applies a temporary override scoped to the current asyncio task (or OS thread) only, with zero effect on any other concurrent request.

### `override_settings()`

```python
from ndastro_engine.config import override_settings, EngineSettingsOverride

with override_settings(EngineSettingsOverride(node_type="mean")) as s:
    # Inside this block, get_effective_settings().node_type == "mean"
    # All other settings are inherited from the global settings.
    results = get_lunar_node_positions(dt)

# Outside the block, global settings are fully restored.
```

Fields not set in `EngineSettingsOverride` inherit from the currently active settings. Overrides can be nested:

```python
with override_settings(EngineSettingsOverride(position_reference="topocentric")):
    with override_settings(EngineSettingsOverride(node_type="mean")):
        # Both overrides are active here
        ...
    # node_type restored; position_reference still "topocentric"
```

### `get_effective_settings()`

Engine internals use `get_effective_settings()` as the single authoritative accessor. It returns the per-request override if one is active, otherwise the global `settings`:

```python
from ndastro_engine.config import get_effective_settings

s = get_effective_settings()
print(s.node_type)            # per-request override value, or global default
print(s.position_reference)  # same
```

You can call this in your own code if you need to read whichever settings are currently in effect without worrying about whether an override is active.

### Concurrency safety

`override_settings()` stores the override in a [`contextvars.ContextVar`](https://docs.python.org/3/library/contextvars.html), which is automatically scoped to the current asyncio task. Two concurrent FastAPI requests each get their own isolated context — neither can observe the other's override.

!!! warning "Don't use `configure()` per-request"
    `configure()` mutates the global `settings` module attribute. Calling it inside a request handler in a concurrent server will race with every other in-flight request. Use `override_settings()` for request-scoped changes.

### Performance

| Path | Cost |
|---|---|
| `get_effective_settings()` (no override active) | ~90 ns — one `ContextVar.get()` |
| `override_settings()` with values | ~4.6 µs — one `dataclasses.replace()` + ContextVar set/reset |
| `override_settings()` with no changed fields | ~1.5 µs — fast path, skips object allocation |

These costs are negligible compared to the 5–50 ms Skyfield ephemeris lookups they wrap.

## EngineSettingsOverride Dataclass

All fields are `None` by default. Set only the fields you want to change:

```python
from ndastro_engine.config import EngineSettingsOverride

# Only change node type; everything else stays unchanged
override = EngineSettingsOverride(node_type="mean")
```

## Position Reference

`geocentric` (default) measures planet positions from the centre of the Earth. `topocentric` corrects for the observer's actual location on the Earth's surface — the difference is most significant for the Moon (~1°).

```python
from ndastro_engine.config import configure, EngineSettingsOverride

# Geocentric (default)
configure(EngineSettingsOverride(position_reference="geocentric"))

# Topocentric (observer on Earth's surface)
configure(EngineSettingsOverride(position_reference="topocentric"))
```

## Lunar Node Type

`true` (default) uses the osculating (instantaneous) node — what JHora and most modern software use. `mean` uses the smoothed IAU 2006 polynomial (Meeus Ch. 22), which matches software such as AstroSage.

True and mean nodes can differ by up to ~1.5°.

```python
from ndastro_engine.config import configure, EngineSettingsOverride

# True (osculating) nodes — matches JHora
configure(EngineSettingsOverride(node_type="true"))

# Mean nodes — matches AstroSage and older software
configure(EngineSettingsOverride(node_type="mean"))
```

## Ayanamsa Delta

Apply a personal correction on top of the selected ayanamsa system:

```python
from ndastro_engine.config import configure, EngineSettingsOverride

# Add 0.25° correction to every ayanamsa result
configure(EngineSettingsOverride(ayanamsa_delta=0.25))
```

## Sunrise Definition

`geometric` (default) uses the geometric centre of the Sun crossing the horizon. `disc_centre` is an alias for the same centre-of-disc calculation. Future versions may add a `upper_limb` option.

```python
from ndastro_engine.config import configure, EngineSettingsOverride

configure(EngineSettingsOverride(sunrise_definition="disc_centre"))
```

## Integration with ndastro-api

When using ndastro-api, `configure()` is called from the FastAPI lifespan using the API's own `.env` file:

```python
# ndastro_api/main.py (simplified)
from ndastro_engine.config import configure
from ndastro_api.core.config import env_path

configure(env_file=env_path)
```

All `NDASTRO_*` variables in the API's `.env` are forwarded to the engine automatically.

## See Also

- [Planet Positions](planets.md)
- [Ayanamsa Calculations](ayanamsa.md)
- [API Reference: Config](../api/core.md)
