"""
Modules and packages tab for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QScrollArea, QGroupBox, QFrame, QInputDialog
)
from PySide6.QtCore import Qt
from .widgets import ListBoxWithButtons, add_tooltip


class TabModules(QWidget):
    """Tab for module and package inclusion settings."""

    def __init__(self, parent, config):
        """
        Initialize modules tab.

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
        """Create widgets for modules tab."""
        # Import following section
        import_frame = QGroupBox("Import Following")
        import_layout = QVBoxLayout(import_frame)
        import_layout.setSpacing(8)

        self.widgets['follow_imports'] = QCheckBox("Follow all imports (recommended for standalone/onefile)")
        self.widgets['follow_imports'].setChecked(True)
        self.widgets['follow_imports'].setToolTip("Automatically include all imported modules")
        import_layout.addWidget(self.widgets['follow_imports'])

        self.widgets['follow_stdlib'] = QCheckBox("Follow standard library imports")
        self.widgets['follow_stdlib'].setToolTip("Include standard library modules that are imported")
        import_layout.addWidget(self.widgets['follow_stdlib'])

        self.content_layout.addWidget(import_frame)

        # Include packages
        pkg_frame = QGroupBox("Include Packages")
        pkg_layout = QVBoxLayout(pkg_frame)

        self.widgets['include_packages'] = ListBoxWithButtons(
            pkg_frame,
            "Packages to include:",
            add_callback=self._add_package,
            height=5
        )
        self.widgets['include_packages'].setToolTip("Force inclusion of entire packages (e.g., 'numpy', 'pandas')")
        pkg_layout.addWidget(self.widgets['include_packages'])

        self.content_layout.addWidget(pkg_frame)

        # Include modules
        mod_frame = QGroupBox("Include Modules")
        mod_layout = QVBoxLayout(mod_frame)

        self.widgets['include_modules'] = ListBoxWithButtons(
            mod_frame,
            "Modules to include:",
            add_callback=self._add_module,
            height=5
        )
        self.widgets['include_modules'].setToolTip("Force inclusion of specific modules (e.g., 'myapp.utils')")
        mod_layout.addWidget(self.widgets['include_modules'])

        self.content_layout.addWidget(mod_frame)

        # Don't follow modules
        nofollow_frame = QGroupBox("Exclude from Following")
        nofollow_layout = QVBoxLayout(nofollow_frame)

        self.widgets['nofollow_to'] = ListBoxWithButtons(
            nofollow_frame,
            "Don't follow these modules:",
            add_callback=self._add_nofollow,
            height=5
        )
        self.widgets['nofollow_to'].setToolTip("Modules to exclude from import following (supports wildcards: '*.tests')")
        nofollow_layout.addWidget(self.widgets['nofollow_to'])

        self.content_layout.addWidget(nofollow_frame)

    def _add_package(self):
        """Add a package."""
        package, ok = QInputDialog.getText(
            self,
            "Add Package",
            "Enter package name (e.g., 'numpy', 'pandas'):"
        )
        return package if ok else None

    def _add_module(self):
        """Add a module."""
        module, ok = QInputDialog.getText(
            self,
            "Add Module",
            "Enter module name (e.g., 'myapp.utils', 'os.path'):"
        )
        return module if ok else None

    def _add_nofollow(self):
        """Add a module to exclude."""
        module, ok = QInputDialog.getText(
            self,
            "Add Exclusion",
            "Enter module pattern (e.g., '*.tests', 'debug.*'):"
        )
        return module if ok else None

    def load_from_config(self):
        """Load values from config."""
        self.widgets['follow_imports'].setChecked(
            self.config.get('modules.follow_imports', True)
        )
        self.widgets['follow_stdlib'].setChecked(
            self.config.get('modules.follow_stdlib', False)
        )

        self.widgets['include_packages'].set_items(
            self.config.get('modules.include_packages', [])
        )
        self.widgets['include_modules'].set_items(
            self.config.get('modules.include_modules', [])
        )
        self.widgets['nofollow_to'].set_items(
            self.config.get('modules.nofollow_to', [])
        )

    def save_to_config(self):
        """Save values to config."""
        self.config.set('modules.follow_imports', self.widgets['follow_imports'].isChecked())
        self.config.set('modules.follow_stdlib', self.widgets['follow_stdlib'].isChecked())

        self.config.set('modules.include_packages', self.widgets['include_packages'].get_items())
        self.config.set('modules.include_modules', self.widgets['include_modules'].get_items())
        self.config.set('modules.nofollow_to', self.widgets['nofollow_to'].get_items())
