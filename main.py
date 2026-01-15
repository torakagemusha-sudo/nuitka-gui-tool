#!/usr/bin/env python3
"""
Nuitka GUI - A graphical user interface for the Nuitka Python Compiler.

This tool provides a user-friendly interface for all Nuitka command-line options,
making it easy to compile Python applications without memorizing flags.
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QLibraryInfo
from PySide6.QtGui import QScreen

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from src.app import NuitkaGUI
from src.ui.styles import apply_stylesheet


def main():
    """Main entry point for the application."""
    # Ensure Qt can locate platform plugins (fixes missing "windows" plugin).
    plugin_base = QLibraryInfo.path(QLibraryInfo.PluginsPath)
    if plugin_base:
        os.environ.setdefault("QT_PLUGIN_PATH", plugin_base)
        os.environ.setdefault(
            "QT_QPA_PLATFORM_PLUGIN_PATH",
            str(Path(plugin_base) / "platforms"),
        )
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Nuitka GUI")
    app.setOrganizationName("Nuitka Tools")

    # Apply Modern Fluent Design stylesheet
    apply_stylesheet(app)

    # Create main window
    window = NuitkaGUI()

    # Center window on screen
    screen = QScreen.availableGeometry(QApplication.primaryScreen())
    window_rect = window.frameGeometry()
    center_point = screen.center()
    window_rect.moveCenter(center_point)
    window.move(window_rect.topLeft())

    # Show window
    window.show()

    # Run application event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
