"""
Advanced options tab for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox,
    QSpinBox, QScrollArea, QGroupBox, QFrame
)
from PySide6.QtCore import Qt
from .widgets import add_tooltip


class TabAdvanced(QWidget):
    """Tab for advanced compilation settings."""

    def __init__(self, parent, config):
        """
        Initialize advanced tab.

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
        """Create widgets for advanced tab."""
        # Optimization section
        opt_frame = QGroupBox("Optimization")
        opt_layout = QVBoxLayout(opt_frame)
        opt_layout.setSpacing(8)

        # LTO
        lto_frame = QWidget()
        lto_layout = QHBoxLayout(lto_frame)
        lto_layout.setContentsMargins(0, 0, 0, 0)

        lto_label = QLabel("Link-Time Optimization:")
        lto_layout.addWidget(lto_label)

        self.widgets['lto'] = QComboBox()
        self.widgets['lto'].addItems(['auto', 'yes', 'no'])
        self.widgets['lto'].setFixedWidth(100)
        add_tooltip(self.widgets['lto'], "Enable link-time optimization for smaller/faster binaries")
        lto_layout.addWidget(self.widgets['lto'])
        lto_layout.addStretch(1)

        opt_layout.addWidget(lto_frame)

        # Jobs
        jobs_frame = QWidget()
        jobs_layout = QHBoxLayout(jobs_frame)
        jobs_layout.setContentsMargins(0, 0, 0, 0)

        jobs_label = QLabel("Parallel Jobs:")
        jobs_layout.addWidget(jobs_label)

        self.widgets['jobs'] = QSpinBox()
        self.widgets['jobs'].setRange(0, 32)
        self.widgets['jobs'].setValue(0)
        self.widgets['jobs'].setFixedWidth(100)
        add_tooltip(self.widgets['jobs'], "Number of parallel compilation jobs (0 = auto)")
        jobs_layout.addWidget(self.widgets['jobs'])
        jobs_layout.addStretch(1)

        opt_layout.addWidget(jobs_frame)

        # Low memory
        self.widgets['low_memory'] = QCheckBox("Low memory mode")
        add_tooltip(self.widgets['low_memory'], "Use less memory during compilation (slower)")
        opt_layout.addWidget(self.widgets['low_memory'])

        # Static libpython
        self.widgets['static_libpython'] = QCheckBox("Static libpython")
        add_tooltip(self.widgets['static_libpython'], "Link Python library statically")
        opt_layout.addWidget(self.widgets['static_libpython'])

        self.content_layout.addWidget(opt_frame)

        # Compatibility section
        compat_frame = QGroupBox("Compatibility")
        compat_layout = QVBoxLayout(compat_frame)
        compat_layout.setSpacing(8)

        self.widgets['full_compat'] = QCheckBox("Full CPython compatibility mode")
        add_tooltip(self.widgets['full_compat'], "Maximum compatibility with CPython (may reduce performance)")
        compat_layout.addWidget(self.widgets['full_compat'])

        # File reference choice
        ref_frame = QWidget()
        ref_layout = QHBoxLayout(ref_frame)
        ref_layout.setContentsMargins(0, 0, 0, 0)

        ref_label = QLabel("File Reference:")
        ref_layout.addWidget(ref_label)

        self.widgets['file_reference_choice'] = QComboBox()
        self.widgets['file_reference_choice'].addItems(['runtime', 'original', 'frozen'])
        self.widgets['file_reference_choice'].setFixedWidth(120)
        add_tooltip(self.widgets['file_reference_choice'], "How to reference __file__ in modules")
        ref_layout.addWidget(self.widgets['file_reference_choice'])
        ref_layout.addStretch(1)

        compat_layout.addWidget(ref_frame)

        self.content_layout.addWidget(compat_frame)

        # Debug section
        debug_frame = QGroupBox("Debug & Development")
        debug_layout = QVBoxLayout(debug_frame)
        debug_layout.setSpacing(8)

        self.widgets['debug'] = QCheckBox("Debug mode")
        add_tooltip(self.widgets['debug'], "Enable debug mode with additional checks")
        debug_layout.addWidget(self.widgets['debug'])

        self.widgets['unstripped'] = QCheckBox("Keep debug symbols (unstripped)")
        add_tooltip(self.widgets['unstripped'], "Keep debug symbols in binary")
        debug_layout.addWidget(self.widgets['unstripped'])

        self.widgets['trace_execution'] = QCheckBox("Trace execution")
        add_tooltip(self.widgets['trace_execution'], "Output execution trace (very verbose)")
        debug_layout.addWidget(self.widgets['trace_execution'])

        self.widgets['generate_c_only'] = QCheckBox("Generate C code only (don't compile)")
        add_tooltip(self.widgets['generate_c_only'], "Only generate C source code without compiling")
        debug_layout.addWidget(self.widgets['generate_c_only'])

        self.content_layout.addWidget(debug_frame)

        # Cache control section
        cache_frame = QGroupBox("Cache Control")
        cache_layout = QVBoxLayout(cache_frame)
        cache_layout.setSpacing(8)

        self.widgets['disable_ccache'] = QCheckBox("Disable ccache")
        add_tooltip(self.widgets['disable_ccache'], "Disable C compiler caching")
        cache_layout.addWidget(self.widgets['disable_ccache'])

        self.widgets['disable_bytecode_cache'] = QCheckBox("Disable bytecode cache")
        add_tooltip(self.widgets['disable_bytecode_cache'], "Disable bytecode caching")
        cache_layout.addWidget(self.widgets['disable_bytecode_cache'])

        self.content_layout.addWidget(cache_frame)

    def load_from_config(self):
        """Load values from config."""
        # LTO
        lto_value = self.config.get('advanced.lto', 'auto')
        index = self.widgets['lto'].findText(lto_value)
        if index >= 0:
            self.widgets['lto'].setCurrentIndex(index)

        # Jobs
        jobs = self.config.get('advanced.jobs', 0)
        self.widgets['jobs'].setValue(jobs)

        # Checkboxes
        self.widgets['low_memory'].setChecked(self.config.get('advanced.low_memory', False))
        self.widgets['static_libpython'].setChecked(self.config.get('advanced.static_libpython', False))
        self.widgets['full_compat'].setChecked(self.config.get('advanced.full_compat', False))

        # File reference choice
        file_ref = self.config.get('advanced.file_reference_choice', 'runtime')
        index = self.widgets['file_reference_choice'].findText(file_ref)
        if index >= 0:
            self.widgets['file_reference_choice'].setCurrentIndex(index)

        # Debug checkboxes
        self.widgets['debug'].setChecked(self.config.get('advanced.debug', False))
        self.widgets['unstripped'].setChecked(self.config.get('advanced.unstripped', False))
        self.widgets['trace_execution'].setChecked(self.config.get('advanced.trace_execution', False))
        self.widgets['generate_c_only'].setChecked(self.config.get('advanced.generate_c_only', False))

        # Cache checkboxes
        self.widgets['disable_ccache'].setChecked(self.config.get('advanced.disable_ccache', False))
        self.widgets['disable_bytecode_cache'].setChecked(
            self.config.get('advanced.disable_bytecode_cache', False)
        )

    def save_to_config(self):
        """Save values to config."""
        self.config.set('advanced.lto', self.widgets['lto'].currentText())
        self.config.set('advanced.jobs', self.widgets['jobs'].value())
        self.config.set('advanced.low_memory', self.widgets['low_memory'].isChecked())
        self.config.set('advanced.static_libpython', self.widgets['static_libpython'].isChecked())
        self.config.set('advanced.full_compat', self.widgets['full_compat'].isChecked())
        self.config.set('advanced.file_reference_choice', self.widgets['file_reference_choice'].currentText())
        self.config.set('advanced.debug', self.widgets['debug'].isChecked())
        self.config.set('advanced.unstripped', self.widgets['unstripped'].isChecked())
        self.config.set('advanced.trace_execution', self.widgets['trace_execution'].isChecked())
        self.config.set('advanced.generate_c_only', self.widgets['generate_c_only'].isChecked())
        self.config.set('advanced.disable_ccache', self.widgets['disable_ccache'].isChecked())
        self.config.set('advanced.disable_bytecode_cache', self.widgets['disable_bytecode_cache'].isChecked())
