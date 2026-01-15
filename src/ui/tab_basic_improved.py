"""
Improved basic settings tab with better UX/UI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QCheckBox,
    QLineEdit, QComboBox, QScrollArea, QGroupBox, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import os

from ..utils.constants import MODES, COMPILERS, PYTHON_FLAGS
from .widgets import FileSelectFrame, add_tooltip


class TabBasic(QWidget):
    """Improved tab for basic compilation settings."""

    def __init__(self, parent, config):
        """
        Initialize basic settings tab.

        Args:
            parent: Parent widget
            config: ConfigManager instance
        """
        super().__init__(parent)
        self.config = config
        self.widgets = {}

        # Configure colors
        self.colors = {
            'required': '#E81123',
            'success': '#107C10',
            'bg_highlight': '#F3F2F1',
            'primary': '#0078D4'
        }

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
        """Create improved widgets for basic tab."""
        # SECTION 1: Input File (MOST IMPORTANT - Make it prominent)
        input_section = QWidget()
        input_layout = QVBoxLayout(input_section)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        # Header with required indicator
        header_frame = QWidget()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("📄 Input File")
        title_font = title_label.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)

        required_label = QLabel("* Required")
        required_font = required_label.font()
        required_font.setPointSize(9)
        required_label.setFont(required_font)
        required_label.setStyleSheet(f"color: {self.colors['required']};")
        header_layout.addWidget(required_label)

        header_layout.addStretch(1)
        input_layout.addWidget(header_frame)

        # Description
        desc_label = QLabel("Select the main Python script you want to compile")
        desc_font = desc_label.font()
        desc_font.setPointSize(9)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet("color: #605E5C;")
        input_layout.addWidget(desc_label)

        # File selector with validation indicator
        file_frame = QWidget()
        file_layout = QHBoxLayout(file_frame)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.setSpacing(8)

        self.widgets['input_file'] = FileSelectFrame(
            file_frame,
            "",  # No label, we have a header
            mode='file',
            file_types='Python files (*.py);;All files (*.*)'
        )
        file_layout.addWidget(self.widgets['input_file'], 1)

        # Validation indicator
        self.input_validation = QLabel("")
        validation_font = self.input_validation.font()
        validation_font.setPointSize(14)
        self.input_validation.setFont(validation_font)
        file_layout.addWidget(self.input_validation)

        input_layout.addWidget(file_frame)

        # Bind validation
        self.widgets['input_file'].entry.textChanged.connect(self._validate_input_file)

        self.content_layout.addWidget(input_section)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.content_layout.addWidget(separator)

        # SECTION 2: Compilation Mode
        mode_section = QGroupBox("  🎯 Compilation Mode  ")
        mode_layout = QVBoxLayout(mode_section)
        mode_layout.setSpacing(12)

        # Description
        mode_desc = QLabel("Choose how you want to package your application")
        mode_desc_font = mode_desc.font()
        mode_desc_font.setPointSize(9)
        mode_desc.setFont(mode_desc_font)
        mode_desc.setStyleSheet("color: #605E5C;")
        mode_layout.addWidget(mode_desc)

        # Button group for radio buttons
        self.mode_group = QButtonGroup(self)

        # Create mode options with better layout and descriptions
        descriptions = {
            'accelerated': "Fast compilation, creates extension module (.pyd/.so)",
            'standalone': "✨ Recommended: Creates folder with all dependencies",
            'onefile': "📦 Single executable file (larger, slower startup)",
            'app': "🍎 macOS application bundle (.app)"
        }

        for label, value in MODES:
            mode_card = QWidget()
            mode_card_layout = QHBoxLayout(mode_card)
            mode_card_layout.setContentsMargins(0, 4, 0, 4)

            rb = QRadioButton(label)
            rb.setProperty('mode_value', value)
            if value == 'standalone':
                rb.setChecked(True)
            self.mode_group.addButton(rb)
            mode_card_layout.addWidget(rb)

            desc = QLabel(descriptions.get(value, ""))
            desc_font = desc.font()
            desc_font.setPointSize(9)
            desc.setFont(desc_font)
            desc.setStyleSheet(
                f"color: {self.colors['success'] if value == 'standalone' else '#605E5C'};"
            )
            mode_card_layout.addWidget(desc)
            mode_card_layout.addStretch(1)

            mode_layout.addWidget(mode_card)

        self.content_layout.addWidget(mode_section)

        # SECTION 3: Output Settings
        output_section = QGroupBox("  📁 Output Settings  ")
        output_layout = QVBoxLayout(output_section)
        output_layout.setSpacing(12)

        # Output directory
        dir_label = QLabel("Output Directory (optional):")
        dir_font = dir_label.font()
        dir_font.setPointSize(10)
        dir_label.setFont(dir_font)
        output_layout.addWidget(dir_label)

        self.widgets['output_dir'] = FileSelectFrame(
            output_section,
            "",
            mode='directory'
        )
        output_layout.addWidget(self.widgets['output_dir'])

        # Output filename
        filename_label = QLabel("Output Filename (optional):")
        filename_font = filename_label.font()
        filename_font.setPointSize(10)
        filename_label.setFont(filename_font)
        output_layout.addWidget(filename_label)

        self.widgets['output_filename'] = QLineEdit()
        output_layout.addWidget(self.widgets['output_filename'])

        # Cleanup option
        self.widgets['remove_output'] = QCheckBox("🗑️  Clean up build files after compilation")
        self.widgets['remove_output'].setChecked(True)
        output_layout.addWidget(self.widgets['remove_output'])

        self.content_layout.addWidget(output_section)

        # SECTION 4: Compiler Selection
        compiler_section = QGroupBox("  🔨 Compiler Selection  ")
        compiler_layout = QVBoxLayout(compiler_section)
        compiler_layout.setSpacing(12)

        # Auto-detect recommendation
        rec_frame = QWidget()
        rec_layout = QHBoxLayout(rec_frame)
        rec_layout.setContentsMargins(0, 0, 0, 0)

        rec_icon = QLabel("💡")
        rec_icon_font = rec_icon.font()
        rec_icon_font.setPointSize(12)
        rec_icon.setFont(rec_icon_font)
        rec_layout.addWidget(rec_icon)

        rec_text = QLabel("Auto-detect is recommended for most users")
        rec_font = rec_text.font()
        rec_font.setPointSize(9)
        rec_text.setFont(rec_font)
        rec_text.setStyleSheet(f"color: {self.colors['primary']};")
        rec_layout.addWidget(rec_text)
        rec_layout.addStretch(1)

        compiler_layout.addWidget(rec_frame)

        # Compiler options in a grid
        self.compiler_group = QButtonGroup(self)
        compiler_grid = QWidget()
        compiler_grid_layout = QHBoxLayout(compiler_grid)
        compiler_grid_layout.setContentsMargins(0, 0, 0, 0)

        col_layout1 = QVBoxLayout()
        col_layout2 = QVBoxLayout()

        for i, (label, value) in enumerate(COMPILERS):
            rb = QRadioButton(label)
            rb.setProperty('compiler_value', value)
            if value == 'auto':
                rb.setChecked(True)
            self.compiler_group.addButton(rb)

            if i % 2 == 0:
                col_layout1.addWidget(rb)
            else:
                col_layout2.addWidget(rb)

        compiler_grid_layout.addLayout(col_layout1)
        compiler_grid_layout.addLayout(col_layout2)
        compiler_grid_layout.addStretch(1)

        compiler_layout.addWidget(compiler_grid)

        # MSVC version
        msvc_frame = QWidget()
        msvc_layout = QHBoxLayout(msvc_frame)
        msvc_layout.setContentsMargins(0, 0, 0, 0)

        msvc_label = QLabel("MSVC Version:")
        msvc_label_font = msvc_label.font()
        msvc_label_font.setPointSize(9)
        msvc_label.setFont(msvc_label_font)
        msvc_label.setStyleSheet("color: #605E5C;")
        msvc_layout.addWidget(msvc_label)

        self.widgets['msvc_version'] = QComboBox()
        self.widgets['msvc_version'].addItems(['latest', '2022', '2019', '2017'])
        self.widgets['msvc_version'].setFixedWidth(120)
        msvc_layout.addWidget(self.widgets['msvc_version'])
        msvc_layout.addStretch(1)

        compiler_layout.addWidget(msvc_frame)

        self.content_layout.addWidget(compiler_section)

        # SECTION 5: Python Flags
        flags_section = QGroupBox("  🐍 Python Behavior Flags (Optional)  ")
        flags_layout = QVBoxLayout(flags_section)
        flags_layout.setSpacing(12)

        # Description
        flags_desc = QLabel("Modify Python runtime behavior (leave unchecked for standard behavior)")
        flags_desc_font = flags_desc.font()
        flags_desc_font.setPointSize(9)
        flags_desc.setFont(flags_desc_font)
        flags_desc.setStyleSheet("color: #605E5C;")
        flags_layout.addWidget(flags_desc)

        # Flags in a grid layout
        flags_grid = QWidget()
        flags_grid_layout = QHBoxLayout(flags_grid)
        flags_grid_layout.setContentsMargins(0, 0, 0, 0)

        col1_layout = QVBoxLayout()
        col2_layout = QVBoxLayout()

        self.widgets['python_flags'] = {}
        for i, (flag_name, description) in enumerate(PYTHON_FLAGS):
            flag_frame = QWidget()
            flag_layout = QHBoxLayout(flag_frame)
            flag_layout.setContentsMargins(0, 0, 0, 0)

            cb = QCheckBox(flag_name)
            flag_layout.addWidget(cb)

            # Info icon with tooltip
            info_label = QLabel("ℹ️")
            info_label.setStyleSheet("color: #0078D4;")
            info_label.setToolTip(description)
            flag_layout.addWidget(info_label)
            flag_layout.addStretch(1)

            self.widgets['python_flags'][flag_name] = cb

            if i % 2 == 0:
                col1_layout.addWidget(flag_frame)
            else:
                col2_layout.addWidget(flag_frame)

        flags_grid_layout.addLayout(col1_layout)
        flags_grid_layout.addLayout(col2_layout)
        flags_grid_layout.addStretch(1)

        flags_layout.addWidget(flags_grid)

        self.content_layout.addWidget(flags_section)

    def _validate_input_file(self):
        """Validate input file and show visual indicator."""
        path = self.widgets['input_file'].get_path()

        if not path or not isinstance(path, str):
            self.input_validation.setText("")
            self.input_validation.setStyleSheet("")
        elif os.path.exists(path) and path.endswith('.py'):
            self.input_validation.setText("✓")
            self.input_validation.setStyleSheet(f"color: {self.colors['success']};")
        else:
            self.input_validation.setText("✗")
            self.input_validation.setStyleSheet(f"color: {self.colors['required']};")

    def load_from_config(self):
        """Load values from config."""
        # Input file
        input_file = self.config.get('basic.input_file', '')
        self.widgets['input_file'].set_path(input_file)
        self._validate_input_file()

        # Mode
        mode = self.config.get('basic.mode', 'standalone')
        for button in self.mode_group.buttons():
            if button.property('mode_value') == mode:
                button.setChecked(True)
                break

        # Output
        output_dir = self.config.get('basic.output_dir', '')
        self.widgets['output_dir'].set_path(output_dir)

        output_filename = self.config.get('basic.output_filename', '')
        self.widgets['output_filename'].setText(output_filename)

        remove_output = self.config.get('basic.remove_output', True)
        self.widgets['remove_output'].setChecked(remove_output)

        # Compiler
        compiler = self.config.get('basic.compiler', 'auto')
        for button in self.compiler_group.buttons():
            if button.property('compiler_value') == compiler:
                button.setChecked(True)
                break

        msvc_version = self.config.get('basic.msvc_version', 'latest')
        index = self.widgets['msvc_version'].findText(msvc_version)
        if index >= 0:
            self.widgets['msvc_version'].setCurrentIndex(index)

        # Python flags
        python_flags = self.config.get('basic.python_flags', [])
        for flag_name, checkbox in self.widgets['python_flags'].items():
            checkbox.setChecked(flag_name in python_flags)

    def save_to_config(self):
        """Save values to config."""
        # Input file
        self.config.set('basic.input_file', self.widgets['input_file'].get_path())

        # Mode
        mode_value = 'standalone'
        for button in self.mode_group.buttons():
            if button.isChecked():
                mode_value = button.property('mode_value')
                break
        self.config.set('basic.mode', mode_value)

        # Output
        self.config.set('basic.output_dir', self.widgets['output_dir'].get_path())
        self.config.set('basic.output_filename', self.widgets['output_filename'].text())
        self.config.set('basic.remove_output', self.widgets['remove_output'].isChecked())

        # Compiler
        compiler_value = 'auto'
        for button in self.compiler_group.buttons():
            if button.isChecked():
                compiler_value = button.property('compiler_value')
                break
        self.config.set('basic.compiler', compiler_value)
        self.config.set('basic.msvc_version', self.widgets['msvc_version'].currentText())

        # Python flags
        selected_flags = [
            flag_name
            for flag_name, checkbox in self.widgets['python_flags'].items()
            if checkbox.isChecked()
        ]
        self.config.set('basic.python_flags', selected_flags)
