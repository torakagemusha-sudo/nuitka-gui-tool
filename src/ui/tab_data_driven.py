"""
Data-driven settings tab.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QSpinBox,
    QRadioButton,
    QButtonGroup,
    QToolButton,
)

from .widgets import FileSelectFrame, ListBoxWithButtons, RiskBadge, ImpactTag, PluginPicker
from ..core.setting_definitions import SettingRegistry
from ..core.platform_detector import PlatformDetector


class DataDrivenTab(QWidget):
    settingChanged = Signal(str)
    explainRequested = Signal(str)

    def __init__(self, parent, config, registry: SettingRegistry, tab_id: str):
        super().__init__(parent)
        self.config = config
        self.registry = registry
        self.tab_id = tab_id
        self.controls: Dict[str, Dict[str, object]] = {}
        self.rows: Dict[str, QWidget] = {}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(16)

        self._build_sections()
        self.content_layout.addStretch(1)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def _build_sections(self):
        tab = self._get_tab_data()
        if not tab:
            return

        for section in tab.get("sections", []):
            section_frame = QFrame()
            section_frame.setProperty("class", "card")
            section_layout = QVBoxLayout(section_frame)
            section_layout.setContentsMargins(12, 12, 12, 12)
            section_layout.setSpacing(10)

            title = QLabel(section.get("title", ""))
            title.setProperty("class", "sectiontitle")
            section_layout.addWidget(title)

            for setting in section.get("settings", []):
                if not self._platform_ok(setting.get("platform_constraints")):
                    continue
                row = self._build_setting_row(setting)
                section_layout.addWidget(row)
                key = setting.get("key", "")
                if key:
                    self.rows[key] = row

            self.content_layout.addWidget(section_frame)

    def _platform_ok(self, constraints: Optional[Dict[str, List[str]]]) -> bool:
        if not constraints:
            return True
        os_list = constraints.get("os")
        if os_list:
            current = PlatformDetector.get_platform()
            return current in os_list
        return True

    def _build_setting_row(self, setting: Dict[str, object]) -> QWidget:
        key = setting.get("key", "")
        label = setting.get("label", "")
        effect = setting.get("effect", "")
        risk = setting.get("risk", "safe")
        impacts = setting.get("impact", [])

        row = QFrame()
        layout = QVBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(8)

        label_widget = QLabel(label)
        top_layout.addWidget(label_widget)

        control_widget = self._create_control(setting)
        top_layout.addWidget(control_widget, 1)

        explain_btn = QToolButton()
        explain_btn.setText("Explain")
        explain_btn.clicked.connect(lambda: self.explainRequested.emit(key))
        top_layout.addWidget(explain_btn)

        layout.addWidget(top)

        meta = QWidget()
        meta_layout = QHBoxLayout(meta)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(6)

        effect_label = QLabel(effect)
        effect_label.setProperty("class", "muted")
        meta_layout.addWidget(effect_label, 1)

        badge = RiskBadge(risk)
        meta_layout.addWidget(badge)

        for tag in impacts:
            meta_layout.addWidget(ImpactTag(tag))

        meta_layout.addStretch(1)
        layout.addWidget(meta)

        return row

    def _create_control(self, setting: Dict[str, object]) -> QWidget:
        key = setting.get("key", "")
        control = setting.get("control", {})
        control_type = control.get("type", "text")

        if control_type in ("file", "directory"):
            widget = FileSelectFrame(
                self, "", mode="directory" if control_type == "directory" else "file",
                file_types=control.get("file_types")
            )
            widget.entry.textChanged.connect(lambda _, k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        if control_type == "text":
            widget = QLineEdit()
            widget.textChanged.connect(lambda _, k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        if control_type == "checkbox":
            widget = QCheckBox()
            widget.stateChanged.connect(lambda _, k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        if control_type == "combo":
            widget = QComboBox()
            options = control.get("options", [])
            for opt in options:
                widget.addItem(opt.get("label"), opt.get("value"))
            widget.currentIndexChanged.connect(lambda _, k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        if control_type == "spin":
            widget = QSpinBox()
            widget.setRange(control.get("min", 0), control.get("max", 999))
            widget.valueChanged.connect(lambda _, k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        if control_type == "radio":
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)
            group_layout.setContentsMargins(0, 0, 0, 0)
            group_layout.setSpacing(4)
            button_group = QButtonGroup(group_widget)
            for opt in control.get("options", []):
                rb = QRadioButton(opt.get("label"))
                rb.setProperty("value", opt.get("value"))
                rb.toggled.connect(lambda checked, k=key: checked and self._on_change(k))
                button_group.addButton(rb)
                group_layout.addWidget(rb)
            self.controls[key] = {
                "type": control_type,
                "widget": group_widget,
                "group": button_group,
            }
            return group_widget

        if control_type == "multi_check":
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)
            group_layout.setContentsMargins(0, 0, 0, 0)
            group_layout.setSpacing(4)
            checkboxes = []
            for opt in control.get("options", []):
                cb = QCheckBox(opt.get("label"))
                cb.setProperty("value", opt.get("value"))
                cb.stateChanged.connect(lambda _, k=key: self._on_change(k))
                checkboxes.append(cb)
                group_layout.addWidget(cb)
            self.controls[key] = {"type": control_type, "widget": group_widget, "items": checkboxes}
            return group_widget

        if control_type == "list":
            widget = ListBoxWithButtons(self, "", height=5)
            widget.itemsChanged.connect(lambda k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        if control_type == "plugin_picker":
            widget = PluginPicker(self)
            widget.itemsChanged.connect(lambda k=key: self._on_change(k))
            self.controls[key] = {"type": control_type, "widget": widget}
            return widget

        widget = QLineEdit()
        widget.textChanged.connect(lambda _, k=key: self._on_change(k))
        self.controls[key] = {"type": "text", "widget": widget}
        return widget

    def _on_change(self, key: str):
        value = self.get_value(key)
        self.config.set(key, value)
        self.settingChanged.emit(key)

    def get_value(self, key: str):
        control = self.controls.get(key)
        if not control:
            return None
        control_type = control["type"]
        widget = control["widget"]

        if control_type in ("file", "directory"):
            return widget.get_path()
        if control_type == "text":
            return widget.text()
        if control_type == "checkbox":
            return widget.isChecked()
        if control_type == "combo":
            return widget.currentData()
        if control_type == "spin":
            return widget.value()
        if control_type == "radio":
            for button in control["group"].buttons():
                if button.isChecked():
                    return button.property("value")
            return None
        if control_type == "multi_check":
            values = []
            for cb in control.get("items", []):
                if cb.isChecked():
                    values.append(cb.property("value"))
            return values
        if control_type == "list":
            return widget.get_items()
        if control_type == "plugin_picker":
            return widget.get_items()
        return None

    def set_value(self, key: str, value):
        control = self.controls.get(key)
        if not control:
            return
        control_type = control["type"]
        widget = control["widget"]

        if control_type in ("file", "directory"):
            widget.set_path(value or "")
        elif control_type == "text":
            widget.setText(value or "")
        elif control_type == "checkbox":
            widget.setChecked(bool(value))
        elif control_type == "combo":
            index = widget.findData(value)
            if index >= 0:
                widget.setCurrentIndex(index)
        elif control_type == "spin":
            widget.setValue(int(value or 0))
        elif control_type == "radio":
            for button in control["group"].buttons():
                if button.property("value") == value:
                    button.setChecked(True)
                    break
        elif control_type == "multi_check":
            values = set(value or [])
            for cb in control.get("items", []):
                cb.setChecked(cb.property("value") in values)
        elif control_type == "list":
            widget.set_items(value or [])
        elif control_type == "plugin_picker":
            widget.set_items(value or [])

    def load_from_config(self):
        tab = self._get_tab_data()
        if not tab:
            return
        for section in tab.get("sections", []):
            for setting in section.get("settings", []):
                key = setting.get("key", "")
                if key:
                    self.set_value(key, self.config.get(key))

    def filter_settings(self, query: str):
        query = (query or "").strip().lower()
        for key, row in self.rows.items():
            definition = self.registry.get_setting(key)
            if not definition:
                row.setVisible(True)
                continue
            flag_terms = []
            for mapping in definition.flag_mapping:
                flag = mapping.get("flag")
                if flag:
                    flag_terms.append(flag)
            haystack = " ".join(
                [
                    definition.key,
                    definition.label,
                    definition.description,
                    definition.effect,
                    " ".join(flag_terms),
                ]
            ).lower()
            row.setVisible(query in haystack if query else True)

    def _get_tab_data(self) -> Optional[Dict[str, object]]:
        for tab in self.registry.get_tabs():
            if tab.get("id") == self.tab_id:
                return tab
        return None
