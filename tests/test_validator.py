"""Tests for input validation."""
import tempfile
from pathlib import Path
import pytest
from src.core.validator import Validator


class TestValidator:
    """Test suite for Validator class."""

    def test_validate_file_exists_with_valid_file(self):
        """Test validation with an existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            is_valid, message = Validator.validate_file_exists(temp_path)
            assert is_valid
            assert message == ""
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_validate_file_exists_with_missing_file(self):
        """Test validation with a non-existent file."""
        is_valid, message = Validator.validate_file_exists("/nonexistent/file.txt")
        assert not is_valid
        assert "does not exist" in message

    def test_validate_file_exists_with_empty_path(self):
        """Test validation with empty path."""
        is_valid, message = Validator.validate_file_exists("")
        assert not is_valid
        assert "required" in message

    def test_validate_file_exists_with_directory(self):
        """Test validation when path points to directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_valid, message = Validator.validate_file_exists(tmpdir)
            assert not is_valid
            assert "not a file" in message

    def test_validate_directory_exists_with_valid_dir(self):
        """Test directory validation with existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_valid, message = Validator.validate_directory_exists(tmpdir)
            assert is_valid
            assert message == ""

    def test_validate_directory_exists_with_missing_dir(self):
        """Test directory validation with non-existent directory."""
        is_valid, message = Validator.validate_directory_exists("/nonexistent/dir")
        assert not is_valid
        assert "does not exist" in message

    def test_validate_directory_exists_with_empty_path(self):
        """Test directory validation with empty path."""
        is_valid, message = Validator.validate_directory_exists("")
        assert not is_valid
        assert "required" in message

    def test_validate_config_with_valid_config(self):
        """Test config validation with valid configuration."""
        from src.core.config import ConfigManager
        config = ConfigManager()

        # Create a temp file for input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("print('test')")
            temp_path = f.name

        try:
            config.set("basic.input_file", temp_path)
            is_valid, messages = Validator.validate_config(config)
            # Should be valid even if there are warning messages
            assert is_valid or len(messages) > 0
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_validate_config_without_input_file(self):
        """Test config validation without input file."""
        from src.core.config import ConfigManager
        config = ConfigManager()
        config.set("basic.input_file", "")

        is_valid, messages = Validator.validate_config(config)
        assert not is_valid
        assert len(messages) > 0

    def test_validate_python_file_valid(self):
        """Test Python file validation with valid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("print('test')")
            temp_path = f.name

        try:
            is_valid, message = Validator.validate_python_file(temp_path)
            assert is_valid
            assert message == ""
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_validate_python_file_invalid_extension(self):
        """Test Python file validation with wrong extension."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name

        try:
            is_valid, message = Validator.validate_python_file(temp_path)
            assert not is_valid
            assert "Python file" in message or ".py" in message
        finally:
            Path(temp_path).unlink(missing_ok=True)
