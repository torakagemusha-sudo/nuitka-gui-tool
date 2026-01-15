"""
Output and plugins tab for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox,
    QScrollArea, QGroupBox, QFrame, QListWidget, QPushButton,
    QAbstractItemView
)
from PySide6.QtCore import Qt
from ..utils.constants import COMMON_PLUGINS, PROGRESS_BAR_MODES
from .widgets import add_tooltip


class TabOutput(QWidget):
    """Tab for output control and plugin management."""

    def __init__(self, parent, config):
        """
        Initialize output tab.

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
        """Create widgets for output tab."""
        # Output control section
        output_frame = QGroupBox("Output Control")
        output_layout = QVBoxLayout(output_frame)
        output_layout.setSpacing(8)

        self.widgets['quiet'] = QCheckBox("Quiet mode (minimal output)")
        output_layout.addWidget(self.widgets['quiet'])

        self.widgets['verbose'] = QCheckBox("Verbose output")
        output_layout.addWidget(self.widgets['verbose'])

        self.widgets['show_progress'] = QCheckBox("Show progress bar")
        self.widgets['show_progress'].setChecked(True)
        output_layout.addWidget(self.widgets['show_progress'])

        # Progress bar mode
        progress_frame = QWidget()
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(8)

        progress_label = QLabel("Progress Style:")
        progress_layout.addWidget(progress_label)

        self.widgets['progress_mode'] = QComboBox()
        self.widgets['progress_mode'].addItems([label for label, _ in PROGRESS_BAR_MODES])
        self.widgets['progress_mode'].setCurrentText('Auto')
        self.widgets['progress_mode'].setFixedWidth(120)
        progress_layout.addWidget(self.widgets['progress_mode'])
        progress_layout.addStretch(1)

        output_layout.addWidget(progress_frame)

        self.widgets['show_memory'] = QCheckBox("Show memory usage")
        output_layout.addWidget(self.widgets['show_memory'])

        self.content_layout.addWidget(output_frame)

        # Plugins section
        plugins_frame = QGroupBox("Plugins")
        plugins_layout = QVBoxLayout(plugins_frame)
        plugins_layout.setSpacing(8)

        # Create two-column layout for available and enabled plugins
        columns_frame = QWidget()
        columns_layout = QHBoxLayout(columns_frame)
        columns_layout.setContentsMargins(0, 0, 0, 0)
        columns_layout.setSpacing(10)

        # Available plugins (left)
        available_frame = QWidget()
        available_layout = QVBoxLayout(available_frame)
        available_layout.setContentsMargins(0, 0, 0, 0)
        available_layout.setSpacing(4)

        available_label = QLabel("Available Plugins:")
        available_layout.addWidget(available_label)

        self.available_listbox = QListWidget()
        self.available_listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # Set approximate height for 10 items
        font_metrics = self.available_listbox.fontMetrics()
        item_height = font_metrics.height() + 6
        self.available_listbox.setMinimumHeight(10 * item_height + 10)

        # Populate available plugins
        for plugin_name, description in COMMON_PLUGINS:
            self.available_listbox.addItem(plugin_name)
            # Set tooltip on the item
            item = self.available_listbox.item(self.available_listbox.count() - 1)
            item.setToolTip(description)

        available_layout.addWidget(self.available_listbox, 1)
        columns_layout.addWidget(available_frame, 1)

        # Buttons in the middle
        btn_frame = QWidget()
        btn_layout = QVBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        btn_layout.addStretch(1)

        enable_btn = QPushButton("Enable ->")
        enable_btn.clicked.connect(self._enable_plugin)
        btn_layout.addWidget(enable_btn)

        disable_btn = QPushButton("<- Disable")
        disable_btn.clicked.connect(self._disable_plugin)
        btn_layout.addWidget(disable_btn)

        btn_layout.addStretch(1)
        columns_layout.addWidget(btn_frame)

        # Enabled plugins (right)
        enabled_frame = QWidget()
        enabled_layout = QVBoxLayout(enabled_frame)
        enabled_layout.setContentsMargins(0, 0, 0, 0)
        enabled_layout.setSpacing(4)

        enabled_label = QLabel("Enabled Plugins:")
        enabled_layout.addWidget(enabled_label)

        self.enabled_listbox = QListWidget()
        self.enabled_listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.enabled_listbox.setMinimumHeight(10 * item_height + 10)

        enabled_layout.addWidget(self.enabled_listbox, 1)
        columns_layout.addWidget(enabled_frame, 1)

        plugins_layout.addWidget(columns_frame)

        self.content_layout.addWidget(plugins_frame)

        # Warning section
        warn_frame = QGroupBox("Warnings")
        warn_layout = QVBoxLayout(warn_frame)
        warn_layout.setSpacing(8)

        self.widgets['warn_implicit_exceptions'] = QCheckBox("Warn about implicit exceptions")
        warn_layout.addWidget(self.widgets['warn_implicit_exceptions'])

        self.widgets['warn_unusual_code'] = QCheckBox("Warn about unusual code")
        warn_layout.addWidget(self.widgets['warn_unusual_code'])

        self.widgets['assume_yes_for_downloads'] = QCheckBox("Assume yes for downloads")
        add_tooltip(self.widgets['assume_yes_for_downloads'],
                    "Automatically download dependencies without prompting")
        warn_layout.addWidget(self.widgets['assume_yes_for_downloads'])

        self.content_layout.addWidget(warn_frame)

    def _enable_plugin(self):
        """Enable selected plugin(s)."""
        selected_items = self.available_listbox.selectedItems()
        # Get list of already enabled plugins
        enabled_plugins = [
            self.enabled_listbox.item(i).text()
            for i in range(self.enabled_listbox.count())
        ]

        for item in selected_items:
            plugin = item.text()
            if plugin not in enabled_plugins:
                self.enabled_listbox.addItem(plugin)

    def _disable_plugin(self):
        """Disable selected plugin(s)."""
        selected_items = self.enabled_listbox.selectedItems()
        for item in selected_items:
            row = self.enabled_listbox.row(item)
            self.enabled_listbox.takeItem(row)

    def load_from_config(self):
        """Load values from config."""
        self.widgets['quiet'].setChecked(self.config.get('output.quiet', False))
        self.widgets['verbose'].setChecked(self.config.get('output.verbose', False))
        self.widgets['show_progress'].setChecked(self.config.get('output.show_progress', True))

        progress_mode = self.config.get('output.progress_mode', 'auto')
        for label, value in PROGRESS_BAR_MODES:
            if value == progress_mode:
                self.widgets['progress_mode'].setCurrentText(label)
                break

        self.widgets['show_memory'].setChecked(self.config.get('output.show_memory', False))

        # Plugins
        enabled_plugins = self.config.get('plugins.enabled', [])
        self.enabled_listbox.clear()
        for plugin in enabled_plugins:
            self.enabled_listbox.addItem(plugin)

        self.widgets['warn_implicit_exceptions'].setChecked(
            self.config.get('output.warn_implicit_exceptions', False)
        )
        self.widgets['warn_unusual_code'].setChecked(
            self.config.get('output.warn_unusual_code', False)
        )
        self.widgets['assume_yes_for_downloads'].setChecked(
            self.config.get('output.assume_yes_for_downloads', False)
        )

    def save_to_config(self):
        """Save values to config."""
        self.config.set('output.quiet', self.widgets['quiet'].isChecked())
        self.config.set('output.verbose', self.widgets['verbose'].isChecked())
        self.config.set('output.show_progress', self.widgets['show_progress'].isChecked())

        # Map progress mode label to value
        progress_label = self.widgets['progress_mode'].currentText()
        for label, value in PROGRESS_BAR_MODES:
            if label == progress_label:
                self.config.set('output.progress_mode', value)
                break

        self.config.set('output.show_memory', self.widgets['show_memory'].isChecked())

        # Plugins
        enabled_plugins = [
            self.enabled_listbox.item(i).text()
            for i in range(self.enabled_listbox.count())
        ]
        self.config.set('plugins.enabled', enabled_plugins)

        self.config.set('output.warn_implicit_exceptions',
                        self.widgets['warn_implicit_exceptions'].isChecked())
        self.config.set('output.warn_unusual_code',
                        self.widgets['warn_unusual_code'].isChecked())
        self.config.set('output.assume_yes_for_downloads',
                        self.widgets['assume_yes_for_downloads'].isChecked())
