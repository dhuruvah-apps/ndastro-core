"""Unit tests for ndastro_engine.constants module."""

from ndastro_engine.constants import OS_LINUX, OS_MAC, OS_WIN


class TestConstants:
    """Test cases for constants module."""

    def test_os_constants_are_strings(self) -> None:
        """Test that all OS constants are strings."""
        assert isinstance(OS_WIN, str)
        assert isinstance(OS_MAC, str)
        assert isinstance(OS_LINUX, str)

    def test_os_constants_values(self) -> None:
        """Test that OS constants have expected values."""
        assert OS_WIN == "win32"
        assert OS_MAC == "darwin"
        assert OS_LINUX == "linux"

    def test_os_constants_not_empty(self) -> None:
        """Test that OS constants are not empty strings."""
        assert OS_WIN
        assert OS_MAC
        assert OS_LINUX
