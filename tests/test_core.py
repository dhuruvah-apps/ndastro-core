"""Tests for astronomical calculations in ndastro engine."""

from datetime import datetime
from unittest.mock import patch

import pytest
import pytz

from ndastro_engine.core import (
    get_ascendent_position,
    get_planet_position,
    get_planets_position,
    get_sunrise_sunset,
)
from ndastro_engine.enums import Planets
from ndastro_engine.models import PlanetPosition
from ndastro_engine.retrograde import is_planet_in_retrograde


@pytest.fixture(autouse=True)
def mock_elevation_lookup() -> None:
    """Avoid external elevation API calls in core tests."""
    with patch("ndastro_engine.core.get_elevation_by_latlon", return_value=914.0):
        yield


class TestGetPlanetPosition:
    """Test suite for get_planet_position function."""

    @pytest.mark.unit
    def test_get_planet_position_returns_planet_position(self):
        """Test that get_planet_position returns a PlanetPosition dataclass."""
        result = get_planet_position(planet=Planets.SUN, lat=40.7128, lon=-74.0060, given_time=datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC))

        assert isinstance(result, PlanetPosition)
        assert isinstance(result.latitude, float)
        assert isinstance(result.longitude, float)
        assert isinstance(result.distance, float)
        assert isinstance(result.speed_latitude, float)
        assert isinstance(result.speed_longitude, float)
        assert isinstance(result.speed_distance, float)

    @pytest.mark.unit
    def test_get_planet_position_latitude_range(self):
        """Test that latitude is within valid range (-90 to 90 degrees)."""
        result = get_planet_position(planet=Planets.JUPITER, lat=-33.8688, lon=151.2093, given_time=datetime(2024, 3, 20, 6, 0, 0, tzinfo=pytz.UTC))

        assert -90 <= result.latitude <= 90

    @pytest.mark.unit
    def test_get_planet_position_distance_positive(self):
        """Test that distance is always positive."""
        result = get_planet_position(planet=Planets.VENUS, lat=35.6762, lon=139.6503, given_time=datetime(2024, 12, 25, 18, 0, 0, tzinfo=pytz.UTC))

        assert result.distance > 0

    @pytest.mark.unit
    def test_get_planet_position_different_planets(self):
        """Test that different planets return different positions."""
        time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        lat, lon = 0.0, 0.0

        sun_pos = get_planet_position(Planets.SUN, lat, lon, time)
        moon_pos = get_planet_position(Planets.MOON, lat, lon, time)

        assert sun_pos != moon_pos

    @pytest.mark.unit
    def test_get_planet_position_different_times(self):
        """Test that same planet at different times returns different positions."""
        lat, lon = 40.7128, -74.0060

        pos1 = get_planet_position(Planets.MERCURY, lat, lon, datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC))
        pos2 = get_planet_position(Planets.MERCURY, lat, lon, datetime(2024, 6, 1, 0, 0, 0, tzinfo=pytz.UTC))

        assert pos1 != pos2

    @pytest.mark.unit
    def test_get_planet_position_different_locations(self):
        """Test that same planet from different locations may return different positions."""
        time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        pos1 = get_planet_position(Planets.SATURN, 40.7128, -74.0060, time)
        pos2 = get_planet_position(Planets.SATURN, -33.8688, 151.2093, time)

        # Positions may differ slightly due to parallax
        assert isinstance(pos1, PlanetPosition)
        assert isinstance(pos2, PlanetPosition)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("planet", "longitude", "latitude", "distance", "speed_latitude", "speed_longitude", "speed_distance"),
        [
            (
                Planets.SUN,
                279.8051877358686,
                0.0006220123496504032,
                0.9833628050249553,
                -0.000554830285817659,
                1.0340674080547134,
                9.214610959975152e-06,
            )
        ],
    )
    def test_get_planet_position_all_planets(  # noqa: PLR0913
        self,
        planet: Planets,
        longitude: float,
        latitude: float,
        distance: float,
        speed_latitude: float,
        speed_longitude: float,
        speed_distance: float,
    ) -> None:
        """Test that function works for all major planets."""
        result = get_planet_position(planet=planet, lat=12.97, lon=77.59, given_time=datetime(2023, 12, 31, 18, 30, 0, tzinfo=pytz.UTC))

        assert result.latitude == latitude
        assert result.longitude == longitude
        assert result.distance == distance
        assert result.speed_latitude == speed_latitude
        assert result.speed_longitude == speed_longitude
        assert result.speed_distance == speed_distance

    @pytest.mark.unit
    def test_get_planet_position_has_speed_attributes(self) -> None:
        """Test that PlanetPosition includes speed attributes."""
        result = get_planet_position(planet=Planets.MARS, lat=12.97, lon=77.59, given_time=datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC))

        # Speed attributes should exist and be floats
        assert isinstance(result.speed_latitude, float)
        assert isinstance(result.speed_longitude, float)
        assert isinstance(result.speed_distance, float)

    @pytest.mark.unit
    def test_get_planet_position_speed_longitude_indicates_motion(self) -> None:
        """Test that speed longitude indicates planet's motion."""
        result = get_planet_position(planet=Planets.MERCURY, lat=0.0, lon=0.0, given_time=datetime(2024, 6, 1, 0, 0, 0, tzinfo=pytz.UTC))

        # SpeedLongitude should be non-zero for most planets (they're moving)
        # Note: This tests the attribute exists and has a value
        assert isinstance(result.speed_longitude, float)


class TestGetSunriseSunset:
    """Test cases for get_sunrise_sunset function."""

    @pytest.mark.unit
    def test_get_sunrise_sunset_basic(self) -> None:
        """Test basic sunrise/sunset calculation."""
        # Setup test data
        lat = 12.97
        lon = 77.59
        test_date = datetime(2026, 1, 5, 10, 0, 0, tzinfo=pytz.timezone("UTC"))

        # Execute function
        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date)

        # Assertions
        assert sunrise.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S") == "06:43:09"
        assert sunset.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S") == "18:06:46"

    @pytest.mark.unit
    def test_get_sunrise_sunset_returns_datetime(self) -> None:
        """Test that sunrise and sunset are datetime objects."""
        lat = 40.7128
        lon = -74.0060
        test_date = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date)

        assert isinstance(sunrise, datetime)
        assert isinstance(sunset, datetime)

    @pytest.mark.unit
    def test_get_sunrise_sunset_order(self) -> None:
        """Test that sunrise occurs before sunset."""
        lat = 51.5074
        lon = -0.1278
        test_date = datetime(2026, 6, 21, 0, 0, 0, tzinfo=pytz.UTC)  # Summer solstice

        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date)

        assert sunrise < sunset

    @pytest.mark.unit
    def test_get_sunrise_sunset_with_elevation(self) -> None:
        """Test sunrise/sunset calculation with custom elevation."""
        lat = 35.6762
        lon = 139.6503
        test_date = datetime(2026, 3, 20, 0, 0, 0, tzinfo=pytz.UTC)

        sunrise1, sunset1 = get_sunrise_sunset(lat, lon, test_date, elevation=0)
        sunrise2, sunset2 = get_sunrise_sunset(lat, lon, test_date, elevation=1000)

        # Higher elevation should have slightly different times
        assert isinstance(sunrise1, datetime)
        assert isinstance(sunrise2, datetime)
        # Times should be close but not identical
        assert abs((sunrise1 - sunrise2).total_seconds()) < 300  # Within 5 minutes


class TestGetAllPlanetPositions:
    """Test cases for get_all_planet_positions function."""

    @pytest.mark.unit
    def test_get_all_planet_positions_returns_dict(self) -> None:
        """Test that function returns a dictionary."""
        lat = 12.97166667
        lon = 77.59361111
        test_time = datetime(2026, 1, 12, 18, 30, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        assert isinstance(result, dict)
        assert len(result) == 11

        assert result[Planets.ASCENDANT].longitude == 197.13930724837974
        assert result[Planets.SUN].longitude == 292.5613192065848
        assert result[Planets.MOON].longitude == 226.43748381648348
        assert result[Planets.MARS].longitude == 291.75343198140524
        assert result[Planets.MERCURY].longitude == 287.03848290381467
        assert result[Planets.JUPITER].longitude == 109.78310583323993
        assert result[Planets.VENUS].longitude == 294.014258990699
        assert result[Planets.SATURN].longitude == 356.9562483752751
        assert result[Planets.RAHU].longitude == 339.88525356186483
        assert result[Planets.KETHU].longitude == 159.88525356186483

    @pytest.mark.unit
    def test_get_all_planet_positions_contains_major_planets(self) -> None:
        """Test that result contains all major planets."""
        lat = 40.7128
        lon = -74.0060
        test_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        expected_planets = [
            Planets.SUN,
            Planets.MOON,
            Planets.MARS,
            Planets.MERCURY,
            Planets.JUPITER,
            Planets.VENUS,
            Planets.SATURN,
            Planets.RAHU,
            Planets.KETHU,
            Planets.ASCENDANT,
        ]

        for planet in expected_planets:
            assert planet in result

    @pytest.mark.unit
    def test_get_all_planet_positions_values_are_planet_positions(self) -> None:
        """Test that all values are PlanetPosition dataclass instances."""
        lat = 19.0760
        lon = 72.8777
        test_time = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        for planet, position in result.items():
            assert isinstance(position, PlanetPosition)
            assert isinstance(position.latitude, float)
            assert isinstance(position.longitude, float)
            assert isinstance(position.distance, float)
            assert isinstance(position.speed_latitude, float)
            assert isinstance(position.speed_longitude, float)
            assert isinstance(position.speed_distance, float)

    @pytest.mark.unit
    def test_get_all_planet_positions_rahu_kethu_opposite(self) -> None:
        """Test that Rahu and Kethu are 180 degrees apart."""
        lat = 0.0
        lon = 0.0
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        rahu_lon = result[Planets.RAHU].longitude
        kethu_lon = result[Planets.KETHU].longitude

        # Calculate angular difference
        diff = abs(rahu_lon - kethu_lon)
        # Account for wrap-around at 360 degrees
        if diff > 180:
            diff = 360 - diff

        assert abs(diff - 180) < 0.01, f"Rahu at {rahu_lon}, Kethu at {kethu_lon}"

    @pytest.mark.unit
    def test_get_all_planet_positions_ascendant_included(self) -> None:
        """Test that ascendant is included in positions."""
        lat = 51.5074
        lon = -0.1278
        test_time = datetime(2026, 1, 5, 12, 0, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        assert Planets.ASCENDANT in result
        asc_pos = result[Planets.ASCENDANT]
        assert asc_pos.latitude == 0.0  # Ascendant latitude should be 0
        assert 0 <= asc_pos.longitude <= 360  # Longitude should be in valid range
        assert asc_pos.distance == 0.0  # Ascendant distance should be 0

    @pytest.mark.unit
    def test_get_all_planet_positions_lunar_nodes_zero_latitude(self) -> None:
        """Test that Rahu and Kethu have zero latitude."""
        lat = 35.6762
        lon = 139.6503
        test_time = datetime(2026, 3, 20, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        assert result[Planets.RAHU].latitude == 0.0
        assert result[Planets.KETHU].latitude == 0.0
        assert result[Planets.RAHU].distance == 0.0
        assert result[Planets.KETHU].distance == 0.0


class TestPlanetPositionEdgeCases:
    """Test edge cases and boundary conditions for planet calculations."""

    @pytest.mark.unit
    def test_planet_position_at_poles(self) -> None:
        """Test planet position calculation at polar latitudes."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        # North pole
        north_pos = get_planet_position(Planets.SUN, 90.0, 0.0, test_time)
        assert isinstance(north_pos, PlanetPosition)

        # South pole
        south_pos = get_planet_position(Planets.SUN, -90.0, 0.0, test_time)
        assert isinstance(south_pos, PlanetPosition)

    @pytest.mark.unit
    def test_planet_position_at_dateline(self) -> None:
        """Test planet position at international date line."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        pos1 = get_planet_position(Planets.MOON, 0.0, 180.0, test_time)
        pos2 = get_planet_position(Planets.MOON, 0.0, -180.0, test_time)

        # Positions should be very similar (same point on Earth)
        assert abs(pos1.longitude - pos2.longitude) < 0.01

    @pytest.mark.unit
    @pytest.mark.parametrize("planet", [Planets.SUN, Planets.MOON, Planets.MARS, Planets.MERCURY, Planets.JUPITER, Planets.VENUS, Planets.SATURN])
    def test_all_major_planets_valid_positions(self, planet: Planets) -> None:
        """Test that all major planets return valid positions."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_planet_position(planet, 0.0, 0.0, test_time)

        assert -90 <= result.latitude <= 90, f"{planet.name} latitude out of range"
        assert 0 <= result.longitude <= 360, f"{planet.name} longitude out of range"
        assert result.distance > 0, f"{planet.name} distance should be positive"

    @pytest.mark.unit
    def test_sunrise_sunset_different_dates(self) -> None:
        """Test that sunrise/sunset times vary across seasons."""
        lat = 51.5074
        lon = -0.1278

        # Winter solstice
        winter = datetime(2025, 12, 21, 0, 0, 0, tzinfo=pytz.UTC)
        sunrise_winter, sunset_winter = get_sunrise_sunset(lat, lon, winter)

        # Summer solstice
        summer = datetime(2026, 6, 21, 0, 0, 0, tzinfo=pytz.UTC)
        sunrise_summer, sunset_summer = get_sunrise_sunset(lat, lon, summer)

        # Calculate day lengths
        winter_day_length = (sunset_winter - sunrise_winter).total_seconds()
        summer_day_length = (sunset_summer - sunrise_summer).total_seconds()

        # Summer days should be longer at this latitude
        assert summer_day_length > winter_day_length


class TestIsPlanetInRetrograde:
    """Test cases for is_planet_in_retrograde function."""

    @pytest.mark.unit
    def test_mercury_in_retrograde_positive(self) -> None:
        """Test Mercury is in retrograde during a known retrograde period."""
        # Mercury retrograde: December 13, 2023 - January 1, 2024 (known period)
        check_date = datetime(2023, 12, 20, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = 12.97  # Bengaluru
        longitude = 77.59

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.MERCURY.astronomical_code, latitude, longitude)

        assert is_retrograde is True
        assert start_date is not None
        assert end_date is not None
        assert start_date <= check_date <= end_date

    @pytest.mark.unit
    def test_mercury_not_in_retrograde_negative(self) -> None:
        """Test Mercury is not in retrograde during a known direct motion period."""
        # Mercury direct motion period (between retrogrades)
        check_date = datetime(2024, 2, 15, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = 28.6139  # New Delhi
        longitude = 77.2090

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.MERCURY.astronomical_code, latitude, longitude)

        assert is_retrograde is False
        assert start_date is None
        assert end_date is None

    @pytest.mark.unit
    def test_sun_never_retrograde(self) -> None:
        """Test that Sun is never in retrograde."""
        check_date = datetime(2024, 6, 15, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = 28.6139
        longitude = 77.2090

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.SUN.astronomical_code, latitude, longitude)

        assert is_retrograde is False
        assert start_date is None
        assert end_date is None

    @pytest.mark.unit
    def test_moon_never_retrograde(self) -> None:
        """Test that Moon is never in retrograde."""
        check_date = datetime(2024, 6, 15, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = 28.6139
        longitude = 77.2090

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.MOON.astronomical_code, latitude, longitude)

        assert is_retrograde is False
        assert start_date is None
        assert end_date is None


class TestGetAscendentPosition:
    """Test cases for get_ascendent_position function."""

    @pytest.mark.unit
    def test_get_ascendent_position_returns_float(self) -> None:
        """Test that get_ascendent_position returns a float."""
        lat = 12.97
        lon = 77.59
        test_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        result = get_ascendent_position(lat, lon, test_time)

        assert isinstance(result, float)
        assert 0 <= result <= 360

    @pytest.mark.unit
    def test_get_ascendent_position_different_times(self) -> None:
        """Test that ascendant changes with time."""
        lat = 40.7128
        lon = -74.0060

        time1 = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        time2 = datetime(2024, 1, 1, 6, 0, 0, tzinfo=pytz.UTC)

        asc1 = get_ascendent_position(lat, lon, time1)
        asc2 = get_ascendent_position(lat, lon, time2)

        # Ascendant should change significantly in 6 hours
        assert asc1 != asc2

    @pytest.mark.unit
    def test_get_ascendent_position_different_locations(self) -> None:
        """Test that ascendant differs based on location."""
        test_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        asc1 = get_ascendent_position(12.97, 77.59, test_time)  # Bengaluru
        asc2 = get_ascendent_position(40.7128, -74.0060, test_time)  # New York

        # Different locations at same time should have different ascendants
        assert asc1 != asc2

    @pytest.mark.unit
    def test_get_ascendent_position_at_poles(self) -> None:
        """Test ascendant calculation at polar latitudes."""
        test_time = datetime(2024, 6, 21, 12, 0, 0, tzinfo=pytz.UTC)

        # North pole
        asc_north = get_ascendent_position(90.0, 0.0, test_time)
        assert isinstance(asc_north, float)
        assert 0 <= asc_north <= 360

        # South pole
        asc_south = get_ascendent_position(-90.0, 0.0, test_time)
        assert isinstance(asc_south, float)
        assert 0 <= asc_south <= 360


class TestGetPlanetsPositionWithSpecificList:
    """Test cases for get_planets_position with specific planet lists."""

    @pytest.mark.unit
    def test_get_planets_position_with_specific_planets(self) -> None:
        """Test that function returns only requested planets."""
        lat = 12.97
        lon = 77.59
        test_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        planets = [Planets.SUN, Planets.MOON, Planets.MARS]

        result = get_planets_position(planets, lat, lon, test_time)

        assert len(result) == 3
        assert Planets.SUN in result
        assert Planets.MOON in result
        assert Planets.MARS in result
        assert Planets.JUPITER not in result
        assert Planets.VENUS not in result

    @pytest.mark.unit
    def test_get_planets_position_single_planet(self) -> None:
        """Test that function works with a single planet."""
        lat = 40.7128
        lon = -74.0060
        test_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        planets = [Planets.JUPITER]

        result = get_planets_position(planets, lat, lon, test_time)

        assert len(result) == 1
        assert Planets.JUPITER in result

    @pytest.mark.unit
    def test_get_planets_position_with_lunar_nodes(self) -> None:
        """Test that function correctly handles Rahu and Kethu in planet list."""
        lat = 19.0760
        lon = 72.8777
        test_time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        planets = [Planets.RAHU, Planets.KETHU]

        result = get_planets_position(planets, lat, lon, test_time)

        assert len(result) == 2
        assert Planets.RAHU in result
        assert Planets.KETHU in result

        # Verify they are 180 degrees apart
        rahu_lon = result[Planets.RAHU].longitude
        kethu_lon = result[Planets.KETHU].longitude
        diff = abs(rahu_lon - kethu_lon)
        if diff > 180:
            diff = 360 - diff
        assert abs(diff - 180) < 0.01

    @pytest.mark.unit
    def test_get_planets_position_with_ascendant_only(self) -> None:
        """Test that function works with only ascendant."""
        lat = 51.5074
        lon = -0.1278
        test_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        planets = [Planets.ASCENDANT]

        result = get_planets_position(planets, lat, lon, test_time)

        assert len(result) == 1
        assert Planets.ASCENDANT in result
        assert result[Planets.ASCENDANT].latitude == 0.0  # latitude
        assert result[Planets.ASCENDANT].distance == 0.0  # distance

    @pytest.mark.unit
    def test_get_planets_position_empty_list_returns_all(self) -> None:
        """Test that empty list returns all planets."""
        lat = 12.97
        lon = 77.59
        test_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        result = get_planets_position([], lat, lon, test_time)

        # Should contain all enum members
        assert len(result) == len(Planets)


class TestGetSunriseSunsetElevation:
    """Test cases for get_sunrise_sunset with various elevations."""

    @pytest.mark.unit
    def test_sunrise_sunset_sea_level(self) -> None:
        """Test sunrise/sunset calculation at sea level."""
        lat = 19.0760  # Mumbai (coastal)
        lon = 72.8777
        test_date = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date, elevation=0)

        assert isinstance(sunrise, datetime)
        assert isinstance(sunset, datetime)
        assert sunrise < sunset

    @pytest.mark.unit
    def test_sunrise_sunset_high_elevation(self) -> None:
        """Test sunrise/sunset at high elevation (mountain)."""
        lat = 27.9881  # Mount Everest base camp area
        lon = 86.9250
        test_date = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        sunrise_low = get_sunrise_sunset(lat, lon, test_date, elevation=100)[0]
        sunrise_high = get_sunrise_sunset(lat, lon, test_date, elevation=5000)[0]

        # Higher elevation typically sees sunrise earlier
        time_diff = abs((sunrise_high - sunrise_low).total_seconds())
        assert time_diff > 0  # There should be a difference

    @pytest.mark.unit
    def test_sunrise_sunset_negative_elevation(self) -> None:
        """Test sunrise/sunset below sea level."""
        lat = 31.5  # Dead Sea area (below sea level)
        lon = 35.5
        test_date = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date, elevation=-400)

        assert isinstance(sunrise, datetime)
        assert isinstance(sunset, datetime)
        assert sunrise < sunset

    @pytest.mark.unit
    def test_sunrise_sunset_elevation_effect_on_day_length(self) -> None:
        """Test that elevation affects day length."""
        lat = 35.6762  # Tokyo
        lon = 139.6503
        test_date = datetime(2026, 6, 21, 0, 0, 0, tzinfo=pytz.UTC)  # Summer solstice

        sunrise_sea, sunset_sea = get_sunrise_sunset(lat, lon, test_date, elevation=0)
        sunrise_mountain, sunset_mountain = get_sunrise_sunset(lat, lon, test_date, elevation=3000)

        day_length_sea = (sunset_sea - sunrise_sea).total_seconds()
        day_length_mountain = (sunset_mountain - sunrise_mountain).total_seconds()

        # Day length should differ with elevation
        assert day_length_sea != day_length_mountain

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("elevation", "expected_valid"),
        [
            (0, True),  # Sea level
            (914, True),  # Default elevation
            (5000, True),  # High mountain
            (8848, True),  # Mount Everest height
            (-400, True),  # Below sea level (Dead Sea)
        ],
    )
    def test_sunrise_sunset_various_elevations(self, elevation: float, expected_valid: bool) -> None:
        """Test sunrise/sunset calculation at various elevations."""
        lat = 40.7128
        lon = -74.0060
        test_date = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        sunrise, sunset = get_sunrise_sunset(lat, lon, test_date, elevation=elevation)

        if expected_valid:
            assert isinstance(sunrise, datetime)
            assert isinstance(sunset, datetime)
            assert sunrise < sunset
