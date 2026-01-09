# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.4.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.4.0
[0.3.2]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.3.2
[0.3.1]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.3.1
[0.3.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.3.0
[0.2.1]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.2.1
[0.2.0]: https://github.com/jaganathanb/ndastro-core/releases/tag/v0.2.0
