"""
Input validation utilities for Nuitka GUI.
"""
import re
from pathlib import Path


class Validator:
    """Validates user inputs and configurations."""

    @staticmethod
    def validate_file_exists(path):
        """
        Validate that a file exists.

        Args:
            path: Path to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not path:
            return False, "File path is required"

        p = Path(path)
        if not p.exists():
            return False, f"File does not exist: {path}"

        if not p.is_file():
            return False, f"Path is not a file: {path}"

        return True, ""

    @staticmethod
    def validate_directory_exists(path):
        """
        Validate that a directory exists.

        Args:
            path: Path to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not path:
            return False, "Directory path is required"

        p = Path(path)
        if not p.exists():
            return False, f"Directory does not exist: {path}"

        if not p.is_dir():
            return False, f"Path is not a directory: {path}"

        return True, ""

    @staticmethod
    def validate_python_file(path):
        """
        Validate that a file is a Python file.

        Args:
            path: Path to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        is_valid, message = Validator.validate_file_exists(path)
        if not is_valid:
            return False, message

        if not path.endswith('.py'):
            return False, "File must be a Python file (.py)"

        return True, ""

    @staticmethod
    def validate_version(version_str):
        """
        Validate version number format (e.g., 1.0 or 1.0.0.0).

        Args:
            version_str: Version string to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not version_str:
            return True, ""  # Empty is okay

        # Version should be 1-4 numbers separated by dots
        pattern = r'^\d+(\.\d+){0,3}$'
        if not re.match(pattern, version_str):
            return False, "Version must be in format like '1.0' or '1.0.0.0'"

        return True, ""

    @staticmethod
    def validate_module_name(name):
        """
        Validate Python module name.

        Args:
            name: Module name to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not name:
            return False, "Module name is required"

        # Module name should be valid Python identifier (may contain dots)
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$'
        if not re.match(pattern, name):
            return False, "Invalid module name format"

        return True, ""

    @staticmethod
    def validate_bundle_id(bundle_id):
        """
        Validate macOS bundle identifier.

        Args:
            bundle_id: Bundle ID to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not bundle_id:
            return True, ""  # Empty is okay

        # Bundle ID should be like com.company.appname
        pattern = r'^[a-z][a-z0-9]*(\.[a-z][a-z0-9-]*)+$'
        if not re.match(pattern, bundle_id):
            return False, "Bundle ID should be like 'com.company.appname' (lowercase, dots)"

        return True, ""

    @staticmethod
    def validate_icon_file(path, platform_type='windows'):
        """
        Validate icon file format.

        Args:
            path: Path to icon file
            platform_type: 'windows', 'darwin', or 'linux'

        Returns:
            tuple: (is_valid, error_message)
        """
        if not path:
            return True, ""  # Empty is okay

        is_valid, message = Validator.validate_file_exists(path)
        if not is_valid:
            return False, message

        if platform_type == 'windows':
            if not (path.endswith('.ico') or path.endswith('.png')):
                return False, "Windows icon must be .ico or .png file"
        elif platform_type == 'darwin':
            if not (path.endswith('.icns') or path.endswith('.png')):
                return False, "macOS icon must be .icns or .png file"
        else:
            if not path.endswith('.png'):
                return False, "Linux icon must be .png file"

        return True, ""

    @staticmethod
    def validate_config(config):
        """
        Validate entire configuration.

        Args:
            config: ConfigManager instance

        Returns:
            tuple: (is_valid, list_of_messages)
        """
        errors = []
        warnings = []

        # Validate input file (required)
        input_file = config.get('basic.input_file')
        if not input_file:
            errors.append("Input Python file is required")
        else:
            is_valid, message = Validator.validate_python_file(input_file)
            if not is_valid:
                errors.append(message)

        # Validate output directory if specified
        output_dir = config.get('basic.output_dir')
        if output_dir and not Path(output_dir).exists():
            warnings.append(f"Output directory '{output_dir}' will be created")

        # Validate version numbers
        file_version = config.get('platform.windows.file_version')
        if file_version:
            is_valid, message = Validator.validate_version(file_version)
            if not is_valid:
                errors.append(f"File version: {message}")

        product_version = config.get('platform.windows.product_version')
        if product_version:
            is_valid, message = Validator.validate_version(product_version)
            if not is_valid:
                errors.append(f"Product version: {message}")

        # Validate bundle ID
        bundle_id = config.get('platform.macos.bundle_id')
        if bundle_id:
            is_valid, message = Validator.validate_bundle_id(bundle_id)
            if not is_valid:
                errors.append(f"Bundle ID: {message}")

        # Validate icon files
        win_icon = config.get('platform.windows.icon')
        if win_icon:
            is_valid, message = Validator.validate_icon_file(win_icon, 'windows')
            if not is_valid:
                errors.append(f"Windows icon: {message}")

        mac_icon = config.get('platform.macos.icon')
        if mac_icon:
            is_valid, message = Validator.validate_icon_file(mac_icon, 'darwin')
            if not is_valid:
                errors.append(f"macOS icon: {message}")

        # Validate included modules
        for module in config.get('modules.include_modules', []):
            is_valid, message = Validator.validate_module_name(module)
            if not is_valid:
                errors.append(f"Module '{module}': {message}")

        # Mode-specific validation
        mode = config.get('basic.mode')
        if mode in ['standalone', 'onefile']:
            if not config.get('modules.follow_imports', True):
                warnings.append(
                    "Standalone/onefile modes typically need 'Follow imports' enabled"
                )

        return len(errors) == 0, errors + warnings
