"""Constants for ndastro engine.

This module defines constant values used throughout the ndastro_engine package.
"""

OS_WIN = "win32"
OS_MAC = "darwin"
OS_LINUX = "linux"

DEGREE_MAX = 360.0

DEGREE_PER_NAKSHATRA = 13.333333333333334
DEGREE_PER_PADA = 3.3333333333333335
DEGREE_PER_RASI = 30.0

# Lahiri Ayanamsa constants (referenced to J2000.0)
AYANAMSA_AT_J2000 = 22.460148  # Ayanamsa value at J2000.0 epoch
DEG_PER_JCENTURY = 1.396042  # Linear term (degrees per Julian century)
DEG_PER_SQUARE_JCENTURY = 0.000308  # Quadratic term (degrees per square Julian century)

CENTURY_19 = 1900
CENTURY_20 = 2000
CENTURY_21 = 2100

DAYS_IN_YEAR = 365.25
AVERAGE_DAYS_IN_MONTH = DAYS_IN_YEAR / 12
ONE_GHATI = 24 / 60  # One Ghati is 24 minutes, which is 0.4 hours
DAYS_IN_CENTURY = DAYS_IN_YEAR * 100
