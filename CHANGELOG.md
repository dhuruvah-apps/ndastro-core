# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.1] - 2026-01-18

### Added

### Changed
- Enums package `__init__.py` for cleaner imports
- **Breaking**:
- Simplified imports: Use `from ndastro_engine.enums import Planets` instead of `from ndastro_engine.enums.planet_enum import Planets`




## [0.7.0] - 2026-01-14

### Added
- `PlanetPosition` named tuple to represent planet positions with velocity components
- Speed attributes for planetary motion: `speed_latitude`, `speed_longitude`, and `speed_distance`
- Tests for speed attributes and planetary motion rates
- Comprehensive test suite with 65+ unit tests achieving 96.80% code coverage

### Changed
- **Breaking**: `get_planet_position()` now returns `PlanetPosition` named tuple instead of plain tuple
- **Breaking**: `get_planets_position()` now returns `dict[Planets, PlanetPosition]` instead of tuples
- **Breaking**: Removed `ayanamsa` parameter from `get_planet_position()` and `get_planets_position()` - use separate ayanamsa calculation functions instead
- **Breaking**: `is_planet_in_retrograde()` now accepts float `latitude` and `longitude` instead of Skyfield `Angle` objects
- Simplified imports: Use `from ndastro_engine.enums import Planets` instead of `from ndastro_engine.enums.planet_enum import Planets`
- Updated `get_lunar_node_positions()` to use `ts.from_datetime()` for better datetime handling
- Improved workflow conditions for `create-tag` job (PR merge or manual dispatch)
- Enhanced frame calculation using `ecliptic_frame` for consistency

### Fixed
- Corrected attribute access in all tests to use named tuple attributes
- Fixed edge case handling for polar coordinates and international dateline
- Fixed speed rate calculations to properly cast Rate objects to float using `.per_day`

## [0.5.0] - 2026-01-11

### Added
- `is_planet_in_retrograde()` function to get the tuple `(bool, start_date, end_date)` for planet retrograde
- Complete MkDocs Material documentation site with GitHub Pages deployment
- Comprehensive user guides for ayanamsa, planet positions, sunrise/sunset, and retrograde periods
- Auto-generated API reference documentation with mkdocstrings
- GitHub Actions workflow for automated documentation deployment
- Documentation dependency group in pyproject.toml

## [0.4.1] - 2026-01-09

### Changed
- **Internal**: Refactored B6 calculation method using new reference epoch
- Updated all ayanamsa formulas to use quadratic equation: `c0 + c1*b6 + c2*b6²`
- Adjusted all test expected values to match new B6 calculation methodology

## [0.4.0] - 2026-01-09

### Added
- 16 ayanamsa calculation functions (Lahiri, Raman, KP New/Old, Fagan-Bradley, and 11 others)
- 31 unit tests for ayanamsa calculations

### Fixed
- Corrected all ayanamsa constants to match astro-seek.com reference values
- Fixed J2000 epoch baseline (was using 1900)
- Fixed B6 calculation to use J2000.0 epoch reference

## [0.3.2] - 2026-01-06

### Changed
- Refactored planet position functions for better code organization

## [0.3.1] - 2026-01-06

### Added
- Comprehensive test coverage with pytest-cov and pytest-xdist
- 47 unit tests for core functionality
- GitHub Actions CI/CD workflow
- Test runner scripts (PowerShell, batch, Makefile)

### Fixed
- **Critical**: Fixed Kethu longitude calculation (was using Rahu's latitude)

## [0.3.0] - 2026-01-06

### Added
- `get_planet_position` function for planetary position calculations
- Ayanamsa parameter support for sidereal astronomy
- Four enum modules (Planet, House, Nakshatra, Rasi)

## [0.2.1] - 2026-01-06

### Changed
- Simplified `get_sunrise_sunset` API to use float coordinates

## [0.2.0] - 2026-01-05

### Added
- Initial public release on PyPI
- Sunrise/sunset calculations
- WGS84 coordinate support
- Automatic JPL ephemeris management (DE441)

---

[0.5.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.5.0
[0.4.1]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.4.1
[0.4.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.4.0
[0.3.2]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.3.2
[0.3.1]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.3.1
[0.3.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.3.0
[0.2.1]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.2.1
[0.2.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.2.0

## v0.8.0 (2026-01-18)

### Refactor

- **enums**: Changed the way you import enums

## v0.7.0 (2026-01-14)

### Refactor

- **core.py**: Now methods which returns positions will return in tropical only positions

## v0.6.0 (2026-01-13)

### Refactor

- **core.py**: renamed the get_all_planet_positions to get_planets_position with new args planets

## v0.5.0 (2026-01-11)

## v0.4.1 (2026-01-09)
