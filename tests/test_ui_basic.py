"""Basic UI tests (non-interactive)."""
import pytest
import os
from PySide6.QtWidgets import QApplication
import sys


# Skip UI tests in headless environments
pytestmark = pytest.mark.skipif(
    os.environ.get('QT_QPA_PLATFORM') == 'offscreen',
    reason="UI tests skipped in headless environment"
)


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


class TestUIBasics:
    """Basic UI component tests."""

    def test_main_window_creation(self, qapp):
        """Test that main window can be created."""
        from src.app import NuitkaGUI
        try:
            window = NuitkaGUI()
            assert window is not None
            assert window.windowTitle() != ""
            window.close()
        except Exception as e:
            pytest.fail(f"Failed to create main window: {e}")

    def test_config_manager_integration(self, qapp):
        """Test config manager integration with UI."""
        from src.app import NuitkaGUI
        window = NuitkaGUI()
        assert window.config is not None
        assert hasattr(window.config, 'get')
        assert hasattr(window.config, 'set')
        window.close()

    def test_menu_bar_exists(self, qapp):
        """Test that menu bar is created."""
        from src.app import NuitkaGUI
        window = NuitkaGUI()
        menubar = window.menuBar()
        assert menubar is not None
        # Check for expected menus
        actions = menubar.actions()
        assert len(actions) > 0
        window.close()

    def test_main_window_widget_exists(self, qapp):
        """Test that main window widget is set."""
        from src.app import NuitkaGUI
        window = NuitkaGUI()
        central_widget = window.centralWidget()
        assert central_widget is not None
        window.close()

    def test_styles_application(self, qapp):
        """Test that styles can be applied."""
        from src.ui.styles import apply_stylesheet
        try:
            apply_stylesheet(qapp)
            assert True
        except Exception as e:
            pytest.fail(f"Failed to apply stylesheet: {e}")
