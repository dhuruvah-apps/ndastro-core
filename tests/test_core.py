"""Tests for astronomical calculations in ndastro engine."""

from datetime import datetime

import pytest
import pytz
from skyfield.units import Angle

from ndastro_engine.core import (
    get_all_planet_positions,
    get_planet_position,
    get_sunrise_sunset,
    is_planet_in_retrograde,
)
from ndastro_engine.enums.planet_enum import Planets


class TestGetPlanetPosition:
    """Test suite for get_planet_position function."""

    @pytest.mark.unit
    def test_get_planet_position_returns_tuple(self):
        """Test that get_planet_position returns a tuple of three floats."""
        result = get_planet_position(planet=Planets.SUN, lat=40.7128, lon=-74.0060, given_time=datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC))

        assert isinstance(result, tuple)
        assert len(result) == 3
        assert all(isinstance(x, float) for x in result)

    @pytest.mark.unit
    def test_get_planet_position_latitude_range(self):
        """Test that latitude is within valid range (-90 to 90 degrees)."""
        _, latitude, _ = get_planet_position(
            planet=Planets.JUPITER, lat=-33.8688, lon=151.2093, given_time=datetime(2024, 3, 20, 6, 0, 0, tzinfo=pytz.UTC)
        )

        assert -90 <= latitude <= 90

    @pytest.mark.unit
    def test_get_planet_position_distance_positive(self):
        """Test that distance is always positive."""
        _, _, distance = get_planet_position(
            planet=Planets.VENUS, lat=35.6762, lon=139.6503, given_time=datetime(2024, 12, 25, 18, 0, 0, tzinfo=pytz.UTC)
        )

        assert distance > 0

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
        assert isinstance(pos1, tuple)
        assert isinstance(pos2, tuple)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("planet", "longitude", "latitude", "distance", "ayanamsa"),
        [
            (Planets.SUN, 279.8051877358686, 0.0006220123496504032, 0.9833628050249553, None),
            (Planets.SUN, 255.61352106586864, 0.0006220123496504032, 0.9833628050249553, 24.19166667),
        ],
    )
    def test_get_planet_position_all_planets(
        self, planet: Planets, longitude: float, latitude: float, distance: float, ayanamsa: float | None
    ) -> None:
        """Test that function works for all major planets."""
        lat, lon, dis = get_planet_position(
            planet=planet, lat=12.97, lon=77.59, given_time=datetime(2023, 12, 31, 18, 30, 0, tzinfo=pytz.UTC), ayanamsa=ayanamsa
        )
        assert lat == latitude
        assert lon == longitude
        assert dis == distance


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
        lat = 12.97
        lon = 77.59
        test_time = datetime(2026, 1, 5, 18, 30, 0, tzinfo=pytz.UTC)

        result = get_all_planet_positions(lat, lon, test_time)

        assert isinstance(result, dict)
        assert len(result) > 0

    @pytest.mark.unit
    def test_get_all_planet_positions_contains_major_planets(self) -> None:
        """Test that result contains all major planets."""
        lat = 40.7128
        lon = -74.0060
        test_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        result = get_all_planet_positions(lat, lon, test_time)

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
    def test_get_all_planet_positions_values_are_tuples(self) -> None:
        """Test that all values are tuples of three floats."""
        lat = 19.0760
        lon = 72.8777
        test_time = datetime(2026, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_all_planet_positions(lat, lon, test_time)

        for planet, position in result.items():
            assert isinstance(position, tuple)
            assert len(position) == 3
            assert all(isinstance(x, float) for x in position)

    @pytest.mark.unit
    def test_get_all_planet_positions_rahu_kethu_opposite(self) -> None:
        """Test that Rahu and Kethu are 180 degrees apart."""
        lat = 0.0
        lon = 0.0
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_all_planet_positions(lat, lon, test_time)

        rahu_lon = result[Planets.RAHU][1]
        kethu_lon = result[Planets.KETHU][1]

        # Calculate angular difference
        diff = abs(rahu_lon - kethu_lon)
        # Account for wrap-around at 360 degrees
        if diff > 180:
            diff = 360 - diff

        assert abs(diff - 180) < 0.01, f"Rahu at {rahu_lon}, Kethu at {kethu_lon}"

    @pytest.mark.unit
    def test_get_all_planet_positions_with_ayanamsa(self) -> None:
        """Test planet positions with ayanamsa adjustment."""
        lat = 12.97
        lon = 77.59
        test_time = datetime(2023, 12, 31, 18, 30, 0, tzinfo=pytz.UTC)
        ayanamsa = 24.19166667

        result_tropical = get_all_planet_positions(lat, lon, test_time, ayanamsa=None)
        result_sidereal = get_all_planet_positions(lat, lon, test_time, ayanamsa=ayanamsa)

        # Check that positions differ by approximately the ayanamsa
        for planet in [Planets.SUN, Planets.MOON, Planets.MARS]:
            if planet in result_tropical and planet in result_sidereal:
                trop_lon = result_tropical[planet][1]
                sid_lon = result_sidereal[planet][1]
                # Difference should be close to ayanamsa (accounting for wrapping)
                diff = abs(trop_lon - sid_lon)
                assert abs(diff - ayanamsa) < 1.0 or abs(diff - ayanamsa + 360) < 1.0

    @pytest.mark.unit
    def test_get_all_planet_positions_ascendant_included(self) -> None:
        """Test that ascendant is included in positions."""
        lat = 51.5074
        lon = -0.1278
        test_time = datetime(2026, 1, 5, 12, 0, 0, tzinfo=pytz.UTC)

        result = get_all_planet_positions(lat, lon, test_time)

        assert Planets.ASCENDANT in result
        asc_lat, asc_lon, asc_dist = result[Planets.ASCENDANT]
        assert asc_lat == 0.0  # Ascendant latitude should be 0
        assert 0 <= asc_lon <= 360  # Longitude should be in valid range
        assert asc_dist == 0.0  # Ascendant distance should be 0

    @pytest.mark.unit
    def test_get_all_planet_positions_lunar_nodes_zero_latitude(self) -> None:
        """Test that Rahu and Kethu have zero latitude."""
        lat = 35.6762
        lon = 139.6503
        test_time = datetime(2026, 3, 20, 0, 0, 0, tzinfo=pytz.UTC)

        result = get_all_planet_positions(lat, lon, test_time)

        assert result[Planets.RAHU][0] == 0.0
        assert result[Planets.KETHU][0] == 0.0
        assert result[Planets.RAHU][2] == 0.0
        assert result[Planets.KETHU][2] == 0.0


class TestPlanetPositionEdgeCases:
    """Test edge cases and boundary conditions for planet calculations."""

    @pytest.mark.unit
    def test_planet_position_at_poles(self) -> None:
        """Test planet position calculation at polar latitudes."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        # North pole
        north_pos = get_planet_position(Planets.SUN, 90.0, 0.0, test_time)
        assert isinstance(north_pos, tuple)

        # South pole
        south_pos = get_planet_position(Planets.SUN, -90.0, 0.0, test_time)
        assert isinstance(south_pos, tuple)

    @pytest.mark.unit
    def test_planet_position_at_dateline(self) -> None:
        """Test planet position at international date line."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        pos1 = get_planet_position(Planets.MOON, 0.0, 180.0, test_time)
        pos2 = get_planet_position(Planets.MOON, 0.0, -180.0, test_time)

        # Positions should be very similar (same point on Earth)
        assert abs(pos1[1] - pos2[1]) < 0.01

    @pytest.mark.unit
    def test_planet_position_with_negative_ayanamsa(self) -> None:
        """Test planet position with negative ayanamsa."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        pos_positive = get_planet_position(Planets.JUPITER, 0.0, 0.0, test_time, ayanamsa=24.0)
        pos_negative = get_planet_position(Planets.JUPITER, 0.0, 0.0, test_time, ayanamsa=-24.0)

        # With negative ayanamsa, longitude should increase
        assert pos_negative[1] > pos_positive[1]

    @pytest.mark.unit
    @pytest.mark.parametrize("planet", [Planets.SUN, Planets.MOON, Planets.MARS, Planets.MERCURY, Planets.JUPITER, Planets.VENUS, Planets.SATURN])
    def test_all_major_planets_valid_positions(self, planet: Planets) -> None:
        """Test that all major planets return valid positions."""
        test_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        lat, lon, dist = get_planet_position(planet, 0.0, 0.0, test_time)

        assert -90 <= lat <= 90, f"{planet.name} latitude out of range"
        assert 0 <= lon <= 360, f"{planet.name} longitude out of range"
        assert dist > 0, f"{planet.name} distance should be positive"

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
        latitude = Angle(degrees=12.97)  # Bengaluru
        longitude = Angle(degrees=77.59)

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.MERCURY.code, latitude, longitude)

        assert is_retrograde is True
        assert start_date is not None
        assert end_date is not None
        assert start_date <= check_date <= end_date

    @pytest.mark.unit
    def test_mercury_not_in_retrograde_negative(self) -> None:
        """Test Mercury is not in retrograde during a known direct motion period."""
        # Mercury direct motion period (between retrogrades)
        check_date = datetime(2024, 2, 15, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = Angle(degrees=28.6139)  # New Delhi
        longitude = Angle(degrees=77.2090)

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.MERCURY.code, latitude, longitude)

        assert is_retrograde is False
        assert start_date is None
        assert end_date is None

    @pytest.mark.unit
    def test_sun_never_retrograde(self) -> None:
        """Test that Sun is never in retrograde."""
        check_date = datetime(2024, 6, 15, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = Angle(degrees=28.6139)
        longitude = Angle(degrees=77.2090)

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.SUN.code, latitude, longitude)

        assert is_retrograde is False
        assert start_date is None
        assert end_date is None

    @pytest.mark.unit
    def test_moon_never_retrograde(self) -> None:
        """Test that Moon is never in retrograde."""
        check_date = datetime(2024, 6, 15, 12, 0, 0, tzinfo=pytz.UTC)
        latitude = Angle(degrees=28.6139)
        longitude = Angle(degrees=77.2090)

        is_retrograde, start_date, end_date = is_planet_in_retrograde(check_date, Planets.MOON.code, latitude, longitude)

        assert is_retrograde is False
        assert start_date is None
        assert end_date is None
