"""
Configuration management for Nuitka GUI.
"""
import json
import logging
from pathlib import Path
from typing import Any, Optional

# Set up logging for configuration operations
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration and state."""

    def __init__(self):
        """Initialize configuration with default values."""
        self._config = self._get_default_config()
        self._file_path = None

    def _get_default_config(self):
        """Get default configuration structure."""
        return {
            "app": {
                "theme": "light",  # "light", "dark", or "auto"
                "theme_auto_switch": False,
            },
            "basic": {
                "input_file": "",
                "mode": "standalone",
                "output_dir": "",
                "output_filename": "",
                "compiler": "auto",
                "python_flags": [],
                "msvc_version": "latest",
                "remove_output": True,
            },
            "modules": {
                "include_packages": [],
                "include_modules": [],
                "follow_imports": True,
                "follow_stdlib": False,
                "follow_to": [],
                "nofollow_to": [],
                "package_configs": [],
            },
            "data": {
                "package_data": [],
                "data_files": [],
                "data_dirs": [],
                "external_data": [],
                "exclude_patterns": [],
                "dll_excludes": [],
                "distributions": [],
            },
            "platform": {
                "windows": {
                    "icon": "",
                    "console_mode": "auto",
                    "uac_admin": False,
                    "uac_uiaccess": False,
                    "splash_screen": "",
                    "company_name": "",
                    "product_name": "",
                    "product_version": "",
                    "file_version": "",
                    "file_description": "",
                    "copyright": "",
                    "trademarks": "",
                },
                "macos": {
                    "create_bundle": False,
                    "icon": "",
                    "app_name": "",
                    "bundle_id": "",
                    "app_version": "",
                    "protected_resources": [],
                },
                "linux": {
                    "icon": "",
                },
            },
            "advanced": {
                "lto": "auto",
                "static_libpython": False,
                "jobs": 0,  # 0 means auto
                "low_memory": False,
                "onefile_tempdir_spec": "",
                "onefile_temp_mode": "auto",
                "full_compat": False,
                "file_reference_choice": "runtime",
                "module_name_choice": "runtime",
                "debug": False,
                "unstripped": False,
                "generate_c_only": False,
                "trace_execution": False,
                "xml_output": "",
                "disable_ccache": False,
                "disable_bytecode_cache": False,
                "pgo_c": False,
                "pgo_args": "",
                "pgo_executable": "",
                "force_environment": [],
                "deployment": False,
            },
            "output": {
                "quiet": False,
                "verbose": False,
                "verbose_output": "",
                "show_progress": True,
                "progress_mode": "auto",
                "show_memory": False,
                "show_scons": False,
                "report_file": "",
                "report_diffable": False,
                "report_templates": [],
                "report_user_data": [],
                "warn_implicit_exceptions": False,
                "warn_unusual_code": False,
                "assume_yes_for_downloads": False,
                "nowarn_mnemonics": [],
            },
            "plugins": {
                "enabled": [],
                "disabled": [],
                "user_plugins": [],
                "no_detection": False,
                "module_parameters": [],
                "anti_bloat": {
                    "show_changes": False,
                    "custom_choices": {},
                },
            },
        }

    def get(self, key, default=None):
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'basic.input_file')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key, value):
        """
        Set configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'basic.input_file')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config

        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

    def save(self, filepath):
        """
        Save configuration to JSON file.

        Args:
            filepath: Path to save configuration

        Returns:
            bool: True if successful
        """
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)

            self._file_path = filepath
            return True
        except (IOError, PermissionError) as e:
            logger.error(f"Cannot write to configuration file '{filepath}': {e}")
            return False
        except TypeError as e:
            logger.error(f"Invalid configuration data (cannot serialize to JSON): {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error saving configuration: {e}")
            return False

    def load(self, filepath):
        """
        Load configuration from JSON file.

        Args:
            filepath: Path to load configuration from

        Returns:
            bool: True if successful
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                logger.warning(f"Configuration file not found: {filepath}")
                return False

            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)

            # Merge with defaults to ensure all keys exist
            self._config = self._merge_configs(
                self._get_default_config(),
                loaded_config
            )

            self._file_path = filepath
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file '{filepath}': {e}")
            return False
        except (IOError, PermissionError) as e:
            logger.error(f"Cannot read configuration file '{filepath}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")
            return False

    def _merge_configs(self, default, loaded):
        """
        Merge loaded configuration with defaults.

        Args:
            default: Default configuration
            loaded: Loaded configuration

        Returns:
            Merged configuration
        """
        if not isinstance(loaded, dict):
            return loaded

        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def reset(self):
        """Reset configuration to defaults."""
        self._config = self._get_default_config()
        self._file_path = None

    def to_dict(self):
        """
        Get configuration as dictionary.

        Returns:
            dict: Complete configuration
        """
        return self._config.copy()

    def get_file_path(self):
        """
        Get current file path.

        Returns:
            Path or None: Current file path
        """
        return self._file_path

    def has_unsaved_changes(self):
        """
        Check if there are unsaved changes.

        Returns:
            bool: True if there are unsaved changes
        """
        # This could be enhanced to track actual changes
        return self._file_path is None
