"""
Data and resources tab for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGroupBox, QFrame, QInputDialog, QFileDialog
)
from PySide6.QtCore import Qt
from .widgets import ListBoxWithButtons, add_tooltip


class TabData(QWidget):
    """Tab for data file and resource inclusion settings."""

    def __init__(self, parent, config):
        """
        Initialize data tab.

        Args:
            parent: Parent widget
            config: ConfigManager instance
        """
        super().__init__(parent)
        self.config = config
        self.widgets = {}

        # Create scrollable layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        # Content widget
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(16)

        self.create_widgets()

        self.content_layout.addStretch(1)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def create_widgets(self):
        """Create widgets for data tab."""
        # Package data
        pkg_data_frame = QGroupBox("Package Data")
        pkg_data_layout = QVBoxLayout(pkg_data_frame)

        self.widgets['package_data'] = ListBoxWithButtons(
            pkg_data_frame,
            "Package data patterns:",
            add_callback=self._add_package_data,
            height=4
        )
        self.widgets['package_data'].setToolTip("Include package data files (e.g., 'myapp:*.json', 'package:data/*')")
        pkg_data_layout.addWidget(self.widgets['package_data'])

        self.content_layout.addWidget(pkg_data_frame)

        # Data files
        data_files_frame = QGroupBox("Data Files")
        data_files_layout = QVBoxLayout(data_files_frame)

        self.widgets['data_files'] = ListBoxWithButtons(
            data_files_frame,
            "Data file mappings:",
            add_callback=self._add_data_file,
            height=4
        )
        self.widgets['data_files'].setToolTip("Include data files (format: 'source=destination', e.g., 'data/config.json=config.json')")
        data_files_layout.addWidget(self.widgets['data_files'])

        self.content_layout.addWidget(data_files_frame)

        # Data directories
        data_dirs_frame = QGroupBox("Data Directories")
        data_dirs_layout = QVBoxLayout(data_dirs_frame)

        self.widgets['data_dirs'] = ListBoxWithButtons(
            data_dirs_frame,
            "Directory mappings:",
            add_callback=self._add_data_dir,
            height=4
        )
        self.widgets['data_dirs'].setToolTip("Include entire directories (format: 'source=destination')")
        data_dirs_layout.addWidget(self.widgets['data_dirs'])

        self.content_layout.addWidget(data_dirs_frame)

        # Exclude patterns
        exclude_frame = QGroupBox("Exclusions")
        exclude_layout = QVBoxLayout(exclude_frame)

        self.widgets['exclude_patterns'] = ListBoxWithButtons(
            exclude_frame,
            "Patterns to exclude:",
            add_callback=self._add_exclude_pattern,
            height=4
        )
        self.widgets['exclude_patterns'].setToolTip("Exclude matching files (e.g., '*.pyc', '*.pyx', '__pycache__')")
        exclude_layout.addWidget(self.widgets['exclude_patterns'])

        self.content_layout.addWidget(exclude_frame)

    def _add_package_data(self):
        """Add package data pattern."""
        pattern, ok = QInputDialog.getText(
            self,
            "Add Package Data",
            "Enter package data pattern (e.g., 'myapp:*.json'):\nFormat: package:pattern"
        )
        return pattern if ok else None

    def _add_data_file(self):
        """Add data file mapping."""
        # Ask for source file
        source, _ = QFileDialog.getOpenFileName(self, "Select data file")
        if not source:
            return None

        # Ask for destination
        import os
        dest, ok = QInputDialog.getText(
            self,
            "Destination Path",
            f"Enter destination path for '{source}':",
            text=os.path.basename(source)
        )
        if not ok or not dest:
            return None

        return f"{source}={dest}"

    def _add_data_dir(self):
        """Add data directory mapping."""
        # Ask for source directory
        source = QFileDialog.getExistingDirectory(self, "Select data directory")
        if not source:
            return None

        # Ask for destination
        import os
        dest, ok = QInputDialog.getText(
            self,
            "Destination Path",
            f"Enter destination path for directory '{source}':",
            text=os.path.basename(source)
        )
        if not ok or not dest:
            return None

        return f"{source}={dest}"

    def _add_exclude_pattern(self):
        """Add exclusion pattern."""
        pattern, ok = QInputDialog.getText(
            self,
            "Add Exclusion Pattern",
            "Enter file pattern to exclude (e.g., '*.pyc', '__pycache__'):"
        )
        return pattern if ok else None

    def load_from_config(self):
        """Load values from config."""
        self.widgets['package_data'].set_items(
            self.config.get('data.package_data', [])
        )
        self.widgets['data_files'].set_items(
            self.config.get('data.data_files', [])
        )
        self.widgets['data_dirs'].set_items(
            self.config.get('data.data_dirs', [])
        )
        self.widgets['exclude_patterns'].set_items(
            self.config.get('data.exclude_patterns', [])
        )

    def save_to_config(self):
        """Save values to config."""
        self.config.set('data.package_data', self.widgets['package_data'].get_items())
        self.config.set('data.data_files', self.widgets['data_files'].get_items())
        self.config.set('data.data_dirs', self.widgets['data_dirs'].get_items())
        self.config.set('data.exclude_patterns', self.widgets['exclude_patterns'].get_items())
