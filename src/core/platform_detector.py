"""
Platform detection utilities for Nuitka GUI.
"""
import sys
import platform
import shutil
import subprocess


class PlatformDetector:
    """Detects platform and available compilers."""

    @staticmethod
    def get_platform():
        """Get platform name: 'windows', 'darwin', or 'linux'."""
        system = platform.system().lower()
        if system == 'windows':
            return 'windows'
        elif system == 'darwin':
            return 'darwin'
        else:
            return 'linux'

    @staticmethod
    def is_windows():
        """Check if running on Windows."""
        return PlatformDetector.get_platform() == 'windows'

    @staticmethod
    def is_macos():
        """Check if running on macOS."""
        return PlatformDetector.get_platform() == 'darwin'

    @staticmethod
    def is_linux():
        """Check if running on Linux."""
        return PlatformDetector.get_platform() == 'linux'

    @staticmethod
    def get_available_compilers():
        """Get list of available compilers on this platform."""
        compilers = ['auto']

        if PlatformDetector.is_windows():
            # Check for MSVC
            if shutil.which('cl'):
                compilers.append('msvc')

            # MinGW64 and Clang are always available as fallbacks
            compilers.extend(['mingw64', 'clang'])

        # Zig is available on all platforms
        if shutil.which('zig'):
            compilers.append('zig')

        # Clang on Unix
        if not PlatformDetector.is_windows() and shutil.which('clang'):
            if 'clang' not in compilers:
                compilers.append('clang')

        return compilers

    @staticmethod
    def get_default_compiler():
        """Get the default recommended compiler for this platform."""
        if PlatformDetector.is_windows():
            return 'msvc' if shutil.which('cl') else 'mingw64'
        else:
            return 'auto'

    @staticmethod
    def has_nuitka():
        """Check if Nuitka is installed."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'nuitka', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
            return False
        except subprocess.SubprocessError:
            # Log unexpected subprocess errors if needed
            return False

    @staticmethod
    def get_nuitka_version():
        """Get Nuitka version string."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'nuitka', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Parse version from output
                output = result.stdout.strip()
                # Output is usually like "Nuitka 2.0.3"
                if 'Nuitka' in output:
                    return output
                return output
            return "Unknown"
        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
            return "Not installed"
        except subprocess.SubprocessError:
            # Log unexpected subprocess errors if needed
            return "Not installed"

    @staticmethod
    def should_show_windows_options():
        """Determine if Windows-specific options should be shown."""
        return PlatformDetector.is_windows()

    @staticmethod
    def should_show_macos_options():
        """Determine if macOS-specific options should be shown."""
        return PlatformDetector.is_macos()

    @staticmethod
    def should_show_linux_options():
        """Determine if Linux-specific options should be shown."""
        return PlatformDetector.is_linux()
