"""Pytest configuration and fixtures."""
import pytest


@pytest.fixture
def sample_config():
    """Provide a sample configuration for testing."""
    return {
        "basic": {
            "input_file": "test_app.py",
            "mode": "standalone",
            "output_dir": "dist",
            "compiler": "auto",
        },
        "modules": {
            "follow_imports": True,
            "include_packages": ["numpy"],
        },
        "data": {
            "package_data": [],
            "data_files": [],
        },
        "platform": {
            "windows": {
                "console": True,
            }
        },
        "advanced": {
            "lto": "auto",
            "jobs": "auto",
        },
        "output": {
            "verbose": False,
        }
    }
