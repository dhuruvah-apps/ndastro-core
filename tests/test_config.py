"""Unit tests for ndastro_engine.config module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from skyfield.api import Loader

import ndastro_engine.config as engine_config
from ndastro_engine.config import (
    ConfigurationManager,
    EngineSettings,
    EngineSettingsOverride,
    configure,
    eph,
    ts,
)


class TestConfigurationManager:
    """Test cases for ConfigurationManager class."""

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
    @patch("ndastro_engine.config.get_app_data_dir")
    @patch("ndastro_engine.config.Path")
    @patch("ndastro_engine.config.Loader")
    def test_corrupted_ephemeris_deleted_and_retried(
        self,
        mock_loader: MagicMock,
        mock_path: MagicMock,
        mock_get_app_data_dir: MagicMock,
    ) -> None:
        """Corrupted ephemeris file should be deleted and re-downloaded."""
        import struct

        mock_get_app_data_dir.return_value = "/mock/data/dir"

        # The corrupted_file is constructed as Path(data_dir) / ephemeris_file.
        # Path(data_dir) returns mock_path_instance; / calls __truediv__ on it.
        mock_path_instance = MagicMock()
        mock_corrupted_file = MagicMock()
        mock_corrupted_file.exists.return_value = True  # file exists on disk
        mock_path_instance.__truediv__ = MagicMock(return_value=mock_corrupted_file)
        mock_path.return_value = mock_path_instance

        mock_loader_instance = MagicMock(spec=Loader)
        mock_loader_instance.timescale.return_value = MagicMock()
        # First ephemeris load raises struct.error (corrupted); second succeeds.
        mock_loader_instance.side_effect = [struct.error("corrupted"), MagicMock()]
        mock_loader.return_value = mock_loader_instance

        ConfigurationManager()

        # unlink() should have been called on the corrupted file path
        mock_corrupted_file.unlink.assert_called_once()
        # loader was called twice: first failed, second succeeded
        assert mock_loader_instance.call_count == 2

    @pytest.mark.unit
    @patch("ndastro_engine.config.get_app_data_dir")
    @patch("ndastro_engine.config.Path")
    @patch("ndastro_engine.config.Loader")
    def test_corrupted_ephemeris_not_on_disk_reraises(
        self,
        mock_loader: MagicMock,
        mock_path: MagicMock,
        mock_get_app_data_dir: MagicMock,
    ) -> None:
        """If corrupted file doesn't exist on disk, original error should re-raise."""
        import struct

        mock_get_app_data_dir.return_value = "/mock/data/dir"

        mock_path_instance = MagicMock()
        mock_corrupted_file = MagicMock()
        mock_corrupted_file.exists.return_value = False  # file not on disk
        mock_path_instance.__truediv__ = MagicMock(return_value=mock_corrupted_file)
        mock_path.return_value = mock_path_instance

        mock_loader_instance = MagicMock(spec=Loader)
        mock_loader_instance.timescale.return_value = MagicMock()
        mock_loader_instance.side_effect = struct.error("corrupted")
        mock_loader.return_value = mock_loader_instance

        with pytest.raises(RuntimeError, match="Failed to initialize astronomical data"):
            ConfigurationManager()

    @pytest.mark.unit
    def test_ndastro_config_singleton_exists(self) -> None:
        """Test that ndastro_config singleton is instantiated."""
        assert ts is not None
        assert eph is not None

    @pytest.mark.unit
    def test_ndastro_config_has_required_attributes(self) -> None:
        """Test that ndastro_config has required attributes."""
        # ts should have timescale methods
        assert hasattr(ts, "J2000")
        assert hasattr(ts, "J")


class TestEngineSettings:
    """Tests for EngineSettings dataclass."""

    @pytest.mark.unit
    def test_defaults(self) -> None:
        """Default instance should have expected values."""
        s = EngineSettings()
        assert s.position_reference == "geocentric"
        assert s.node_type == "true"
        assert s.ayanamsa_delta == 0.0
        assert s.dasa_year_length == 365.25
        assert s.apply_nutation is True
        assert s.apply_aberration is True
        assert s.apply_grav_deflection is True
        assert s.sunrise_definition == "geometric"

    @pytest.mark.unit
    def test_invalid_position_reference_raises(self) -> None:
        """Invalid position_reference should raise ValueError."""
        with pytest.raises(ValueError, match="position_reference"):
            EngineSettings(position_reference="barycentric")  # type: ignore[arg-type]

    @pytest.mark.unit
    def test_invalid_node_type_raises(self) -> None:
        """Invalid node_type should raise ValueError."""
        with pytest.raises(ValueError, match="node_type"):
            EngineSettings(node_type="osculating")  # type: ignore[arg-type]

    @pytest.mark.unit
    def test_invalid_sunrise_definition_raises(self) -> None:
        """Invalid sunrise_definition should raise ValueError."""
        with pytest.raises(ValueError, match="sunrise_definition"):
            EngineSettings(sunrise_definition="upper_limb")  # type: ignore[arg-type]

    @pytest.mark.unit
    def test_from_env_reads_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """from_env() should read NDASTRO_* environment variables."""
        monkeypatch.setenv("NDASTRO_POSITION_REFERENCE", "topocentric")
        monkeypatch.setenv("NDASTRO_NODE_TYPE", "mean")
        monkeypatch.setenv("NDASTRO_AYANAMSA_DELTA", "0.5")
        monkeypatch.setenv("NDASTRO_DASA_YEAR_LENGTH", "365.0")
        monkeypatch.setenv("NDASTRO_APPLY_NUTATION", "false")
        monkeypatch.setenv("NDASTRO_APPLY_ABERRATION", "0")
        monkeypatch.setenv("NDASTRO_APPLY_GRAV_DEFLECTION", "yes")
        monkeypatch.setenv("NDASTRO_SUNRISE_DEFINITION", "disc_centre")

        s = EngineSettings.from_env()

        assert s.position_reference == "topocentric"
        assert s.node_type == "mean"
        assert s.ayanamsa_delta == 0.5
        assert s.dasa_year_length == 365.0
        assert s.apply_nutation is False
        assert s.apply_aberration is False
        assert s.apply_grav_deflection is True
        assert s.sunrise_definition == "disc_centre"

    @pytest.mark.unit
    def test_from_env_invalid_value_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """from_env() should raise ValueError when env var has invalid value."""
        monkeypatch.setenv("NDASTRO_NODE_TYPE", "wrong")
        with pytest.raises(ValueError, match="NDASTRO_NODE_TYPE"):
            EngineSettings.from_env()

    @pytest.mark.unit
    def test_from_env_bad_float_falls_back_to_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Non-numeric NDASTRO_AYANAMSA_DELTA should silently use default."""
        monkeypatch.setenv("NDASTRO_AYANAMSA_DELTA", "not-a-number")
        s = EngineSettings.from_env()
        assert s.ayanamsa_delta == 0.0

    @pytest.mark.unit
    def test_from_env_absent_bool_and_float_use_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When bool/float env vars are absent, defaults are returned (covers raw-is-None branches)."""
        for key in ("NDASTRO_APPLY_NUTATION", "NDASTRO_APPLY_ABERRATION",
                    "NDASTRO_APPLY_GRAV_DEFLECTION", "NDASTRO_AYANAMSA_DELTA",
                    "NDASTRO_DASA_YEAR_LENGTH"):
            monkeypatch.delenv(key, raising=False)
        s = EngineSettings.from_env()
        assert s.apply_nutation is True
        assert s.apply_aberration is True
        assert s.apply_grav_deflection is True
        assert s.ayanamsa_delta == 0.0
        assert s.dasa_year_length == 365.25


class TestEngineSettingsOverride:
    """Tests for EngineSettingsOverride dataclass."""

    @pytest.mark.unit
    def test_all_fields_default_to_none(self) -> None:
        """All fields should default to None."""
        o = EngineSettingsOverride()
        assert o.position_reference is None
        assert o.node_type is None
        assert o.ayanamsa_delta is None
        assert o.dasa_year_length is None
        assert o.apply_nutation is None
        assert o.apply_aberration is None
        assert o.apply_grav_deflection is None
        assert o.sunrise_definition is None

    @pytest.mark.unit
    def test_partial_override_sets_only_given_fields(self) -> None:
        """Setting one field should leave others None."""
        o = EngineSettingsOverride(node_type="mean")
        assert o.node_type == "mean"
        assert o.position_reference is None


class TestConfigure:
    """Tests for the configure() function.

    IMPORTANT: configure() mutates the module-level ``ndastro_engine.config.settings``
    object.  Every test uses an autouse fixture to restore the defaults so no
    test can poison a later one through shared global state.
    """

    @pytest.fixture(autouse=True)
    def _restore_settings(self) -> None:
        """Save and restore the module-level settings around every test."""
        saved = engine_config.settings
        yield
        engine_config.settings = saved

    @pytest.mark.unit
    def test_configure_with_no_args_reads_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """configure() with no args should refresh settings from env."""
        monkeypatch.setenv("NDASTRO_NODE_TYPE", "mean")
        configure()
        assert engine_config.settings.node_type == "mean"

    @pytest.mark.unit
    def test_configure_override_applies_non_none_fields(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """configure(override) should apply only non-None fields."""
        monkeypatch.delenv("NDASTRO_NODE_TYPE", raising=False)
        monkeypatch.delenv("NDASTRO_POSITION_REFERENCE", raising=False)
        configure(EngineSettingsOverride(node_type="mean", position_reference="topocentric"))
        assert engine_config.settings.node_type == "mean"
        assert engine_config.settings.position_reference == "topocentric"

    @pytest.mark.unit
    def test_configure_none_override_uses_env_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """configure() with override=None should use env vars only."""
        monkeypatch.setenv("NDASTRO_POSITION_REFERENCE", "topocentric")
        monkeypatch.delenv("NDASTRO_NODE_TYPE", raising=False)
        configure(None)
        assert engine_config.settings.position_reference == "topocentric"
        assert engine_config.settings.node_type == "true"

    @pytest.mark.unit
    def test_configure_with_env_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """configure(env_file=...) should load the file and apply settings."""
        env_file = tmp_path / ".env"
        env_file.write_text("NDASTRO_NODE_TYPE=mean\n")
        monkeypatch.delenv("NDASTRO_NODE_TYPE", raising=False)
        configure(env_file=env_file)
        assert engine_config.settings.node_type == "mean"

    @pytest.mark.unit
    def test_configure_override_with_env_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """configure(override, env_file) should load file then apply override on top."""
        env_file = tmp_path / ".env"
        env_file.write_text("NDASTRO_NODE_TYPE=mean\n")
        monkeypatch.delenv("NDASTRO_NODE_TYPE", raising=False)
        monkeypatch.delenv("NDASTRO_POSITION_REFERENCE", raising=False)
        configure(EngineSettingsOverride(position_reference="topocentric"), env_file=env_file)
        assert engine_config.settings.node_type == "mean"
        assert engine_config.settings.position_reference == "topocentric"

    @pytest.mark.unit
    def test_configure_with_env_file_as_string(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Configure accepts env_file as a plain string path."""
        env_file = tmp_path / ".env"
        env_file.write_text("NDASTRO_SUNRISE_DEFINITION=disc_centre\n")
        monkeypatch.delenv("NDASTRO_SUNRISE_DEFINITION", raising=False)
        configure(env_file=str(env_file))
        assert engine_config.settings.sunrise_definition == "disc_centre"

