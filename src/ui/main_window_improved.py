"""
Improved main window with engineer-focused instrument panel UI (PySide6).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget,
    QPlainTextEdit, QSplitter, QFrame, QLineEdit, QComboBox, QListWidget,
    QStackedWidget, QTableWidget, QTableWidgetItem, QSizePolicy, QApplication
)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPainter, QColor, QDesktopServices
import platform
import sys
from pathlib import Path
import hashlib

from .tab_data_driven import DataDrivenTab
from ..core.flag_plan import compile_flag_plan, render_command_string
from ..core.diffing import diff_flag_plans
from ..core.setting_definitions import load_setting_definitions
from ..core.presets import apply_preset, get_preset
from ..core.platform_detector import PlatformDetector
from ..utils.constants import APP_NAME


class StatusIndicator(QWidget):
    """Custom widget for drawing a colored status circle."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(10, 10)
        self.color = QColor("#3A7C3A")

    def set_color(self, color_hex):
        """Set the indicator color."""
        self.color = QColor(color_hex)
        self.update()

    def paintEvent(self, event):
        """Paint the status circle."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 8, 8)


class MainWindow(QWidget):
    """Improved main window with instrument panel UX/UI."""

    def __init__(self, parent, config, app):
        super().__init__(parent)
        self.config = config
        self.app = app

        self.registry = load_setting_definitions()
        self.tab_ids = [tab.get("id") for tab in self.registry.get_tabs()]
        self.tab_labels = [tab.get("label") for tab in self.registry.get_tabs()]
        self.current_plan = None
        self.last_success_plan = None

        self.create_ui()
        self.load_from_config()

    def create_ui(self):
        """Create the main UI layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        self.top_header = self.create_top_header()
        main_layout.addWidget(self.top_header)

        self.status_strip = self.create_status_strip()
        main_layout.addWidget(self.status_strip)

        self.main_splitter = QSplitter(Qt.Vertical, self)
        main_layout.addWidget(self.main_splitter, 1)

        self.workspace_splitter = QSplitter(Qt.Horizontal, self)
        self.main_splitter.addWidget(self.workspace_splitter)

        self.left_nav = self.create_left_nav()
        self.settings_center = self.create_settings_center()
        self.inspector_panel = self.create_inspector_panel()

        self.workspace_splitter.addWidget(self.left_nav)
        self.workspace_splitter.addWidget(self.settings_center)
        self.workspace_splitter.addWidget(self.inspector_panel)
        self.workspace_splitter.setStretchFactor(0, 1)
        self.workspace_splitter.setStretchFactor(1, 3)
        self.workspace_splitter.setStretchFactor(2, 2)

        self.console_dock = self.create_console_dock()
        self.main_splitter.addWidget(self.console_dock)

        self.main_splitter.setStretchFactor(0, 4)
        self.main_splitter.setStretchFactor(1, 2)

        self.tab_list.setCurrentRow(0)

    def create_top_header(self):
        """Create the top app header with project context and actions."""
        header = QFrame()
        header.setProperty("class", "topbar")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        left = QWidget()
        left_layout = QHBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        app_label = QLabel(APP_NAME)
        app_label.setProperty("class", "appname")
        left_layout.addWidget(app_label)

        project_label = QLabel("Project")
        project_label.setProperty("class", "muted")
        left_layout.addWidget(project_label)

        self.project_path = QLineEdit()
        self.project_path.setReadOnly(True)
        self.project_path.setPlaceholderText("Select a project or config")
        self.project_path.setMinimumWidth(260)
        left_layout.addWidget(self.project_path, 1)

        profile_label = QLabel("Profile")
        profile_label.setProperty("class", "muted")
        left_layout.addWidget(profile_label)

        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Default"])
        self.profile_combo.setMinimumWidth(120)
        left_layout.addWidget(self.profile_combo)

        layout.addWidget(left, 2)

        center = QWidget()
        center_layout = QHBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(8)

        preset_label = QLabel("Preset")
        preset_label.setProperty("class", "muted")
        center_layout.addWidget(preset_label)

        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Standalone GUI App (recommended)",
            "CLI Tool (console on)",
            "Onefile Distribution",
            "Debug / Trace Build",
            "Minimal Size",
            "Max Compatibility",
        ])
        self.preset_combo.setMinimumWidth(200)
        center_layout.addWidget(self.preset_combo)

        apply_btn = QPushButton("Apply")
        apply_btn.setProperty("class", "ghost")
        apply_btn.clicked.connect(self.apply_preset_placeholder)
        center_layout.addWidget(apply_btn)

        layout.addWidget(center, 2)

        right = QWidget()
        right_layout = QHBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)

        open_btn = QPushButton("Open Config")
        open_btn.setProperty("class", "ghost")
        open_btn.clicked.connect(self.app.on_load_config)
        right_layout.addWidget(open_btn)

        save_btn = QPushButton("Save Config")
        save_btn.setProperty("class", "ghost")
        save_btn.clicked.connect(self.app.on_save_config)
        right_layout.addWidget(save_btn)

        export_btn = QPushButton("Export")
        export_btn.setProperty("class", "ghost")
        export_btn.clicked.connect(self.export_placeholder)
        right_layout.addWidget(export_btn)

        help_btn = QPushButton("Help")
        help_btn.setProperty("class", "ghost")
        help_btn.clicked.connect(self.app.open_nuitka_docs)
        right_layout.addWidget(help_btn)

        layout.addWidget(right, 1, Qt.AlignRight)

        return header

    def create_status_strip(self):
        """Create a thin status strip with environment and warnings."""
        strip = QFrame()
        strip.setProperty("class", "statusstrip")
        layout = QHBoxLayout(strip)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(12)

        self.status_indicator = StatusIndicator()
        layout.addWidget(self.status_indicator)

        self.status_label = QLabel("Ready")
        self.status_label.setProperty("class", "status")
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        python_exe = sys.executable
        nuitka_version = PlatformDetector.get_nuitka_version()
        os_arch = f"{platform.system()} / {platform.machine()}"
        compiler = PlatformDetector.get_default_compiler()

        env_label = QLabel(f"Python: {python_exe}")
        env_label.setProperty("class", "muted")
        layout.addWidget(env_label)

        nuitka_label = QLabel(nuitka_version)
        nuitka_label.setProperty("class", "muted")
        layout.addWidget(nuitka_label)

        os_label = QLabel(os_arch)
        os_label.setProperty("class", "muted")
        layout.addWidget(os_label)

        compiler_label = QLabel(f"Compiler: {compiler}")
        compiler_label.setProperty("class", "muted")
        layout.addWidget(compiler_label)

        self.repro_label = QLabel("Repro: Floating")
        self.repro_label.setProperty("class", "pill")
        layout.addWidget(self.repro_label)

        self.warnings_btn = QPushButton("Warnings: 0")
        self.warnings_btn.setProperty("class", "ghost")
        self.warnings_btn.clicked.connect(self.focus_diagnostics)
        layout.addWidget(self.warnings_btn)

        return strip

    def create_left_nav(self):
        """Create the navigation panel with tabs and section index."""
        panel = QFrame()
        panel.setProperty("class", "leftnav")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        nav_title = QLabel("Navigation")
        nav_title.setProperty("class", "sectiontitle")
        layout.addWidget(nav_title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search settings or flags")        
        self.search_input.textChanged.connect(self.on_search_changed)
        layout.addWidget(self.search_input)

        self.tab_list = QListWidget()
        self.tab_list.addItems(self.tab_labels)
        self.tab_list.currentRowChanged.connect(self.set_current_tab)
        layout.addWidget(self.tab_list, 1)

        section_label = QLabel("Sections")
        section_label.setProperty("class", "sectiontitle")
        layout.addWidget(section_label)

        self.section_list = QListWidget()
        layout.addWidget(self.section_list, 1)

        return panel

    def create_settings_center(self):
        """Create the central settings workspace with a stacked tab view."""
        panel = QFrame()
        panel.setProperty("class", "workspace")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        title = QLabel("Settings Workspace")
        title.setProperty("class", "sectiontitle")
        header_layout.addWidget(title)

        header_layout.addStretch(1)

        consequence = QLabel("Consequence-aware controls")
        consequence.setProperty("class", "muted")
        header_layout.addWidget(consequence)

        layout.addWidget(header)

        self.tab_stack = QStackedWidget()
        self.tabs = []
        for tab_id in self.tab_ids:
            tab = DataDrivenTab(self.tab_stack, self.config, self.registry, tab_id)
            tab.settingChanged.connect(self.on_setting_changed)
            tab.explainRequested.connect(self.show_inspector_for_key)
            self.tab_stack.addWidget(tab)
            self.tabs.append(tab)

        layout.addWidget(self.tab_stack, 1)

        return panel

    def create_inspector_panel(self):
        """Create the inspector panel on the right."""
        panel = QFrame()
        panel.setProperty("class", "inspector")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        title = QLabel("Inspector")
        title.setProperty("class", "sectiontitle")
        layout.addWidget(title)

        subtitle = QLabel("Why / Effect / Risk / Docs / Output")
        subtitle.setProperty("class", "muted")
        layout.addWidget(subtitle)

        self.inspector_body = QPlainTextEdit()
        self.inspector_body.setReadOnly(True)
        self.inspector_body.setPlaceholderText(
            "Select a control to see explainability, flags, and risks."
        )
        self.inspector_body.setProperty("class", "inspectorbody")
        layout.addWidget(self.inspector_body, 1)

        return panel

    def create_console_dock(self):
        """Create the build console dock with action bar and tabs."""
        dock = QFrame()
        dock.setProperty("class", "dock")
        layout = QVBoxLayout(dock)
        layout.setContentsMargins(10, 8, 10, 10)
        layout.setSpacing(8)

        layout.addWidget(self.create_action_bar())

        self.console_tabs = QTabWidget()
        self.console_tabs.setObjectName("consoleTabs")
        layout.addWidget(self.console_tabs, 1)

        self.console_tabs.addTab(self.create_command_tab(), "Command")
        self.console_tabs.addTab(self.create_diff_tab(), "Diff")
        self.console_tabs.addTab(self.create_logs_tab(), "Logs")
        self.console_tabs.addTab(self.create_diagnostics_tab(), "Diagnostics")
        self.console_tabs.addTab(self.create_artifacts_tab(), "Artifacts")

        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        self.build_status_label = QLabel("Build: Idle | Exit code: -")
        self.build_status_label.setProperty("class", "muted")
        footer_layout.addWidget(self.build_status_label)
        footer_layout.addStretch(1)

        layout.addWidget(footer)

        return dock

    def create_action_bar(self):
        """Create the action bar with validation and build controls."""
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.validate_btn = QPushButton("Validate")
        self.validate_btn.setProperty("class", "ghost")
        self.validate_btn.clicked.connect(self.validate_placeholder)
        layout.addWidget(self.validate_btn)

        self.dry_run_btn = QPushButton("Dry Run")
        self.dry_run_btn.setProperty("class", "ghost")
        self.dry_run_btn.clicked.connect(self.dry_run_placeholder)
        layout.addWidget(self.dry_run_btn)

        self.build_btn = QPushButton("Build")
        self.build_btn.setProperty("class", "primary")
        self.build_btn.setMinimumHeight(34)
        self.build_btn.clicked.connect(self.app.on_compile)
        layout.addWidget(self.build_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setProperty("class", "ghost")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.app.on_cancel_compile)
        layout.addWidget(self.cancel_btn)

        layout.addStretch(1)

        self.open_output_btn = QPushButton("Open Output")
        self.open_output_btn.setProperty("class", "ghost")
        self.open_output_btn.clicked.connect(self.open_output_folder)
        layout.addWidget(self.open_output_btn)

        self.copy_command_btn = QPushButton("Copy Command")
        self.copy_command_btn.setProperty("class", "ghost")
        self.copy_command_btn.clicked.connect(self.copy_command)
        layout.addWidget(self.copy_command_btn)

        return bar

    def create_command_tab(self):
        """Create the command preview tab."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        self.command_text = QPlainTextEdit()
        self.command_text.setReadOnly(True)
        self.command_text.setProperty("class", "console")
        self.command_text.setPlaceholderText("Command preview will appear here.")
        layout.addWidget(self.command_text, 1)

        return panel

    def create_diff_tab(self):
        """Create the diff preview tab."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        self.diff_text = QPlainTextEdit()
        self.diff_text.setReadOnly(True)
        self.diff_text.setProperty("class", "console")
        self.diff_text.setPlaceholderText("Semantic diff will appear here.")
        layout.addWidget(self.diff_text, 1)

        return panel

    def create_logs_tab(self):
        """Create the logs tab."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setProperty("class", "console")
        layout.addWidget(self.output_text, 1)

        return panel

    def create_diagnostics_tab(self):
        """Create the diagnostics tab."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        self.diagnostics_list = QListWidget()
        self.diagnostics_list.addItem("No diagnostics yet.")
        layout.addWidget(self.diagnostics_list, 1)

        return panel

    def create_artifacts_tab(self):
        """Create the artifacts tab."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        self.artifacts_table = QTableWidget(0, 4)
        self.artifacts_table.setHorizontalHeaderLabels(
            ["File", "Size", "Hash", "Timestamp"]
        )
        self.artifacts_table.horizontalHeader().setStretchLastSection(True)
        self.artifacts_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.artifacts_table, 1)

        return panel

    def set_current_tab(self, index):
        """Switch stacked tab and update section index."""
        if index < 0:
            return
        self.tab_stack.setCurrentIndex(index)
        self.section_list.clear()
        tab_id = self.tab_ids[index]
        for tab in self.registry.get_tabs():
            if tab.get("id") == tab_id:
                for section in tab.get("sections", []):
                    self.section_list.addItem(section.get("title", ""))
                break

    def set_compiling(self, is_compiling):
        """Update UI for compilation state with visual feedback."""
        if is_compiling:
            self.build_btn.setEnabled(False)
            self.build_btn.setText("Building...")
            self.cancel_btn.setEnabled(True)
            self.update_status("Building", "warning")
            self.build_status_label.setText("Build: Running | Exit code: -")
            self.console_tabs.setCurrentIndex(2)
        else:
            self.build_btn.setEnabled(True)
            self.build_btn.setText("Build")
            self.cancel_btn.setEnabled(False)

    def set_command_preview(self, command_text):
        """Update the command preview panel."""
        self.command_text.setPlainText(command_text)

    def set_build_result(self, status_text, exit_code):
        """Update build status footer."""
        self.build_status_label.setText(f"Build: {status_text} | Exit code: {exit_code}")

    def append_output(self, text):
        """Append text to logs panel."""
        self.output_text.appendPlainText(text.rstrip())
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_output(self):
        """Clear logs panel."""
        self.output_text.clear()

    def update_status(self, message, status_type="info"):
        """Update status strip."""
        self.status_label.setText(message)
        color_map = {
            "info": "#3B5C8A",
            "success": "#3A7C3A",
            "warning": "#C27A2A",
            "error": "#B23A3A",
        }
        self.status_indicator.set_color(color_map.get(status_type, "#3B5C8A"))

    def load_from_config(self):
        """Load values from config into UI."""
        for tab in self.tabs:
            tab.load_from_config()

        config_path = self.config.get_file_path()
        if config_path:
            self.project_path.setText(str(config_path))
        else:
            self.project_path.setText(str(Path.cwd()))

        self.refresh_flag_plan()

    def save_to_config(self):
        """Save values from UI into config."""
        pass

    def copy_command(self):
        """Copy command preview to clipboard."""
        command_text = self.command_text.toPlainText().strip()
        if not command_text:
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(command_text)
        self.update_status("Command copied", "success")

    def on_setting_changed(self, key):
        """Handle setting change and refresh previews."""
        self.refresh_flag_plan()

    def refresh_flag_plan(self):
        """Recompute flag plan and update previews."""
        self.current_plan = compile_flag_plan(self.config.to_dict(), self.registry)
        command = render_command_string(self.current_plan, python_exe=sys.executable)
        self.set_command_preview(command)
        self.update_diff_view()

    def update_diff_view(self):
        if not self.last_success_plan or not self.current_plan:
            self.diff_text.setPlainText("No previous successful build to diff.")
            return
        diff = diff_flag_plans(self.last_success_plan, self.current_plan)
        lines = [
            "Added:",
            *[f"  + {item}" for item in diff["added"]],
            "",
            "Removed:",
            *[f"  - {item}" for item in diff["removed"]],
            "",
            "Changed:",
            *[f"  ~ {item}" for item in diff["changed"]],
            "",
            "Provenance Changed:",
            *[f"  * {item}" for item in diff["provenance_changed"]],
        ]
        self.diff_text.setPlainText("\n".join(lines))

    def show_inspector_for_key(self, key):
        definition = self.registry.get_setting(key)
        if not definition:
            self.inspector_body.setPlainText("No inspector data available.")
            return
        flag_lines = []
        if self.current_plan:
            for atom in self.current_plan.flags:
                if key in atom.sources:
                    flag_lines.append(" ".join(atom.args))
        flags_text = "\n".join(flag_lines) if flag_lines else "(no flags generated)"
        impact = ", ".join(definition.impact) if definition.impact else "none"
        details = [
            f"Setting: {definition.key}",
            f"Label: {definition.label}",
            f"Description: {definition.description}",
            f"Effect: {definition.effect}",
            f"Risk: {definition.risk}",
            f"Impact: {impact}",
            "",
            "Flags:",
            flags_text,
        ]
        self.inspector_body.setPlainText("\n".join(details))

    def on_search_changed(self, text):
        index = self.tab_stack.currentIndex()
        if 0 <= index < len(self.tabs):
            self.tabs[index].filter_settings(text)

    def set_last_success_plan(self, plan):
        self.last_success_plan = plan
        self.update_diff_view()

    def open_output_folder(self):
        """Open the output folder in file explorer."""
        output_dir = self.config.get("basic.output_dir")
        input_file = self.config.get("basic.input_file")

        path = None
        if output_dir:
            path = Path(output_dir)
        elif input_file:
            path = Path(input_file).parent / "dist"
        else:
            path = Path.cwd() / "dist"

        if path and path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        else:
            self.append_output(f"Output folder not found: {path}\n")

    def populate_artifacts(self):
        """Populate artifacts table with files in output directory."""
        output_dir = self.config.get("basic.output_dir")
        input_file = self.config.get("basic.input_file")

        if output_dir:
            base_path = Path(output_dir)
        elif input_file:
            base_path = Path(input_file).parent / "dist"
        else:
            base_path = Path.cwd() / "dist"

        self.artifacts_table.setRowCount(0)
        if not base_path.exists():
            return

        files = [p for p in base_path.rglob("*") if p.is_file()]
        for path in files:
            row = self.artifacts_table.rowCount()
            self.artifacts_table.insertRow(row)
            rel = str(path.relative_to(base_path))
            size = path.stat().st_size
            mtime = path.stat().st_mtime
            digest = self._hash_file(path)

            self.artifacts_table.setItem(row, 0, QTableWidgetItem(rel))
            self.artifacts_table.setItem(row, 1, QTableWidgetItem(str(size)))
            self.artifacts_table.setItem(row, 2, QTableWidgetItem(digest))
            self.artifacts_table.setItem(row, 3, QTableWidgetItem(str(mtime)))

    def _hash_file(self, path: Path) -> str:
        hasher = hashlib.sha256()
        try:
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(8192), b""):
                    hasher.update(chunk)
        except OSError:
            return "unreadable"
        return hasher.hexdigest()[:12]

    def focus_diagnostics(self):
        """Focus diagnostics tab."""
        self.console_tabs.setCurrentIndex(3)

    def validate_placeholder(self):
        """Placeholder for validation flow."""
        self.append_output("[validate] Validation is not wired yet.\n")
        self.console_tabs.setCurrentIndex(3)

    def dry_run_placeholder(self):
        """Placeholder for dry run flow."""
        self.append_output("[dry-run] Dry run is not wired yet.\n")
        self.console_tabs.setCurrentIndex(3)

    def export_placeholder(self):
        """Placeholder for export actions."""
        self.append_output("[export] Export options are not wired yet.\n")
        self.console_tabs.setCurrentIndex(0)

    def apply_preset_placeholder(self):
        """Apply preset and show diff summary."""
        preset_name = self.preset_combo.currentText()
        preset = get_preset(preset_name)
        if not preset:
            self.append_output(f"[preset] Unknown preset: {preset_name}\n")
            return
        changes = apply_preset(self.config, preset)
        for tab in self.tabs:
            tab.load_from_config()
        self.refresh_flag_plan()
        self.append_output(f"[preset] Applied preset: {preset.name}\n")
        if changes:
            for key, old, new in changes:
                self.append_output(f"  - {key}: {old} -> {new}\n")
        self.console_tabs.setCurrentIndex(1)
