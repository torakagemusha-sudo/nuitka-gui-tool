"""Smoke tests for imports and module loading."""
import pytest
import sys
from pathlib import Path

try:
    import PySide6  # noqa: F401
    _has_pyside6 = True
except ImportError:
    _has_pyside6 = False

requires_pyside6 = pytest.mark.skipif(not _has_pyside6, reason="PySide6 not installed")


class TestImports:
    """Test that all modules can be imported without errors."""

    def test_import_main(self):
        """Test importing main module."""
        # This will work if main.py can be imported
        assert Path(__file__).parent.parent.joinpath("main.py").exists()

    @requires_pyside6
    def test_import_app(self):
        """Test importing app module."""
        from src import app
        assert hasattr(app, 'NuitkaGUI')

    def test_import_config(self):
        """Test importing config module."""
        from src.core import config
        assert hasattr(config, 'ConfigManager')

    def test_import_command_builder(self):
        """Test importing command_builder module."""
        from src.core import command_builder
        assert hasattr(command_builder, 'CommandBuilder')

    def test_import_validator(self):
        """Test importing validator module."""
        from src.core import validator
        assert hasattr(validator, 'Validator')

    def test_import_platform_detector(self):
        """Test importing platform_detector module."""
        from src.core import platform_detector
        assert hasattr(platform_detector, 'PlatformDetector')

    def test_import_executor(self):
        """Test importing executor module."""
        from src.core import executor
        assert hasattr(executor, 'CompilationExecutor')

    def test_import_presets(self):
        """Test importing presets module."""
        from src.core import presets
        assert presets is not None

    def test_import_setting_definitions(self):
        """Test importing setting_definitions module."""
        from src.core import setting_definitions
        assert hasattr(setting_definitions, 'load_setting_definitions')

    def test_import_flag_plan(self):
        """Test importing flag_plan module."""
        from src.core import flag_plan
        assert hasattr(flag_plan, 'compile_flag_plan')

    def test_import_diffing(self):
        """Test importing diffing module."""
        from src.core import diffing
        assert diffing is not None

    def test_import_constants(self):
        """Test importing constants module."""
        from src.utils import constants
        assert hasattr(constants, 'APP_NAME')
        assert hasattr(constants, 'APP_VERSION')

    def test_import_styles(self):
        """Test importing styles module."""
        from src.ui import styles
        assert hasattr(styles, 'apply_stylesheet')

    @requires_pyside6
    def test_import_widgets(self):
        """Test importing widgets module."""
        from src.ui import widgets
        assert widgets is not None

    @requires_pyside6
    def test_pyside6_available(self):
        """Test that PySide6 is available."""
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        assert QApplication is not None
        assert Qt is not None

    def test_constants_values(self):
        """Test that constants have expected values."""
        from src.utils.constants import APP_NAME, APP_VERSION
        assert isinstance(APP_NAME, str)
        assert len(APP_NAME) > 0
        assert isinstance(APP_VERSION, str)
        assert len(APP_VERSION) > 0
