"""Tests for platform detection."""
import sys
import pytest
from src.core.platform_detector import PlatformDetector


class TestPlatformDetector:
    """Test suite for PlatformDetector class."""

    def test_get_platform(self):
        """Test getting current platform."""
        platform = PlatformDetector.get_platform()
        assert platform in ["windows", "darwin", "linux"]

    def test_is_windows(self):
        """Test Windows detection."""
        is_win = PlatformDetector.is_windows()
        assert isinstance(is_win, bool)
        assert is_win == (sys.platform == "win32")

    def test_is_macos(self):
        """Test macOS detection."""
        is_mac = PlatformDetector.is_macos()
        assert isinstance(is_mac, bool)
        assert is_mac == (sys.platform == "darwin")

    def test_is_linux(self):
        """Test Linux detection."""
        is_linux = PlatformDetector.is_linux()
        assert isinstance(is_linux, bool)
        assert is_linux == (sys.platform.startswith("linux"))

    def test_has_nuitka(self):
        """Test Nuitka detection."""
        has_nuitka = PlatformDetector.has_nuitka()
        assert isinstance(has_nuitka, bool)
        # Should return True or False, not error

    def test_get_nuitka_version(self):
        """Test getting Nuitka version."""
        version = PlatformDetector.get_nuitka_version()
        assert isinstance(version, str)
        # Should return version string or "Not installed"

    def test_platform_consistency(self):
        """Test that exactly one platform is detected."""
        platforms = [
            PlatformDetector.is_windows(),
            PlatformDetector.is_macos(),
            PlatformDetector.is_linux()
        ]
        # Exactly one should be True
        assert sum(platforms) == 1
