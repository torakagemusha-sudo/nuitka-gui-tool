"""
Custom reusable widgets for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
    QListWidget, QFileDialog, QInputDialog, QAbstractItemView, QToolButton
)
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve

from ..utils.constants import COMMON_PLUGINS
from PySide6.QtGui import QFont


class FileSelectFrame(QWidget):
    """Widget with label, entry, and browse button for file/folder selection."""

    pathChanged = Signal(str)  # Signal emitted when path changes

    def __init__(self, parent, label, mode='file', file_types=None):
        """
        Initialize file select frame.

        Args:
            parent: Parent widget
            label: Label text
            mode: 'file', 'files', or 'directory'
            file_types: String for file filter (e.g., 'Python files (*.py);;All files (*.*)')
        """
        super().__init__(parent)

        self.mode = mode
        self.file_types = file_types or 'All files (*.*)'

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        self.label = QLabel(label, self)
        layout.addWidget(self.label)

        # Entry
        self.entry = QLineEdit(self)
        self.entry.setMinimumWidth(300)
        self.entry.textChanged.connect(self.pathChanged.emit)

        # Accessibility: Set accessible names and descriptions
        self.entry.setAccessibleName(f"{label} path")
        self.entry.setAccessibleDescription(f"Enter or browse for a {mode}")

        layout.addWidget(self.entry, 1)  # Stretch factor 1

        # Browse button
        self.browse_btn = QPushButton("Browse...", self)
        self.browse_btn.clicked.connect(self._browse)

        # Accessibility: Set accessible names for browse button
        self.browse_btn.setAccessibleName(f"Browse for {label}")
        self.browse_btn.setAccessibleDescription(f"Open {mode} selection dialog")

        layout.addWidget(self.browse_btn)

    def _browse(self):
        """Handle browse button click."""
        if self.mode == 'file':
            path, _ = QFileDialog.getOpenFileName(
                self,
                f"Select {self.label.text()}",
                "",
                self.file_types
            )
            if path:
                self.entry.setText(path)
        elif self.mode == 'files':
            paths, _ = QFileDialog.getOpenFileNames(
                self,
                f"Select {self.label.text()}",
                "",
                self.file_types
            )
            if paths:
                self.entry.setText(';'.join(paths))
        elif self.mode == 'directory':
            path = QFileDialog.getExistingDirectory(
                self,
                f"Select {self.label.text()}"
            )
            if path:
                self.entry.setText(path)

    def get_path(self):
        """Get current path value."""
        return self.entry.text()

    def set_path(self, path):
        """Set path value."""
        self.entry.setText(path)


class ListBoxWithButtons(QWidget):
    """List widget with add/remove buttons."""

    itemsChanged = Signal()  # Signal emitted when items change

    def __init__(self, parent, label, add_callback=None, height=6):
        """
        Initialize listbox with buttons.

        Args:
            parent: Parent widget
            label: Label text
            add_callback: Callback for add button (should return item to add or None)
            height: Approximate height in items (affects size hint)
        """
        super().__init__(parent)

        self.add_callback = add_callback

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Label
        label_widget = QLabel(label, self)
        layout.addWidget(label_widget)

        # List widget
        self.listbox = QListWidget(self)
        self.listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # Set approximate height
        font_metrics = self.listbox.fontMetrics()
        item_height = font_metrics.height() + 6  # padding
        self.listbox.setMinimumHeight(height * item_height + 10)

        # Accessibility: Set accessible names and descriptions
        self.listbox.setAccessibleName(label)
        self.listbox.setAccessibleDescription(f"List of {label.lower()}")

        layout.addWidget(self.listbox, 1)  # Stretch factor 1

        # Button frame
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.add_btn = QPushButton("Add", self)
        self.add_btn.setProperty("class", "compact")
        self.add_btn.clicked.connect(self._add_item)

        # Accessibility: Set accessible names for buttons
        self.add_btn.setAccessibleName(f"Add {label}")
        self.add_btn.setAccessibleDescription(f"Add new item to {label.lower()}")

        btn_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Remove", self)
        self.remove_btn.setProperty("class", "compact")
        self.remove_btn.clicked.connect(self._remove_selected)

        # Accessibility: Set accessible names for remove button
        self.remove_btn.setAccessibleName(f"Remove selected {label}")
        self.remove_btn.setAccessibleDescription(f"Remove selected items from {label.lower()}")

        btn_layout.addWidget(self.remove_btn)

        btn_layout.addStretch(1)

        layout.addLayout(btn_layout)

    def _add_item(self):
        """Handle add button click."""
        if self.add_callback:
            item = self.add_callback()
            if item:
                self.add_item(item)
        else:
            # Simple dialog
            item, ok = QInputDialog.getText(self, "Add Item", "Enter item:")
            if ok and item:
                self.add_item(item)

    def _remove_selected(self):
        """Remove selected items."""
        selected_items = self.listbox.selectedItems()
        for item in selected_items:
            row = self.listbox.row(item)
            self.listbox.takeItem(row)
        self.itemsChanged.emit()

    def add_item(self, item):
        """Add an item to the listbox."""
        self.listbox.addItem(item)
        self.itemsChanged.emit()

    def remove_item(self, item):
        """Remove an item from the listbox."""
        items = self.listbox.findItems(item, Qt.MatchExactly)
        for list_item in items:
            row = self.listbox.row(list_item)
            self.listbox.takeItem(row)
        self.itemsChanged.emit()

    def get_items(self):
        """Get all items as a list."""
        return [self.listbox.item(i).text() for i in range(self.listbox.count())]

    def set_items(self, items):
        """Set all items (replaces existing)."""
        self.listbox.clear()
        for item in items:
            self.listbox.addItem(item)
        self.itemsChanged.emit()

    def clear(self):
        """Clear all items."""
        self.listbox.clear()
        self.itemsChanged.emit()


class CollapsibleFrame(QWidget):
    """Widget that can be collapsed/expanded with smooth animation."""

    def __init__(self, parent, title):
        """
        Initialize collapsible frame.

        Args:
            parent: Parent widget
            title: Frame title
        """
        super().__init__(parent)

        self.is_expanded = True

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Toggle button
        self.toggle_btn = QPushButton(f"▼ {title}", self)
        self.toggle_btn.setProperty("class", "secondary")
        font = self.toggle_btn.font()
        font.setWeight(QFont.DemiBold)
        self.toggle_btn.setFont(font)
        self.toggle_btn.clicked.connect(self.toggle)
        self.toggle_btn.setFlat(True)
        main_layout.addWidget(self.toggle_btn)

        # Content frame
        self.content = QWidget(self)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.addWidget(self.content)

        # Animation for smooth collapse/expand
        self.animation = QPropertyAnimation(self.content, b"maximumHeight")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def toggle(self):
        """Toggle collapsed/expanded state with animation."""
        if self.is_expanded:
            # Collapse
            self.animation.setStartValue(self.content.height())
            self.animation.setEndValue(0)
            self.animation.start()
            text = self.toggle_btn.text()
            self.toggle_btn.setText(text.replace('▼', '▶'))
            self.is_expanded = False
        else:
            # Expand
            self.content.setMaximumHeight(16777215)  # QWIDGETSIZE_MAX
            content_height = self.content.sizeHint().height()
            self.content.setMaximumHeight(0)
            self.animation.setStartValue(0)
            self.animation.setEndValue(content_height)
            self.animation.start()
            text = self.toggle_btn.text()
            self.toggle_btn.setText(text.replace('▶', '▼'))
            self.is_expanded = True


class TooltipLabel(QLabel):
    """Label with built-in tooltip support (uses Qt's native tooltip system)."""

    def __init__(self, parent, text, tooltip):
        """
        Initialize tooltip label.

        Args:
            parent: Parent widget
            text: Label text
            tooltip: Tooltip text
        """
        super().__init__(text, parent)
        self.setToolTip(tooltip)


def add_tooltip(widget, text):
    """
    Add tooltip to any widget (uses Qt's native tooltip system).

    Args:
        widget: Widget to add tooltip to
        text: Tooltip text
    """
    widget.setToolTip(text)


class RiskBadge(QLabel):
    """Risk badge label with level."""

    def __init__(self, level, parent=None):
        super().__init__(level.title(), parent)
        self.setProperty("class", "risk")
        self.setProperty("risk", level)


class ImpactTag(QLabel):
    """Impact tag label."""

    def __init__(self, text, parent=None):
        super().__init__(text.title(), parent)
        self.setProperty("class", "impact")


class PluginPicker(QWidget):
    """Two-list plugin selector for enabled plugins."""

    itemsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        available_frame = QVBoxLayout()
        available_label = QLabel("Available")
        available_frame.addWidget(available_label)
        self.available = QListWidget()
        self.available.setSelectionMode(QAbstractItemView.ExtendedSelection)
        for plugin_name, description in COMMON_PLUGINS:
            self.available.addItem(plugin_name)
            item = self.available.item(self.available.count() - 1)
            item.setToolTip(description)
        available_frame.addWidget(self.available, 1)

        buttons = QVBoxLayout()
        buttons.addStretch(1)
        add_btn = QPushButton("Enable ->")
        add_btn.clicked.connect(self.enable_selected)
        buttons.addWidget(add_btn)
        remove_btn = QPushButton("<- Disable")
        remove_btn.clicked.connect(self.disable_selected)
        buttons.addWidget(remove_btn)
        buttons.addStretch(1)

        enabled_frame = QVBoxLayout()
        enabled_label = QLabel("Enabled")
        enabled_frame.addWidget(enabled_label)
        self.enabled = QListWidget()
        self.enabled.setSelectionMode(QAbstractItemView.ExtendedSelection)
        enabled_frame.addWidget(self.enabled, 1)

        layout.addLayout(available_frame, 1)
        layout.addLayout(buttons)
        layout.addLayout(enabled_frame, 1)

    def enable_selected(self):
        selected = self.available.selectedItems()
        existing = {self.enabled.item(i).text() for i in range(self.enabled.count())}
        for item in selected:
            if item.text() not in existing:
                self.enabled.addItem(item.text())
        self.itemsChanged.emit()

    def disable_selected(self):
        for item in self.enabled.selectedItems():
            row = self.enabled.row(item)
            self.enabled.takeItem(row)
        self.itemsChanged.emit()

    def set_items(self, items):
        self.enabled.clear()
        for item in items:
            self.enabled.addItem(item)
        self.itemsChanged.emit()

    def get_items(self):
        return [self.enabled.item(i).text() for i in range(self.enabled.count())]
