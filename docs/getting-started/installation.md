# Installation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Install from PyPI

The easiest way to install ndastro-engine is from PyPI:

```bash
pip install ndastro-engine
```

## Install for Development

If you want to contribute or modify the package:

1. Clone the repository:
```bash
git clone https://github.com/jaganathanb/ndastro-core.git
cd ndastro-core
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Verify Installation

To verify the installation works correctly:

```python
import ndastro_engine
from datetime import datetime
from ndastro_engine.ayanamsa import get_lahiri_ayanamsa

# Calculate ayanamsa
date = datetime(2026, 1, 11, 12, 0, 0)
ayanamsa = get_lahiri_ayanamsa(date)
print(f"Lahiri Ayanamsa: {ayanamsa:.6f}°")
```

If this runs without errors, you're all set!

## Dependencies

The package automatically installs these dependencies:

- **skyfield** (>= 1.53): For astronomical calculations
- **pytz** (>= 2025.2): For timezone handling

## Optional Development Dependencies

For development, these additional packages are included:

- **pytest**: Testing framework
- **pytest-cov**: Code coverage
- **pytest-xdist**: Parallel test execution
- **ruff**: Linting and formatting
- **mypy**: Static type checking

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're using Python 3.10 or higher:

```bash
python --version
```

### Ephemeris Data

On first run, skyfield will automatically download JPL ephemeris data (~10MB). This is a one-time download and is cached locally.

### Virtual Environment Issues

If you have issues with virtual environments, try recreating it:

```bash
deactivate  # if already in a venv
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install ndastro-engine
```
