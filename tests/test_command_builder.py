"""Tests for command builder."""
import pytest
from src.core.config import ConfigManager
from src.core.command_builder import CommandBuilder


class TestCommandBuilder:
    """Test suite for CommandBuilder class."""

    def test_init(self):
        """Test CommandBuilder initialization."""
        config = ConfigManager()
        builder = CommandBuilder(config)
        assert builder.config is not None
        assert builder.registry is not None

    def test_build_returns_list(self):
        """Test that build returns a list of command arguments."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("basic.mode", "standalone")

        builder = CommandBuilder(config)
        command = builder.build()

        assert isinstance(command, list)
        assert len(command) > 0

    def test_build_includes_python_module(self):
        """Test that build includes python -m nuitka."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")

        builder = CommandBuilder(config)
        command = builder.build()

        # Should contain -m and nuitka
        assert "-m" in command
        assert "nuitka" in command

    def test_build_includes_mode(self):
        """Test that build includes compilation mode."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("basic.mode", "onefile")

        builder = CommandBuilder(config)
        command = builder.build()

        # Check for onefile flag
        command_str = " ".join(command)
        assert "onefile" in command_str.lower()

    def test_get_command_string(self):
        """Test getting command as string."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("basic.mode", "standalone")

        builder = CommandBuilder(config)
        command_str = builder.get_command_string()

        assert isinstance(command_str, str)
        assert "nuitka" in command_str
        assert "test.py" in command_str

    def test_build_with_output_dir(self):
        """Test building command with output directory."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("basic.output_dir", "dist")

        builder = CommandBuilder(config)
        command_str = builder.get_command_string()

        assert "dist" in command_str

    def test_build_with_compiler(self):
        """Test building command with specific compiler."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("basic.compiler", "mingw64")

        builder = CommandBuilder(config)
        command_str = builder.get_command_string()

        assert "mingw64" in command_str.lower() or "--mingw64" in command_str

    def test_build_with_include_packages(self):
        """Test building command with included packages."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("modules.include_packages", ["numpy", "pandas"])

        builder = CommandBuilder(config)
        command_str = builder.get_command_string()

        assert "numpy" in command_str or "include-package" in command_str

    def test_build_with_follow_imports(self):
        """Test building command with follow imports."""
        config = ConfigManager()
        config.set("basic.input_file", "test.py")
        config.set("modules.follow_imports", True)

        builder = CommandBuilder(config)
        command = builder.build()

        # Should work without errors
        assert isinstance(command, list)
