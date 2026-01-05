"""Unit tests for ndastro_engine.config module."""

from unittest.mock import MagicMock, patch

import pytest
from skyfield.api import Loader

from ndastro_engine.config import ConfigurationManager, eph, ts


class TestConfigurationManager:
    """Test cases for ConfigurationManager class."""

    @patch("ndastro_engine.config.get_app_data_dir")
    @patch("ndastro_engine.config.Path")
    @patch("ndastro_engine.config.Loader")
    def test_initialization_success(
        self,
        mock_loader: MagicMock,
        mock_path: MagicMock,
        mock_get_app_data_dir: MagicMock,
    ) -> None:
        """Test successful initialization of ConfigurationManager."""
        # Setup mocks
        mock_data_dir = "/mock/data/dir"
        mock_get_app_data_dir.return_value = mock_data_dir

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance

        mock_loader_instance = MagicMock(spec=Loader)
        mock_timescale = MagicMock()
        mock_ephemeris = MagicMock()
        mock_loader_instance.timescale.return_value = mock_timescale
        mock_loader_instance.return_value = mock_ephemeris
        mock_loader.return_value = mock_loader_instance

        # Create instance
        config = ConfigurationManager()

        # Assertions
        mock_get_app_data_dir.assert_called_once_with("ndastro")
        mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_loader.assert_called_once_with(mock_data_dir, verbose=True)
        assert config.ts == mock_timescale
        assert config.eph == mock_ephemeris

    @patch("ndastro_engine.config.get_app_data_dir")
    @patch("ndastro_engine.config.Path")
    @patch("ndastro_engine.config.Loader")
    def test_initialization_failure(
        self,
        mock_loader: MagicMock,
        mock_path: MagicMock,
        mock_get_app_data_dir: MagicMock,
    ) -> None:
        """Test ConfigurationManager initialization failure handling."""
        mock_get_app_data_dir.return_value = "/mock/data/dir"
        mock_path.return_value.mkdir.side_effect = OSError("Permission denied")

        with pytest.raises(RuntimeError, match="Failed to initialize astronomical data"):
            ConfigurationManager()

    @patch("ndastro_engine.config.get_app_data_dir")
    @patch("ndastro_engine.config.Path")
    @patch("ndastro_engine.config.Loader")
    def test_loader_failure(
        self,
        mock_loader: MagicMock,
        mock_path: MagicMock,
        mock_get_app_data_dir: MagicMock,
    ) -> None:
        """Test ConfigurationManager when Loader fails."""
        mock_get_app_data_dir.return_value = "/mock/data/dir"
        mock_loader.side_effect = Exception("Network error")

        with pytest.raises(RuntimeError, match="Failed to initialize astronomical data"):
            ConfigurationManager()

    def test_ndastro_config_singleton_exists(self) -> None:
        """Test that ndastro_config singleton is instantiated."""
        assert ts is not None
        assert eph is not None

    def test_ndastro_config_has_required_attributes(self) -> None:
        """Test that ndastro_config has required attributes."""
        # ts should have timescale methods
        assert hasattr(ts, "J2000")
        assert hasattr(ts, "J")
