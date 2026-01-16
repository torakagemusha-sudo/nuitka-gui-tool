"""Tests for configuration management."""
import json
import tempfile
from pathlib import Path
import pytest
from src.core.config import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager class."""

    def test_init_creates_default_config(self):
        """Test that initialization creates default configuration."""
        config = ConfigManager()
        assert config._config is not None
        assert "basic" in config._config
        assert "modules" in config._config
        assert "data" in config._config

    def test_get_returns_value(self):
        """Test that get method returns values correctly."""
        config = ConfigManager()
        mode = config.get("basic.mode")
        assert mode == "standalone"

    def test_set_updates_value(self):
        """Test that set method updates values correctly."""
        config = ConfigManager()
        config.set("basic.mode", "onefile")
        assert config.get("basic.mode") == "onefile"

    def test_get_nonexistent_key_returns_none(self):
        """Test that getting non-existent key returns None."""
        config = ConfigManager()
        value = config.get("nonexistent.key")
        assert value is None

    def test_set_nested_key(self):
        """Test setting nested keys."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        assert config.get("basic.input_file") == "test.py"

    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = ConfigManager()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "basic" in config_dict

    def test_reset(self):
        """Test resetting configuration."""
        config = ConfigManager()
        config.set("basic.mode", "onefile")
        config.reset()
        assert config.get("basic.mode") == "standalone"

    def test_save_and_load(self):
        """Test saving and loading configuration."""
        config = ConfigManager()
        config.set("basic.mode", "onefile")
        config.set("basic.input_file", "test.py")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            # Save
            assert config.save(temp_path)

            # Load into new config
            new_config = ConfigManager()
            assert new_config.load(temp_path)
            assert new_config.get("basic.mode") == "onefile"
            assert new_config.get("basic.input_file") == "test.py"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_save_creates_file(self):
        """Test that save creates a file."""
        config = ConfigManager()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test_config.json"
            assert config.save(str(file_path))
            assert file_path.exists()

    def test_load_invalid_file_returns_false(self):
        """Test that loading invalid file returns False."""
        config = ConfigManager()
        assert not config.load("/nonexistent/file.json")

    def test_get_file_path(self):
        """Test getting current file path."""
        config = ConfigManager()
        assert config.get_file_path() is None

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            config.save(temp_path)
            file_path = config.get_file_path()
            # Handle both string and Path objects
            assert str(file_path) == temp_path or file_path == Path(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)
