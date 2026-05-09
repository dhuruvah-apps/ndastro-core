"""Unit tests for ndastro_engine.utils module."""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ndastro_engine.constants import OS_LINUX, OS_MAC, OS_WIN
from ndastro_engine.utils import (
    dd2dms,
    dd2dmsstr,
    decimal_years_to_years_months_days_ghatis,
    dms2dd,
    get_app_data_dir,
    get_elevation_by_latlon,
    normalize_degree,
    parse_iso_datetime,
)


class TestGetAppDataDir:
    """Test cases for get_app_data_dir function."""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("platform", "expected_path"),
        [
            (OS_WIN, Path.home() / "AppData/Local" / "testapp"),
            (OS_MAC, Path.home() / "Library/Application Support" / "testapp"),
            (OS_LINUX, Path.home() / ".local/share" / "testapp"),
        ],
    )
    def test_get_app_data_dir_platforms(self, platform: str, expected_path: Path) -> None:
        """Test get_app_data_dir returns correct path for different platforms."""
        with patch.object(sys, "platform", platform):
            result = get_app_data_dir("testapp")
            assert result == expected_path

    @pytest.mark.unit
    def test_get_app_data_dir_windows(self) -> None:
        """Test get_app_data_dir on Windows platform."""
        with patch.object(sys, "platform", OS_WIN):
            result = get_app_data_dir("myapp")
            assert "AppData" in str(result)
            assert "Local" in str(result)
            assert result.name == "myapp"

    @pytest.mark.unit
    def test_get_app_data_dir_mac(self) -> None:
        """Test get_app_data_dir on macOS platform."""
        with patch.object(sys, "platform", OS_MAC):
            result = get_app_data_dir("myapp")
            assert "Library" in str(result)
            assert "Application Support" in str(result)
            assert result.name == "myapp"

    @pytest.mark.unit
    def test_get_app_data_dir_linux_default(self) -> None:
        """Test get_app_data_dir on Linux with default XDG path."""
        mock_home = Path("/home/testuser")

        def mock_expanduser(self):
            """Mock expanduser to replace ~ with mock_home."""
            path_str = str(self)
            if path_str.startswith("~"):
                return Path(path_str.replace("~", str(mock_home)))
            return self

        with (
            patch.object(sys, "platform", OS_LINUX),
            patch("ndastro_engine.utils.Path.home", return_value=mock_home),
            patch.object(Path, "expanduser", mock_expanduser),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = get_app_data_dir("myapp")
            expected = mock_home / ".local" / "share" / "myapp"
            assert result == expected

    @pytest.mark.unit
    def test_get_app_data_dir_linux_custom_xdg(self) -> None:
        """Test get_app_data_dir on Linux with custom XDG_DATA_HOME."""
        custom_path = "/custom/data/path"
        mock_home = Path("/home/testuser")
        with (
            patch.object(sys, "platform", OS_LINUX),
            patch("ndastro_engine.utils.Path.home", return_value=mock_home),
            patch.dict("os.environ", {"XDG_DATA_HOME": custom_path}),
        ):
            result = get_app_data_dir("myapp")
            expected = Path(custom_path) / "myapp"
            assert result == expected

    @pytest.mark.unit
    def test_get_app_data_dir_returns_path_object(self) -> None:
        """Test that get_app_data_dir returns a Path object."""
        result = get_app_data_dir("testapp")
        assert isinstance(result, Path)

    @pytest.mark.unit
    def test_get_app_data_dir_with_special_characters(self) -> None:
        """Test get_app_data_dir with app name containing special characters."""
        app_name = "my-app_2024"
        result = get_app_data_dir(app_name)
        assert result.name == app_name
        assert isinstance(result, Path)


class TestNormalizeDegree:
    """Test cases for normalize_degree function."""

    @pytest.mark.unit
    def test_normalize_degree_zero(self) -> None:
        """Test that 0 degrees remains 0."""
        result = normalize_degree(0.0)
        assert result == 0.0

    @pytest.mark.unit
    def test_normalize_degree_valid_range(self) -> None:
        """Test values already in valid range (0-360)."""
        test_values = [0.0, 45.0, 90.0, 180.0, 270.0, 359.99]
        for value in test_values:
            result = normalize_degree(value)
            assert result == value

    @pytest.mark.unit
    def test_normalize_degree_exactly_360(self) -> None:
        """Test that exactly 360 degrees normalizes to 0."""
        result = normalize_degree(360.0)
        assert result == 0.0

    @pytest.mark.unit
    def test_normalize_degree_above_360(self) -> None:
        """Test values above 360 degrees."""
        assert normalize_degree(361.0) == 1.0
        assert normalize_degree(450.0) == 90.0
        assert normalize_degree(720.0) == 0.0
        assert normalize_degree(725.5) == 5.5

    @pytest.mark.unit
    def test_normalize_degree_negative_values(self) -> None:
        """Test negative degree values."""
        assert normalize_degree(-1.0) == 359.0
        assert normalize_degree(-90.0) == 270.0
        assert normalize_degree(-180.0) == 180.0
        assert normalize_degree(-270.0) == 90.0
        assert normalize_degree(-359.0) == 1.0

    @pytest.mark.unit
    def test_normalize_degree_large_positive(self) -> None:
        """Test very large positive values."""
        assert normalize_degree(1080.0) == 0.0  # 3 full rotations
        assert normalize_degree(1125.0) == 45.0
        assert abs(normalize_degree(3600.0) - 0.0) < 0.0001

    @pytest.mark.unit
    def test_normalize_degree_large_negative(self) -> None:
        """Test very large negative values."""
        assert normalize_degree(-360.0) == 0.0
        assert normalize_degree(-720.0) == 0.0
        assert normalize_degree(-450.0) == 270.0

    @pytest.mark.unit
    def test_normalize_degree_decimal_precision(self) -> None:
        """Test that decimal precision is maintained."""
        result = normalize_degree(45.123456)
        assert abs(result - 45.123456) < 0.0001

        result = normalize_degree(370.987654)
        assert abs(result - 10.987654) < 0.0001

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "input_deg,expected",
        [
            (0.0, 0.0),
            (180.0, 180.0),
            (360.0, 0.0),
            (540.0, 180.0),
            (-180.0, 180.0),
            (-360.0, 0.0),
            (365.5, 5.5),
            (-5.5, 354.5),
        ],
    )
    def test_normalize_degree_parametrized(self, input_deg: float, expected: float) -> None:
        """Test normalize_degree with various inputs."""
        result = normalize_degree(input_deg)
        assert abs(result - expected) < 0.0001

    @pytest.mark.unit
    def test_normalize_degree_output_range(self) -> None:
        """Test that output is always in valid range [0, 360)."""
        test_values = [-1000.0, -500.0, -360.0, -180.0, -1.0, 0.0, 1.0, 180.0, 359.0, 360.0, 361.0, 500.0, 1000.0]

        for value in test_values:
            result = normalize_degree(value)
            assert 0.0 <= result < 360.0, f"normalize_degree({value}) = {result} is out of range"

    @pytest.mark.unit
    def test_normalize_degree_idempotent(self) -> None:
        """Test that normalizing twice gives same result."""
        test_values = [370.0, -10.0, 725.0]

        for value in test_values:
            first = normalize_degree(value)
            second = normalize_degree(first)
            assert first == second

    @pytest.mark.unit
    def test_decimal_years_to_years_months_days_ghatis(self) -> None:
        """Test decimal_years_to_years_months_days_ghatis function."""
        # Test with 2.25 years
        result = decimal_years_to_years_months_days_ghatis(2.24875)
        assert result == (2, 2, 29, 23, 33, 18, 57)


class TestParseIsoDatetime:
    """Test cases for parse_iso_datetime function."""

    @pytest.mark.unit
    def test_parse_iso_datetime_defaults_to_utc_when_tz_missing(self) -> None:
        """Naive ISO datetime should default to UTC."""
        result = parse_iso_datetime("2026-01-11T12:30:45")

        assert result == datetime(2026, 1, 11, 12, 30, 45, tzinfo=UTC)

    @pytest.mark.unit
    def test_parse_iso_datetime_keeps_existing_offset(self) -> None:
        """Timezone-aware ISO datetime should preserve its offset."""
        result = parse_iso_datetime("2026-01-11T12:30:45+05:30")

        assert result == datetime.fromisoformat("2026-01-11T12:30:45+05:30")

    @pytest.mark.unit
    def test_parse_iso_datetime_supports_z_suffix(self) -> None:
        """ISO datetime with Z suffix should be parsed as UTC."""
        result = parse_iso_datetime("2026-01-11T12:30:45Z")

        assert result == datetime(2026, 1, 11, 12, 30, 45, tzinfo=UTC)

    @pytest.mark.unit
    def test_parse_iso_datetime_rejects_invalid_value(self) -> None:
        """Invalid datetime string should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid ISO datetime string"):
            parse_iso_datetime("not-a-date")


class TestGetElevationByLatlon:
    """Test cases for get_elevation_by_latlon function."""

    @pytest.mark.unit
    def test_get_elevation_by_latlon_returns_api_value(self) -> None:
        """Should return elevation value from API payload."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"elevation": 920.5}).encode("utf-8")

        get_elevation_by_latlon.cache_clear()
        with patch("ndastro_engine.utils.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = mock_response

            result = get_elevation_by_latlon(12.97, 77.59)

        assert result == 920.5

    @pytest.mark.unit
    def test_get_elevation_by_latlon_falls_back_to_zero_on_error(self) -> None:
        """Should return 0.0 when API call fails."""
        get_elevation_by_latlon.cache_clear()
        with patch("ndastro_engine.utils.urlopen", side_effect=OSError):
            result = get_elevation_by_latlon(12.97, 77.59)

        assert result == 0.0


class TestDms2Dd:
    """Test cases for dms2dd (DMS → decimal degrees) conversion."""

    @pytest.mark.unit
    def test_positive_values(self) -> None:
        """Positive DMS converts correctly."""
        assert dms2dd(16, 6, 32) == pytest.approx(16 + 6 / 60 + 32 / 3600)

    @pytest.mark.unit
    def test_zero_minutes_seconds(self) -> None:
        """Only degree component."""
        assert dms2dd(30, 0, 0) == pytest.approx(30.0)

    @pytest.mark.unit
    def test_negative_sign(self) -> None:
        """Negative sign flips the result."""
        result = dms2dd(10, 30, 0, sign=-1)
        assert result == pytest.approx(-(10 + 30 / 60))

    @pytest.mark.unit
    def test_fractional_seconds(self) -> None:
        """Fractional seconds handled correctly."""
        expected = 1 + 1 / 60 + 1.5 / 3600
        assert dms2dd(1, 1, 1.5) == pytest.approx(expected)


class TestDd2Dms:
    """Test cases for dd2dms (decimal degrees → DMS) conversion."""

    @pytest.mark.unit
    def test_positive_value(self) -> None:
        """Positive decimal converts correctly."""
        deg, minutes, secs, sign = dd2dms(16 + 6 / 60 + 32 / 3600)
        assert deg == 16
        assert minutes == 6
        assert secs == pytest.approx(32.0, abs=1e-6)
        assert sign == 1

    @pytest.mark.unit
    def test_negative_value(self) -> None:
        """Negative decimal yields sign == -1."""
        deg, minutes, secs, sign = dd2dms(-10.5)
        assert sign == -1
        assert deg == 10
        assert minutes == 30
        assert secs == pytest.approx(0.0, abs=1e-6)

    @pytest.mark.unit
    def test_zero(self) -> None:
        """Zero decimal gives all zeros with positive sign."""
        deg, minutes, secs, sign = dd2dms(0.0)
        assert deg == 0
        assert minutes == 0
        assert secs == pytest.approx(0.0)
        assert sign == 1

    @pytest.mark.unit
    def test_roundtrip(self) -> None:
        """dms2dd(dd2dms(x)) should recover the original value."""
        original = 256.109722  # ~256° 06' 35"
        deg, minutes, secs, sign = dd2dms(original)
        recovered = dms2dd(deg, minutes, secs, sign)
        assert recovered == pytest.approx(original, abs=1e-9)


class TestDd2DmsStr:
    """Test cases for dd2dmsstr formatting."""

    @pytest.mark.unit
    def test_positive_format(self) -> None:
        """Positive value formats without leading minus."""
        result = dd2dmsstr(30.5)
        assert result.startswith("30°")
        assert "'" in result
        assert '"' in result
        assert not result.startswith("-")

    @pytest.mark.unit
    def test_negative_format(self) -> None:
        """Negative value formats with leading minus."""
        result = dd2dmsstr(-10.25)
        assert result.startswith("-10°")

    @pytest.mark.unit
    def test_zero_format(self) -> None:
        """Zero formats as 0° 0' 0.00\"."""
        result = dd2dmsstr(0.0)
        assert "0°" in result
