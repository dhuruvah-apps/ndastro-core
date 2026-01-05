"""Unit tests for ndastro_engine.utils module."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from ndastro_engine.constants import OS_LINUX, OS_MAC, OS_WIN
from ndastro_engine.utils import get_app_data_dir


class TestGetAppDataDir:
    """Test cases for get_app_data_dir function."""

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

    def test_get_app_data_dir_windows(self) -> None:
        """Test get_app_data_dir on Windows platform."""
        with patch.object(sys, "platform", OS_WIN):
            result = get_app_data_dir("myapp")
            assert "AppData" in str(result)
            assert "Local" in str(result)
            assert result.name == "myapp"

    def test_get_app_data_dir_mac(self) -> None:
        """Test get_app_data_dir on macOS platform."""
        with patch.object(sys, "platform", OS_MAC):
            result = get_app_data_dir("myapp")
            assert "Library" in str(result)
            assert "Application Support" in str(result)
            assert result.name == "myapp"

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

    def test_get_app_data_dir_returns_path_object(self) -> None:
        """Test that get_app_data_dir returns a Path object."""
        result = get_app_data_dir("testapp")
        assert isinstance(result, Path)

    def test_get_app_data_dir_with_special_characters(self) -> None:
        """Test get_app_data_dir with app name containing special characters."""
        app_name = "my-app_2024"
        result = get_app_data_dir(app_name)
        assert result.name == app_name
        assert isinstance(result, Path)
