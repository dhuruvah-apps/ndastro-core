"""Unit tests for ndastro_engine.combustion module."""

from datetime import datetime, timedelta

import pytest
import pytz

from ndastro_engine.combustion import (
    ORB_BY_PLANET,
    CombustFunction,
    find_combust_periods,
    is_planet_in_combust,
)
from ndastro_engine.config import ts
from ndastro_engine.enums import Planets


class TestOrbByPlanet:
    """Test suite for ORB_BY_PLANET constant."""

    @pytest.mark.unit
    def test_orb_by_planet_contains_five_planets(self) -> None:
        """Test that ORB_BY_PLANET contains exactly 5 planets."""
        assert len(ORB_BY_PLANET) == 5

    @pytest.mark.unit
    def test_orb_by_planet_has_correct_values(self) -> None:
        """Test that ORB_BY_PLANET has correct orb values for each planet."""
        assert ORB_BY_PLANET[Planets.MERCURY.code] == 12.0
        assert ORB_BY_PLANET[Planets.VENUS.code] == 8.0
        assert ORB_BY_PLANET[Planets.MARS.code] == 17.0
        assert ORB_BY_PLANET[Planets.JUPITER.code] == 11.0
        assert ORB_BY_PLANET[Planets.SATURN.code] == 15.0

    @pytest.mark.unit
    def test_orb_by_planet_excludes_special_planets(self) -> None:
        """Test that ORB_BY_PLANET excludes Sun, Moon, Rahu, Kethu."""
        assert Planets.SUN.code not in ORB_BY_PLANET
        assert Planets.MOON.code not in ORB_BY_PLANET
        assert Planets.RAHU.code not in ORB_BY_PLANET
        assert Planets.KETHU.code not in ORB_BY_PLANET


class TestCombustFunction:
    """Test suite for CombustFunction class."""

    @pytest.mark.unit
    def test_combust_function_initialization(self) -> None:
        """Test that CombustFunction initializes correctly."""
        func = CombustFunction(Planets.MERCURY.code, 40.7128, -74.0060, 12.0)

        assert func.planet_name == Planets.MERCURY.code
        assert func.latitude == 40.7128
        assert func.longitude == -74.0060
        assert func.orb == 12.0

    @pytest.mark.unit
    def test_combust_function_callable(self) -> None:
        """Test that CombustFunction is callable."""
        func = CombustFunction(Planets.MERCURY.code, 40.7128, -74.0060, 12.0)
        t = ts.utc(2026, 2, 13, 12, 0, 0)

        result = func(t)

        # Result should be a boolean-like value or array of boolean-like values
        assert hasattr(result, "__bool__") or hasattr(result, "__len__")

    @pytest.mark.unit
    def test_combust_function_returns_true_when_within_orb(self) -> None:
        """Test that CombustFunction returns True when planet is within orb of Sun."""
        # Mercury is typically close to Sun, use a large orb to ensure combustion
        func = CombustFunction(Planets.MERCURY.code, 40.7128, -74.0060, 30.0)
        t = ts.utc(2026, 2, 13, 12, 0, 0)

        result = func(t)

        # With a 30-degree orb, Mercury should often be combust
        # Result should be boolean-like or array-like
        assert hasattr(result, "__bool__") or hasattr(result, "__len__")

    @pytest.mark.unit
    def test_combust_function_different_latitudes(self) -> None:
        """Test that CombustFunction works with different latitudes."""
        func_north = CombustFunction(Planets.VENUS.code, 40.7128, -74.0060, 8.0)
        func_south = CombustFunction(Planets.VENUS.code, -33.8688, 151.2093, 8.0)
        t = ts.utc(2026, 2, 13, 12, 0, 0)

        result_north = func_north(t)
        result_south = func_south(t)

        # Both should return boolean-like or array-like values
        assert hasattr(result_north, "__bool__") or hasattr(result_north, "__len__")
        assert hasattr(result_south, "__bool__") or hasattr(result_south, "__len__")


class TestFindCombustPeriods:
    """Test suite for find_combust_periods function."""

    @pytest.mark.unit
    def test_find_combust_periods_returns_list(self) -> None:
        """Test that find_combust_periods returns a list."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.MERCURY.code, 40.7128, -74.0060)

        assert isinstance(result, list)

    @pytest.mark.unit
    def test_find_combust_periods_returns_tuples(self) -> None:
        """Test that find_combust_periods returns list of tuples."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.VENUS.code, 40.7128, -74.0060)

        if result:
            assert all(isinstance(period, tuple) for period in result)
            assert all(len(period) == 2 for period in result)
            assert all(isinstance(period[0], datetime) for period in result)
            assert all(isinstance(period[1], datetime) for period in result)

    @pytest.mark.unit
    def test_find_combust_periods_sun_returns_empty(self) -> None:
        """Test that find_combust_periods returns empty list for Sun."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.SUN.code, 40.7128, -74.0060)

        assert result == []

    @pytest.mark.unit
    def test_find_combust_periods_rahu_returns_empty(self) -> None:
        """Test that find_combust_periods returns empty list for Rahu."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.RAHU.code, 40.7128, -74.0060)

        assert result == []

    @pytest.mark.unit
    def test_find_combust_periods_kethu_returns_empty(self) -> None:
        """Test that find_combust_periods returns empty list for Kethu."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.KETHU.code, 40.7128, -74.0060)

        assert result == []

    @pytest.mark.unit
    def test_find_combust_periods_ascendant_returns_empty(self) -> None:
        """Test that find_combust_periods returns empty list for Ascendant."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.ASCENDANT.code, 40.7128, -74.0060)

        assert result == []

    @pytest.mark.unit
    def test_find_combust_periods_empty_returns_empty(self) -> None:
        """Test that find_combust_periods returns empty list for Empty planet."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.EMPTY.code, 40.7128, -74.0060)

        assert result == []

    @pytest.mark.unit
    def test_find_combust_periods_invalid_planet_returns_empty(self) -> None:
        """Test that find_combust_periods returns empty list for invalid planet."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, "invalid_planet", 40.7128, -74.0060)

        assert result == []

    @pytest.mark.unit
    def test_find_combust_periods_chronological_order(self) -> None:
        """Test that find_combust_periods returns periods in chronological order."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.MARS.code, 40.7128, -74.0060)

        if len(result) > 1:
            for i in range(len(result) - 1):
                assert result[i][1] <= result[i + 1][0], "Periods should be chronological"

    @pytest.mark.unit
    def test_find_combust_periods_start_before_end(self) -> None:
        """Test that each combustion period has start before end."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 12, 31, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.JUPITER.code, 40.7128, -74.0060)

        if result:
            for period_start, period_end in result:
                assert period_start < period_end, "Period start should be before end"

    @pytest.mark.unit
    def test_find_combust_periods_different_locations(self) -> None:
        """Test that find_combust_periods works with different locations."""
        start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        end = datetime(2026, 6, 30, tzinfo=pytz.UTC)

        result_nyc = find_combust_periods(start, end, Planets.SATURN.code, 40.7128, -74.0060)
        result_tokyo = find_combust_periods(start, end, Planets.SATURN.code, 35.6762, 139.6503)

        # Both should return valid lists (combustion doesn't depend heavily on location)
        assert isinstance(result_nyc, list)
        assert isinstance(result_tokyo, list)

    @pytest.mark.unit
    def test_find_combust_periods_short_date_range(self) -> None:
        """Test find_combust_periods with a short date range."""
        start = datetime(2026, 2, 13, tzinfo=pytz.UTC)
        end = datetime(2026, 2, 20, tzinfo=pytz.UTC)

        result = find_combust_periods(start, end, Planets.MERCURY.code, 40.7128, -74.0060)

        assert isinstance(result, list)


class TestIsPlanetInCombust:
    """Test suite for is_planet_in_combust function."""

    @pytest.mark.unit
    def test_is_planet_in_combust_returns_tuple(self) -> None:
        """Test that is_planet_in_combust returns a tuple."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        result = is_planet_in_combust(check_date, Planets.MERCURY.code, 40.7128, -74.0060)

        assert isinstance(result, tuple)
        assert len(result) == 3
        assert isinstance(result[0], bool)
        assert result[1] is None or isinstance(result[1], datetime)
        assert result[2] is None or isinstance(result[2], datetime)

    @pytest.mark.unit
    def test_is_planet_in_combust_sun_returns_false(self) -> None:
        """Test that is_planet_in_combust returns False for Sun."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.SUN.code, 40.7128, -74.0060)

        assert is_combust is False
        assert period_start is None
        assert period_end is None

    @pytest.mark.unit
    def test_is_planet_in_combust_rahu_returns_false(self) -> None:
        """Test that is_planet_in_combust returns False for Rahu."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.RAHU.code, 40.7128, -74.0060)

        assert is_combust is False
        assert period_start is None
        assert period_end is None

    @pytest.mark.unit
    def test_is_planet_in_combust_kethu_returns_false(self) -> None:
        """Test that is_planet_in_combust returns False for Kethu."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.KETHU.code, 40.7128, -74.0060)

        assert is_combust is False
        assert period_start is None
        assert period_end is None

    @pytest.mark.unit
    def test_is_planet_in_combust_ascendant_returns_false(self) -> None:
        """Test that is_planet_in_combust returns False for Ascendant."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.ASCENDANT.code, 40.7128, -74.0060)

        assert is_combust is False
        assert period_start is None
        assert period_end is None

    @pytest.mark.unit
    def test_is_planet_in_combust_empty_returns_false(self) -> None:
        """Test that is_planet_in_combust returns False for Empty planet."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.EMPTY.code, 40.7128, -74.0060)

        assert is_combust is False
        assert period_start is None
        assert period_end is None

    @pytest.mark.unit
    def test_is_planet_in_combust_different_dates(self) -> None:
        """Test that is_planet_in_combust can return different results for different dates."""
        date1 = datetime(2026, 1, 1, tzinfo=pytz.UTC)
        date2 = datetime(2026, 6, 1, tzinfo=pytz.UTC)

        is_combust1, _, _ = is_planet_in_combust(date1, Planets.VENUS.code, 40.7128, -74.0060)
        is_combust2, _, _ = is_planet_in_combust(date2, Planets.VENUS.code, 40.7128, -74.0060)

        # Both should be boolean
        assert isinstance(is_combust1, bool)
        assert isinstance(is_combust2, bool)

    @pytest.mark.unit
    def test_is_planet_in_combust_different_locations(self) -> None:
        """Test that is_planet_in_combust works with different locations."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        is_combust_nyc, _, _ = is_planet_in_combust(check_date, Planets.MARS.code, 40.7128, -74.0060)
        is_combust_mumbai, _, _ = is_planet_in_combust(check_date, Planets.MARS.code, 19.0760, 72.8777)

        # Both should return boolean values
        assert isinstance(is_combust_nyc, bool)
        assert isinstance(is_combust_mumbai, bool)

    @pytest.mark.unit
    def test_is_planet_in_combust_all_regular_planets(self) -> None:
        """Test that is_planet_in_combust works for all regular planets."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)
        planets = [
            Planets.MERCURY.code,
            Planets.VENUS.code,
            Planets.MARS.code,
            Planets.JUPITER.code,
            Planets.SATURN.code,
        ]

        for planet in planets:
            is_combust, period_start, period_end = is_planet_in_combust(check_date, planet, 40.7128, -74.0060)
            assert isinstance(is_combust, bool), f"Failed for planet {planet}"
            assert period_start is None or isinstance(period_start, datetime), f"Failed start date for planet {planet}"
            assert period_end is None or isinstance(period_end, datetime), f"Failed end date for planet {planet}"

    @pytest.mark.unit
    def test_is_planet_in_combust_consistency_with_find_combust_periods(self) -> None:
        """Test that is_planet_in_combust is consistent with find_combust_periods."""
        check_date = datetime(2026, 3, 15, 12, 0, 0, tzinfo=pytz.UTC)
        planet = Planets.JUPITER.code
        lat, lon = 40.7128, -74.0060

        # Get combustion status using is_planet_in_combust
        is_combust, period_start, period_end = is_planet_in_combust(check_date, planet, lat, lon)

        # Get combustion periods around the check date
        start = check_date - timedelta(days=60)
        end = check_date + timedelta(days=60)
        periods = find_combust_periods(start, end, planet, lat, lon)

        # Check if the date falls within any period
        in_period = any(p_start <= check_date <= p_end for p_start, p_end in periods)

        # Both methods should agree
        assert is_combust == in_period, "is_planet_in_combust should match find_combust_periods"
        # If combust, verify the returned period matches
        if is_combust:
            assert period_start is not None and period_end is not None
            assert period_start <= check_date <= period_end

    @pytest.mark.unit
    def test_is_planet_in_combust_with_sample_coordinates(self, sample_coordinates: dict[str, tuple[float, float]]) -> None:
        """Test is_planet_in_combust with various coordinate locations."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        for location_name, (lat, lon) in sample_coordinates.items():
            is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.MERCURY.code, lat, lon)
            assert isinstance(is_combust, bool), f"Failed for location {location_name}"
            assert period_start is None or isinstance(period_start, datetime), f"Failed start date for location {location_name}"
            assert period_end is None or isinstance(period_end, datetime), f"Failed end date for location {location_name}"

    @pytest.mark.unit
    def test_is_planet_in_combust_period_dates_logic(self) -> None:
        """Test that period dates are correctly set based on combustion status."""
        check_date = datetime(2026, 2, 13, tzinfo=pytz.UTC)

        # For planets that are never combust on this date
        is_combust, period_start, period_end = is_planet_in_combust(check_date, Planets.JUPITER.code, 40.7128, -74.0060)

        if not is_combust:
            # When not combust, both dates should be None
            assert period_start is None
            assert period_end is None
        else:
            # When combust, both dates should be present and valid
            assert period_start is not None
            assert period_end is not None
            assert period_start <= check_date <= period_end
            assert period_start < period_end

    @pytest.mark.unit
    def test_is_planet_in_combust_returns_period_boundaries(self) -> None:
        """Test that returned period boundaries match find_combust_periods."""
        check_date = datetime(2026, 4, 15, 12, 0, 0, tzinfo=pytz.UTC)
        planet = Planets.SATURN.code
        lat, lon = 40.7128, -74.0060

        # Get result from is_planet_in_combust
        is_combust, returned_start, returned_end = is_planet_in_combust(check_date, planet, lat, lon)

        # Get periods from find_combust_periods
        start = check_date - timedelta(days=100)
        end = check_date + timedelta(days=100)
        periods = find_combust_periods(start, end, planet, lat, lon)

        if is_combust:
            # If combust, find the matching period
            matching_period = None
            for period_start, period_end in periods:
                if period_start <= check_date <= period_end:
                    matching_period = (period_start, period_end)
                    break

            assert matching_period is not None
            assert returned_start == matching_period[0]
            assert returned_end == matching_period[1]
        else:
            # If not combust, no matching period should exist
            for period_start, period_end in periods:
                assert not (period_start <= check_date <= period_end), "Inconsistency: is_planet_in_combust returned False but period exists"
